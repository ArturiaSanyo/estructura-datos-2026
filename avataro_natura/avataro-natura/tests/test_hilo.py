"""Pruebas del Hilo de comentarios. Cada docstring dice qué criterio verifica."""

import pytest

from estructuras.errores import (
    ComentarioInvalidoError,
    ComentarioNoEncontradoError,
    ProfundidadExcedidaError,
)
from estructuras.hilo import Hilo


def test_comentar_primero():
    """CA-01: el primer comentario recibe el número 1 y el hilo cuenta 1."""
    hilo = Hilo()
    numero = hilo.comentar("Ana", "Hola a todos")
    assert numero == 1
    assert hilo.cantidad() == 1


def test_comentarios_en_orden():
    """CA-02: dos comentarios principales salen en el orden en que se escribieron."""
    hilo = Hilo()
    assert hilo.comentar("Ana", "Primero") == 1
    assert hilo.comentar("Luis", "Segundo") == 2
    assert hilo.mostrar() == "#1 Ana: Primero\n#2 Luis: Segundo"


def test_respuesta_queda_bajo_padre():
    """CA-03: una respuesta queda debajo del comentario al que responde."""
    hilo = Hilo()
    hilo.comentar("Ana", "Sembremos árboles")      # 1
    hilo.comentar("Luis", "Yo llevo agua")          # 2
    numero = hilo.responder(1, "Marta", "Cuenten conmigo")
    assert numero == 3
    assert hilo.mostrar() == (
        "#1 Ana: Sembremos árboles\n"
        "  #3 Marta: Cuenten conmigo\n"
        "#2 Luis: Yo llevo agua"
    )


def test_hilo_en_preorden():
    """CA-04: cada comentario aparece después de su padre, con sangría por nivel."""
    hilo = Hilo()
    hilo.comentar("Ana", "A")             # 1
    hilo.responder(1, "Luis", "B")        # 2
    hilo.responder(2, "Marta", "C")       # 3
    hilo.responder(1, "Pedro", "D")       # 4
    assert hilo.mostrar() == (
        "#1 Ana: A\n"
        "  #2 Luis: B\n"
        "    #3 Marta: C\n"
        "  #4 Pedro: D"
    )


def test_respuestas_en_orden():
    """CA-05: las respuestas de un mismo comentario salen en orden cronológico."""
    hilo = Hilo()
    hilo.comentar("Ana", "Pregunta")
    hilo.responder(1, "Luis", "Uno")
    hilo.responder(1, "Marta", "Dos")
    hilo.responder(1, "Pedro", "Tres")
    assert hilo.mostrar() == (
        "#1 Ana: Pregunta\n"
        "  #2 Luis: Uno\n"
        "  #3 Marta: Dos\n"
        "  #4 Pedro: Tres"
    )


def test_responder_inexistente():
    """CA-06: responder a un comentario que no existe lanza ComentarioNoEncontradoError."""
    hilo = Hilo()
    hilo.comentar("Ana", "Hola")
    with pytest.raises(ComentarioNoEncontradoError):
        hilo.responder(99, "Luis", "¿Hay alguien?")
    with pytest.raises(ComentarioNoEncontradoError):
        hilo.responder(0, "Luis", "El cero tampoco existe")
    assert hilo.cantidad() == 1


def test_texto_vacio():
    """CA-07: un texto vacío o solo con espacios lanza ComentarioInvalidoError."""
    hilo = Hilo()
    with pytest.raises(ComentarioInvalidoError):
        hilo.comentar("Ana", "")
    with pytest.raises(ComentarioInvalidoError):
        hilo.comentar("Ana", "    ")
    assert hilo.cantidad() == 0


def test_autor_vacio():
    """CA-08: un autor vacío o solo con espacios lanza ComentarioInvalidoError."""
    hilo = Hilo()
    with pytest.raises(ComentarioInvalidoError):
        hilo.comentar("", "Hola")
    with pytest.raises(ComentarioInvalidoError):
        hilo.comentar("   ", "Hola")
    assert hilo.cantidad() == 0


