# Plan técnico — Hilo de comentarios

**Especificación de referencia:** spec.md v1.1 · **Versión del plan:** 2.0

> **En palabras simples:** la conversación se guarda como un árbol: cada
> comentario es una "hoja" unida a la rama del comentario al que responde.
> Para encontrar rápido un comentario por su número se usa además un
> índice (el componente 03). Cómo leer los costos: **O(1)** significa que
> tarda lo mismo sin importar cuántos comentarios haya; **O(n)** significa
> que tarda más mientras más comentarios haya.

## 1. Estructura de datos elegida

**Árbol general** representado con *primer hijo / siguiente hermano*. Cada
comentario (`Nodo`) guarda su número, autor, texto, nivel, si está oculto y
tres referencias: `primer_hijo` (su primera respuesta), `ultimo_hijo` (su
última respuesta) y `siguiente_hermano` (el siguiente comentario de su mismo
nivel).

El hilo tiene una **raíz falsa** (número 0, nivel 0) que no se muestra.
Los comentarios principales son sus hijos, así `comentar` y `responder`
usan el mismo código para agregar. La raíz falsa **no** se guarda en el
índice, por eso el número 0 "no existe" para el usuario sin ningún caso
especial.

Para encontrar un comentario por su número, el hilo usa un **Índice**
(componente 03, tabla hash con encadenamiento). Cada comentario nuevo se
anota en el índice en el momento de crearse.

Como la constitución exige no usar `list` como sustituto de la estructura,
las respuestas de un comentario forman su propia cadena de hermanos en
lugar de una lista de Python.

## 2. Alternativas consideradas

| Alternativa | Ventaja | Por qué se descartó |
|-------------|---------|---------------------|
| Lista de comentarios con el número del padre | Muy simple de escribir | Para mostrar el hilo hay que buscar los hijos de cada comentario: O(n²). Además usa `list` como sustituto de la estructura (viola la constitución) |
| Árbol donde cada comentario guarda una `list` de respuestas | Fácil de entender | Usa `list` como sustituto de la estructura (viola la constitución) |
| Árbol binario de búsqueda por número | Búsqueda O(log n) | No representa "respuestas": un comentario puede tener 0, 1 o muchas, no solo 2 hijos |
| Árbol + búsqueda recorriendo el árbol (plan 1.0 y 1.1) | No necesita estructuras extra | Cada `responder`, `existe` u `ocultar` cuesta O(n). **Reemplazada en el plan 2.0** |
| Árbol + índice de números (**elegida en el plan 2.0**) | Encontrar un comentario por su número en O(1) promedio | Cuesta algo de memoria extra, O(n), y hay que anotar cada comentario nuevo en el índice |

## 3. Complejidad esperada

| Operación | Tiempo | Espacio | Justificación |
|-----------|--------|---------|---------------|
| `comentar` | O(1) | O(1) | Se agrega al final de los hijos de la raíz usando `ultimo_hijo`; anotar en el índice es O(1) (de vez en cuando el índice se agranda; ver plan 03) |
| `responder` | O(1) promedio | O(1) | El índice encuentra al padre sin recorrer el árbol; agregar es O(1). *(Con el plan 1.x costaba O(n).)* |
| `existe` | O(1) promedio | O(1) | Una consulta al índice |
| `ocultar` | O(1) promedio | O(1) | Una consulta al índice y cambiar una marca |
| `mostrar` | O(n) | O(n) | Se visita cada comentario una vez (preorden); el texto resultante ocupa O(n) |
| `cantidad` | O(1) | O(1) | Se guarda un contador |

Nota: `mostrar` arma el texto con `+=`. El número de comentarios visitados
es O(n); copiar el texto en cada unión podría costar más si el hilo fuera
gigante. Con los hilos de este proyecto no es un problema; si lo fuera,
se cambia el plan, no la spec.

## 4. Diseño interno

- `_raiz`: comentario falso que sostiene a los principales
- `_indice`: el índice (componente 03) donde se anota cada comentario por su número
- `_cantidad`: contador para `cantidad()` en O(1)
- `_ultimo_numero`: último número entregado; solo avanza cuando no hay error
- `_encontrar(numero)`: pide el comentario al índice; si no existe, el índice
  lanza `ComentarioNoEncontradoError`
- `_recorrer(nodo)`: preorden; escribe un comentario y luego sus respuestas.
  Baja con recursión un nivel por vez (máximo 5) y recorre las respuestas
  de cada comentario con un ciclo `while`
- **Invariante de representación:** `_cantidad` = número de comentarios
  alcanzables desde `_raiz` (sin contarla) = cantidad de números en el
  índice; `ultimo_hijo` de un comentario es el último de su cadena de hijos

## 5. Riesgos técnicos

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Recursión demasiado profunda (`RecursionError`) | Alto | El nivel máximo es 5 (spec), así la recursión nunca pasa de 6 llamadas. Recorrer las respuestas con `while`, no con recursión |
| Olvidar actualizar `ultimo_hijo` y perder respuestas | Medio | Pruebas CA-03 y CA-05 con varias respuestas seguidas |
| Gastar un número cuando la operación falla | Medio | Validar y comprobar el nivel antes de incrementar `_ultimo_numero` y antes de anotar en el índice (CA-11) |
| El índice y el árbol quedan desincronizados (un comentario existe en uno y no en el otro) | Alto | Un solo lugar crea comentarios (`_agregar`) y ahí mismo se anota en el índice; prueba `test_existe` y pruebas de `responder` |
| `responder` lento con muchos comentarios | Bajo | Resuelto con el índice (plan 2.0); medido en `analisis/medir_tiempos.py` |

## 6. Historial de cambios del plan

| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 2026-10-17 | Árbol con búsqueda por recorrido | Versión inicial |
| 1.1 | 2026-11-11 | Cubre la spec 1.1: `existe`, `ocultar` y el aviso de oculto (con búsqueda por recorrido, O(n)) | La spec 01 cambió a la versión 1.1 |
| 2.0 | 2026-11-11 | Se usa el índice (componente 03) en vez de recorrer el árbol; se elimina la función `_buscar` | HU-04: encontrar comentarios en tiempo casi constante. **La spec no cambia**; las pruebas siguen pasando |
