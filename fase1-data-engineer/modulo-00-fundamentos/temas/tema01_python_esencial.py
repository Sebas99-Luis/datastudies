# Ejemplo

# --- Bloque 1: tipos y conversion ---
medicion = {"station": 98210, "value": "-3.2", "quality": "G"}

temp_texto = medicion["value"]
print(type(temp_texto))  # <class 'str'>

temp = float(temp_texto)  # conversion explicita de str a float
print(type(temp), temp)  # <class 'float'>

ciudad = "Stockholm"
print(f"{ciudad}: {temp:.1f} °C")  # f-string con 1 decimal

lluvia = None  # dato faltante
print(lluvia is None)  # True -> con None se usa 'is', no ==


# --- Bloque 2: listas ---
temps = [-3.2, -2.8, -1.5, 0.4, 1.1]  # temps horarias, Stockholm

print(temps[0])  # -3.2 -> primera
print(temps[-1])  # 1.1 -> última
print(temps[1:3])  # [-2.8, -1.5, 0.4] -> slice de 1 a 3
print(len(temps))  # 5 -> cantidad de elementos

temps.append(2.0)  # agrego un elemento al final(modifica la lista original)
print(
    max(temps), min(temps), sum(temps) / len(temps)
)  # 2.0 -3.2  -0.4 -> max, min, promedio

for t in temps:  # recorro la lista
    if t < 0:
        print(f"Bajo cero: {t}")

print(-1.5 in temps)  # True -> existe el valor en la lista?


# --- Bloque 2: practica guiada ---
gbg = [4.1, 3.8, 3.5, 3.9, 4.6, 5.2]
# 1 - Imprime la tercera medicion
print(gbg[2])  # 3.5
# 2 - Imprime las ultimas 3 mediciones usando slicing con indice negativo
print(gbg[-3:])
# 3 - Calcule el promedio y lo imprima con un f-string con 2 decimales
promedio = sum(gbg) / len(gbg)
print(f"Promedio: {promedio:.2f}")  # Promedio: 4.18


# --- Bloque 3: diccionarios ---
estacion = {"id": 98210, "nombre": "Stockholm", "activa": True}

print(estacion["nombre"])  # Stockholm -> accedo a un valor por su clave
estacion["altura_m"] = 44  # agrego un nuevo par clave-valor
estacion["activa"] = False  # modifico un valor existente

print(estacion.get("pais"))  # None -> la clave no existe, pero no da error
print(
    estacion.get("pais", "SE")
)  # SE -> la clave no existe, pero devuelve un valor por defecto

for clave, valor in estacion.items():  # recorro el diccionario
    print(f"{clave}: {valor}")

# Anidado: un dict con una lista de dict dentro (forma tipica de un JSON de un API)
respuesta = {
    "station": {"key": 98210, "name": "Stockholm"},
    "value": [
        {"date": 1730887200000, "value": -3.2, "quality": "G"},
        {"date": 1730890800000, "value": -2.8, "quality": "G"},
    ],
}

print(respuesta["station"]["name"])
# Stockholm -> accedo a un valor dentro de un dict anidado

print(respuesta["value"][0]["value"])
# -3.2 -> string


# --- Bloque 3: prectica guiada ---
# Usando respuesta dict
# 1. Imprimer el id de la estacion (key)
print(respuesta["station"]["key"])
# 2. Imprimir cuantas mediciones hay
print(len(respuesta["value"]))
# 3. Imprimir la ultima medicion como floar. Usa indice negativo
# print(float(respuesta["value"][-1]["value"])) ->
ultima = respuesta["value"][-1]
temp_ultima = float(ultima["value"])
print(temp_ultima)
# 4. Intente leer la clave "unit" de respuesta sin que falle,
# usando "°C" como valor por defecto
print(respuesta.get("unit", "°C"))


# --- Bloque 4: comprehensions ---
textos = ["-3.2", "-2.8", "1.5", "0.4"]  # lista

# Con un for normal:
temps = []
for t in textos:
    temps.append(float(t))

# Lo mismo con list comprehension:
temps = [float(t) for t in textos]  # [-3.2, -2.8, 1.5, 0.4]

# Con filtro: solo las bajo cero
bajo_cero = [t for t in temps if t < 0]  # [-3.2, -2.8]

# Dict comprehension: clave -> valor
ciudades = {"Stockholm": [-3.2, -2.8], "Malmö": {2.1, 3.0}}

promedios = {c: sum(v) / len(v) for c, v in ciudades.items()}


# --- Práctica guiada – Paso 4, punto 1 (repetición) ---
respuesta_malmo = {
    "station": {"key": "52350", "name": "Malmö"},
    "value": [
        {"date": 1730887200000, "value": "2.1", "quality": "G"},
        {"date": 1730890800000, "value": "2.6", "quality": "Y"},
        {"date": 1730894400000, "value": "3.0", "quality": "G"},
    ],
}
# 1.1 con for normal usa append()
temps_malmo = []
for m in respuesta_malmo["value"]:
    temps_malmo.append(float(m["value"]))

