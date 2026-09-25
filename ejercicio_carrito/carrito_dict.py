"""
Implementación del TAD Carrito usando un DICCIONARIO.

Guardamos los productos como pares clave -> valor, donde
la clave es el nombre del producto y el valor es la cantidad.
Ejemplo de cómo se ve por dentro:

    {"pan": 5, "leche": 2}

Nivel básico: si algo no es válido, solo se imprime un mensaje
y no se hace ningún cambio. No se usan errores (raise/ValueError).
"""


def normalizar_producto(producto):
    """
    Recibe el nombre de un producto y lo deja limpio:
    sin espacios de sobra y en minúsculas.

    Si el producto no es válido (no es texto, o queda vacío),
    devuelve None para avisar que algo está mal.
    """
    if type(producto) != str:
        return None

    texto = " ".join(producto.split())  # quita espacios de sobra
    texto = texto.lower()

    if texto == "":
        return None

    return texto


def cantidad_valida(cantidad):
    """Devuelve True si la cantidad es un entero mayor que cero."""
    return type(cantidad) == int and cantidad >= 1


class Carrito:
    def __init__(self):
        self.productos = {}  # nombre -> cantidad

    def meter(self, producto, cantidad):
        nombre = normalizar_producto(producto)
        if nombre is None:
            print("Ese producto no es válido.")
            return

        if not cantidad_valida(cantidad):
            print("La cantidad debe ser un número entero mayor que cero.")
            return

        if nombre in self.productos:
            self.productos[nombre] = self.productos[nombre] + cantidad
        else:
            self.productos[nombre] = cantidad

    def sacar(self, producto, cantidad):
        nombre = normalizar_producto(producto)
        if nombre is None:
            print("Ese producto no es válido.")
            return

        if not cantidad_valida(cantidad):
            print("La cantidad debe ser un número entero mayor que cero.")
            return

        if nombre not in self.productos:
            print(f"No tienes '{nombre}' en el carrito.")
            return

        cantidad_guardada = self.productos[nombre]

        if cantidad > cantidad_guardada:
            print("No hay suficientes unidades para sacar.")
            return

        nueva_cantidad = cantidad_guardada - cantidad

        if nueva_cantidad == 0:
            del self.productos[nombre]
        else:
            self.productos[nombre] = nueva_cantidad

    def cuanto_hay(self, producto):
        nombre = normalizar_producto(producto)
        if nombre is None:
            print("Ese producto no es válido.")
            return 0

        if nombre in self.productos:
            return self.productos[nombre]

        return 0

    def cuanto_llevo(self):
        total = 0
        for cantidad in self.productos.values():
            total = total + cantidad
        return total
