# Ejercicio 3: consumo electrico y frio
# Practica: todo el Tema 2 + Tema 1(json), con menos pistas
# Tipo: mini-caso desde cero

# Una compania electrica de Estocolmo quiere saber cuanto sube
# el consumo de cada barrio en las horas frias, para planificar
# la produccion.

"""Requisitos:
1. Predicciones primero: antes de programar,
    escribe cuántas filas tendrá el consumo limpio y
    el resultado final completo que esperas.
2. Consumo: leer, quitar las filas sin consumo,
    y crear fecha_utc a partir de tid. Cuidado: es hora sueca.
3. Temperatura: del JSON a un DataFrame con fecha_utc
    y temp (número).
4. Unir las dos tablas por fecha_utc. Cada hora del consumo tiene
 una temperatura, así que valida la relación con el
 validate adecuado (piensa: muchas filas de consumo por cada temperatura).
5. Columna frio: True si la temperatura es menor o igual a -2 °C.
6. Resultado final: una fila por barrio, con las columnas omrade,
 total_mwh, media_frio (consumo medio en las horas frías)
 y media_no_frio (consumo medio en las demás), con 1 decimal.
7. Guardar el resultado en Parquet, en temas/tema02/datos/.
"""

texto_api = """{"station": {"name": "Stockholm"},
 "value": [
  {"date": 1730865600000, "value": "-1,4", "quality": "G"},
  {"date": 1730869200000, "value": "-2.0", "quality": "G"},
  {"date": 1730872800000, "value": "-2,9", "quality": "G"}
 ]}"""

import json
import pandas as pd
import numpy as np

df_consumo = pd.read_csv(
    "/home/sebastian/datastudies/fase1-data-engineer/modulo-00-fundamentos/temas/tema02/datos/consumo_sthlm.csv",
    sep=";",
    decimal=",",
)
print(df_consumo)
#         omrade               tid  forbrukning_mwh
# 0    Södermalm  2024-11-06 05:00             12.4
# 1    Södermalm  2024-11-06 06:00             15.1
# 2    Södermalm  2024-11-06 07:00             18.9
# 3  Kungsholmen  2024-11-06 05:00              9.8
# 4  Kungsholmen  2024-11-06 06:00             11.2
# 5  Kungsholmen  2024-11-06 07:00              NaN

df_limpio = df_consumo.dropna(subset="forbrukning_mwh")
print(df_limpio)

df_limpio["fecha_utc"] = (
    pd.to_datetime(df_limpio["tid"])
    .dt.tz_localize("Europe/Stockholm")
    .dt.tz_convert("UTC")
)

print(df_limpio)

#         omrade               tid  forbrukning_mwh fecha_utc
# 0    Södermalm  2024-11-06 05:00             12.4     06:00
# 1    Södermalm  2024-11-06 06:00             15.1     07:00
# 2    Södermalm  2024-11-06 07:00             18.9     08:00
# 3  Kungsholmen  2024-11-06 05:00              9.8     06:00
# 4  Kungsholmen  2024-11-06 06:00             11.2     07:00

respuesta = json.loads(texto_api)
df_respuesta = pd.json_normalize(
    respuesta,
    record_path="value",
    meta=[["station", "name"]],
).reset_index(drop=True)
# record_path -> define que se convierte en filas
# meta -> define que informacion externa/padre en este caso
#         station - se repite y el que queremos es el name

df_respuesta["temp"] = pd.to_numeric(
    df_respuesta["value"].str.replace(",", "."), errors="coerce"
)

df_respuesta["fecha_utc"] = pd.to_datetime(df_respuesta["date"], unit="ms", utc=True)

print(df_respuesta)

#             date value quality station.name  temp         fecha_utc
# 0  1730865600000  -1,4       G    Stockholm  -1.4  2024-11-06 05:00
# 1  1730869200000  -2.0       G    Stockholm  -2.0  2024-11-06 06:00
# 2  1730872800000  -2,9       G    Stockholm  -2.9  2024-11-06 07:00

df = df_limpio.merge(
    df_respuesta[["fecha_utc", "temp"]],
    on="fecha_utc",
    how="left",
    validate="many_to_one",
)

print(df)

df["frio"] = np.where(df["temp"] <= -2, True, False)

print(df)

df_resumen = df.groupby("omrade").agg(total_mwh=("forbrukning_mwh", "sum"))
print(df_resumen)

df_media = df.groupby(["omrade", "frio"])["forbrukning_mwh"].mean().unstack()
print(df_media)

df_media = df_media.rename(columns={False: "media_no_frio", True: "media_frio"})

print(df_media)

resumen = (
    df_resumen.merge(df_media[["media_frio", "media_no_frio"]], on="omrade", how="left")
    .round(1)
    .reset_index()
)

print(resumen)

resumen.to_parquet(
    "/home/sebastian/datastudies/fase1-data-engineer/modulo-00-fundamentos/temas/tema02/datos/consumo_frio_por_barrio.parquet",
    index=False,
)

df_parquet = pd.read_parquet(
    "/home/sebastian/datastudies/fase1-data-engineer/modulo-00-fundamentos/temas/tema02/datos/consumo_frio_por_barrio.parquet"
)
print(df_parquet)
