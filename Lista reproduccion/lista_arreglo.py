class ListaArreglo:
    """Lista secuencial basada en un arreglo dinámico de Python."""

    def __init__(self):
        self._datos = []
        self._actual = -1

    def esta_vacia(self):
        return len(self._datos) == 0

    def tamano(self):
        return len(self._datos)

    def insertar_al_principio(self, dato):
        self._datos.insert(0, dato)
        if self._actual >= 0:
            self._actual += 1
        else:
            self._actual = 0

    def insertar_al_final(self, dato):
        self._datos.append(dato)
        if self._actual == -1:
            self._actual = 0

    def obtener(self, indice):
        if indice < 0 or indice >= len(self._datos):
            raise IndexError("Índice fuera de rango")
        return self._datos[indice]

    def recorrer(self):
        for dato in self._datos:
            yield dato

    def ir_a(self, indice):
        if indice < 0 or indice >= len(self._datos):
            raise IndexError("Índice fuera de rango")
        self._actual = indice
        return self._datos[indice]

    def borrar_actual(self):
        if self.esta_vacia():
            raise IndexError("No se puede borrar en una lista vacía")
        dato = self._datos.pop(self._actual)
        if not self._datos:
            self._actual = -1
        elif self._actual >= len(self._datos):
            self._actual = len(self._datos) - 1
        return dato
