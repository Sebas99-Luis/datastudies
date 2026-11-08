# Ejercicio 2: de la API a la tabla
# Practica: Tema 1 (json, comprehensions, funciones)
#           Tema 2 (DataFrame, to_numeric, fechas y zonas,
#                   filtrar, groupby y merge)
# Tipo: completar codigo

# Una cadena de hoteles de Gotland y Skåne quiere ver las temp
# de la madrugadra en sus ubicaciones, junto con la informacion
# de cada estacion.
# Los datos llegan de la API, en el formato de SMHI que ya
# conoces del Tema 1. Hay que pasarlos a una tabla de pandas.
# El reto nuevo: el nombre de la estacion esta fuera de la lista
# de mediciones.

"""Predicciones:
1. despues del paso tendra 6 filas y despues del paso 4 tendra 3 filas
2. de minima tendra en visby 3.8 y en ystad tendra 5.0
3. por que en el merge vamos a unirlos en left eso quiere decir que vamos
    a usar los datos de la tabla resumen y los que no concuender en la clave
    de la tabla de la derecha no se unen"""

import json

import pandas as pd

texto_api = """[
 {"station": {"name": "Visby"},
  "value": [
   {"date": 1730865600000, "value": "4,1", "quality": "G"},
   {"date": 1730869200000, "value": "3.8", "quality": "G"},
   {"date": 1730872800000, "value": "", "quality": "G"}
  ]},
 {"station": {"name": "Ystad"},
  "value": [
   {"date": 1730865600000, "value": "5.0", "quality": "G"},
   {"date": 1730869200000, "value": "error", "quality": "G"},
   {"date": 1730872800000, "value": "4.4", "quality": "Y"}
  ]}
]"""

info_estaciones = pd.DataFrame(
    {
        "estacion": ["Visby", "Ystad", "Kalmar"],
        "region": ["Gotland", "Skåne", "Kalmar län"],
        "altura_m": [47, 2, 15],
    }
)


def aplanar(respuestas: list[dict]) -> list[dict]:
    """Devuelve una fila (dict) por medición, con el nombre de su estación."""
    return [
        {
            "estacion": r["station"]["name"],
            "date": m["date"],
            "value": m["value"],
            "quality": m["quality"],
        }
        for r in respuestas
        for m in r["value"]
    ]


# 1. JSON → lista → DataFrame
respuestas = json.loads(texto_api)
df = pd.DataFrame(aplanar(respuestas))
print(df)

# 2. Texto → número (lo que no se pueda, NaN)
df["temp"] = pd.to_numeric(
    df["value"].str.replace(",", ".", regex=False),
    errors="coerce",
)

# 3. Epoch → hora sueca HH:MM
df["hora_suecia"] = (
    pd.to_datetime(df["date"], unit="ms", utc=True)
    .dt.tz_convert("Europe/Stockholm")
    .dt.strftime("%H:%M")
)
print(df)

# 4. Solo mediciones válidas: calidad G y temperatura no nula
df_ok = df[(df["quality"] == "G") & (df["temp"].notna())]

# 5. Resumen por estación
resumen = (
    df_ok.groupby("estacion")
    .agg(minima=("temp", "min"), n=("date", "count"))
    .reset_index()
)

# 6. Añadir la información de cada estación
final = resumen.merge(info_estaciones, on="estacion", how="left")
print(final)
