# Parte D — Comparación y decisión del reproductor

## Datos de entrada

- Lista: **5.000 canciones**.
- Insertar al principio: **40 veces/día**.
- Recorrer toda la lista: **3 veces/día**.
- Ir a la canción N: **200 veces/día**.
- Borrar la canción actual: **15 veces/día**.

## Coste teórico

| Operación | ListaArreglo | ListaEnlazada |
|---|---:|---:|
| Insertar al principio | O(n) | O(1) |
| Recorrer toda la lista | O(n) | O(n) |
| Ir a canción N | O(1) | O(n) |
| Borrar canción actual | O(n) | O(1) con `actual` + `anterior` |
| Memoria por elemento | O(1) adicional | O(1) adicional para el enlace |

## Tabla resumen: costo teórico y medido

Los valores medidos corresponden a una ejecución de referencia realizada con Python 3 en el entorno de preparación. Son tiempos promedio de cinco ejecuciones y están expresados en microsegundos (µs). En otro equipo pueden variar.

| Operación | Arreglo — teórico | Arreglo — medido | Enlazada — teórico | Enlazada — medido |
|---|---|---:|---|---:|
| Insertar al principio | O(n) | 1.08 µs | O(1) | 1.62 µs |
| Recorrer toda la lista | O(n) | 148.07 µs | O(n) | 190.21 µs |
| Ir a la canción N | O(1) | 0.81 µs | O(n) | 190.83 µs |
| Borrar la canción actual | O(n) | 1.09 µs | O(1)¹ | 0.92 µs |

¹ En la implementación, `ir_a` conserva el nodo anterior y el nodo actual, por lo que el enlace del borrado no necesita buscar el elemento desde el principio. La actualización posterior del estado cuando se elimina el último elemento puede requerir recorrido; la medición mostrada corresponde a una posición intermedia.

## Modelo de coste diario

Para comparar el impacto de las frecuencias, se usa el número de operaciones multiplicado por el número de posiciones que, en promedio, deben procesarse.

Para `n = 5.000`:

### ListaArreglo

- Insertar al principio: `40 × 5.000 = 200.000` unidades.
- Recorrer: `3 × 5.000 = 15.000` unidades.
- Ir a N: `200 × 1 = 200` unidades.
- Borrar actual: `15 × 2.500 = 37.500` unidades (promedio de desplazamientos).
- **Total aproximado: 252.700 unidades de trabajo.**

### ListaEnlazada

- Insertar al principio: `40 × 1 = 40` unidades.
- Recorrer: `3 × 5.000 = 15.000` unidades.
- Ir a N: `200 × 2.500 = 500.000` unidades (posición media).
- Borrar actual: `15 × 1 = 15` unidades.
- **Total aproximado: 515.055 unidades de trabajo.**

Este modelo no sustituye la medición real: sirve para relacionar la complejidad con las frecuencias entregadas.

## Medición real

Ejecutar:

```bash
python comparacion.py
```

El programa imprime el tiempo promedio medido en la máquina donde se ejecuta.

La medición puede cambiar entre equipos, sistemas operativos, versiones de Python y carga del sistema. La tabla de arriba permite mantener una comparación reproducible aunque cambie el hardware.

## Decisión basada en los datos

Con las frecuencias dadas y `n = 5.000`, el costo ponderado del acceso por posición domina en la lista enlazada: se realizan **200 accesos por día**, frente a solo **40 inserciones al principio** y **15 borrados**.

Por ello, para este escenario concreto, el modelo de operaciones favorece `ListaArreglo`.

No se concluye que una estructura sea universalmente mejor. La decisión depende de las frecuencias.

## ¿Qué tendría que cambiar para cambiar la recomendación?

Si se mantienen las demás frecuencias y se hace que la inserción al principio sea la operación dominante, la lista enlazada puede pasar a tener menor costo ponderado.

Con el modelo anterior, si `I` es el número de inserciones al principio:

- Arreglo: `I × 5.000 + 52.700`
- Enlazada: `I + 515.015`

Igualando ambos modelos:

`I × 5.000 + 52.700 = I + 515.015`

`I ≈ 92,5`

Por tanto, **aproximadamente desde 93 inserciones al principio por día**, manteniendo las demás frecuencias, el modelo ponderado deja de favorecer al arreglo.

Este umbral es específico del modelo de costo utilizado y no representa una medición de tiempo absoluta.
