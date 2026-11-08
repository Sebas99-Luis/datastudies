datos = [
    {"station": {"name": "Visby"}, "value": [{"value": "5.1"}, {"value": "4.7"}]},
    {"station": {"name": "Ystad"}, "value": [{"value": "6.0"}]},
]

print(len(datos))  # a)
print(datos[1]["station"]["name"])  # b)
print(len(datos[0]["value"]))  # c)
print([e["station"]["name"] for e in datos])  # d)
print({e["station"]["name"]: len(e["value"]) for e in datos})  # e)
print(datos["station"])  # f)

for e in datos:  # g)
    print(e["value"][-1]["value"])


nombres = ["Visby", "Ystad", "Kiruna"]

print([n.upper() for n in nombres])  # h)

for n in nombres:  # i)
    print(n.upper())

print({n: len(n) for n in nombres})  # j)

print(nombres["Visby"])  # k)


ciudades = ["Visby", "Ystad"]
largos = {"Visby": 5, "Ystad": 5}

print(ciudades[1])  # l)
print(largos["Ystad"])  # m)
print(largos[0])  # n)
print(ciudades[-1][0])  # o)

estaciones = ["Kiruna", "Lund", "Malmö"]

print(estaciones[0])  # p)
print(estaciones[2][-1])  # q)
print(estaciones[1][:2])  # r)
