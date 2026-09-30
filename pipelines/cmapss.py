"""Pure transforms for the NASA C-MAPSS turbofan data: text lines -> bronze -> silver.

Every function takes DataFrames and returns a DataFrame; nothing reads or writes tables.
The load job (T-005) reads the files, calls these functions and writes the results.

Raw files (D-007): `train_FD00x.txt` and `test_FD00x.txt` hold 26 whitespace-separated
numbers per line (`unit cycle op1 op2 op3 s1..s21`), often with trailing spaces.
`RUL_FD00x.txt` holds one integer per line: line n is the true remaining useful life
(RUL) of test unit n, counted from that unit's last recorded cycle.

Line order matters only for the RUL files. Spark does not promise to keep the order of
lines in a file, so the reader numbers the lines itself before Spark sees them:
`lines_frame` enumerates the file's text in Python and stores the number in `line_no`.
`parse_rul` uses that column, never row order or `monotonically_increasing_id`.
"""

import re

from pyspark.sql import Column, DataFrame, SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql import types as T

from pipelines.cmapss_schema import DATASETS, OP_SETTINGS, SENSORS

RAW_SENSORS = [raw for raw, _, _, _ in SENSORS]
RAW_FIELDS = ["unit", "cycle", *OP_SETTINGS, *RAW_SENSORS]  # 26 per line
KEY = ["dataset", "split", "unit"]


def _file_pattern(kinds: str) -> str:
    """Regex for a C-MAPSS file name at the end of a path; group 1 = kind, group 2 = dataset."""
    return rf"(?:^|/)({kinds})_(FD00[1-4])\.txt$"


def parse_file_name(path: str) -> tuple[str, str]:
    """`.../train_FD001.txt` -> ("FD001", "train"); test -> "test"; RUL files -> "rul"."""
    match = re.search(_file_pattern("train|test|RUL"), path)
    if not match:
        raise ValueError(f"Not a C-MAPSS file name: {path!r}")
    kind, dataset = match.groups()
    return dataset, kind.lower()


def lines_frame(spark: SparkSession, source_file: str, text: str) -> DataFrame:
    """One file's text as rows (source_file, line_no, value); line_no is 1-based file order."""
    rows = [(source_file, n, value) for n, value in enumerate(text.splitlines(), start=1)]
    schema = "source_file STRING, line_no INT, value STRING"
    return spark.createDataFrame(rows, schema)


def _from_file_name(source_file: Column, kinds: str, group: int) -> Column:
    """Part of the file name, or a query-time error naming the file if it does not match."""
    pattern = _file_pattern(kinds)
    return F.when(
        source_file.rlike(pattern), F.regexp_extract(source_file, pattern, group)
    ).otherwise(F.raise_error(F.concat(F.lit("Not a C-MAPSS file name: "), source_file)))


def _non_blank(lines: DataFrame) -> DataFrame:
    return lines.withColumn("value", F.trim("value")).where(F.col("value") != "")


def to_bronze(lines: DataFrame) -> DataFrame:
    """Raw train/test lines (source_file, value) -> one typed row per line, blank lines dropped."""
    fields = F.split("value", r"\s+")
    checked = F.when(F.size(fields) == len(RAW_FIELDS), fields).otherwise(
        F.raise_error(
            F.concat(
                F.lit(f"Expected {len(RAW_FIELDS)} fields in a C-MAPSS line, got: "),
                F.col("value"),
            )
        )
    )
    source = F.col("source_file")
    return (
        _non_blank(lines)
        .withColumn("fields", checked)
        .select(
            "source_file",
            _from_file_name(source, "train|test", 2).alias("dataset"),
            _from_file_name(source, "train|test", 1).alias("split"),
            *[
                F.col("fields")[i]
                .cast("int" if name in ("unit", "cycle") else "double")
                .alias(name)
                for i, name in enumerate(RAW_FIELDS)
            ],
        )
    )


def parse_rul(lines: DataFrame) -> DataFrame:
    """RUL file lines (source_file, line_no, value) -> (dataset, unit, true_rul); unit = line_no."""
    return _non_blank(lines).select(
        _from_file_name(F.col("source_file"), "RUL", 2).alias("dataset"),
        F.col("line_no").cast("int").alias("unit"),
        F.col("value").cast("int").alias("true_rul"),
    )


def _test_rul(rul: DataFrame) -> DataFrame:
    """RUL rows keyed like the silver tables; the RUL files only describe test engines."""
    return rul.withColumn("split", F.lit("test"))


def _engine_id() -> Column:
    return F.format_string("%s_%s_%03d", "dataset", "split", "unit")


def to_sensor_readings(bronze: DataFrame, rul: DataFrame) -> DataFrame:
    """Bronze + true RUL -> one row per engine per cycle, paper sensor names and `rul`."""
    last_cycle = F.max("cycle").over(Window.partitionBy(*KEY))
    remaining = F.when(F.col("split") == "train", last_cycle - F.col("cycle")).otherwise(
        F.col("true_rul") + last_cycle - F.col("cycle")
    )
    return bronze.join(_test_rul(rul), KEY, "left").select(
        "dataset",
        "split",
        _engine_id().alias("engine_id"),
        "unit",
        "cycle",
        *OP_SETTINGS,
        *[F.col(raw).alias(name) for raw, name, _, _ in SENSORS],
        remaining.cast("int").alias("rul"),
    )


def to_engines(sensor_readings: DataFrame, rul: DataFrame) -> DataFrame:
    """One row per engine: its length in cycles and, for test engines, the true RUL."""
    return (
        sensor_readings.groupBy("engine_id", *KEY)
        .agg(F.max("cycle").cast("int").alias("total_cycles"))
        .join(_test_rul(rul), KEY, "left")
        .select("engine_id", *KEY, "total_cycles", "true_rul")
    )


def to_datasets(spark: SparkSession, engines: DataFrame) -> DataFrame:
    """One row per subset: readme facts plus engine counts computed from `engines`."""
    facts = spark.createDataFrame(
        [(name, conditions, faults) for name, (conditions, faults) in DATASETS.items()],
        T.StructType(
            [
                T.StructField("dataset", T.StringType(), False),
                T.StructField("operating_conditions", T.IntegerType(), False),
                T.StructField("fault_modes", T.StringType(), False),
            ]
        ),
    )

    def count(split: str) -> Column:
        return F.count(F.when(F.col("split") == split, True)).alias(f"{split}_engines")

    counts = engines.groupBy("dataset").agg(count("train"), count("test"))
    return facts.join(counts, "dataset", "left").select(
        "dataset",
        "operating_conditions",
        "fault_modes",
        *[
            F.coalesce(F.col(c), F.lit(0)).cast("int").alias(c)
            for c in ("train_engines", "test_engines")
        ],
    )
