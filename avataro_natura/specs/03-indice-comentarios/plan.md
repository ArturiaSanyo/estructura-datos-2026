# Plan técnico — Índice de comentarios

**Especificación de referencia:** spec.md v1.1 · **Versión del plan:** 1.0

> **En palabras simples:** imagina un archivador con casilleros numerados.
> Para guardar el comentario número N, se hace una cuenta sencilla (el
> **resto de dividir N entre la cantidad de casilleros**) que dice en cuál
> casillero va. Para buscarlo después, se repite la misma cuenta y se
> abre ese casillero directamente. Si en un casillero caen varios
> comentarios, se unen en una cadena corta. Cuando el archivador se llena
> demasiado, se cambia por uno del doble de tamaño y se reacomoda todo,
> así las cadenas siempre se mantienen cortas.

## 1. Estructura de datos elegida

**Tabla de dispersión (hash) con encadenamiento.**

- Hay una fila de **casilleros** numerados de 0 a `tamaño - 1`.
- El casillero de un número es `numero % tamaño` (el resto de dividir el
  número entre el tamaño). Esa cuenta es la *función de dispersión*.
- Cada casillero guarda el inicio de una **cadena** de `NodoIndice`. Cada
  `NodoIndice` guarda un número, su elemento y una referencia `siguiente`
  al otro nodo del mismo casillero.
- Al agregar, el nodo nuevo se pone al **inicio** de la cadena: no hay que
  recorrerla para pegarlo al final.
- Tamaño inicial: 8 casilleros. Cuando hay más de 3 números por cada 4
  casilleros (carga máxima 0,75) la tabla **se agranda al doble** y cada
  nodo se reubica con la nueva cuenta. Así la cadena promedio mide menos de 1.

### Uso justificado de `list` (constitución, principio 1)

Los casilleros necesitan acceso directo por posición ("abre el casillero
5"). Para eso se usa **una sola `list` de tamaño fijo**, creada como
`[None] * tamaño` y usada solo como fila de casilleros. Nunca se usan
`append`, `insert`, `pop` ni ninguna operación que la haga crecer: cuando la
tabla se agranda, se crea otra fila nueva. Las cadenas, la búsqueda, la
inserción y el reacomodo están escritos a mano con `NodoIndice`. La `list`
solo hace el papel de una "fila de cajones" y no sustituye a la estructura.

## 2. Alternativas consideradas

| Alternativa | Ventaja | Por qué se descartó |
|-------------|---------|---------------------|
| Recorrer el árbol del hilo (plan 1 del componente 01) | No usa memoria extra | Buscar cuesta O(n): con 16 000 comentarios hay que mirar hasta 16 000 |
| Árbol binario de búsqueda | Ordenado, O(log n) si está equilibrado | Los números llegan en orden creciente (1, 2, 3...): el árbol se vuelve una fila y buscar cuesta O(n). Para evitarlo habría que equilibrarlo (AVL, rojinegro): mucho más código sin ganar frente al O(1) promedio |
| Lista ordenada con búsqueda binaria | Búsqueda O(log n) | Insertar en el medio mueve elementos; como los números llegan en orden se evitaría, pero usa `list` como sustituto de la estructura (viola la constitución) |
| Dispersión con direccionamiento abierto | Sin nodos extra | Borrar y manejar choques es más delicado; no se pide borrar, pero el encadenamiento es más simple de explicar y de probar |
| Diccionario de Python (`dict`) | Una línea | Viola el principio 1: es justo la estructura que se pidió construir |

## 3. Complejidad esperada

| Operación | Tiempo | Espacio | Justificación |
|-----------|--------|---------|---------------|
| `agregar` | O(1) promedio (amortizado) | O(1) | Se calcula el casillero y se pone el nodo al inicio de la cadena. De vez en cuando la tabla se agranda (cuesta O(n)), pero ocurre cada vez menos seguido: repartido entre todas las altas sale O(1) |
| `buscar` | O(1) promedio | O(1) | Se calcula el casillero y se recorre su cadena, que mide menos de 1 en promedio (carga máxima 0,75). En el peor caso (todos en un casillero) sería O(n), pero con números consecutivos no ocurre |
| `existe` | O(1) promedio | O(1) | Igual que `buscar` |
| `cantidad` | O(1) | O(1) | Se guarda un contador |
| Agrandar (interno) | O(n) | O(n) | Se reubican todos los nodos en la tabla nueva |

Memoria total del componente: O(n).

## 4. Diseño interno

- `_casilleros`: la fila de casilleros (`list` fija, ver justificación)
- `_tamano`: cuántos casilleros hay
- `_cantidad`: cuántos números hay guardados
- `_buscar_nodo(numero)`: devuelve el `NodoIndice` o `None`; la usan
  `agregar`, `buscar` y `existe`
- `_agrandar()`: crea una fila del doble de tamaño y pasa cada nodo existente
  a su casillero nuevo (sin crear nodos nuevos)
- `_cadena_mas_larga()`: función de apoyo para las pruebas de rendimiento
- **Invariante de representación:** `_cantidad` = número de nodos en todas
  las cadenas; todo nodo está en el casillero `numero % _tamano`; no hay dos
  nodos con el mismo número; `_cantidad * 4 <= _tamano * 3` después de cada alta

## 5. Cómo se comprueba la complejidad

| Verificación | Qué comprueba | Dónde |
|--------------|---------------|-------|
| PLAN-01 | Con 10 000 números consecutivos la cadena más larga mide 3 o menos | `test_plan_cadenas_cortas` |
| PLAN-02 | Números que caen en el mismo casillero (1, 9, 17, 25 con 8 casilleros) se encuentran todos | `test_plan_numeros_que_chocan` |
| PLAN-03 | La tabla se agranda al cruzar la carga máxima y no se pierde ningún número | `test_plan_se_agranda` |
| PLAN-04 | Medición de tiempos: `responder` con índice no crece con el tamaño del hilo; sin índice sí | `analisis/medir_tiempos.py` |

## 6. Riesgos técnicos

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Perder números al agrandar la tabla (nodos mal reubicados) | Alto | Prueba CA-06 (10 000 números, todos se encuentran) y PLAN-03 |
| Muchos números en el mismo casillero si siguen un patrón (todos múltiplos del tamaño) | Medio | Los números del sistema van de 1 en 1 sin huecos (INV-02 del hilo), por lo que se reparten parejo. PLAN-01 lo mide |
| Aceptar `True` como número 1 | Medio | Comprobar el tipo exacto (`type(x) is int`); prueba CA-05 |
| Que una búsqueda con texto falle con un error raro al calcular el casillero | Medio | Validar el número **antes** de calcular el casillero; pruebas CA-02 y CA-05 |
| Agregar un número repetido y dejar la cantidad inconsistente | Medio | Comprobar repetición antes de tocar la tabla; prueba CA-04 |

## 7. Historial de cambios del plan

| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 2026-11-11 | Versión inicial | Entrega final |
