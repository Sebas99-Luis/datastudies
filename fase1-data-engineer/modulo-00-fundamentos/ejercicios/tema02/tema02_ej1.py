# Ejercicio 1 del tema 2 : lluvia en Västra Götland

# Practica: Bloques 2 (leer y explorar),
#                   3 (filtrar),
#                   4 (nulos, duplicados y fechas),
#                   5 (columnas y orden), 6 (agrupar)
#                   8 (guardar)

# Una empresa municipal de agua y alcantarillado VA-bolag de la region
# quiere saber que municipios recibieron ams lluvia en los primeros
# dias de nov, para revisar la capacidad de sus desagues.


# Lo que tienes que hacer:

# 0. Predicciones primero. Al principio del archivo, en un comentario, escribe antes de programar nada:
#       - El shape del CSV leído.
#       - Cuántas filas tendrá la tabla limpia.
#       - El total de lluvia de cada municipio después de limpiar.
# 1. Leer el CSV correctamente e imprimir shape y dtypes.
# 2. Explorar: imprimir cuántos nulos hay en cada columna y cuántas filas duplicadas hay.
# 3. Limpiar en df_limpio, con method chaining: solo calidad G, sin lluvia nula, sin duplicados por estación + fecha, e índice limpio.
# 4. Convertir datum a fecha.
# 5. Crear la columna lluvia_fuerte: True si la lluvia del día es mayor o igual a 10 mm.
# 6. Resumir por municipio en resumen, con las columnas total_mm (redondeado a 1 decimal), max_mm, dias y dias_fuertes. Ordénalo del municipio con más lluvia total al de menos, con el índice limpio.
# 7. Guardar resumen como Parquet, volver a leerlo e imprimirlo.

"""Prediciones:
shape (10, 4)
limpios un total de 7 filas
GT -> 18.0
Borås -> 21.5
Alingsås -> 19.2"""

# --- 1 leer y shapes types ---
import pandas as pd
import numpy as np

df = pd.read_csv("temas/tema02/datos/lluvia_vg.csv", sep=";", decimal=(","))
print(df)

print(df.shape)

print(df.dtypes)


# --- 2 explorar CSV ---
print(df.isna().sum())

print(df["nederbord_mm"].isna())

print(df.duplicated())

print(df.duplicated().sum())


# --- 3 Limpiar ---
df_limpio = (
    df[df["kvalitet"] == "G"]
    .dropna(subset="nederbord_mm")
    .drop_duplicates(subset=["station", "datum"])
    .reset_index(drop=True)
)
print(df_limpio)

# --- 4. convertir datum ---
print(df_limpio["datum"].dtypes)

df_limpio["datum"] = pd.to_datetime(df_limpio["datum"])
print(df_limpio["datum"].dtypes)


# --- 5. crear columna lluvia fuerte ---

df_limpio["lluvia_fuerte"] = np.where(df_limpio["nederbord_mm"] >= 10, True, False)
print(df_limpio)

# -- 6 resumen por municipio ---
resumen = (
    df_limpio.groupby("station")
    .agg(
        total_mm=("nederbord_mm", "sum"),
        max_mm=("nederbord_mm", "max"),
        dias=("datum", "count"),
        dias_fuertes=("lluvia_fuerte", "sum"),
    )
    .round(1)
    .sort_values("total_mm", ascending=False)
    .reset_index()
)

print(resumen)


# --- 7 guarda y cargar en paguet otra vez ---
resumen.to_parquet("temas/tema02/datos/resumen_lluvia.parquet", index=False)

df_resumen = pd.read_parquet("temas/tema02/datos/resumen_lluvia.parquet")
print(df_resumen)
