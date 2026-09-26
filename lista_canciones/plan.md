# Plan — Actividad 3

## Orden de trabajo

1. **Nodos a mano** (sin clase `ListaEnlazada` todavía): construir 3 nodos, engancharlos, recorrerlos con un `while`, y entender el error de perder la referencia al resto de la cadena.
2. **Construir `ListaEnlazada`**: usar lo aprendido en el paso 1 para escribir la clase completa, cumpliendo el mismo contrato de `spec.md`.
3. **Verificar contra `test_lista_arreglo.py`**: correr ese archivo (sin tocarlo) apuntando a `ListaEnlazada`, para confirmar que el contrato se cumple igual.
4. **Casos extremos** (`test_extremos.py`): probar lista vacía, un elemento, borrar el primero y borrar el último, en las dos implementaciones.
5. **Medir de verdad** las 4 operaciones de la emisora sobre una lista de 5.000 canciones, en las dos estructuras.
6. **Calcular el costo de un día** de emisión con cada estructura, usando las frecuencias reales, y recomendar una.

## Cómo correr el paso 3 sin tocar el archivo de pruebas

`test_lista_arreglo.py` empieza con:
```python
from lista_arreglo import ListaArreglo, PosicionInvalidaError
```

Como el archivo no se puede modificar, para probarlo contra `ListaEnlazada` la forma más simple es hacerlo manualmente, sin trucos de código:

1. Guarda una copia de tu `lista_arreglo.py` real en otro lado (por ejemplo `lista_arreglo_real.py`).
2. Copia el contenido de `lista_enlazada.py`, pero renombra la clase `ListaEnlazada` a `ListaArreglo` y `Nodo` como quieras, SOLO en esa copia temporal, y guárdala como `lista_arreglo.py`.
3. Corre `pytest test_lista_arreglo.py -v`. Si pasa, `ListaEnlazada` cumple el contrato.
4. Cuando termines, recupera tu `lista_arreglo.py` real (paso 1).

Esto prueba literalmente el mismo archivo de pruebas, sin cambiarle una sola línea, contra la otra implementación.
