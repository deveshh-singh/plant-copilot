"""Tests for the C-MAPSS bronze and silver transforms, on tiny hand-written inputs."""

import pytest

from pipelines import cmapss
from pipelines.cmapss_schema import COLUMN_COMMENTS, SENSORS, TABLE_COMMENTS

TRAIN_FILE = "/Volumes/workspace/plant_bronze/raw/cmapss/train_FD001.txt"
TEST_FILE = "/Volumes/workspace/plant_bronze/raw/cmapss/test_FD001.txt"
RUL_FILE = "/Volumes/workspace/plant_bronze/raw/cmapss/RUL_FD001.txt"

# 21 sensor values; the numbers themselves do not matter to the transforms.
SENSOR_TEXT = " ".join(f"{500 + i}.{i:02d}" for i in range(1, 22))


def line(unit, cycle):
    return f"{unit} {cycle} -0.0007 -0.0004 100.0 {SENSOR_TEXT}"


# 2 engines x 3 cycles in each file; one line with trailing spaces (as in the real
# files) and one blank line.
TRAIN_TEXT = "\n".join(
    [line(1, 1), line(1, 2) + "  ", line(1, 3), "", line(2, 1), line(2, 2), line(2, 3)]
)
TEST_TEXT = "\n".join([line(1, c) for c in (1, 2, 3)] + [line(2, c) for c in (1, 2, 3)])
RUL_TEXT = "10\n20\n"


@pytest.fixture(scope="module")
def lines(spark):
    return cmapss.lines_frame(spark, TRAIN_FILE, TRAIN_TEXT).unionByName(
        cmapss.lines_frame(spark, TEST_FILE, TEST_TEXT)
    )


@pytest.fixture(scope="module")
def bronze(lines):
    return cmapss.to_bronze(lines)


@pytest.fixture(scope="module")
def rul(spark):
    return cmapss.parse_rul(cmapss.lines_frame(spark, RUL_FILE, RUL_TEXT))


@pytest.fixture(scope="module")
def readings(bronze, rul):
    return cmapss.to_sensor_readings(bronze, rul)


@pytest.fixture(scope="module")
def engines(readings, rul):
    return cmapss.to_engines(readings, rul)


@pytest.fixture(scope="module")
def datasets(spark, engines):
    return cmapss.to_datasets(spark, engines)


def rul_of(readings, engine_id):
    rows = readings.where(f"engine_id = '{engine_id}'").orderBy("cycle").collect()
    return [r["rul"] for r in rows]


# --- parse_file_name (A3) ---


@pytest.mark.parametrize(
    "path, expected",
    [
        ("train_FD001.txt", ("FD001", "train")),
        ("dbfs:/Volumes/x/y/test_FD004.txt", ("FD004", "test")),
        (RUL_FILE, ("FD001", "rul")),
        ("RUL_FD001.txt", ("FD001", "rul")),
    ],
)
def test_parse_file_name(path, expected):
    assert cmapss.parse_file_name(path) == expected


@pytest.mark.parametrize("path", ["foo.txt", "train_FD005.txt", "train_FD001.csv", ""])
def test_parse_file_name_rejects_other_names(path):
    with pytest.raises(ValueError):
        cmapss.parse_file_name(path)


# --- bronze (A1) ---


def test_bronze_drops_blank_lines_and_keeps_every_reading(bronze):
    assert bronze.count() == 12


def test_bronze_columns_and_types(bronze):
    types = dict(bronze.dtypes)
    assert list(types)[:5] == ["source_file", "dataset", "split", "unit", "cycle"]
    assert types["unit"] == "int" and types["cycle"] == "int"
    doubles = [f"op_setting_{i}" for i in (1, 2, 3)] + [f"s{i}" for i in range(1, 22)]
    assert list(types)[5:] == doubles
    assert all(types[c] == "double" for c in doubles)


def test_bronze_parses_values_and_file_name(bronze):
    row = bronze.where("split = 'train' AND unit = 1 AND cycle = 2").collect()[0]
    assert row["dataset"] == "FD001"
    assert row["source_file"] == TRAIN_FILE
    assert row["op_setting_1"] == -0.0007
    assert row["s21"] == 521.21


def test_bronze_rejects_a_line_with_the_wrong_field_count(spark):
    bad = cmapss.lines_frame(spark, TRAIN_FILE, "1 2 3")
    with pytest.raises(Exception, match="26 fields"):
        cmapss.to_bronze(bad).collect()


