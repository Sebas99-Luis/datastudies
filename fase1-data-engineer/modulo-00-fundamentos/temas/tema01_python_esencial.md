# Tema 1 - Python esencial
## Bloque 1: tipos de datos y conversion

Cada valor en Python tiene un tipo, y ese dipo decide que puedes hcer con el.

- Puedes sumar dos **float**, pero si intentas sumar un **str** con un **float** obtienes un error.


int -> IDs de esatcion, conteos -> 98210

float -> temperaturas, precios -> -3.2

str -> nombres, codigos, fechas sin convertir -> "Stockholm"

bool -> flags(la medicion es valida?) -> True

None -> dato faltante(en Spark sera null) -> None

##### Por que es importante
- Las Apis y los CSV casi nunca te entregan los tipos correctos.
- Si no la conviertes, no se pueden hacer calculos a futuro.


## Bloque 2: Listas

Una **lista** es una coleccion ordenada y modificable de valores, []

Una serie de valores del mismo tipo, como las temperauras horarias de una ciudad, los nombres de las ciudades de un pais o los archivos que tienes que cargar.

## Bloque 3: Diccionarios

Una coleciion de **clave -> valor**, entre{}.

- Al valor no se accede por posicion, sino por su clave.
- Loa archivos JSON se conviertne en diccionarios y listal al leerlo en Python.
- Las repuestas de Apis, config files y eventos de logs funcionan en diccionarios.


## Bloque 4: list y dict comprehensions

Una forma corta de crear una lista o diccionario nuevo a partir de otro transformando o filtrando cada elemento en una sola linea.

- Convertir todas las temp de string a float, quedarte solo con las mediciones de calidad "G" o armar un dict ciudad -> promedio.


## Bloque 5: funciones

Un bloque de codigo con nombre que recibe datos(parametros), hace una funcion con ellos y devuelve un resultado.

Lo escribes una vez y lo usas todas las veces que sean necesarias.


## Bloque 6: manejo de errores

Es la forma de anticipar los errores y decidir que hacer en ese caso, en ligar de que el programa se detenga.

- Los datos reales vienen sucios. Una API puede devolcer "" en lugar de un numero, un archivo puede no existir...
- En un pipeline que corre solo a las 3 AM, un valor malo no deberia tirar abajo la carga de las otras 500 buenas


## Bloque 7: modulos

Un modulo es un archivo .py con codigo que puedes importar desde otro archivo.

- Python trae modulos listos, y tambien se puede crear propios.

- **No reinventar la rueda**.
  - Leer JSON, trabajar con fechas o clacular la media ya existe y no crearlos otra vez es lo correcto

- Organizar tu propio codigo.
  - Las funciones reutilizables, viven en un archivo aparte, y todos sus notebooks y scripts las importan.

  - En Databricks se hace igual, si importan funcionen desde archivos .py del workspace o de un git folder


