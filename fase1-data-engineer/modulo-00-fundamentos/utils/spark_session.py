"""Crea la SparkSession: local (por defecto) o Databricks (SPARK_MODE=databricks)."""

import os


def get_spark():
    """Devuelve una SparkSession local o de Databricks, según SPARK_MODE."""
    if os.environ.get("SPARK_MODE", "local") == "databricks":
        from databricks.connect import DatabricksSession

        return DatabricksSession.builder.serverless().getOrCreate()

    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder.master("local[*]")
        .appName("datastudies")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark
