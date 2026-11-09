# Ejercicio 2: encuentro de errores

import pandas as pd
from utils.spark_session import get_spark

#  --- Preparar ---

spark = get_spark()

pdf = pd.read_csv(
    "temas/tema02/datos/observaciones.csv",
    sep=";",
    decimal=",",
)

df = spark.createDataFrame(pdf)  # 2. enviar los datos a Spark
df.createOrReplaceTempView("observaciones")


# Consulta 1. Objetivo: las mediciones bajo el punto de
#                       congelación (32 °F), en Fahrenheit
spark.sql("""
    SELECT
        station,
        tid,
        ROUND(temperatur * 9 / 5 + 32, 1) AS temp_f
    FROM observaciones
    WHERE ((temperatur * 9 / 5) + 32) < 32
""").show()
"""El error esta en el where por que where se ejcuta antes
entonces nunca hay un temp_f cuando se ejecuta el where"""

# # Consulta 2. Objetivo: cuántas mediciones SIN temperatura
#                         tiene cada estación
spark.sql("""
    SELECT
        station,
        SUM(CASE WHEN temperatur IS NULL THEN 1 ELSE 0 END) AS sin_dato
    FROM observaciones
    GROUP BY station
""").show()
""""El error """
# # Consulta 3. Objetivo: la media de cada estación, solo las
#                         de media negativa
spark.sql("""
    SELECT
        station,
        ROUND(AVG(temperatur), 1) AS media
    FROM observaciones
    GROUP BY station
    HAVING AVG(temperatur) < 0
""").show()
"""el error esta que no es where es having"""
# # Consulta 4. Objetivo: la temperatura máxima de cada estación
#                         en cada hora
spark.sql("""
    SELECT
        station,
        tid,
        MAX(temperatur) AS maxima
    FROM observaciones
    GROUP BY station ,tid
    ORDER BY station, tid
""").show()
""" aqui el error esta en el tid no lo necesitamos y si lo usamos
tendriamos que ponerlo tambinen el group by"""
# # Consulta 5. Objetivo: la hora de cada medición en formato
#                         HH:mm (por ejemplo, 05:00)
spark.sql("""
    SELECT
        station,
        date_format(to_timestamp(datum || ' ' || tid, 'yyyy-MM-dd HH:mm'), 'HH:mm') AS hora
    FROM observaciones
""").show()
"""el error estaba en el fromato no MM sino mm"""
