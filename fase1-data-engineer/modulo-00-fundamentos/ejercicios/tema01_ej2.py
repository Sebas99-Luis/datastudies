# Ejercicio 2: ecnuentra los errores
# Practica: bloques 3,5,6,7

# Una empresa de logistica planifica las rutas de sus caminos de madrugada
# Si la temp baja de 0°C, hay riesgo de hielo en la carretera
# Tienen que avisar a los conductores
# Se escrbiio este script pero no fucniona.
# Tiene 4 errores

import json
from datetime import datetime, timezone

texto_api = """{"station": {"key": "52350", "name": "Malmö"},
 "value": [
  {"date": 1730865600000, "value": "1.2", "quality": "G"},
  {"date": 1730869200000, "value": "-0,4", "quality": "G"},
  {"date": 1730872800000, "value": "", "quality": "G"},
  {"date": 1730876400000, "value": "-1.1", "quality": "G"},
  {"date": 1730880000000, "value": "0.3", "quality": "G"}
 ]}"""


def horas_con_helada(respuesta: dict, limite: float = 0.0) -> list[str]:
    """Devuelve las horas (UTC, 'HH:MM') con temperatura <= limite."""
    horas = []
    for m in respuesta["value"]:
        try:
            temp = float(m["value"].strip().replace(",", "."))
        except ValueError:
            print(f"Valor inválido: {m['value']!r}")
            continue
        if temp <= limite:
            fecha = datetime.fromtimestamp(m["date"] / 1000, tz=timezone.utc)
            horas.append(fecha.strftime("%H:%M"))

    return horas


respuesta = json.loads(texto_api)
heladas = horas_con_helada(respuesta)
print(f"Horas con helada: {len(heladas)}")
for h in heladas:
    print(h)


# 1 error que aparece en el la transformacion json de la linea 38
# json.load trae un archivo pero en este caso tenemos un str
# el correcto es usar json.loads(texto.api)


# Al intentar correr el codigo otra vez solo sale Horas con helada:0
# primer error que vi la indexsacion del return estaba dentro de for loop
# despues sale que la llamada a la funcion en la linea 40 sale mal
# y sale que es por que en la linea 33 tienen un error especialmente
# tiene un ValueError year 56819 is out of range
# tenia dos error
# el primero es que no se dividia entre 1000
# el segundo error es que la fecha no daba el resultado
# por que el formato estaba "%H:%m" en vez de -> "%H:%M"
