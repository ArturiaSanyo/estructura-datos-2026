"""Pruebas de los Reportes (Componente 02). Cada docstring dice qué criterio verifica."""

import pytest

from estructuras.errores import NoHayReportesError, ReporteInvalidoError
from estructuras.reportes import Reportes


def test_reportar_primero():
    """CA-01: el primer reporte recibe el número 1 y la cantidad pasa a 1."""
    reportes = Reportes()
    numero = reportes.reportar(4, "Luis", "Es ofensivo")
    assert numero == 1
    assert reportes.cantidad() == 1


def test_atender_en_orden():
    """CA-02: los reportes se atienden en el mismo orden en que se hicieron."""
    reportes = Reportes()
    reportes.reportar(7, "Ana", "Primero")
    reportes.reportar(3, "Luis", "Segundo")
    reportes.reportar(5, "Marta", "Tercero")
    assert reportes.atender().numero == 1
    assert reportes.atender().numero == 2
    assert reportes.atender().numero == 3
    assert reportes.cantidad() == 0


def test_atender_vacio():
    """CA-03: atender sin reportes pendientes lanza NoHayReportesError."""
    reportes = Reportes()
    with pytest.raises(NoHayReportesError):
        reportes.atender()


def test_ver_siguiente():
    """CA-04: ver_siguiente devuelve el más antiguo sin sacarlo."""
    reportes = Reportes()
    reportes.reportar(1, "Ana", "Uno")
    reportes.reportar(2, "Luis", "Dos")
    visto = reportes.ver_siguiente()
    assert visto.numero == 1
    assert reportes.cantidad() == 2           # no se sacó nada
    assert reportes.ver_siguiente() is visto  # mirar otra vez da el mismo
    assert reportes.atender() is visto        # y atender entrega ese mismo


def test_ver_siguiente_vacio():
    """CA-05: ver_siguiente sin reportes pendientes lanza NoHayReportesError."""
    reportes = Reportes()
    with pytest.raises(NoHayReportesError):
        reportes.ver_siguiente()


def test_reportante_vacio():
    """CA-06: un reportante vacío o de solo espacios lanza ReporteInvalidoError."""
    reportes = Reportes()
    with pytest.raises(ReporteInvalidoError):
        reportes.reportar(1, "", "Motivo")
    with pytest.raises(ReporteInvalidoError):
        reportes.reportar(1, "   ", "Motivo")
    assert reportes.cantidad() == 0


def test_motivo_vacio():
    """CA-07: un motivo vacío o de solo espacios lanza ReporteInvalidoError."""
    reportes = Reportes()
    with pytest.raises(ReporteInvalidoError):
        reportes.reportar(1, "Ana", "")
    with pytest.raises(ReporteInvalidoError):
        reportes.reportar(1, "Ana", "    ")
    assert reportes.cantidad() == 0


def test_numero_comentario_invalido():
    """CA-08: un número de comentario que no sea entero mayor que 0 lanza ReporteInvalidoError."""
    reportes = Reportes()
    for malo in (0, -3, 2.5, "7", True, None):
        with pytest.raises(ReporteInvalidoError):
            reportes.reportar(malo, "Ana", "Motivo")
    assert reportes.cantidad() == 0


def test_error_no_consume_numero():
    """CA-09: un reporte fallido no gasta número; el siguiente no se salta."""
    reportes = Reportes()
    reportes.reportar(1, "Ana", "Uno")             # reporte 1
    with pytest.raises(ReporteInvalidoError):
        reportes.reportar(1, "", "Sin nombre")
    with pytest.raises(ReporteInvalidoError):
        reportes.reportar(0, "Luis", "Número malo")
    assert reportes.reportar(2, "Marta", "Dos") == 2


def test_reportar_despues_de_vaciar():
    """CA-10: tras atender todos se puede volver a reportar; el orden y el número siguen bien."""
    reportes = Reportes()
    reportes.reportar(1, "Ana", "Uno")
    reportes.reportar(2, "Luis", "Dos")
    reportes.atender()
    reportes.atender()
    assert reportes.cantidad() == 0
    assert reportes.reportar(3, "Marta", "Tres") == 3   # el número continúa
    assert reportes.reportar(4, "Pedro", "Cuatro") == 4
    assert reportes.atender().numero == 3
    assert reportes.atender().numero == 4
    with pytest.raises(NoHayReportesError):
        reportes.atender()


def test_mismo_comentario_dos_veces():
    """CA-11: reportar dos veces el mismo comentario genera dos reportes separados."""
    reportes = Reportes()
    primero = reportes.reportar(5, "Ana", "Ofensivo")
    segundo = reportes.reportar(5, "Ana", "Ofensivo otra vez")
    assert primero == 1
    assert segundo == 2
    assert reportes.cantidad() == 2
    assert reportes.atender().numero == 1
    assert reportes.atender().numero == 2


def test_reporte_trae_sus_datos():
    """CA-12: el reporte atendido trae los cuatro datos tal como se registraron."""
    reportes = Reportes()
    reportes.reportar(8, "Luisa", "Insulta a otra persona")
    reporte = reportes.atender()
    assert reporte.numero == 1
    assert reporte.numero_comentario == 8
    assert reporte.reportante == "Luisa"
    assert reporte.motivo == "Insulta a otra persona"
