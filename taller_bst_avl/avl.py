"""Árbol AVL: un BST que se mantiene equilibrado solo.

Regla del AVL: en cada nodo, la altura del subárbol izquierdo y la del derecho
no pueden diferir en más de 1. Si una inserción rompe la regla, se arregla
"rotando" nodos en ese mismo lugar.

  factor de balance = altura(izquierda) - altura(derecha)
  Si el factor es 2 o -2 hay que rotar. Hay cuatro casos:

    LL (izquierda-izquierda): rotación simple a la derecha
    RR (derecha-derecha):     rotación simple a la izquierda
    LR (izquierda-derecha):   rotar a la izquierda el hijo, luego a la derecha el nodo
    RL (derecha-izquierda):   rotar a la derecha el hijo, luego a la izquierda el nodo

Cada nodo guarda su altura. Esa altura se actualiza cuando la inserción "regresa"
(vuelve de la recursión), así nunca hay que recalcular el árbol entero.
Altura en niveles: vacío = 0, una hoja = 1.
"""


class NodoAVL:
    def __init__(self, clave, valor=None):
        self.clave = clave
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 1         # un nodo nuevo es una hoja


def altura_de(nodo):
    """Altura guardada en el nodo (0 si no hay nodo)."""
    if nodo is None:
        return 0
    return nodo.altura


def actualizar_altura(nodo):
    """Recalcula la altura de UN nodo a partir de las de sus dos hijos."""
    nodo.altura = 1 + max(altura_de(nodo.izq), altura_de(nodo.der))


def factor_balance(nodo):
    return altura_de(nodo.izq) - altura_de(nodo.der)


def rotar_derecha(y):
    """      y             x
            / \\          / \\
           x   C   ->   A   y
          / \\              / \\
         A   B            B   C
    """
    x = y.izq
    y.izq = x.der
    x.der = y
    actualizar_altura(y)    # primero y, que quedó abajo
    actualizar_altura(x)    # después x, que quedó arriba
    return x                # x es la nueva raíz de este subárbol


def rotar_izquierda(x):
    """    x                 y
          / \\              / \\
         A   y     ->     x   C
            / \\          / \\
           B   C        A   B
    """
    y = x.der
    x.der = y.izq
    y.izq = x
    actualizar_altura(x)
    actualizar_altura(y)
    return y


class AVL:
    def __init__(self):
        self.raiz = None
        self.tamano = 0
        # Cuántas veces ocurrió cada caso de desbalance
        self.casos = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}

    def total_reequilibrios(self):
        """Cuántas veces hubo que arreglar un desbalance."""
        return self.casos["LL"] + self.casos["RR"] + self.casos["LR"] + self.casos["RL"]

    def total_rotaciones(self):
        """Rotaciones simples hechas. Los casos LR y RL cuentan 2 (son dos rotaciones)."""
        return (self.casos["LL"] + self.casos["RR"]
                + 2 * self.casos["LR"] + 2 * self.casos["RL"])

    # ------------------------------------------------------------------
    # Insertar
    # ------------------------------------------------------------------
    def insertar(self, clave, valor=None):
        """Inserta la clave. Devuelve True si era nueva, False si ya existía."""
        tamano_antes = self.tamano
        self.raiz = self._insertar(self.raiz, clave, valor)
        return self.tamano > tamano_antes

    def _insertar(self, nodo, clave, valor):
        """Inserta dentro del subárbol `nodo` y devuelve la raíz de ese subárbol."""
        if nodo is None:                    # llegamos a un hueco: nodo nuevo
            self.tamano += 1
            return NodoAVL(clave, valor)

        if clave < nodo.clave:
            nodo.izq = self._insertar(nodo.izq, clave, valor)
        elif clave > nodo.clave:
            nodo.der = self._insertar(nodo.der, clave, valor)
        else:
            nodo.valor = valor              # clave repetida: solo se actualiza el valor
            return nodo

        # ---- CAMINO DE VUELTA ----
        # Aquí ya insertamos abajo. Ahora actualizamos la altura de este nodo
        # y miramos si quedó desequilibrado.
        actualizar_altura(nodo)
        return self._equilibrar(nodo)

    def _equilibrar(self, nodo):
        """Si el nodo está desequilibrado, rota. Devuelve la nueva raíz del subárbol."""
        balance = factor_balance(nodo)

        if balance > 1:                             # pesa de más a la izquierda
            if factor_balance(nodo.izq) < 0:        # caso LR
                nodo.izq = rotar_izquierda(nodo.izq)
                self.casos["LR"] += 1
            else:                                   # caso LL
                self.casos["LL"] += 1
            return rotar_derecha(nodo)

        if balance < -1:                            # pesa de más a la derecha
            if factor_balance(nodo.der) > 0:        # caso RL
                nodo.der = rotar_derecha(nodo.der)
                self.casos["RL"] += 1
            else:                                   # caso RR
                self.casos["RR"] += 1
            return rotar_izquierda(nodo)

        return nodo                                 # ya estaba equilibrado

    # ------------------------------------------------------------------
    # Buscar (igual que en el BST)
    # ------------------------------------------------------------------
    def _buscar_nodo(self, clave):
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
        nodo = self._buscar_nodo(clave)
        if nodo is None:
            return None
        return nodo.valor

    def contiene(self, clave):
        return self._buscar_nodo(clave) is not None

    def pasos_busqueda(self, clave):
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
    # Utilidades
    # ------------------------------------------------------------------
    def altura(self):
        return altura_de(self.raiz)

    def en_orden(self):
        resultado = []
        _recorrer_en_orden(self.raiz, resultado)
        return resultado

    def es_valido(self):
        """Comprueba tres cosas: que sea un BST válido, que las alturas guardadas
        sean las reales, y que ningún nodo esté desequilibrado."""
        if not _esta_en_rango(self.raiz, None, None):
            return False
        return _alturas_y_balance_correctos(self.raiz)


def _recorrer_en_orden(nodo, resultado):
    if nodo is None:
        return
    _recorrer_en_orden(nodo.izq, resultado)
    resultado.append(nodo.clave)
    _recorrer_en_orden(nodo.der, resultado)


def _esta_en_rango(nodo, minimo, maximo):
    """Revisa la regla del BST en todo el subárbol (ver explicación en bst.py)."""
    if nodo is None:
        return True
    if minimo is not None and nodo.clave <= minimo:
        return False
    if maximo is not None and nodo.clave >= maximo:
        return False
    return (_esta_en_rango(nodo.izq, minimo, nodo.clave)
            and _esta_en_rango(nodo.der, nodo.clave, maximo))


def _altura_real(nodo):
    """Calcula la altura mirando el árbol, sin fiarse del valor guardado."""
    if nodo is None:
        return 0
    return 1 + max(_altura_real(nodo.izq), _altura_real(nodo.der))


def _alturas_y_balance_correctos(nodo):
    if nodo is None:
        return True
    if nodo.altura != _altura_real(nodo):
        return False                                    # la altura guardada está mal
    if abs(_altura_real(nodo.izq) - _altura_real(nodo.der)) > 1:
        return False                                    # nodo desequilibrado
    return (_alturas_y_balance_correctos(nodo.izq)
            and _alturas_y_balance_correctos(nodo.der))
