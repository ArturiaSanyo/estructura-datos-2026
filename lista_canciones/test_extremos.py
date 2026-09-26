"""
Pruebas de los cuatro casos extremos (Parte C de la Actividad 3):
lista vacía, lista de un elemento, borrar el primero, borrar el último.

Se corren contra las DOS implementaciones (ListaArreglo y ListaEnlazada)
para comprobar que ambas cumplen el mismo contrato.
"""

import pytest

from lista_arreglo import ListaArreglo
from lista_enlazada import ListaEnlazada

IMPLEMENTACIONES = [ListaArreglo, ListaEnlazada]
IDS = ["arreglo", "enlazada"]


@pytest.mark.parametrize("Clase", IMPLEMENTACIONES, ids=IDS)
def test_extremo_lista_vacia(Clase):
    lista = Clase()
    assert lista.tamaño() == 0
    assert len(lista) == 0
    assert list(lista) == []
    assert lista.buscar("nada") == -1


@pytest.mark.parametrize("Clase", IMPLEMENTACIONES, ids=IDS)
def test_extremo_lista_de_un_elemento(Clase):
    lista = Clase()
    lista.insertar(0, "unica_cancion")
    assert lista.tamaño() == 1
    assert lista.obtener(0) == "unica_cancion"
    assert list(lista) == ["unica_cancion"]


@pytest.mark.parametrize("Clase", IMPLEMENTACIONES, ids=IDS)
def test_extremo_borrar_el_primero(Clase):
    lista = Clase()
    lista.insertar(0, "cancion_1")
    lista.insertar(1, "cancion_2")
    lista.insertar(2, "cancion_3")

    elemento = lista.eliminar(0)

    assert elemento == "cancion_1"
    assert list(lista) == ["cancion_2", "cancion_3"]
    assert lista.tamaño() == 2


@pytest.mark.parametrize("Clase", IMPLEMENTACIONES, ids=IDS)
def test_extremo_borrar_el_ultimo(Clase):
    lista = Clase()
    lista.insertar(0, "cancion_1")
    lista.insertar(1, "cancion_2")
    lista.insertar(2, "cancion_3")

    elemento = lista.eliminar(2)

    assert elemento == "cancion_3"
    assert list(lista) == ["cancion_1", "cancion_2"]
    assert lista.tamaño() == 2
