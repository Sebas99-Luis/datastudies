# Ejercicio 3: minimo por estacion
# Archivo temas/clima_utils.py
# Practica: todo el tema
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from temas.clima_utils import parsear_temp_segura, minima_estacion, resumen_estaciones

"""Una empresa de energia de Suecia ajusta su produccion de calefaccion
urbana segun el frio.
Todos los dias su equipo de operaciones necesitan saber,
para cada estacion, cual fue la tem minima de la madrugada y
a que hora occurio, en hora sueca.
"""

texto_api = """[
 {"station": {"name": "Umeå"},
  "value": [
   {"date": 1730865600000, "value": "-6.1", "quality": "G"},
   {"date": 1730869200000, "value": "-8,3", "quality": "G"},
   {"date": 1730872800000, "value": "-9.0", "quality": "Y"},
   {"date": 1730876400000, "value": "error", "quality": "G"}
  ]},
 {"station": {"name": "Luleå"},
  "value": [
   {"date": 1730865600000, "value": "-10.2", "quality": "G"},
   {"date": 1730869200000, "value": "", "quality": "G"},
   {"date": 1730872800000, "value": "-11,4", "quality": "G"},
   {"date": 1730876400000, "value": "-10.9", "quality": "G"}
  ]}
]"""
# Una lista(texto_api) -> dentro tiene dos dict(1 y 2)
# 1 -> tiene dos dict (station -> )otro dict )
#                      (value) - > tiene una lista con dicts

api = json.loads(texto_api)
resumen = resumen_estaciones(api)
for c, v in resumen.items():
    print(f"{c}: minima {v["min"]:.1f} °C a las {v["hora"]} (hora sueca)")
