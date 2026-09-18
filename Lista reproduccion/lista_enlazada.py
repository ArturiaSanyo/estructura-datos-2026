class Nodo:
    """Nodo simple de una lista enlazada."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    """Lista enlazada simple sin usar list de Python para almacenar datos."""

    def __init__(self):
        self._primero = None
        self._ultimo = None
        self._actual = None
        self._anterior = None
        self._tamano = 0

    def esta_vacia(self):
        return self._primero is None

    def tamano(self):
        return self._tamano

    def insertar_al_principio(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self._primero
        self._primero = nuevo

        if self._ultimo is None:
            self._ultimo = nuevo

        if self._actual is None:
            self._actual = nuevo
            self._anterior = None

        self._tamano += 1

    def insertar_al_final(self, dato):
        nuevo = Nodo(dato)

        if self._ultimo is None:
            self._primero = nuevo
            self._ultimo = nuevo
            self._actual = nuevo
            self._anterior = None
        else:
            self._ultimo.siguiente = nuevo
            self._ultimo = nuevo

        self._tamano += 1

    def _buscar(self, indice):
        if indice < 0 or indice >= self._tamano:
            raise IndexError("Índice fuera de rango")

        anterior = None
        actual = self._primero
        posicion = 0

        while posicion < indice:
            anterior = actual
            actual = actual.siguiente
            posicion += 1

        return anterior, actual

    def obtener(self, indice):
        _, nodo = self._buscar(indice)
        return nodo.dato

    def recorrer(self):
        actual = self._primero
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def ir_a(self, indice):
        anterior, actual = self._buscar(indice)
        self._anterior = anterior
        self._actual = actual
        return actual.dato

    def borrar_actual(self):
        if self.esta_vacia():
            raise IndexError("No se puede borrar en una lista vacía")

        anterior = self._anterior
        actual = self._actual

        if anterior is None:
            self._primero = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente

        if actual is self._ultimo:
            self._ultimo = anterior

        self._tamano -= 1

        if self._primero is None:
            self._actual = None
            self._anterior = None
        elif actual.siguiente is not None:
            self._actual = actual.siguiente
            self._anterior = anterior
        else:
            self._actual = self._ultimo
            self._anterior = None

            cursor = self._primero
            while cursor is not None and cursor.siguiente is not self._actual:
                cursor = cursor.siguiente
            self._anterior = cursor

        return actual.dato
