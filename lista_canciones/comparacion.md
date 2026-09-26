# Comparación ListaArreglo vs ListaEnlazada — reproductor de la emisora

## 1. El caso

La emisora usa la lista de reproducción así, medido durante una semana real:

| Operación | Veces al día |
|---|---|
| Insertar al principio (canción de última hora) | 40 |
| Recorrer toda la lista (generar la parrilla) | 3 |
| Ir a la canción número N (saltar en el aire) | 200 |
| Borrar la canción actual | 15 |

## 2. Costo teórico (Big-O)

| Operación | ListaArreglo | ListaEnlazada |
|---|---|---|
| Insertar al principio | O(n) | O(1) |
| Recorrer toda la lista | O(n) | O(n) |
| Obtener posición N | O(1) | O(n) |
| Borrar (posición cualquiera) | O(n) | O(n) |

## 3. Costo medido

Se midió el tiempo real de cada operación sobre una lista de **5.000 canciones**, promediando varias repeticiones para que la medición fuera estable. Tiempos por una sola llamada:

| Operación | ListaArreglo (s) | ListaEnlazada (s) |
|---|---|---|
| Insertar al principio | 0.000344 | 0.00000044 |
| Recorrer toda la lista | 0.000169 | 0.000143 |
| Obtener posición N (medio) | 0.00000014 | 0.000036 |
| Borrar posición N (medio) | 0.000159 | 0.000077 |

Esto confirma lo que dice la teoría: `ListaArreglo` es casi instantánea para "obtener" (acceso directo), y `ListaEnlazada` es casi instantánea para "insertar al principio" (no mueve nada, solo cambia un gancho).

## 3.1 Tabla resumen (teórico y medido, lado a lado)

| Operación | Big-O Arreglo | Medido Arreglo (s) | Big-O Enlazada | Medido Enlazada (s) |
|---|---|---|---|---|
| Insertar al principio | O(n) | 0.000344 | O(1) | 0.00000044 |
| Recorrer toda la lista | O(n) | 0.000169 | O(n) | 0.000143 |
| Obtener posición N | O(1) | 0.00000014 | O(n) | 0.000036 |
| Borrar posición N | O(n) | 0.000159 | O(n) | 0.000077 |

## 4. Costo de un día de emisión

Costo del día = suma de (veces al día × tiempo de esa operación):

**ListaArreglo:**
```
40 × 0.000344  = 0.013762 s   (insertar al principio)
 3 × 0.000169  = 0.000507 s   (recorrer)
200 × 0.00000014 = 0.000027 s (obtener)
15 × 0.000159  = 0.002388 s   (borrar)
-----------------------------
Total ≈ 0.016684 s  (16.68 ms)
```

**ListaEnlazada:**
```
40 × 0.00000044 = 0.0000176 s (insertar al principio)
 3 × 0.000143   = 0.000430 s  (recorrer)
200 × 0.000036  = 0.007218 s  (obtener)
15 × 0.000077   = 0.001155 s  (borrar)
-----------------------------
Total ≈ 0.008821 s  (8.82 ms)
```

## 5. Recomendación

Con las frecuencias reales de la emisora, **`ListaEnlazada` es la más barata en total** (8.82 ms/día contra 16.68 ms/día de `ListaArreglo`), casi la mitad.

Esto puede sorprender, porque "ir a la canción N" es la operación que más se usa (200 veces al día) y ahí `ListaArreglo` es muchísimo más rápida. Pero **"insertar al principio" cuesta tanto en `ListaArreglo`** (tiene que correr hasta 5.000 elementos cada vez) que, aunque se usa poco (40 veces), ese costo por sí solo (13.76 ms) ya es más caro que el total completo de `ListaEnlazada`.

**Conclusión:** la recomendación no sale de la intuición ("las enlazadas son mejores para insertar"), sale de hacer la cuenta con los números reales de esta emisora en particular.

## 6. Qué tendría que cambiar en las frecuencias para que cambiara la recomendación

Se puede calcular el punto exacto donde empatan las dos estructuras, dejando las otras operaciones fijas:

- **Si "ir a la canción N" se usara ≈ 419 veces al día o más** (en vez de 200), manteniendo el resto igual, `ListaArreglo` pasaría a ser la más barata. Es decir, la emisora tendría que saltar canciones más del doble de seguido de lo que hace ahora.
- **Si "insertar al principio" se usara ≈ 17 veces al día o menos** (en vez de 40), manteniendo el resto igual, `ListaArreglo` también pasaría a ser la más barata, porque su operación más cara dejaría de pesar tanto en el total.

En resumen: la recomendación actual (`ListaEnlazada`) es sensible sobre todo a qué tan seguido se inserta al principio. Si la emisora cambiara su forma de operar y casi no metiera canciones de última hora, `ListaArreglo` volvería a ser mejor opción.
