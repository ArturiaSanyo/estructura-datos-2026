"""Implementación del TAD Carrito usando un diccionario."""


class Carrito:
    """Carrito que guarda la cantidad de cada producto."""

    def __init__(self):
        """Crea un carrito vacío."""
        self.productos = {}

    @staticmethod
    def _normalizar(producto):
        """Valida y normaliza el nombre del producto."""
        if not isinstance(producto, str):
            raise ValueError("El producto debe ser un texto.")

        producto = " ".join(producto.split()).lower()

        if not producto:
            raise ValueError("El producto no puede estar vacío.")

        return producto

    @staticmethod
    def _validar_cantidad(cantidad):
        """Comprueba que la cantidad sea un entero positivo."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 1:
            raise ValueError("La cantidad debe ser un entero mayor que cero.")

    def meter(self, producto, cantidad):
        """Agrega unidades de un producto."""
        producto = self._normalizar(producto)
        self._validar_cantidad(cantidad)

        self.productos[producto] = self.productos.get(producto, 0) + cantidad

    def sacar(self, producto, cantidad):
        """Retira unidades de un producto."""
        producto = self._normalizar(producto)
        self._validar_cantidad(cantidad)

        if producto not in self.productos:
            raise ValueError("El producto no está en el carrito.")

        if cantidad > self.productos[producto]:
            raise ValueError("No hay suficientes unidades.")

        self.productos[producto] -= cantidad

        if self.productos[producto] == 0:
            del self.productos[producto]

    def cuanto_hay(self, producto):
        """Devuelve las unidades de un producto. Si no existe, devuelve 0."""
        producto = self._normalizar(producto)
        return self.productos.get(producto, 0)

    def cuanto_llevo(self):
        """Devuelve el total de unidades del carrito."""
        return sum(self.productos.values())
