# Databricks notebook source
# MAGIC %md
# MAGIC # 00 · Setup
# MAGIC Creates the Unity Catalog schemas and the raw volume that M1 needs (D-008).
# MAGIC Safe to run again: every statement is `IF NOT EXISTS`.

# COMMAND ----------

CATALOG = "workspace"
SCHEMAS = ["plant_bronze", "plant_silver"]
VOLUME = f"{CATALOG}.plant_bronze.raw"

for schema in SCHEMAS:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{schema}")  # noqa: F821
spark.sql(f"CREATE VOLUME IF NOT EXISTS {VOLUME}")  # noqa: F821

# COMMAND ----------

print(f"spark.version = {spark.version}")  # noqa: F821
spark.sql(f"SHOW SCHEMAS IN {CATALOG} LIKE 'plant*'").show()  # noqa: F821
spark.sql("SHOW VOLUMES IN workspace.plant_bronze").show()  # noqa: F821

# COMMAND ----------

# Return a one-line summary so `databricks jobs get-run-output` shows it (prints are not returned).
schemas = [r[0] for r in spark.sql(f"SHOW SCHEMAS IN {CATALOG} LIKE 'plant*'").collect()]  # noqa: F821
dbutils.notebook.exit(f"spark {spark.version}; schemas {schemas}; volume {VOLUME}")  # noqa: F821
