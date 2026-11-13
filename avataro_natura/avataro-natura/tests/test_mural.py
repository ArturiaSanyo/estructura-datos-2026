"""Pruebas del sistema (Mural): comentarios + reportes + moderación.

Cada docstring dice qué criterio del sistema verifica (ver
specs/99-sistema/spec.md).
"""

import pytest

from estructuras.errores import (
    ComentarioNoEncontradoError,
    NoHayReportesError,
)
from mural import Mural


def test_reportar_existente():
    """CS-02: reportar un comentario que existe deja un reporte pendiente."""
    mural = Mural()
    mural.comentar("Ana", "Hola")
    numero = mural.reportar(1, "Luis", "Es ofensivo")
    assert numero == 1
    assert mural.cantidad_reportes() == 1


def test_reportar_inexistente():
    """CS-03: reportar un comentario que no existe lanza error y no deja reporte."""
    mural = Mural()
    mural.comentar("Ana", "Hola")
    with pytest.raises(ComentarioNoEncontradoError):
        mural.reportar(99, "Luis", "Motivo")
    with pytest.raises(ComentarioNoEncontradoError):
        mural.reportar(0, "Luis", "Motivo")
    assert mural.cantidad_reportes() == 0


def test_reportar_orden_de_errores():
    """CS-04: si el comentario no existe y los datos están vacíos, gana ComentarioNoEncontradoError."""
    mural = Mural()
    with pytest.raises(ComentarioNoEncontradoError):
        mural.reportar(99, "", "")


def test_atender_y_ocultar():
    """CS-05: atender un reporte pidiendo ocultar deja el aviso en el hilo."""
    mural = Mural()
    mural.comentar("Ana", "Texto ofensivo")      # 1
    mural.responder(1, "Luis", "Estoy de acuerdo con reportarlo")  # 2
    mural.reportar(1, "Luis", "Ofensivo")
    reporte = mural.atender_reporte(True)
    assert reporte.numero_comentario == 1
    assert mural.cantidad_reportes() == 0
    assert mural.ver_hilo() == (
        "#1 [comentario oculto por la administración]\n"
        "  #2 Luis: Estoy de acuerdo con reportarlo"
    )


def test_atender_sin_ocultar():
    """CS-06: atender un reporte pidiendo no ocultar deja el hilo igual."""
    mural = Mural()
    mural.comentar("Ana", "Comentario normal")
    mural.reportar(1, "Luis", "No me gustó")
    antes = mural.ver_hilo()
    mural.atender_reporte(False)
    assert mural.ver_hilo() == antes
    assert mural.cantidad_reportes() == 0


def test_reportes_en_orden_de_llegada():
    """CS-07: los reportes se atienden en el orden en que llegaron."""
    mural = Mural()
    mural.comentar("Ana", "Uno")       # 1
    mural.comentar("Luis", "Dos")      # 2
    mural.comentar("Marta", "Tres")    # 3
    mural.reportar(3, "Pedro", "A")
    mural.reportar(1, "Pedro", "B")
    mural.reportar(2, "Pedro", "C")
    assert mural.atender_reporte(False).numero_comentario == 3
    assert mural.atender_reporte(False).numero_comentario == 1
    assert mural.atender_reporte(False).numero_comentario == 2


def test_atender_sin_reportes():
    """CS-08: atender sin reportes pendientes lanza NoHayReportesError."""
    mural = Mural()
    mural.comentar("Ana", "Hola")
    with pytest.raises(NoHayReportesError):
        mural.atender_reporte(True)
    with pytest.raises(NoHayReportesError):
        mural.ver_siguiente_reporte()
