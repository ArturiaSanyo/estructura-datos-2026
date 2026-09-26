# Especificación — Contrato compartido de Lista

Este es el mismo contrato para `ListaArreglo` (Actividad 2) y `ListaEnlazada` (Actividad 3). Ambas clases deben cumplirlo igual.

## Operaciones

### `tamaño()`
Devuelve cuántos elementos hay guardados. Lista vacía: `0`.

### `obtener(posicion)`
Devuelve el elemento en `posicion` (empezando en `0`).
- Si `posicion` está fuera de rango (`< 0` o `>= tamaño()`): lanza `PosicionInvalidaError`.

### `insertar(posicion, elemento)`
Agrega `elemento` en `posicion`, corriendo lo que estaba ahí (y lo siguiente) un puesto.
- `posicion` puede ir de `0` hasta `tamaño()` (insertar al final también es válido).
- Si `posicion` está fuera de ese rango: lanza `PosicionInvalidaError`.

### `eliminar(posicion)`
Quita y devuelve el elemento en `posicion`.
- Si `posicion` está fuera de rango (`< 0` o `>= tamaño()`): lanza `PosicionInvalidaError`.

### `buscar(elemento)`
Devuelve la posición de la primera vez que aparece `elemento`.
- Si no está: devuelve `-1`.

## Además, ambas implementaciones soportan

- `len(lista)` — igual que `tamaño()`.
- `lista[i]` — igual que `obtener(i)`.
- `for x in lista:` — recorre los elementos en orden.
- `repr(lista)` — muestra el contenido, por ejemplo `ListaArreglo(['pan', 'leche'])`.

## Diferencia entre las dos implementaciones

La diferencia está solo **por dentro** (cómo guardan los datos), nunca en el comportamiento hacia afuera:

- `ListaArreglo`: un arreglo de tamaño fijo que se duplica cuando se llena.
- `ListaEnlazada`: una cadena de `Nodo`s conectados con `siguiente`.