def test_profundidad_maxima():
    """CA-09: responder a un comentario del nivel 5 lanza ProfundidadExcedidaError."""
    hilo = Hilo()
    numero = hilo.comentar("Ana", "nivel 1")
    for nivel in range(2, 6):                       # niveles 2, 3, 4 y 5
        numero = hilo.responder(numero, "Ana", f"nivel {nivel}")
    assert hilo.cantidad() == 5
    with pytest.raises(ProfundidadExcedidaError):
        hilo.responder(numero, "Ana", "nivel 6")
    assert hilo.cantidad() == 5


def test_mostrar_vacio():
    """CA-10: mostrar un hilo sin comentarios devuelve texto vacío y no falla."""
    hilo = Hilo()
    assert hilo.mostrar() == ""
    assert hilo.cantidad() == 0


def test_error_no_consume_numero():
    """CA-11: un intento fallido no gasta un número; el siguiente no se salta."""
    hilo = Hilo()
    hilo.comentar("Ana", "Hola")                    # 1
    with pytest.raises(ComentarioInvalidoError):
        hilo.comentar("Luis", "")
    with pytest.raises(ComentarioNoEncontradoError):
        hilo.responder(50, "Luis", "Hola")
    assert hilo.comentar("Marta", "Aquí sigo") == 2


def test_orden_de_errores():
    """CA-12: si hay texto vacío y padre inexistente, gana ComentarioInvalidoError."""
    hilo = Hilo()
    with pytest.raises(ComentarioInvalidoError):
        hilo.responder(99, "Ana", "")


# ---------- Agregadas con la spec 1.1 (existe y ocultar) ----------

def test_existe():
    """CA-13: existe dice True para un comentario publicado y False para el resto."""
    hilo = Hilo()
    assert hilo.existe(1) is False          # hilo vacío
    hilo.comentar("Ana", "Hola")            # 1
    hilo.responder(1, "Luis", "Buenas")     # 2
    assert hilo.existe(1) is True
    assert hilo.existe(2) is True
    assert hilo.existe(3) is False          # todavía no existe
    assert hilo.existe(0) is False          # la raíz falsa no cuenta
    assert hilo.existe(-1) is False
    assert hilo.existe("1") is False        # un texto no es un número
    assert hilo.existe(True) is False       # True no cuenta como el número 1
    assert hilo.cantidad() == 2


def test_ocultar_comentario():
    """CA-14: un comentario oculto muestra el aviso; sus respuestas siguen visibles."""
    hilo = Hilo()
    hilo.comentar("Ana", "Comentario ofensivo")     # 1
    hilo.responder(1, "Luis", "No estoy de acuerdo")  # 2
    hilo.comentar("Marta", "Otro comentario")       # 3
    hilo.ocultar(1)
    assert hilo.mostrar() == (
        "#1 [comentario oculto por la administración]\n"
        "  #2 Luis: No estoy de acuerdo\n"
        "#3 Marta: Otro comentario"
    )
    assert hilo.cantidad() == 3             # ocultar no borra nada


def test_ocultar_inexistente():
    """CA-15: ocultar un número que no existe lanza ComentarioNoEncontradoError."""
    hilo = Hilo()
    hilo.comentar("Ana", "Hola")
    antes = hilo.mostrar()
    with pytest.raises(ComentarioNoEncontradoError):
        hilo.ocultar(99)
    with pytest.raises(ComentarioNoEncontradoError):
        hilo.ocultar(0)
    assert hilo.mostrar() == antes
    assert hilo.cantidad() == 1


def test_ocultar_dos_veces():
    """CA-16: ocultar dos veces el mismo comentario no falla y sigue oculto."""
    hilo = Hilo()
    hilo.comentar("Ana", "Hola")
    hilo.ocultar(1)
    hilo.ocultar(1)
    assert hilo.mostrar() == "#1 [comentario oculto por la administración]"


def test_responder_a_oculto():
    """CA-17: se puede responder a un comentario oculto."""
    hilo = Hilo()
    hilo.comentar("Ana", "Hola")
    hilo.ocultar(1)
    numero = hilo.responder(1, "Luis", "Sigo hablando")
    assert numero == 2
    assert hilo.mostrar() == (
        "#1 [comentario oculto por la administración]\n"
        "  #2 Luis: Sigo hablando"
    )
