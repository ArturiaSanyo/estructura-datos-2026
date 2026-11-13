# Estructuras elegidas — Avataro Natura

| # | Capacidad | Estructura | Por qué | Alternativa descartada |
|---|-----------|-----------|---------|------------------------|
| 01 | Comentar, responder y mostrar el hilo en orden (HU-01, 02, 03) | Árbol general (primer hijo / siguiente hermano) | Un comentario tiene un número cualquiera de respuestas y mostrarlas en orden es un recorrido en preorden, O(n) | Lista con el id del padre: reconstruir el hilo exige buscar los hijos de cada comentario, O(n²) |
| 02 | Atender los reportes en orden de llegada (HU-05, 06) | Cola enlazada con referencias al frente y al final | Encolar y desencolar en O(1) y el primero en llegar es el primero en salir | Arreglo dinámico: desencolar del inicio obliga a correr todos los elementos, O(n) |
| 03 | Encontrar un comentario por su número (HU-04) | Tabla hash con encadenamiento | Buscar por número en O(1) promedio, sin recorrer el hilo | Árbol binario de búsqueda: los números crecen de uno en uno, el árbol se vuelve una fila y buscar cuesta O(n); recorrer el hilo (plan inicial del 01) cuesta O(n) |

## En palabras sencillas

- **01 · Árbol.** Una conversación tiene forma de árbol: un comentario
  principal es una rama de la que salen respuestas, y de cada respuesta
  pueden salir más. Mostrarla en orden es "caminar" el árbol rama por rama.
- **02 · Cola.** Los reportes son como la fila de un banco: el primero que
  llegó es el primero al que se atiende. La estructura guarda dónde empieza
  y dónde termina la fila, así llegar y salir son operaciones rápidas.
- **03 · Tabla de dispersión.** Es como el índice de un libro: en lugar de
  hojear todo el mural para encontrar el comentario #4 500, un cálculo
  sencillo dice en qué "casillero" está y se va directo.

## Notas

- El componente 03 mejora el costo de `responder` del componente 01
  (de O(n) a O(1) promedio) **sin cambiar la spec del 01**: solo cambia su plan.
  Esa es la prueba de que se separó bien el *qué* del *cómo*.
- Orden de construcción: 01 (Entrega 1) → 02 (Entrega 2) → 03 (Entrega final).
- Los componentes 02 y 03 no se conocen entre sí: quien los une es el
  sistema (`mural.py` y `99-sistema/spec.md`), y el 03 lo usa por dentro el 01.
