# Nodos a mano

## ¿Qué es un nodo?

Piensa en un tren. Cada vagón lleva dos cosas:
1. Una carga (el dato).
2. Un gancho que lo conecta al vagón de atrás.

Eso es un **nodo**: una cajita con un dato, más un "gancho" (una referencia) hacia el siguiente nodo. Si un vagón no tiene nada enganchado detrás, es el último del tren.

En Python, la forma más simple de representar esa cajita es una clase pequeñita:

```python
class Nodo:
    def __init__(self, dato, siguiente=None):
        self.dato = dato          # la carga del vagón
        self.siguiente = siguiente  # el gancho hacia el siguiente vagón (o None si es el último)
```

`siguiente=None` por defecto significa: "por ahora este vagón no está enganchado a nada".

---

## Paso 1 — Construir el último vagón primero

Empezamos por el final de la cadena, porque para enganchar un vagón necesitamos que el de atrás ya exista.

```python
nodo3 = Nodo("huevos")
```

Diagrama de memoria:

```
nodo3 --> [ huevos | None ]
```

`nodo3` es una variable que apunta (flecha) a una cajita que tiene el dato `"huevos"` y el gancho en `None` (no hay nada después).

---

## Paso 2 — Construir el segundo vagón, enganchado al tercero

```python
nodo2 = Nodo("leche", nodo3)
```

Aquí le decimos: "el gancho de este nuevo nodo apunta a donde apunta `nodo3`".

Diagrama de memoria:

```
nodo2 --> [ leche | *-] --> [ huevos | None ]
                            (nodo3 sigue apuntando aquí también)
```

Ahora mismo hay **dos flechas** llegando a la cajita de `"huevos"`: la de la variable `nodo3` y la del gancho de `nodo2`. Las dos apuntan al mismo lugar en memoria.

---

## Paso 3 — Construir el primer vagón, enganchado al segundo

```python
nodo1 = Nodo("pan", nodo2)
```

Diagrama de memoria completo:

```
nodo1 --> [ pan | *-] --> [ leche | *-] --> [ huevos | None ]
            ^                ^
      (variable nodo1)  (variable nodo2 también apunta aquí)
```

Ya tenemos la cadena completa de 3 vagones, construida a mano, sin ninguna clase "ListaEnlazada" ni métodos como `insertar`. Solo variables y nodos.

---

## Paso 4 — Recorrer la cadena con un bucle

Para "caminar" por el tren de principio a fin, usamos una variable que va saltando de gancho en gancho hasta que no haya más:

```python
actual = nodo1
while actual is not None:
    print(actual.dato)
    actual = actual.siguiente
```

Esto imprime:
```
pan
leche
huevos
```

`actual` empieza en `nodo1`, y en cada vuelta del `while` salta al `siguiente`. Cuando `actual` llega a `None`, el bucle para: ya no hay más vagones.

---

## Paso 5 — El error real: reasignar el enlace antes de guardar el resto

Ahora imagina que quieres poner un vagón nuevo **al principio** del tren (antes de `nodo1`). Hay una forma correcta y una forma que rompe todo.

### La forma que rompe todo (pérdida de referencia)

```python
cabeza = nodo1              # "cabeza" es la variable que usamos para saber dónde empieza el tren
cabeza = Nodo("queso")      # ⚠️ ERROR: reasignamos "cabeza" ANTES de guardar a dónde apuntaba
```

¿Qué pasó? Antes de la segunda línea, `cabeza` era la única forma en la que "cabeza" señalaba al tren `pan -> leche -> huevos`. En el momento en que hacemos `cabeza = Nodo("queso")`, la variable `cabeza` deja de apuntar al tren viejo y empieza a apuntar a la cajita nueva de `"queso"`, que ni siquiera tiene gancho hacia nada.

Diagrama de memoria, ANTES:
```
cabeza --> [ pan | *-] --> [ leche | *-] --> [ huevos | None ]
```

Diagrama de memoria, DESPUÉS del error:
```
cabeza --> [ queso | None ]

           [ pan | *-] --> [ leche | *-] --> [ huevos | None ]
           (siguen existiendo en memoria, pero YA NADIE los señala)
```

El tren `pan -> leche -> huevos` no se borró mágicamente: sigue estando en algún lugar de la memoria de la computadora. El problema es que **ya no hay ninguna variable que apunte a él**, así que para el programa es como si no existiera. Esto se llama **pérdida de referencia**, y más adelante Python lo limpia solo (se llama "recolección de basura"), pero para efectos prácticos ese dato ya no lo puedes recuperar.

### La forma correcta

La regla es: **primero enganchas el nodo nuevo al resto de la cadena, y solo después mueves la variable de "cabeza" al nodo nuevo.**

```python
cabeza = nodo1                          # cabeza apunta al tren pan -> leche -> huevos
nuevo = Nodo("queso", cabeza)           # 1) primero enganchamos: queso -> (todo lo que cabeza señalaba)
cabeza = nuevo                          # 2) ahora sí movemos "cabeza" al nuevo primer vagón
```

Diagrama de memoria, paso 1 (recién creado `nuevo`, `cabeza` todavía no se mueve):
```
cabeza -----------------------> [ pan | *-] --> [ leche | *-] --> [ huevos | None ]
nuevo --> [ queso | *-] ------------^
```

Diagrama de memoria, paso 2 (después de mover `cabeza`):
```
cabeza --> [ queso | *-] --> [ pan | *-] --> [ leche | *-] --> [ huevos | None ]
```

Nada se perdió: el tren completo sigue siendo alcanzable desde `cabeza`.

---

## La lección para cuando programemos `ListaEnlazada`

El orden de las instrucciones importa muchísimo con nodos. La regla de oro para insertar al principio va a ser siempre:

1. Primero, el nodo nuevo apunta hacia donde apuntaba la cabeza vieja.
2. Solo después, la cabeza se mueve para apuntar al nodo nuevo.

Si se hace al revés, se pierde el resto de la lista para siempre.
