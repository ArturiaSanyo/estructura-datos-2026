"""Pruebas del BST. Se pueden correr con:  python run_tests.py   (o con pytest)."""
import random

from bst import BST, Nodo, es_bst_valido


def construir(claves):
    """Crea un BST insertando las claves en el orden dado."""
    arbol = BST()
    for clave in claves:
        arbol.insertar(clave, "matricula-" + str(clave))
    return arbol


# ----------------------------------------------------- insertar y buscar
def test_insertar_y_buscar():
    arbol = construir([50, 30, 70, 20, 40, 60, 80])
    assert arbol.tamano == 7
    assert arbol.buscar(60) == "matricula-60"
    assert arbol.buscar(99) is None
    assert arbol.contiene(20)
    assert not arbol.contiene(21)
    assert arbol.en_orden() == [20, 30, 40, 50, 60, 70, 80]


def test_clave_repetida_actualiza_el_valor():
    arbol = construir([5, 3, 8])
    assert arbol.insertar(3, "nuevo") is False
    assert arbol.tamano == 3
    assert arbol.buscar(3) == "nuevo"


def test_arbol_vacio():
    arbol = BST()
    assert arbol.buscar(1) is None
    assert arbol.altura() == 0
    assert arbol.eliminar(1) is False
    assert arbol.es_valido()


# ------------------------------------------------------------ eliminar
def test_eliminar_hoja():
    arbol = construir([50, 30, 70, 20, 40, 60, 80])
    assert arbol.eliminar(20) is True
    assert arbol.en_orden() == [30, 40, 50, 60, 70, 80]
    assert arbol.tamano == 6
    assert arbol.es_valido()


def test_eliminar_nodo_con_un_hijo():
    # El 30 solo tiene hijo izquierdo (20) y el 70 solo tiene hijo derecho (80).
    arbol = construir([50, 30, 70, 20, 80])
    assert arbol.eliminar(30) is True
    assert arbol.raiz.izq.clave == 20       # el hijo subió
    assert arbol.eliminar(70) is True
    assert arbol.raiz.der.clave == 80
    assert arbol.en_orden() == [20, 50, 80]
    assert arbol.es_valido()


def test_eliminar_nodo_con_dos_hijos_y_sigue_siendo_bst():
    #            50
    #        30      70
    #      20  40  60  80
    #         35  65
    arbol = construir([50, 30, 70, 20, 40, 60, 80, 35, 65])

    assert arbol.eliminar(30) is True       # tiene dos hijos (20 y 40)
    assert arbol.es_valido()                # sigue siendo BST en TODO el subárbol
    assert arbol.en_orden() == [20, 35, 40, 50, 60, 65, 70, 80]

    assert arbol.eliminar(50) is True       # la raíz, también con dos hijos
    assert arbol.es_valido()
    assert arbol.en_orden() == [20, 35, 40, 60, 65, 70, 80]
    assert arbol.tamano == 7


def test_eliminar_raiz_unica_y_clave_inexistente():
    arbol = construir([10])
    assert arbol.eliminar(99) is False
    assert arbol.eliminar(10) is True
    assert arbol.raiz is None
    assert arbol.tamano == 0


# ----------------------------- el validador revisa todo el subárbol
def comprueba_solo_padre_e_hijos(nodo):
    """La validación INCORRECTA (el error clásico): solo mira padre e hijos directos."""
    if nodo is None:
        return True
    if nodo.izq is not None and nodo.izq.clave >= nodo.clave:
        return False
    if nodo.der is not None and nodo.der.clave <= nodo.clave:
        return False
    return comprueba_solo_padre_e_hijos(nodo.izq) and comprueba_solo_padre_e_hijos(nodo.der)


def test_validador_detecta_una_violacion_lejana():
    # El 55 está en el lado izquierdo de la raíz 50, pero 55 > 50: árbol inválido.
    # Aun así, frente a su padre (40) se ve bien, porque 55 > 40.
    #         50
    #      30    70
    #        40
    #          55   <- mal puesto
    raiz = Nodo(50)
    raiz.izq = Nodo(30)
    raiz.der = Nodo(70)
    raiz.izq.der = Nodo(40)
    raiz.izq.der.der = Nodo(55)

    assert es_bst_valido(raiz) is False                 # nuestro validador lo detecta
    assert comprueba_solo_padre_e_hijos(raiz) is True   # el validador ingenuo NO


# --------------------------------------------------------- más pruebas
def test_carga_ordenada_degenera_en_una_lista():
    arbol = construir(range(1, 501))
    assert arbol.altura() == 500


def test_aleatorio_contra_el_set_de_python():
    azar = random.Random(7)
    arbol = BST()
    referencia = set()                      # un set de Python como "respuesta correcta"
    for _ in range(3000):
        clave = azar.randint(0, 400)
        if azar.random() < 0.6:
            arbol.insertar(clave)
            referencia.add(clave)
        else:
            existia = clave in referencia
            assert arbol.eliminar(clave) == existia
            referencia.discard(clave)
        assert arbol.tamano == len(referencia)
    assert arbol.en_orden() == sorted(referencia)
    assert arbol.es_valido()