# 1.2 list comprehension
temps_malmo = [float(m["value"]) for m in respuesta_malmo["value"]]


# 2. filtrp con list comprehens
buenas_malmo = []
for m in respuesta_malmo["value"]:
    if m["quality"] == "G":
        buenas_malmo.append(m)

# 2.1
buenas_malmo = [m for m in respuesta_malmo["value"] if m["quality"] == "G"]


# --- Bloque 5: funciones ---
def parsear_temp(texto: str) -> float:
    """Convierte una temp en texto ("2,75", "-3.2") a float"""
    limpio = texto.strip().replace(",", ".")
    return float()


print(parsear_temp(" 2,75"))  # 2.75
print(parsear_temp("-3.2"))  # -3.2


def promedio(valores: list[float], decimales: int = 1) -> float:
    """Promedio redondeado.`decimales` es opcional(por defecto 1)"""
    return round(sum(valores) / len(valores), decimales)


temps = [2.1, 2.6, 3.0]
print(promedio(temps))
print(promedio(temps, decimales=3))


# --- Práctica guiada – Paso 5 ---
def temps_validas(respuesta: dict, calidad: str = "G") -> list[float]:
    """ "Devuelve las temperaturas (float) de las mediciones con la calidad indicada."""
    return [float(m["value"]) for m in respuesta["value"] if m["quality"] == calidad]


# --- Bloque 6: manejo de errores ---
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


print(parsear_temp_segura("2,5"))  # 2.5
print(parsear_temp_segura(""))  # Valor invalido: ""  -> None


# A veces el valor si se puede convertir, pero es un valor que no tiene sentido
def validar_temp(valor: float) -> float:
    """Lanza ValueError si la temperatura es fisicamente imposible"""
    if not -60 <= valor <= 45:
        raise ValueError(f"Temperatura imposible: {valor}")
    return valor


# --- Práctica guiada – Paso 6 ---
respuesta_kiruna = {
    "station": {"key": "180940", "name": "Kiruna"},
    "value": [
        {"date": 1730887200000, "value": "-12.4", "quality": "G"},
        {"date": 1730890800000, "value": "", "quality": "G"},
        {"date": 1730894400000, "value": "-13,1", "quality": "G"},
        {"date": 1730898000000, "value": "error", "quality": "G"},
    ],
}

# temps_validas(respuesta_kiruna)


# --- Práctica guiada – Paso 6b: raise y finally ---
def validar_temp(valor: float) -> float:
    if not -60 <= valor <= 45:
        raise ValueError(f"Temperatura imposible: {valor}")
    return valor


for t in [-12.4, 85.0, 3.1]:
    try:
        validar_temp(t)
    except ValueError as e:
        print(f"Descartada → {e}")
    else:
        print(f"OK: {t}")
    finally:
        print("--- revisada")


# --- Bloque 7: módulos ---
import json  # importa el modulo completo
from datetime import datetime, timezone  # importa solo lo que necesitas
import statistics as st  # con alisas (nombre corto)

# llamar funcion desde mis archivos
from clima_utils import temps_validas_seguras

# json: texto JSON(lo que llega de una API) -> dict de Python
texto_api = '{"station": {"name": "Lund"}, "value": [{"value": "4.2"}]}'
datos = json.loads(texto_api)
print(type(datos), datos["station"]["name"])

# datetime: epoch en milisegundos -> fecha legible
ms = 1730887200000
fecha = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
print(fecha)
print(fecha.strftime("%Y-%m-%d %H:%M"))

# statistics: estadistica basica
temps = [2.1, 2.6, 3.0, 25.0]
print(st.mean(temps), st.median(temps))


respuesta_malmo = {
    "station": {"key": "52350", "name": "Malmö"},
    "value": [
        {"date": 1730887200000, "value": "2.1", "quality": "G"},
        {"date": 1730890800000, "value": "2.6", "quality": "Y"},
        {"date": 1730894400000, "value": "3.0", "quality": "G"},
    ],
}

# --- Práctica guiada – Paso 7 ---
# from datetime import datetime, timezone  # importa solo lo que necesitas

fecha_m = respuesta_malmo["value"][0]["date"]
print(fecha_m)

fecha_m = datetime.fromtimestamp(fecha_m / 1000, tz=timezone.utc)
print(fecha_m)

fecha_m_f = fecha_m.strftime("%Y-%m-%d %H:%M")
print(fecha_m_f)

value_m = respuesta_malmo["value"][0]["value"]
value_m_float = float(value_m)
print(value_m_float)

print(f"{fecha_m_f} UTC -> {value_m_float:.1f} °C")

for m in respuesta_malmo["value"]:
    date_m = m["date"]
    date_m = datetime.fromtimestamp(date_m / 1000, tz=timezone.utc)
    date_m_f = date_m.strftime("%Y-%m-%d %H:%M")

    value_malmo = m["value"]
    value_malmo_float = float(value_malmo)

    print(f"{date_m_f} UTC -> {value_malmo_float:.1f} °C")


print(temps_validas_seguras(respuesta_kiruna))
