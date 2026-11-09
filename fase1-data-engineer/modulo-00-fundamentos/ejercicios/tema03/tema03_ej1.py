# Ejercicio 1 del Tema 3: la lluvia de Västra Götaland, ahora en SQL

# La empresa de agua de Göteborg quiere el mismo analisis
# que hicicste en pandas, pero su equipo de datod trabaja en
# Databricks con SQL. Vas a resolver el mismo problema en el otro
# lenguaje, y asi podras compar los dos enfoques.

# Lo que tienes que hacer:

# 0. Predicciones primero, en un comentario al principio
# del archivo:
#   - Los cuatro valores de la consulta 1.
#   - La tabla final de la consulta 2.
# 1. Preparar:
#   - Crear la conexión a Spark (DatabricksSession).
#   - Leer el CSV con pandas.
#   - Enviarlo a Spark y crear la vista temporal lluvia.
# 2. Consulta 1, explorar: una sola fila con estas columnas:
#   - filas: todas las filas
#   - con_lluvia: las que tienen dato de lluvia
#   - municipios: cuántos municipios distintos hay
#   - no_g: cuántas filas tienen una calidad distinta de G
# 3. Limpiar: crea una segunda vista temporal, lluvia_limpia,
#   con las filas de calidad G, sin lluvia nula y sin duplicados.
# 4. Consulta 2, resumir, desde lluvia_limpia:
#   una fila por municipio con estas columnas:
#   - station
#   - total_mm, redondeado a 1 decimal
#   - max_mm
#   - dias
#   - dias_fuertes: días con 10 mm o más

# Muestra solo los municipios con un total de al menos 18.5 mm
# , ordenados del que más llovió al que menos.

# Resultado esperado de la consulta 2:
# +--------+--------+------+----+------------+
# | station|total_mm|max_mm|dias|dias_fuertes|
# +--------+--------+------+----+------------+
# |   Borås|    21.5|  18.4|   2|           1|
# |Alingsås|    19.2|   9.0|   3|           0|
# +--------+--------+------+----+------------+

"""Predicciones:"""

from databricks.connect import DatabricksSession
import pandas as pd

#  --- Preparar ---

spark = DatabricksSession.builder.serverless().getOrCreate()

pdf = pd.read_csv(
    "temas/tema02/datos/lluvia_vg.csv",
    sep=";",
    decimal=",",
)

df = spark.createDataFrame(pdf)

df.createOrReplaceTempView("lluvia")

# --- Consulta 1 ---
spark.sql("""
    SELECT
        COUNT(*) AS filas,
        COUNT(nederbord_mm) AS con_lluvia,
        COUNT(DISTINCT station) AS municipios,
        SUM(CASE WHEN kvalitet != 'G' THEN 1 ELSE 0 END) AS no_g
    FROM lluvia
""").show()

# --- Limpieza ---

lluvia_limpia = spark.sql(
    """
    SELECT DISTINCT *
    FROM lluvia
    WHERE kvalitet = :g
        AND nederbord_mm IS NOT NULL
""",
    args={"g": "G"},
)

lluvia_limpia.createOrReplaceTempView("lluvia_limpia")

lluvia_limpia.show()

# --- Consulta 2 ---

spark.sql("""
    SELECT
        station,
        ROUND(SUM(nederbord_mm), 1) AS total_mm,
        MAX(nederbord_mm) AS max_mm,
        COUNT(datum) AS dias,
        SUM(CASE WHEN nederbord_mm >= 10 THEN 1 ELSE 0 END) AS dias_fuertes
    FROM lluvia_limpia
    GROUP BY station
    HAVING SUM(nederbord_mm) >= 18.5
    ORDER BY total_mm DESC
""").show()
