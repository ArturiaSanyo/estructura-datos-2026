# Código base — Semana 04
# Fuente: 01-Momento-1-Contrato-y-secuencia/04-Semana-04-Arreglos-y-estructuras-estaticas/02-guia-de-laboratorio.html

from array import array

class PosicionInvalidaError(IndexError):
    """La posición solicitada está fuera del rango válido."""

class ListaArreglo:
    """Lista implementada sobre un arreglo de tamaño fijo con redimensionamiento."""

    CAPACIDAD_INICIAL = 4

    def __init__(self):
        self._capacidad = self.CAPACIDAD_INICIAL
        self._datos = [None] * self._capacidad
        self._tamano = 0

    # ---------- operaciones públicas ----------

    def tamano(self):
        """Devuelve el número de elementos en la lista."""
        return self._tamano

    def obtener(self, posicion):
        """Devuelve el elemento en `posicion`. O(1)."""
        self._validar(posicion, incluir_final=False)
        return self._datos[posicion]

    def insertar(self, posicion, elemento):
        """Inserta un elemento en la posición indicada, desplazando los siguientes."""
        self._validar(posicion, incluir_final=True)
        
        # Si el arreglo está lleno, redimensionamos al doble
        if self._tamano == self._capacidad:
            self._redimensionar(self._capacidad * 2)
        
        # Desplazamos los elementos hacia la derecha desde el final
        for i in range(self._tamano, posicion, -1):
            self._datos[i] = self._datos[i-1]
        
        # Insertamos el nuevo elemento
        self._datos[posicion] = elemento
        self._tamano += 1

    def eliminar(self, posicion):
        """Elimina y devuelve el elemento en la posición indicada, desplazando los siguientes."""
        self._validar(posicion, incluir_final=False)
        
        # Guardamos el elemento a eliminar
        elemento_eliminado = self._datos[posicion]
        
        # Desplazamos los elementos hacia la izquierda
        for i in range(posicion, self._tamano - 1):
            self._datos[i] = self._datos[i + 1]
        
        # Dejamos la última posición vacía
        self._datos[self._tamano - 1] = None
        self._tamano -= 1
        
        # Si el tamaño es una cuarta parte de la capacidad, reducimos
        if self._tamano <= self._capacidad // 4 and self._capacidad > self.CAPACIDAD_INICIAL:
            self._redimensionar(self._capacidad // 2)
        
        return elemento_eliminado

    def buscar(self, elemento):
        """Devuelve la posición de la primera aparición del elemento, o -1 si no existe."""
        for i in range(self._tamano):
            if self._datos[i] == elemento:
                return i
        return -1

    # ---------- auxiliares ----------

    def _validar(self, posicion, incluir_final):
        """Valida que la posición esté dentro del rango válido."""
        limite = self._tamano if incluir_final else self._tamano - 1
        if not 0 <= posicion <= limite:
            raise PosicionInvalidaError(
                f"posicion {posicion} fuera de rango [0, {limite}]"
            )

    def _redimensionar(self, nueva_capacidad):
        """Crea un arreglo mayor/menor y copia los elementos. O(n)."""
        nuevos_datos = [None] * nueva_capacidad
        for i in range(self._tamano):
            nuevos_datos[i] = self._datos[i]
        self._datos = nuevos_datos
        self._capacidad = nueva_capacidad

    # ---------- protocolo de Python ----------

    def __len__(self):
        return self._tamano

    def __getitem__(self, i):
        return self.obtener(i)

    def __iter__(self):
        for i in range(self._tamano):
            yield self._datos[i]

    def __repr__(self):
        return f"ListaArreglo({list(self)!r})"


# ---------- Ejemplos de uso ----------
l1 = ListaArreglo()
print("Tamaño inicial:", l1.tamano())

# Insertamos algunos elementos
l1.insertar(0, 9)    # [9]
l1.insertar(1, 98)   # [9, 98]
l1.insertar(2, 66)   # [9, 98, 66]
print("Después de inserciones:", list(l1))

# Buscamos un elemento
print("Posición de 98:", l1.buscar(98))   # 1
print("Posición de 99:", l1.buscar(99))   # -1 (no existe)

# Eliminamos un elemento
eliminado = l1.eliminar(1)   # Elimina 98
print(f"Elemento eliminado: {eliminado}")
print("Después de eliminar:", list(l1))

# Obtenemos un elemento en una posición
print("Elemento en posición 1:", l1.obtener(1))  # 66
