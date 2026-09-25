# Especificación del TAD Carrito

## 1. Objetivo

El TAD `Carrito` permite guardar productos y sus cantidades.

Debe permitir:

- agregar productos;
- retirar productos;
- consultar cuántas unidades hay de un producto;
- consultar cuántas unidades hay en total.

La especificación define **qué debe hacer** el carrito. La forma de guardar los datos queda a decisión de cada implementación.

---

## 2. Decisiones

### Producto
El nombre debe ser un texto no vacío.

Para evitar diferencias accidentales:

- se eliminan espacios al principio y al final;
- varios espacios seguidos se convierten en uno;
- se usan minúsculas.

Ejemplo: `"  Pan   Integral "` se guarda como `"pan integral"`.

Las tildes no se eliminan. `"café"` y `"cafe"` son productos diferentes.

### Cantidad
La cantidad debe ser un número entero mayor que cero.

Por tanto, `0`, números negativos, decimales y textos no son válidos.

### Cómo se manejan los datos inválidos (decisión de nivel básico)
Esta versión **no usa manejo de errores** (no se lanzan excepciones).

Si algo no es válido —el producto está vacío, la cantidad no es un entero mayor que cero, se quiere sacar un producto que no existe, o se quiere sacar más de lo que hay— la operación:

1. muestra un mensaje en pantalla explicando qué pasó, y
2. no hace ningún cambio en el carrito.

### Agregar
`meter(producto, cantidad)` suma la cantidad indicada.

Si el producto no existe, se crea. Si ya existe, se acumula.

Si el producto o la cantidad no son válidos, se muestra un mensaje y no se agrega nada.

### Retirar
`sacar(producto, cantidad)` resta la cantidad indicada.

Si el producto no existe, se muestra un mensaje y no se cambia nada.

Si se intenta retirar más de lo disponible, se muestra un mensaje y el carrito no cambia.

Si la cantidad llega a cero, el producto se elimina del carrito.

### Consultar
`cuanto_hay(producto)` devuelve la cantidad.

Si el producto no existe, devuelve `0`.

Si el nombre no es válido, muestra un mensaje y devuelve `0`.

### Total
`cuanto_llevo()` devuelve el número total de unidades del carrito. No representa dinero.

### Independencia
Cada objeto `Carrito` debe tener sus propios datos. Dos carritos no pueden compartir productos.

---

## 3. Contrato

### `Carrito()`
Crea un carrito vacío.

### `meter(producto, cantidad)`
Agrega `cantidad` unidades de `producto`.

- Producto: texto no vacío.
- Cantidad: `int >= 1`.
- Devuelve: `None`.
- Si los datos no son válidos: muestra un mensaje y no hace nada.

### `sacar(producto, cantidad)`
Retira `cantidad` unidades.

- Producto: texto no vacío.
- Cantidad: `int >= 1`.
- Debe haber suficientes unidades.
- Devuelve: `None`.
- Si los datos no son válidos, el producto no existe, o no hay suficientes unidades: muestra un mensaje y no hace nada.

### `cuanto_hay(producto)`
Consulta la cantidad de un producto.

- Producto: texto no vacío.
- Devuelve: `int`.
- Si no existe: `0`.
- Si el nombre no es válido: muestra un mensaje y devuelve `0`.

### `cuanto_llevo()`
Devuelve la suma de todas las unidades.

- Devuelve: `int`.
- Carrito vacío: `0`.

---

## 4. Invariantes

Mientras el carrito exista:

1. Todas las cantidades guardadas son enteros mayores que cero.
2. Un producto aparece como máximo una vez.
3. No existen cantidades almacenadas iguales a cero.
4. Los datos de un carrito no se comparten con otro carrito.
5. El total es la suma de las cantidades guardadas.

---

## 5. Implementaciones

Se entregan dos implementaciones del mismo TAD:

- `carrito_lista.py`: usa una lista de pares `(producto, cantidad)`.
- `carrito_dict.py`: usa un diccionario `{producto: cantidad}`.

Ambas deben comportarse exactamente igual desde el punto de vista del usuario.

---

## 6. Ejemplo

```python
from carrito_dict import Carrito

carrito = Carrito()

carrito.meter("Pan", 2)
carrito.meter("pan", 3)
carrito.meter("Leche", 1)

print(carrito.cuanto_hay("PAN"))  # 5
print(carrito.cuanto_llevo())     # 6

carrito.sacar("pan", 2)

print(carrito.cuanto_hay("pan"))  # 3

carrito.sacar("pan", 100)         # muestra mensaje, no cambia nada
print(carrito.cuanto_hay("pan"))  # sigue siendo 3
```

Este ejemplo funciona igual con `carrito_lista.Carrito`.
