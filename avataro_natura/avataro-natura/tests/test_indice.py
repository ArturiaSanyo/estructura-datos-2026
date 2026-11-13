"""Pruebas del Índice de comentarios (Componente 03).

Cada docstring dice qué criterio verifica. Las pruebas que empiezan con
test_plan_ no verifican la spec sino lo que promete el plan.md
(forma y costo de la estructura).
"""

import pytest

from estructuras.errores import (
    ComentarioNoEncontradoError,
    NumeroInvalidoError,
    NumeroRepetidoError,
)
from estructuras.indice import Indice


def test_agregar_y_buscar():
    """CA-01: después de agregar un número con su elemento, buscar devuelve ese elemento."""
    indice = Indice()
    indice.agregar(1, "comentario uno")
    assert indice.buscar(1) == "comentario uno"


def test_existe():
    """CA-02: existe dice True para un número agregado y False para los demás."""
    indice = Indice()
    indice.agregar(3, "tres")
    assert indice.existe(3) is True
    assert indice.existe(4) is False
    assert indice.existe(0) is False
    assert indice.existe(-3) is False
    assert indice.existe("3") is False


def test_buscar_inexistente():
    """CA-03: buscar un número que no está lanza ComentarioNoEncontradoError."""
    indice = Indice()
    indice.agregar(1, "uno")
    with pytest.raises(ComentarioNoEncontradoError):
        indice.buscar(2)
    with pytest.raises(ComentarioNoEncontradoError):
        indice.buscar("abc")


def test_agregar_repetido():
    """CA-04: agregar un número repetido lanza NumeroRepetidoError y no cambia nada."""
    indice = Indice()
    indice.agregar(1, "original")
    with pytest.raises(NumeroRepetidoError):
        indice.agregar(1, "intruso")
    assert indice.buscar(1) == "original"
    assert indice.cantidad() == 1


def test_numero_invalido():
    """CA-05: agregar un número no válido lanza NumeroInvalidoError y no cambia nada."""
    indice = Indice()
    for malo in (0, -1, 2.5, "3", True, None):
        with pytest.raises(NumeroInvalidoError):
            indice.agregar(malo, "x")
    assert indice.cantidad() == 0


def test_muchos_numeros():
    """CA-06: con 10 000 números consecutivos, cada uno se encuentra con su propio elemento."""
    indice = Indice()
    for numero in range(1, 10001):
        indice.agregar(numero, f"comentario {numero}")
    assert indice.cantidad() == 10000
    for numero in range(1, 10001):
        assert indice.buscar(numero) == f"comentario {numero}"
    assert indice.existe(10001) is False


def test_cantidad():
    """CA-07: la cantidad empieza en 0, sube de uno en uno y no cambia con los errores."""
    indice = Indice()
    assert indice.cantidad() == 0
    indice.agregar(1, "a")
    assert indice.cantidad() == 1
    indice.agregar(2, "b")
    assert indice.cantidad() == 2
    with pytest.raises(NumeroRepetidoError):
        indice.agregar(2, "c")
    with pytest.raises(NumeroInvalidoError):
        indice.agregar(0, "d")
    assert indice.cantidad() == 2


def test_indice_vacio():
    """CA-08: en un índice vacío buscar lanza error y existe dice False."""
    indice = Indice()
    with pytest.raises(ComentarioNoEncontradoError):
        indice.buscar(1)
    assert indice.existe(1) is False


def test_numeros_salteados():
    """CA-09: números que no son consecutivos también se encuentran, aunque sean muchos."""
    indice = Indice()
    for numero in (5, 500, 99999):
        indice.agregar(numero, f"c{numero}")
    assert indice.buscar(5) == "c5"
    assert indice.buscar(500) == "c500"
    assert indice.buscar(99999) == "c99999"
    assert indice.cantidad() == 3

    # Muchos números saltados: obligan a la tabla a agrandarse varias veces
    # con números más grandes que su tamaño (el caso difícil de reubicar).
    otro = Indice()
    for numero in range(7, 7001, 7):          # 7, 14, 21, ... 7000
        otro.agregar(numero, f"c{numero}")
    assert otro.cantidad() == 1000
    for numero in range(7, 7001, 7):
        assert otro.buscar(numero) == f"c{numero}"
    assert otro.existe(8) is False


# ---------- Verificaciones del plan (forma y costo) ----------

def test_plan_cadenas_cortas():
    """PLAN-01: con 10 000 números consecutivos la cadena más larga mide 3 o menos."""
    indice = Indice()
    for numero in range(1, 10001):
        indice.agregar(numero, numero)
    assert indice._cadena_mas_larga() <= 3


def test_plan_numeros_que_chocan():
    """PLAN-02: números que caen en el mismo casillero (1, 9, 17, 25 con 8 casilleros) se encuentran todos."""
    indice = Indice()
    for numero in (1, 9, 17, 25):
        indice.agregar(numero, f"c{numero}")
    assert indice._tamano == 8
    assert indice._cadena_mas_larga() == 4      # los cuatro quedaron juntos
    for numero in (1, 9, 17, 25):
        assert indice.buscar(numero) == f"c{numero}"


def test_plan_se_agranda():
    """PLAN-03: la tabla se agranda al pasar la carga máxima y no se pierde ningún número."""
    indice = Indice()
    for numero in range(1, 7):                  # 6 números caben en 8 casilleros
        indice.agregar(numero, numero)
    assert indice._tamano == 8
    indice.agregar(7, 7)                        # el séptimo pasa de 0,75: se agranda
    assert indice._tamano == 16
    for numero in range(1, 8):
        assert indice.buscar(numero) == numero
    assert indice.cantidad() == 7
