import json

import pandas as pd
from pyspark.sql import DataFrame, SparkSession

from utils.spark_session import get_spark

texto_api = """[
 {"station": {"name": "Åre"},
  "value": [
   {"date": 1730865600000, "value": "-2,5", "quality": "G"},
   {"date": 1730869200000, "value": "-3.4", "quality": "G"},
   {"date": 1730872800000, "value": "error", "quality": "G"},
   {"date": 1730876400000, "value": "-4,8", "quality": "G"}
  ]},
 {"station": {"name": "Östersund"},
  "value": [
   {"date": 1730865600000, "value": "-1,0", "quality": "G"},
   {"date": 1730869200000, "value": "-3.0", "quality": "G"},
   {"date": 1730872800000, "value": "-2.2", "quality": "Y"},
   {"date": 1730876400000, "value": "", "quality": "G"}
  ]}
]"""

# --- Preparar ---
spark = get_spark()

datos = json.loads(texto_api)

pdf = pd.json_normalize(datos, record_path=["value"], meta=[["station", "name"]])

pdf = pdf.rename(
    columns={"station.name": "station", "value": "temperatur", "quality": "kvalitet"}
)

pdf = pdf[["station", "date", "temperatur", "kvalitet"]]

df = spark.createDataFrame(pdf)

df.createOrReplaceTempView("mediciones")

# --- Limpiar ---

mediciones_limpias = spark.sql("""
    SELECT
        station,
        TRY_CAST(REPLACE(temperatur, ',', '.') AS DOUBLE) AS temp,
        TIMESTAMP_MILLIS(date) AS ts_utc,
        DATE_FORMAT(FROM_UTC_TIMESTAMP(TIMESTAMP_MILLIS(date), 'Europe/Stockholm'), 'HH:mm') AS hora_sueca,
        kvalitet
    FROM mediciones
""")

mediciones_limpias.createOrReplaceTempView("mediciones_limpias")

# --- Una funcion ---


def horas_nieve(spark, umbral: float = -3.0) -> DataFrame:
    """Devuelve, por estación, las horas con
    temperatura <= umbral (calidad G):
    n_validas, horas_nieve, minima y
    primera_hora (hora sueca, HH:mm)."""
    query = """
        SELECT
            station,
            COUNT(*) AS n_validas,
            COUNT(CASE WHEN temp <= :umbral THEN 1 END) AS horas_nieve,
            MIN(temp) AS minima,
            DATE_FORMAT(
                FROM_UTC_TIMESTAMP(
                    MIN(CASE WHEN temp <= :umbral THEN ts_utc END),
                    'Europe/Stockholm'
                ),'HH:mm') AS primera_hora
        FROM mediciones_limpias
        WHERE kvalitet = 'G'
            AND temp IS NOT NULL
        GROUP BY station
        HAVING COUNT(CASE WHEN temp <= :umbral THEN 1 END) > 0
        ORDER BY horas_nieve DESC
    """
    return spark.sql(query, args={"umbral": umbral})


# --- Llammada a la funcion ---
horas_nieve(spark).show()

horas_nieve(spark, umbral=-4.0).show()
