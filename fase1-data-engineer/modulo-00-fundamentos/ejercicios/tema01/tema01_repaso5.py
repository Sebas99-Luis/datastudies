# Mini-caso desde cero
# Una empresa de mantenimiento de carreteras decide cada madrugada
# enviar las maquinas de sal y arena.
# Necesitan un infrome por estacion con las lecturas validas y decartadas¨
# las temperaturas minima y su hora y cuantas horas estuv bajo cero

import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from utils.clima_utils import validar_lectura

texto_api = """[
 {"station": {"name": "Östersund"},
  "value": [
   {"date": 1730865600000, "value": "0,4", "quality": "G"},
   {"date": 1730869200000, "value": "-1.2", "quality": "G"},
   {"date": 1730872800000, "value": "-2,5", "quality": "G"},
   {"date": 1730876400000, "value": "", "quality": "G"},
   {"date": 1730880000000, "value": "-0.3", "quality": "Y"}
  ]},
 {"station": {"name": "Åre"},
  "value": [
   {"date": 1730865600000, "value": "-4.1", "quality": "G"},
   {"date": 1730869200000, "value": "99", "quality": "G"},
   {"date": 1730872800000, "value": "-5,0", "quality": "G"},
   {"date": 1730876400000, "value": "-4.6", "quality": "G"}
  ]},
 {"station": {"name": "Storlien"},
  "value": [
   {"date": 1730865600000, "value": "", "quality": "G"},
   {"date": 1730869200000, "value": "error", "quality": "G"}
  ]}
]"""

# Reglas :
# 1. Las que no sean de calidad G se ignorar no cuentan ni como validas
#    ni como descartadas

# 2. Las medidas que si son G que no pasan la validacion son
#    descartadas y se avisa con "Descartada: <motivo>"

# 3. Si una estacion no tiene ninguna lectura valida
#    el infrome lo indica y el programa no se detiene

api = json.loads(texto_api)
ostersund = api[0]
åre = api[1]
storlien = api[2]
# print(ostersund)

# {'station': {'name': 'Östersund'},
# 'value': [
# {'date': 1730865600000, 'value': '0,4', 'quality': 'G'},
# {'date': 1730869200000, 'value': '-1.2', 'quality': 'G'},
# {'date': 1730872800000, 'value': '-2,5', 'quality': 'G'},
# {'date': 1730876400000, 'value': '', 'quality': 'G'},
# {'date': 1730880000000, 'value': '-0.3', 'quality': 'Y'}
# ]}


def analizar_estacion(estacion: dict) -> dict:
    validas = 0
    descartadas = 0
    bajo_cero = 0
    min_temp = None
    mejor_date = None

    for value in estacion["value"]:
        if value["quality"] != "G":
            continue
        try:
            valor = validar_lectura(value)
        except ValueError as e:
            print(f"Descartada: {e}")
            descartadas += 1
        else:
            validas += 1
            if valor < 0:
                bajo_cero += 1

            if min_temp is None or min_temp > valor:
                min_temp = valor
                mejor_date = value["date"]
    if mejor_date is None:
        time_txt = None
    else:
        fecha_utc = datetime.fromtimestamp(mejor_date / 1000, tz=timezone.utc)
        zona = fecha_utc.astimezone(ZoneInfo("Europe/Stockholm"))
        time_txt = zona.strftime("%H:%M")

    return {
        "validas": validas,
        "descartadas": descartadas,
        "min": min_temp,
        "hora": time_txt,
        "bajo_cero": bajo_cero,
    }


# print(analizar_estacion(ostersund))
# print(analizar_estacion(åre))
# print(analizar_estacion(storlien))


def informe(respuestas: list[dict]) -> dict:
    return {
        estacion["station"]["name"]: analizar_estacion(estacion)
        for estacion in respuestas
    }


api_dict = informe(api)
# print(api_dict)

for estacion, values in api_dict.items():
    if values["min"] is None:
        print(
            f"{estacion}:, {values['validas']} válidas, {values['descartadas']} descartadas | SIN DATOS VÁLIDOS"
        )
        continue
    else:
        print(
            f"{estacion}: {values['validas']} válidas, {values['descartadas']} descartadas | minima {values['min']} °C a las {values['hora']} | {values['bajo_cero']} horas bajo cero"
        )
