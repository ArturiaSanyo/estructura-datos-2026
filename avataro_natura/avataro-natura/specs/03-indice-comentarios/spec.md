# Especificación — Índice de comentarios

**Versión:** 1.1 · **Fecha:** 2026-11-11 · **Autor:** Anwar Joseph

> **En palabras simples:** es como el índice al final de un libro. En
> lugar de hojear todo el mural para encontrar el comentario #4 500, se
> consulta el índice y se llega directo. El índice guarda parejas
> "número → comentario" y contesta dos preguntas: *¿existe este número?* y
> *¿a qué comentario corresponde?*

## 1. Propósito

Permitir que el sistema encuentre un comentario a partir de su número, sin
tener que recorrer toda la conversación, y que lo haga igual de rápido
cuando el mural tiene miles de comentarios. Cubre HU-04.

## 2. Fuera de alcance

- Borrar o cambiar un número ya guardado (los comentarios no se borran).
- Buscar por autor o por texto.
- Decidir qué números se asignan (lo hace el hilo).
- Guardar en disco.

## 3. Reglas generales

- Un **número válido** es un entero mayor que 0 (1, 2, 3...). El 0, los
  negativos, los decimales, el texto y los valores verdadero/falso no valen.
- Cada número aparece una sola vez en el índice.
- Cada número guarda "un elemento" (en el sistema, un comentario). El
  índice no mira qué es ese elemento: solo lo guarda y lo devuelve.
- Si una operación falla, el índice queda exactamente como estaba.

## 4. Operaciones

### `agregar(numero, elemento)`
- **Precondiciones:** `numero` es válido y todavía no está en el índice
- **Postcondiciones:** el número queda asociado al elemento; la cantidad
  aumenta en 1
- **Devuelve:** nada
- **Errores:**
  - `NumeroInvalidoError` si el número no es válido
  - `NumeroRepetidoError` si el número ya estaba en el índice
- **Orden de verificación:** primero que el número sea válido, luego que no
  esté repetido.

### `buscar(numero)`
- **Precondiciones:** ninguna (se puede buscar cualquier valor)
- **Postcondiciones:** el índice no cambia
- **Devuelve:** el elemento asociado a ese número
- **Errores:** `ComentarioNoEncontradoError` si el número no está en el
  índice (incluye los números no válidos, que nunca pueden estar)

### `existe(numero)`
- **Precondiciones:** ninguna
- **Postcondiciones:** el índice no cambia
- **Devuelve:** `True` si el número está en el índice; `False` en cualquier
  otro caso (incluye los números no válidos)

### `cantidad()`
- **Devuelve:** cuántos números hay en el índice

## 5. Invariantes

- INV-01: la cantidad es >= 0 en todo momento
- INV-02: la cantidad es igual al número de parejas que se pueden encontrar
- INV-03: todo número que se agregó con éxito se puede encontrar, sin
  importar cuántos números se hayan agregado después

## 6. Criterios de aceptación

| ID | Criterio | Verificable mediante |
|----|----------|----------------------|
| CA-01 | Después de agregar un número con su elemento, `buscar` devuelve ese mismo elemento | test_agregar_y_buscar |
| CA-02 | `existe` devuelve `True` para un número agregado y `False` para uno que no se agregó, el 0, un negativo y un texto | test_existe |
| CA-03 | Buscar un número que no está lanza `ComentarioNoEncontradoError` | test_buscar_inexistente |
| CA-04 | Agregar un número repetido lanza `NumeroRepetidoError`; el elemento original se conserva y la cantidad no cambia | test_agregar_repetido |
| CA-05 | Agregar un número no válido (0, -1, 2.5, "3", True) lanza `NumeroInvalidoError` y la cantidad no cambia | test_numero_invalido |
| CA-06 | Después de agregar 10 000 números consecutivos, cada uno se encuentra y devuelve su propio elemento | test_muchos_numeros |
| CA-07 | La cantidad empieza en 0, sube de uno en uno al agregar y no cambia cuando una operación falla | test_cantidad |
| CA-08 | En un índice vacío, `buscar` lanza `ComentarioNoEncontradoError` y `existe` devuelve `False` | test_indice_vacio |
| CA-09 | Los números que no son consecutivos también se encuentran, aunque sean muchos: 5, 500 y 99 999, y además todos los múltiplos de 7 entre 7 y 7 000 | test_numeros_salteados |

## 7. Casos extremos considerados

- Índice vacío · un solo número
- Número 0, negativo, decimal, texto, verdadero/falso
- Número repetido
- Miles de números (el índice debe seguir funcionando al crecer)
- Números que no son consecutivos, incluso cientos de ellos

## 8. Historial de cambios

| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 2026-11-11 | Versión inicial | Entrega final: HU-04 |
| 1.1 | 2026-11-11 | CA-09 se amplía: además de tres números sueltos, deben encontrarse cientos de números no consecutivos | Una prueba de "romper el código a propósito" mostró que, con solo números consecutivos (1, 2, 3...), un error al reacomodar la tabla cuando crece pasaba sin que ninguna prueba lo notara. La spec era demasiado floja |
