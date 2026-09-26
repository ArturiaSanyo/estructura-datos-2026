# ListaEnlazada — mismo contrato que ListaArreglo (ver lista_arreglo.py),
# pero por dentro usa nodos conectados en vez de un arreglo.

from lista_arreglo import PosicionInvalidaError


class Nodo:
    """Una cajita con un dato y un gancho ('siguiente') hacia la próxima cajita."""

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class ListaEnlazada:
    """Lista implementada como una cadena de nodos.

    Atributos internos:
        _cabeza    el primer nodo de la cadena (o None si está vacía)
        _tamaño    cuántos nodos hay

    Complejidad:
        obtener          -> O(n)  (hay que caminar nodo por nodo)
        insertar(inicio) -> O(1)
        insertar(final)  -> O(n)  (hay que caminar hasta el final)
        eliminar         -> O(n)
        buscar           -> O(n)
    """

    def __init__(self):
        self._cabeza = None
        self._tamaño = 0

    # ---------- operaciones públicas ----------

    def tamaño(self):
        return self._tamaño

    def obtener(self, posicion):
        """Devuelve el elemento en `posicion`. O(n): hay que caminar hasta ahí."""
        self._validar(posicion, incluir_final=False)
        return self._nodo_en(posicion).dato

    def insertar(self, posicion, elemento):
        """Inserta un nodo nuevo en `posicion`."""
        self._validar(posicion, incluir_final=True)

        nuevo = Nodo(elemento)

        if posicion == 0:
            # Regla de oro (ver nodos_a_mano.md): primero enganchar,
            # después mover la cabeza. Si se hace al revés, se pierde
            # el resto de la lista.
            nuevo.siguiente = self._cabeza
            self._cabeza = nuevo
        else:
            anterior = self._nodo_en(posicion - 1)
            nuevo.siguiente = anterior.siguiente
            anterior.siguiente = nuevo

        self._tamaño += 1

    def eliminar(self, posicion):
        """Elimina y devuelve el elemento en `posicion`."""
        self._validar(posicion, incluir_final=False)

        if posicion == 0:
            nodo_borrado = self._cabeza
            self._cabeza = self._cabeza.siguiente
        else:
            anterior = self._nodo_en(posicion - 1)
            nodo_borrado = anterior.siguiente
            anterior.siguiente = nodo_borrado.siguiente

        self._tamaño -= 1
        return nodo_borrado.dato

    def buscar(self, elemento):
        """Devuelve la posición de la primera aparición, o -1."""
        actual = self._cabeza
        posicion = 0
        while actual is not None:
            if actual.dato == elemento:
                return posicion
            actual = actual.siguiente
            posicion += 1
        return -1

    # ---------- auxiliares ----------

    def _validar(self, posicion, incluir_final):
        limite = self._tamaño if incluir_final else self._tamaño - 1
        if not 0 <= posicion <= limite:
            raise PosicionInvalidaError(
                f"posicion {posicion} fuera de rango [0, {limite}]"
            )

    def _nodo_en(self, posicion):
        """Camina desde la cabeza hasta llegar al nodo en `posicion`."""
        actual = self._cabeza
        for _ in range(posicion):
            actual = actual.siguiente
        return actual

    # ---------- protocolo de Python ----------

    def __len__(self):
        return self._tamaño

    def __getitem__(self, i):
        return self.obtener(i)

    def __iter__(self):
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __repr__(self):
        return f"ListaEnlazada({list(self)!r})"
