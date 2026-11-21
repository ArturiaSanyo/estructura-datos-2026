"""Pruebas del AVL. Se pueden correr con:  python run_tests.py   (o con pytest)."""
import random

from avl import AVL


def construir(claves):
    arbol = AVL()
    for clave in claves:
        arbol.insertar(clave)
    return arbol


def test_los_cuatro_casos_de_rotacion():
    # Insertar tres claves en cada orden provoca cada caso una vez.
    # En los cuatro, el 2 tiene que quedar de raíz.
    pruebas = [([3, 2, 1], "LL"), ([1, 2, 3], "RR"), ([3, 1, 2], "LR"), ([1, 3, 2], "RL")]
    for claves, caso in pruebas:
        arbol = construir(claves)
        assert arbol.casos[caso] == 1
        assert arbol.total_reequilibrios() == 1
        assert arbol.raiz.clave == 2
        assert arbol.altura() == 2
        assert arbol.es_valido()


def test_las_rotaciones_dobles_cuentan_dos():
    assert construir([3, 2, 1]).total_rotaciones() == 1     # LL: una rotación
    assert construir([3, 1, 2]).total_rotaciones() == 2     # LR: dos rotaciones


def test_carga_ordenada_queda_equilibrada():
    arbol = construir(range(1, 128))        # 127 nodos = 2^7 - 1
    assert arbol.altura() == 7              # el mínimo posible: un árbol perfecto
    assert arbol.en_orden() == list(range(1, 128))
    assert arbol.es_valido()


def test_aleatorio_mantiene_todo_en_orden():
    azar = random.Random(3)
    claves = azar.sample(range(100000), 2000)
    arbol = construir(claves)
    assert arbol.tamano == 2000
    assert arbol.en_orden() == sorted(claves)
    assert arbol.es_valido()
    assert arbol.altura() <= 16             # un AVL de 2000 nodos nunca pasa de ~16 niveles


def test_clave_repetida_actualiza_el_valor():
    arbol = construir([2, 1, 3])
    assert arbol.insertar(1, "x") is False
    assert arbol.buscar(1) == "x"
    assert arbol.tamano == 3
