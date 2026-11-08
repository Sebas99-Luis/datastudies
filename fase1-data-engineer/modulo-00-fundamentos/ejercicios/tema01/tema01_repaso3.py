# Un companero escribio este codigo para mostrar las temp de Örebro por hora
# en hora sueca. Tiene 3 errores

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

respuesta = {
    "station": {"name": "Örebro"},
    "value": [
        {"date": 1730865600000, "value": "-1.4"},
        {"date": 1730869200000, "value": "-2.0"},
        {"date": 1730872800000, "value": "-0.8"},
    ],
}


def hora_sueca(epoch_ms: int) -> str:
    """Convierte un epoch en milisegundos a texto 'HH:MM' en hora sueca."""
    fecha_utc = datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc)
    zona = fecha_utc.astimezone(ZoneInfo("Europe/Stockholm"))
    time_txt = zona.strftime("%H:%M")

    return time_txt


def tabla_horas(respuesta: dict) -> list[str]:
    """Devuelve una línea 'HH:MM -> temp °C' por cada medición."""
    lineas = []
    for m in respuesta["value"]:
        lineas.append(f"{hora_sueca(m['date'])} -> {float(m['value']):.1f} °C")

    return lineas


for linea in tabla_horas(respuesta):
    print(linea)

# el primer error que veo es que def hora:sueca no devuelte nada
# no tiene valor de return

# el segundo error era la sintax de como se hacia el cambio de fechas

# el tercer error era que en el return se gacia la conversion y eso generaba error
