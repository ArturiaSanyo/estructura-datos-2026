# Parte A — Nodos a mano

## Objetivo

Construir tres nodos enlazados directamente, sin una clase `ListaEnlazada`, y recorrerlos mediante referencias.

## Código

```python
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


primero = Nodo("Cancion A")
segundo = Nodo("Cancion B")
tercero = Nodo("Cancion C")

primero.siguiente = segundo
segundo.siguiente = tercero

actual = primero
while actual is not None:
    print(actual.dato)
    actual = actual.siguiente
```

## Cadena resultante

```text
primero
  |
  v
[Nodo A] ──siguiente──> [Nodo B] ──siguiente──> [Nodo C] ──> None
```

## Pérdida de referencia

La referencia al segundo nodo debe conservarse antes de modificar el enlace del primero.

### Orden correcto

```text
segundo = primero.siguiente
primero.siguiente = tercero
```

Resultado:

```text
primero
  |
  v
[Nodo A] ──> [Nodo C] ──> None

segundo
  |
  v
[Nodo B] ──> [Nodo C] ──> None
```

### Orden incorrecto

```text
primero.siguiente = tercero
segundo = primero.siguiente
```

Después del primer cambio, `primero.siguiente` ya apunta a `tercero`. Al intentar obtener el segundo nodo desde esa referencia, se obtiene `tercero` y se pierde la referencia directa al nodo B.

```text
primero
  |
  v
[Nodo A] ──> [Nodo C] ──> None

[Nodo B] queda sin una referencia alcanzable desde la cadena.
```

La idea fundamental es: **guardar una referencia antes de reemplazar el enlace que permite llegar a ella**.

## Recorrido

El bucle sigue `siguiente` hasta encontrar `None`, que representa el final de la cadena.
