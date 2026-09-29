import os
from pathlib import Path

import pytest

# PySpark 4 needs Java 17 (D-006). Homebrew's openjdk@17 is keg-only, so it is not on
# the PATH by default; point JAVA_HOME at it when nothing else is set.
HOMEBREW_JDK17 = Path("/opt/homebrew/opt/openjdk@17")
if "JAVA_HOME" not in os.environ and HOMEBREW_JDK17.exists():
    os.environ["JAVA_HOME"] = str(HOMEBREW_JDK17)


@pytest.fixture(scope="session")
def spark():
    """One small local SparkSession shared by the whole test run."""
    from pyspark.sql import SparkSession

    session = (
        SparkSession.builder.master("local[1]")
        .appName("plant-copilot-tests")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )
    session.sparkContext.setLogLevel("ERROR")
    yield session
    session.stop()
