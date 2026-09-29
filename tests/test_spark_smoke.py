from pyspark.sql.types import IntegerType, StringType, StructField, StructType


def test_local_spark_builds_a_dataframe(spark):
    schema = StructType(
        [
            StructField("engine_id", StringType(), nullable=False),
            StructField("cycle", IntegerType(), nullable=False),
        ]
    )
    rows = [("FD001_train_001", 1), ("FD001_train_001", 2), ("FD001_train_002", 1)]

    df = spark.createDataFrame(rows, schema)

    assert df.count() == 3
    assert df.schema == schema
