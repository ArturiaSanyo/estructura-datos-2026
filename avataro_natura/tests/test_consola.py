"""Pruebas del programa de consola (main.py).

Para probar el menú sin que nadie escriba, "engañamos" a input() con
una lista de respuestas preparadas y guardamos lo que el programa imprime.
"""

import io
from contextlib import redirect_stdout
from unittest.mock import patch

import main as programa


def ejecutar_menu(respuestas):
    """Corre el programa con esas respuestas y devuelve todo lo que imprimió."""
    salida = io.StringIO()
    with patch("builtins.input", side_effect=respuestas):
        with redirect_stdout(salida):
            programa.main()
    return salida.getvalue()


def test_error_no_detiene_el_menu():
    """CS-01: un error muestra un mensaje y el menú sigue funcionando."""
    salida = ejecutar_menu([
        "1", "Ana", "Hola",              # comentario #1 correcto
        "2", "99", "Luis", "Hola",       # padre que no existe
        "2", "1", "Luis", "",            # texto vacío
        "4", "50", "Luis", "Motivo",     # reportar comentario que no existe
        "5",                             # revisar sin reportes
        "1", "Marta", "Sigo aquí",       # el menú siguió: comentario #2
        "0",
    ])
    assert "No se pudo: No existe el comentario #99" in salida
    assert "No se pudo: El texto no puede estar vacío" in salida
    assert "No se pudo: No existe el comentario #50" in salida
    assert "No se pudo: No hay reportes pendientes" in salida
    assert "Comentario #2 publicado." in salida
    assert "¡Hasta pronto!" in salida


def test_numero_con_letras():
    """CS-10: si el número se escribe con letras, se avisa y el menú sigue."""
    salida = ejecutar_menu(["2", "abc", "4", "xyz", "0"])
    assert salida.count("Debes escribir un número.") == 2
    assert "¡Hasta pronto!" in salida


def test_salir():
    """CS-11: la opción 0 termina el programa con un saludo."""
    salida = ejecutar_menu(["0"])
    assert "¡Hasta pronto!" in salida


def test_respuesta_no_valida_deja_el_reporte():
    """CS-12: una respuesta que no es s ni n deja el reporte pendiente."""
    salida = ejecutar_menu([
        "1", "Ana", "Hola",
        "4", "1", "Luis", "Motivo",
        "5", "quizás",                   # ni s ni n
        "0",
    ])
    assert "Respuesta no válida. El reporte sigue pendiente." in salida
    assert "pendientes: 1" in salida.split("Respuesta no válida")[1]


def test_flujo_completo_consola():
    """CS-09: comentar, responder, reportar, revisar y ocultar desde el menú."""
    salida = ejecutar_menu([
        "1", "Ana", "Comentario ofensivo",       # 1
        "2", "1", "Luis", "Estoy de acuerdo",    # 2, respuesta al 1
        "4", "1", "Marta", "Es ofensivo",        # reporte 1
        "5", "s",                                # la administración oculta
        "3",                                     # ver el hilo
        "0",
    ])
    despues = salida.split("Comentario ocultado. Reporte atendido.")[1]
    assert "#1 [comentario oculto por la administración]" in despues
    assert "  #2 Luis: Estoy de acuerdo" in despues
    assert "Comentario ofensivo" not in despues