def test_bronze_rejects_an_unknown_file_name(spark):
    bad = cmapss.lines_frame(spark, "/x/foo.txt", line(1, 1))
    with pytest.raises(Exception, match="foo.txt"):
        cmapss.to_bronze(bad).collect()


# --- RUL file ---


def test_parse_rul_uses_line_number_as_unit(rul):
    rows = sorted(rul.collect())
    assert [tuple(r) for r in rows] == [("FD001", 1, 10), ("FD001", 2, 20)]
    assert dict(rul.dtypes) == {"dataset": "string", "unit": "int", "true_rul": "int"}


def test_lines_frame_numbers_lines_in_file_order(spark):
    rows = cmapss.lines_frame(spark, RUL_FILE, "7\n8\n9").orderBy("line_no").collect()
    assert [(r["line_no"], r["value"]) for r in rows] == [(1, "7"), (2, "8"), (3, "9")]


# --- sensor_readings (A1) ---


def test_sensor_readings_columns(readings):
    mnemonics = [name for _, name, _, _ in SENSORS]
    expected = ["dataset", "split", "engine_id", "unit", "cycle"]
    expected += [f"op_setting_{i}" for i in (1, 2, 3)] + mnemonics + ["rul"]
    assert readings.columns == expected
    assert dict(readings.dtypes)["rul"] == "int"


def test_engine_id_format(readings):
    ids = {r["engine_id"] for r in readings.select("engine_id").distinct().collect()}
    assert ids == {"FD001_train_001", "FD001_train_002", "FD001_test_001", "FD001_test_002"}


def test_sensor_readings_unique_on_engine_and_cycle(readings):
    assert readings.select("engine_id", "cycle").distinct().count() == readings.count() == 12


def test_train_rul_counts_down_to_zero(readings):
    assert rul_of(readings, "FD001_train_001") == [2, 1, 0]


def test_test_rul_adds_the_true_rul(readings):
    assert rul_of(readings, "FD001_test_001") == [12, 11, 10]
    assert rul_of(readings, "FD001_test_002") == [22, 21, 20]


def test_sensor_names_follow_the_paper(readings):
    row = readings.where("engine_id = 'FD001_train_001' AND cycle = 1").collect()[0]
    assert row["t2"] == 501.01  # s1
    assert row["t24"] == 502.02  # s2
    assert row["w32"] == 521.21  # s21


# --- engines and datasets ---


def test_engines(engines):
    rows = {r["engine_id"]: r for r in engines.collect()}
    assert engines.columns == ["engine_id", "dataset", "split", "unit", "total_cycles", "true_rul"]
    assert len(rows) == 4
    assert rows["FD001_train_002"]["total_cycles"] == 3
    assert rows["FD001_train_002"]["true_rul"] is None
    assert rows["FD001_test_002"]["true_rul"] == 20


def test_datasets_counts_engines_from_the_data(datasets):
    assert datasets.columns == [
        "dataset",
        "operating_conditions",
        "fault_modes",
        "train_engines",
        "test_engines",
    ]
    rows = {r["dataset"]: r for r in datasets.collect()}
    assert sorted(rows) == ["FD001", "FD002", "FD003", "FD004"]
    assert (rows["FD001"]["train_engines"], rows["FD001"]["test_engines"]) == (2, 2)
    assert (rows["FD002"]["train_engines"], rows["FD002"]["test_engines"]) == (0, 0)
    assert rows["FD004"]["operating_conditions"] == 6
    assert "fan" in rows["FD004"]["fault_modes"]
    assert "fan" not in rows["FD002"]["fault_modes"]


# --- comments (A2) ---


def test_sensor_list_is_complete_and_ordered():
    assert [raw for raw, _, _, _ in SENSORS] == [f"s{i}" for i in range(1, 22)]
    assert all(desc and unit for _, _, desc, unit in SENSORS)


def test_every_output_column_has_a_comment_and_no_extras(bronze, readings, engines, datasets):
    outputs = {
        "cmapss_raw": bronze,
        "sensor_readings": readings,
        "engines": engines,
        "datasets": datasets,
    }
    assert set(COLUMN_COMMENTS) == set(TABLE_COMMENTS) == set(outputs)
    for table, df in outputs.items():
        assert set(COLUMN_COMMENTS[table]) == set(df.columns), table
        assert all(COLUMN_COMMENTS[table].values()), table
