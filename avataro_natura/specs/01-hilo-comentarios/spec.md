# Especificación — Hilo de comentarios

**Versión:** 1.1 · **Fecha:** 2026-11-11 · **Autor:** Anwar Joseph

> **En palabras simples:** el hilo es la conversación de una actividad.
> Alguien opina, otros responden a esa opinión, y otros responden a las
> respuestas. El hilo sabe dar un número a cada comentario, mostrar toda
> la conversación en un orden que se pueda leer de principio a fin, y
> ocultar un comentario cuando la administración lo decide.

## 1. Propósito

Guardar la conversación de una actividad ambiental: personas que opinan y
otras que responden a esas opiniones, a su vez con más respuestas. Permite
mostrar toda la conversación en un orden que se pueda leer de principio a
fin, saber si un comentario existe y ocultar uno cuando la moderación lo
pida. Cubre HU-01, HU-02, HU-03 y la parte de HU-06 que oculta comentarios.

## 2. Fuera de alcance

- Editar o borrar comentarios (ocultar no es borrar).
- Recibir y ordenar reportes (componente 02).
- Reacciones, usuarios registrados, contraseñas y guardar en disco.

## 3. Reglas generales

- Cada comentario tiene: número, autor, texto, nivel y si está oculto o no.
- El número lo asigna el hilo: el primero es 1 y cada nuevo comentario
  recibe el siguiente. Nunca se repite ni se salta.
- Un comentario principal está en el nivel 1; una respuesta está un nivel
  por debajo del comentario al que responde.
- El nivel máximo es **5**.
- Un autor o un texto es **vacío** si no tiene caracteres o solo tiene espacios.
- Si una operación falla, el hilo queda exactamente como estaba.
- Un comentario oculto **sigue existiendo**: conserva su número, cuenta en
  la cantidad, sus respuestas siguen visibles y se puede seguir
  respondiéndole.

## 4. Operaciones

### `comentar(autor, texto)`
- **Precondiciones:** autor y texto no son vacíos
- **Postcondiciones:** existe un comentario principal nuevo, después de todos
  los principales anteriores; la cantidad aumenta en 1
- **Devuelve:** el número del comentario nuevo
- **Errores:** `ComentarioInvalidoError` si autor o texto son vacíos

### `responder(numero_padre, autor, texto)`
- **Precondiciones:** autor y texto no son vacíos; existe un comentario con
  ese número; ese comentario no está en el nivel máximo
- **Postcondiciones:** existe una respuesta nueva, después de las respuestas
  anteriores de ese comentario; la cantidad aumenta en 1
- **Devuelve:** el número de la respuesta nueva
- **Errores:**
  - `ComentarioInvalidoError` si autor o texto son vacíos
  - `ComentarioNoEncontradoError` si no existe un comentario con ese número
  - `ProfundidadExcedidaError` si el comentario está en el nivel máximo
- **Orden de verificación:** primero autor y texto, luego el número, luego
  el nivel.

### `existe(numero)` *(nueva en v1.1)*
- **Precondiciones:** ninguna (se puede preguntar por cualquier valor)
- **Postcondiciones:** el hilo no cambia
- **Devuelve:** `True` si hay un comentario con ese número; `False` en
  cualquier otro caso (incluido el 0, los negativos y lo que no sea un
  número entero)

### `ocultar(numero)` *(nueva en v1.1)*
- **Precondiciones:** existe un comentario con ese número
- **Postcondiciones:** al mostrar el hilo, ese comentario aparece con un
  aviso en lugar de su autor y su texto; la cantidad no cambia; sus
  respuestas no se ven afectadas. Ocultar un comentario que ya estaba
  oculto no hace nada y no falla.
- **Devuelve:** nada
- **Errores:** `ComentarioNoEncontradoError` si no existe un comentario con
  ese número

### `mostrar()`
- **Precondiciones:** ninguna
- **Postcondiciones:** el hilo no cambia
- **Devuelve:** un texto con una línea por comentario, separadas por un salto
  de línea (sin salto al final). Cada comentario aparece justo después del
  comentario al que responde. Las respuestas de un mismo comentario van en
  el orden en que se escribieron. El formato de cada línea es
  `#<número> <autor>: <texto>`, con dos espacios al inicio por cada nivel
  por debajo del primero. Si el comentario está oculto, la línea es
  `#<número> [comentario oculto por la administración]`. Un hilo sin
  comentarios devuelve texto vacío.

