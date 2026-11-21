# Heurística de A*

**Autor:** Anwar Joseph

## 1. La heurística elegida

> **h(punto) = distancia en línea recta, en metros, entre el punto y el destino** (mirando el plano: x e y).

Es como preguntarle a alguien: «si pudieras volar derecho hasta el destino, ¿cuántos metros serían?». A* usa
esa respuesta para decidir cuál de los puntos pendientes conviene revisar primero: el que tenga menor
**costo ya recorrido + estimación de lo que falta**.

Ejemplo: de la *Portería Principal* a la *Biblioteca* la línea recta mide 318,6 m, y el costo real de la mejor ruta
es 435,0. La estimación es menor que el costo real, como debe ser.

## 2. Qué significa «admisible» y por qué lo es

Una heurística es **admisible** si **nunca sobreestima**: lo que dice que falta es siempre menor o igual al
costo real de lo que falta. Si la heurística se pasara de pesimista (dijera «falta más de
lo que de verdad falta»), A* podría descartar la mejor ruta pensando que es muy cara y devolver una ruta peor sin
avisar.

**Argumento (en cuatro pasos):**

1. **Un tramo nunca mide menos que la línea recta entre sus extremos.** Un camino real puede tener curvas, pero no
   puede ser más corto que ir derecho. Los datos del campus cumplen esto y el programa lo revisa al cargarlos
   (si algún dato lo rompe, lanza un error con el nombre del tramo).
2. **El costo de un tramo nunca es menor que su distancia.** El costo es distancia × factor de pendiente, y el
   factor es 1,0, 1,5 o 2,5: nunca menor que 1. Entonces: línea recta ≤ distancia ≤ costo.
3. **Una ruta es una cadena de tramos.** Para ir de un punto N al destino, la ruta pasa por varios tramos seguidos.
   Su costo es la suma de los costos de los tramos, que es mayor o igual que la suma de las líneas rectas de cada
   tramo (por el paso 2).
4. **Ir en varios pedazos rectos nunca es más corto que ir derecho.** Esto es la desigualdad triangular: la suma
   de las líneas rectas de cada tramo es mayor o igual que la línea recta directa de N al destino.

Juntando todo: **costo de cualquier ruta de N al destino ≥ línea recta de N al destino = h(N)**. En particular
también vale para la mejor ruta, así que h(N) ≤ costo real. Eso es exactamente ser admisible.

**¿Y cuando hay puertas cerradas u obras?** Cerrar un tramo solo puede quitar caminos posibles; el costo real de la
mejor ruta que queda sólo puede subir (o la ruta puede dejar de existir). La heurística no cambia, así que sigue
sin sobreestimar a cualquier hora. Por eso es la misma heurística a las 17:45 y a las 18:15.

**Además es consistente** (una propiedad un poco más fuerte): para cualquier tramo entre A y B,
h(A) ≤ costo(A, B) + h(B). Sale del mismo argumento: la línea recta de A al destino es menor o igual que
la línea recta de A a B más la de B al destino (desigualdad triangular), y la línea recta de A a B es menor o igual
que el costo del tramo. La consistencia permite que A* revise cada punto una sola vez y que la primera vez que
llegue al destino ya sea con la ruta de menor costo; por eso el código puede marcar los puntos como «ya explorados».

## 3. Comprobación con los datos del campus

El argumento anterior se comprobó con números, con `python verificar_heuristica.py` (usa un Dijkstra aparte,
para que la comprobación no dependa del propio A*):

```
VERIFICACIÓN DE LA HEURÍSTICA (distancia en línea recta)
======================================================================
1) En cada uno de los 90 tramos se cumple:
      línea recta <= distancia del tramo <= costo del tramo
   Tramos que NO lo cumplen: 0

2) Se comparó la estimación con el costo real de 3540 pares (origen, destino):
   Pares donde la heurística SOBREESTIMA el costo real: 0
   Razón estimación/costo real: promedio 0.59, máxima 0.99 (Laboratorio de Química -> Gimnasio).
   (Una razón <= 1 en todos los pares significa que nunca sobreestima.)

3) Consistencia: h(A) <= costo(A,B) + h(B) en 10800 combinaciones
   (tramo, sentido, destino). Violaciones: 0

RESULTADO: la heurística es admisible (y consistente) con los datos del campus.
```

