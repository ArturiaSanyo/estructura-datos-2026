"""Implementación del TAD Carrito usando una lista."""


class Carrito:
    """Carrito que guarda pares de producto y cantidad."""

    def __init__(self):
        """Crea un carrito vacío."""
        self.productos = []

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

    def _buscar(self, producto):
        """Devuelve la posición del producto o -1 si no existe."""
        for i, (nombre, cantidad) in enumerate(self.productos):
            if nombre == producto:
                return i
        return -1

    def meter(self, producto, cantidad):
        """Agrega unidades de un producto."""
        producto = self._normalizar(producto)
        self._validar_cantidad(cantidad)

        posicion = self._buscar(producto)

        if posicion == -1:
            self.productos.append((producto, cantidad))
        else:
            nombre, actual = self.productos[posicion]
            self.productos[posicion] = (nombre, actual + cantidad)

    def sacar(self, producto, cantidad):
        """Retira unidades de un producto."""
        producto = self._normalizar(producto)
        self._validar_cantidad(cantidad)

        posicion = self._buscar(producto)

        if posicion == -1:
            raise ValueError("El producto no está en el carrito.")

        nombre, actual = self.productos[posicion]

        if cantidad > actual:
            raise ValueError("No hay suficientes unidades.")

        restante = actual - cantidad

        if restante == 0:
            self.productos.pop(posicion)
        else:
            self.productos[posicion] = (nombre, restante)

    def cuanto_hay(self, producto):
        """Devuelve las unidades de un producto. Si no existe, devuelve 0."""
        producto = self._normalizar(producto)

        posicion = self._buscar(producto)

        if posicion == -1:
            return 0

        return self.productos[posicion][1]

    def cuanto_llevo(self):
        """Devuelve el total de unidades del carrito."""
        return sum(cantidad for _, cantidad in self.productos)
