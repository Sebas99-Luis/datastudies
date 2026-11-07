from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def temps_validas_seguras(respuesta: dict, calidad: str = "G") -> list[float]:
    """Convertir de forma segura un dict sus tmp a float solo los valors
    que sean de calidad"""
    temps = []
    for m in respuesta["value"]:
        if m["quality"] != calidad:
            continue
        texto = m["value"].strip().replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print(f"Valor invalido: {texto!r}")
        else:
            temps.append(valor)
    return temps


def parsear_temp_segura(texto: str) -> float | None:
    """Convierte texto a floar; devuelve None si el texto no es un numero"""
    try:
        valor = float(texto.strip().replace(",", "."))  # lo que puede fallar
    except ValueError:
        print(f"Valor invalido: {texto!r}")  # que hacer si es que falla
        return None
    else:
        return valor  # se ejecuta solo si no falla
    finally:
        pass  # se ejecuta SIEMPRE (ej. cerrar un archuvo o una conexion)


# {'station': {'name': 'Luleå'},
# 'value': [
# {'date': 1730865600000, 'value': '-10.2', 'quality': 'G'},
# {'date': 1730869200000, 'value': '', 'quality': 'G'},
# {'date': 1730872800000, 'value': '-11,4', 'quality': 'G'},
# {'date': 1730876400000, 'value': '-10.9', 'quality': 'G'}
# ]}


def minima_estacion(respuesta: dict) -> dict:
    """Guardar la minima temperatura de cada estacion y su fecha"""
    min_temp = None
    date = None

    for m in respuesta["value"]:
        if m["quality"] != "G":
            continue

        temp = parsear_temp_segura(m["value"])
        if temp is None:
            continue
        if min_temp is None or temp < min_temp:
            min_temp = temp
            date = m["date"]

    date_utc = datetime.fromtimestamp(date / 1000, tz=timezone.utc)
    date_suecia = date_utc.astimezone(ZoneInfo("Europe/Stockholm"))
    time_txt = date_suecia.strftime("%H:%M")
    return {"min": min_temp, "hora": time_txt}


def resumen_estaciones(respuesta: list[dict]) -> dict[str, dict]:
    """Devuelve un dict con el nombre de la estacion y otro dict
    con la hora y su temp minima"""
    return {
        estacion["station"]["name"]: minima_estacion(estacion) for estacion in respuesta
    }


def validar_lectura(lectura: dict) -> float:
    """Devuelve la temperatura como float.
    Lanza ValueError si está vacía, no es un número o
    está fuera de -60 a 45."""

    valor = lectura["value"].strip().replace(",", ".")
    if valor == "":
        raise ValueError("Valor vacío")

    valor_float = float(valor)
    if valor_float < -60 or valor_float > 45:
        raise ValueError(f"Temperatura imposible: {valor_float}")

    return valor_float
