# Un sensor envia lecturas que pueden venir mal de varias formas
# Escribe un validaro que explique por que descarta cada una

lecturas = [
    {"value": "4,2"},
    {"value": ""},
    {"value": "85"},
    {"value": "-3.1"},
    {"value": "abc"},
]


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


def procesar_lecturas(lecturas: list[dict]) -> dict:
    """Processar la lista con dict para convertirlo en un dict que
    nos diga todos valores validos y las descartadas"""
    if not lecturas:
        raise ValueError("No hay lecturas para procesar")

    validas = []
    descartadas = 0

    for lectura in lecturas:
        try:
            valor = validar_lectura(lectura)

        except ValueError as e:
            print(f"Descartada: {e}")
            descartadas += 1
        else:
            validas.append(valor)

    return {"validas": validas, "descartadas": descartadas}


lecturas_2 = []
resultado = procesar_lecturas(lecturas)
print(resultado)
try:
    procesar_lecturas(lecturas_2)
except ValueError as e:
    print(f"Error: {e}")