Las pruebas automáticas (`python pruebas.py`) repiten esta comprobación y además verifican que A* devuelve el
costo óptimo en los 3.540 pares de puntos, tanto a las 12:00 como a las 18:15.

**Un contraejemplo para ver qué pasaría con una heurística NO admisible:** si se usara el **doble** de la línea
recta, sobreestimaría el costo real en 2.766 de los 3.540 pares. A* seguiría funcionando, pero ya no
garantizaría la ruta de menor costo.

## 4. Límites de la heurística

- **No usa la pendiente ni las puertas.** Por eso es una estimación optimista: en promedio vale el 59 % del costo
  real (máximo 99 %). Es una heurística segura pero no muy ajustada. Una heurística más ajustada seguiría siendo
  admisible si agregara, por ejemplo, el esfuerzo mínimo inevitable por subir la diferencia de altura entre el punto y
  el destino; no la implementé para mantener el código simple.
- **Se rompería si los datos fueran incorrectos:** una distancia menor que la línea recta, o un factor de
  pendiente menor que 1 (por ejemplo, un «descuento» por bajar). Por eso el programa revisa las distancias y el factor
  nunca baja de 1.

## 5. Nodos explorados por BFS, DFS y A* para la misma consulta

«Explorar» un punto es sacarlo de la lista de pendientes y revisarlo (mirar si es el destino y, si no, anotar sus
vecinos). Las tres búsquedas cuentan igual. Los resultados salen de `python busquedas.py`:

```
NODOS EXPLORADOS POR CADA BÚSQUEDA PARA LA MISMA CONSULTA
(Entre paréntesis: costo de la ruta encontrada; el menor es el óptimo)
====================================================================================================
Consulta                                                        BFS            DFS             A*
----------------------------------------------------------------------------------------------------
Portería Principal -> Biblioteca (12:00)                   21 (446)      41 (2258)       12 (435)
Portería Principal -> Bloque A Ingeniería (17:45)          27 (542)      34 (1735)       18 (532)
Portería Norte -> Cafetería Central (12:00)                37 (644)      47 (2246)       18 (644)
Portería Deportiva -> Admisiones y Registro (12:00)       49 (1058)      54 (2264)      38 (1058)
Mirador -> Portería Principal (12:00)                      41 (658)      59 (1730)       17 (658)
----------------------------------------------------------------------------------------------------
Promedio de las 3540 consultas posibles (12:00)                31.0           31.0           16.6

¿Qué tan buena es la ruta que encuentra cada uno? (las 3540 consultas)
----------------------------------------------------------------------------------------------------
BFS  encuentra la ruta de menor costo en el 61.8 % de las consultas; en promedio su ruta cuesta 1.03 veces la óptima.
DFS  encuentra la ruta de menor costo en el 11.8 % de las consultas; en promedio su ruta cuesta 3.62 veces la óptima.
A*   encuentra la ruta de menor costo en el 100.0 % de las consultas; en promedio su ruta cuesta 1.0 veces la óptima.
```

Cómo leer la tabla:

- **A* explora menos puntos que los otros dos**, porque la heurística lo empuja hacia el destino: en promedio
  16,6 puntos contra 31 de BFS y DFS (casi la mitad).
- **A* es el único que garantiza la ruta de menor costo** (100 % de las consultas). BFS encuentra la ruta con menos
  tramos, no la de menor esfuerzo, y por eso acierta en el 61,8 % de las consultas. DFS solo encuentra *alguna* ruta:
  en promedio cuesta 3,6 veces la óptima.
- BFS y DFS exploran, en promedio, casi el mismo número de puntos, pero la calidad de lo que encuentran es muy distinta.
