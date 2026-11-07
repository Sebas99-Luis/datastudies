# Una cadena de cefetrias quiere poner un cartel
# diaria anunciando la ciudad mas calida del dia¨

temps = {"Visby": 5.1, "Ystad": 6.0, "Kiruna": -12.4, "Lund": 6.3}

# Complete los huecos ---:


def estacion_mas_calida(temps: dict[str, float]) -> dict:
    """Devuelve la ciudad con la temperatura más alta y su valor."""
    mejor_ciudad = None
    mejor_temp = None

    for ciudad, temp in temps.items():
        if mejor_temp is None or temp > mejor_temp:
            mejor_ciudad = ciudad
            mejor_temp = temp

    return {"ciudad": mejor_ciudad, "temp": mejor_temp}


resultado = estacion_mas_calida(temps)
print(resultado)
print(f"La más cálida: {resultado['ciudad']} ({resultado['temp']} °C)")
