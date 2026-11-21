"""Árbol binario de búsqueda (BST) para guardar matrículas por número de documento.

Cómo funciona un BST: cada nodo tiene una clave (el número de documento) y dos hijos.
Todo lo que está a la izquierda es MENOR que el nodo y todo lo que está a la derecha
es MAYOR.

Nota sobre la altura: se cuenta en NIVELES. Un árbol vacío tiene altura 0 y un árbol
con un solo nodo tiene altura 1.
"""
import sys

# Con documentos ordenados el árbol llega a tener 10.000 niveles. Las funciones
# recursivas de este archivo (altura, en_orden, validar) necesitan entonces 10.000
# llamadas una dentro de otra, y Python por defecto solo permite 1.000.
# Por eso subimos el límite.
sys.setrecursionlimit(50000)


class Nodo:
    def __init__(self, clave, valor=None):
        self.clave = clave      # número de documento
        self.valor = valor      # los datos de la matrícula
        self.izq = None         # hijo izquierdo (claves menores)
        self.der = None         # hijo derecho (claves mayores)


class BST:
    def __init__(self):
        self.raiz = None
        self.tamano = 0         # cuántos nodos hay

    # ------------------------------------------------------------------
    # Insertar
    # ------------------------------------------------------------------
    def insertar(self, clave, valor=None):
        """Inserta la clave. Devuelve True si era nueva, False si ya existía."""
        if self.raiz is None:               # árbol vacío: el nuevo nodo es la raíz
            self.raiz = Nodo(clave, valor)
            self.tamano = 1
            return True

        actual = self.raiz
        while True:
            if clave < actual.clave:        # le toca ir a la izquierda
                if actual.izq is None:      # hay un hueco: aquí se queda
                    actual.izq = Nodo(clave, valor)
                    break
                actual = actual.izq
            elif clave > actual.clave:      # le toca ir a la derecha
                if actual.der is None:
                    actual.der = Nodo(clave, valor)
                    break
                actual = actual.der
            else:                           # la clave ya existe: solo actualizamos el valor
                actual.valor = valor
                return False

        self.tamano += 1
        return True

    # ------------------------------------------------------------------
    # Buscar
    # ------------------------------------------------------------------
    def _buscar_nodo(self, clave):
        """Devuelve el nodo con esa clave, o None si no está."""
        actual = self.raiz
        while actual is not None:
            if clave < actual.clave:
                actual = actual.izq
            elif clave > actual.clave:
                actual = actual.der
            else:
                return actual
        return None

    def buscar(self, clave):
        """Devuelve el valor guardado para la clave, o None si no existe."""
        nodo = self._buscar_nodo(clave)
        if nodo is None:
            return None
        return nodo.valor

    def contiene(self, clave):
        return self._buscar_nodo(clave) is not None

    def pasos_busqueda(self, clave):
        """Cuántos nodos hay que visitar para encontrar la clave.

        Sirve para comparar los árboles sin depender de qué tan rápido es el computador.
        """
        pasos = 0
        actual = self.raiz
        while actual is not None:
            pasos += 1
            if clave < actual.clave:
                actual = actual.izq
            elif clave > actual.clave:
                actual = actual.der
            else:
                break
        return pasos

    # ------------------------------------------------------------------
    # Eliminar (tres casos)
    # ------------------------------------------------------------------
    def _reemplazar(self, padre, viejo, nuevo):
        """Cambia el hijo `viejo` del `padre` por `nuevo` (que puede ser None)."""
        if padre is None:               # el nodo viejo era la raíz
            self.raiz = nuevo
        elif padre.izq is viejo:
            padre.izq = nuevo
        else:
            padre.der = nuevo

    def eliminar(self, clave):
        """Elimina la clave. Devuelve True si existía, False si no."""
        # Primero buscamos el nodo, recordando también quién es su padre.
        padre = None
        actual = self.raiz
        while actual is not None and actual.clave != clave:
            padre = actual
            if clave < actual.clave:
                actual = actual.izq
            else:
                actual = actual.der

        if actual is None:              # no estaba
            return False

        if actual.izq is None and actual.der is None:
            # CASO 1: es una hoja (sin hijos). Basta con quitarla.
            self._reemplazar(padre, actual, None)

        elif actual.izq is None or actual.der is None:
            # CASO 2: tiene un solo hijo. El hijo ocupa el lugar del nodo borrado.
            if actual.izq is not None:
                hijo = actual.izq
            else:
                hijo = actual.der
            self._reemplazar(padre, actual, hijo)

        else:
            # CASO 3: tiene dos hijos. No se puede quitar sin más.
            # Buscamos el SUCESOR: el menor de los mayores, o sea el nodo más a la
            # izquierda del subárbol derecho.
            padre_sucesor = actual
            sucesor = actual.der
            while sucesor.izq is not None:
                padre_sucesor = sucesor
                sucesor = sucesor.izq
            # Copiamos los datos del sucesor al nodo que "borramos"...
            actual.clave = sucesor.clave
            actual.valor = sucesor.valor
            # ...y quitamos el sucesor, que como mucho tiene un hijo derecho.
            self._reemplazar(padre_sucesor, sucesor, sucesor.der)

        self.tamano -= 1
        return True

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def altura(self):
        """Número de niveles del árbol."""
        return _altura(self.raiz)

    def en_orden(self):
        """Todas las claves en orden: izquierda, nodo, derecha. Deben salir de menor a mayor."""
        resultado = []
        _recorrer_en_orden(self.raiz, resultado)
        return resultado

    def es_valido(self):
        return es_bst_valido(self.raiz)


def _altura(nodo):
    if nodo is None:
        return 0
    altura_izq = _altura(nodo.izq)
    altura_der = _altura(nodo.der)
    return 1 + max(altura_izq, altura_der)


def _recorrer_en_orden(nodo, resultado):
    if nodo is None:
        return
    _recorrer_en_orden(nodo.izq, resultado)
    resultado.append(nodo.clave)
    _recorrer_en_orden(nodo.der, resultado)


def es_bst_valido(raiz):
    """Comprueba que TODO el árbol cumpla la regla del BST.

    No basta con comparar cada nodo con su padre y sus hijos. Ejemplo: un nodo que
    está en el subárbol izquierdo de la raíz tiene que ser menor que la raíz, aunque
    esté muy abajo y su padre inmediato sea otro. Por eso a cada nodo se le pasa el
    rango (minimo, maximo) en el que tiene que estar según TODOS sus ancestros.
    """
    return _esta_en_rango(raiz, None, None)


def _esta_en_rango(nodo, minimo, maximo):
    if nodo is None:
        return True                         # un árbol vacío no rompe ninguna regla
    if minimo is not None and nodo.clave <= minimo:
        return False
    if maximo is not None and nodo.clave >= maximo:
        return False
    # A la izquierda: todo debe ser menor que este nodo (nuevo máximo = su clave).
    # A la derecha: todo debe ser mayor que este nodo (nuevo mínimo = su clave).
    return (_esta_en_rango(nodo.izq, minimo, nodo.clave)
            and _esta_en_rango(nodo.der, nodo.clave, maximo))
