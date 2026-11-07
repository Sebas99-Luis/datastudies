# Ejercicio 1: lluvia acumulada
# Bloque 1, 3 , 4, 5
# Empresa de seguros quiere saber que ciudades acumulron
# mucha lluvia en los ultimos dias, para anticipar inundaciones

lluvia = {
    "Göteborg": ["5,2", " 3.1", "0,0", "7.4"],
    "Stockholm": ["1.2", "0,8", " 0.0 "],
    "Umeå": ["2,5", "4.0", "6,1"],
}


def parsear_valor(texto: str) -> float:
    """limpia y convierte el str de el dict en float"""
    limpio = texto.strip().replace(",", ".")
    return float(limpio)


lluvia_g_index0 = lluvia["Göteborg"][0]
print(parsear_valor(lluvia_g_index0))


def total_textos(valores: list[str]) -> float:
    """recibe la lista de textos de una ciudad y devuelve la suma de la
    lluvia, redondeada a 1 decimal"""
    lista = [parsear_valor(v) for v in valores]
    return round(sum(lista), 1)


lluvia_st = lluvia["Stockholm"]
print(total_textos(lluvia_st))


def ciudades_con_mucha_lluvia(
    datos: dict[str, list[str]], umbral: float = 10.0
) -> dict[str, float]:
    """Decuelve las ciudades c de sus listas v
    solo si es mayor o igual del umbral"""
    dict_lluvia = {
        c: total_textos(v) for c, v in datos.items() if total_textos(v) >= umbral
    }

    return dict_lluvia


new_dict = ciudades_con_mucha_lluvia(lluvia)

for c, s in new_dict.items():
    print(f"{c}: {s:.1f} mm")

new_dict_umbral = ciudades_con_mucha_lluvia(lluvia, umbral=2.0)

for c, s in new_dict_umbral.items():
    print(f"{c}: {s:.1f} mm")
