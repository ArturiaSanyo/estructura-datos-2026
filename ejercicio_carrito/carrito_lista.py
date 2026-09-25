"""
Implementación del TAD Carrito usando una LISTA.

Guardamos los productos como una lista de pares (nombre, cantidad).
Ejemplo de cómo se ve por dentro:

    [("pan", 5), ("leche", 2)]

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
        self.productos = []  # lista de pares (nombre, cantidad)

    def _buscar_indice(self, nombre):
        """
        Recorre la lista buscando el producto.
        Si lo encuentra, devuelve su posición (índice).
        Si no lo encuentra, devuelve -1.
        """
        for i in range(len(self.productos)):
            if self.productos[i][0] == nombre:
                return i
        return -1

    def meter(self, producto, cantidad):
        nombre = normalizar_producto(producto)
        if nombre is None:
            print("Ese producto no es válido.")
            return

        if not cantidad_valida(cantidad):
            print("La cantidad debe ser un número entero mayor que cero.")
            return

        indice = self._buscar_indice(nombre)

        if indice == -1:
            # No existía: lo agregamos como un par nuevo
            self.productos.append((nombre, cantidad))
        else:
            # Ya existía: sumamos a la cantidad guardada
            nombre_guardado, cantidad_guardada = self.productos[indice]
            self.productos[indice] = (nombre_guardado, cantidad_guardada + cantidad)

    def sacar(self, producto, cantidad):
        nombre = normalizar_producto(producto)
        if nombre is None:
            print("Ese producto no es válido.")
            return

        if not cantidad_valida(cantidad):
            print("La cantidad debe ser un número entero mayor que cero.")
            return

        indice = self._buscar_indice(nombre)

        if indice == -1:
            print(f"No tienes '{nombre}' en el carrito.")
            return

        nombre_guardado, cantidad_guardada = self.productos[indice]

        if cantidad > cantidad_guardada:
            print("No hay suficientes unidades para sacar.")
            return

        nueva_cantidad = cantidad_guardada - cantidad

        if nueva_cantidad == 0:
            del self.productos[indice]
        else:
            self.productos[indice] = (nombre_guardado, nueva_cantidad)

    def cuanto_hay(self, producto):
        nombre = normalizar_producto(producto)
        if nombre is None:
            print("Ese producto no es válido.")
            return 0

        indice = self._buscar_indice(nombre)
        if indice == -1:
            return 0

        return self.productos[indice][1]

    def cuanto_llevo(self):
        total = 0
        for nombre, cantidad in self.productos:
            total = total + cantidad
        return total