### `cantidad()`
- **Devuelve:** cuántos comentarios tiene el hilo (principales, respuestas y
  ocultos).

## 5. Invariantes

- INV-01: la cantidad de comentarios es >= 0 en todo momento
- INV-02: los números son únicos y van de 1 hasta la cantidad, sin huecos
- INV-03: todo comentario tiene un nivel entre 1 y 5, y toda respuesta
  está en el nivel siguiente al del comentario al que responde

## 6. Criterios de aceptación

| ID | Criterio | Verificable mediante |
|----|----------|----------------------|
| CA-01 | El primer comentario de un hilo recibe el número 1 y la cantidad pasa a 1 | test_comentar_primero |
| CA-02 | Dos comentarios principales se muestran en el orden en que se escribieron | test_comentarios_en_orden |
| CA-03 | Una respuesta se muestra debajo del comentario al que responde, antes del siguiente comentario principal | test_respuesta_queda_bajo_padre |
| CA-04 | Al mostrar, cada comentario aparece después de su padre, con dos espacios de sangría por nivel | test_hilo_en_preorden |
| CA-05 | Las respuestas de un mismo comentario se muestran en el orden en que se escribieron | test_respuestas_en_orden |
| CA-06 | Responder a un número que no existe (incluido el 0) lanza `ComentarioNoEncontradoError` y la cantidad no cambia | test_responder_inexistente |
| CA-07 | Un texto vacío o de solo espacios lanza `ComentarioInvalidoError` y la cantidad no cambia | test_texto_vacio |
| CA-08 | Un autor vacío o de solo espacios lanza `ComentarioInvalidoError` y la cantidad no cambia | test_autor_vacio |
| CA-09 | Responder a un comentario del nivel 5 lanza `ProfundidadExcedidaError` y la cantidad no cambia | test_profundidad_maxima |
| CA-10 | Mostrar un hilo sin comentarios devuelve texto vacío y no lanza error | test_mostrar_vacio |
| CA-11 | Una operación fallida no consume número: el siguiente comentario recibe el que correspondía | test_error_no_consume_numero |
| CA-12 | Si el texto es vacío y el número no existe, se lanza `ComentarioInvalidoError` | test_orden_de_errores |
| CA-13 | `existe` devuelve `True` para un comentario publicado y `False` para el 0, un número que no existe y un valor que no es número | test_existe |
| CA-14 | Un comentario oculto se muestra con el aviso en lugar de su autor y texto; sus respuestas siguen visibles con su sangría y la cantidad no cambia | test_ocultar_comentario |
| CA-15 | Ocultar un número que no existe lanza `ComentarioNoEncontradoError` y el hilo no cambia | test_ocultar_inexistente |
| CA-16 | Ocultar dos veces el mismo comentario no falla y sigue oculto | test_ocultar_dos_veces |
| CA-17 | Se puede responder a un comentario oculto | test_responder_a_oculto |

## 7. Casos extremos considerados

- Hilo sin comentarios · un solo comentario
- Un comentario con muchas respuestas seguidas
- Responder al nivel 4 (permitido) y al nivel 5 (rechazado)
- Número 0, número que no existe, valor que no es número
- Autor o texto con solo espacios
- Varios errores a la vez
- Ocultar un comentario que ya está oculto; ocultar uno que tiene respuestas

## 8. Historial de cambios

| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 2026-10-17 | Versión inicial | — |
| 1.1 | 2026-11-11 | Se agregan `existe` y `ocultar`, el aviso de comentario oculto en `mostrar` y los criterios CA-13 a CA-17 | La moderación (HU-05 y HU-06) necesita saber si un comentario existe antes de aceptar un reporte, y poder ocultarlo cuando la administración lo decide |
| 1.1 | 2026-11-11 | Se reescribe el texto en lenguaje cotidiano | Principio 5 de la constitución. El comportamiento de las operaciones que ya existían no cambia |
