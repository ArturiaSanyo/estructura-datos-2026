"""Reportes de comentarios inadecuados (Componente 02).

Estructura elegida: cola enlazada con referencias al frente y al final.
Está explicada en specs/02-reportes/plan.md

La idea, con una imagen:
    Es la fila de un banco. Quien llega se pone al final de la fila, y
    se atiende siempre a quien está al frente. Cada persona de la fila
    sabe quién está detrás de ella. El programa recuerda solo dos cosas:
    quién va primero (_frente) y quién va último (_final).
"""

from estructuras.errores import NoHayReportesError, ReporteInvalidoError


def _es_texto_con_contenido(valor):
    """True si 'valor' es un texto que tiene algo más que espacios."""
    return isinstance(valor, str) and valor.strip() != ""


class Reporte:
    """Un reporte: cuatro datos más la referencia al reporte que sigue en la fila."""

    def __init__(self, numero, numero_comentario, reportante, motivo):
        self.numero = numero                        # número de este reporte
        self.numero_comentario = numero_comentario  # comentario que se reporta
        self.reportante = reportante                # quién reporta
        self.motivo = motivo                        # por qué lo reporta
        self.siguiente = None                       # el reporte que llegó después


class Reportes:
    """La fila de reportes pendientes: el más antiguo sale primero."""

    def __init__(self):
        self._frente = None          # el reporte más antiguo (el que sigue en salir)
        self._final = None           # el reporte más nuevo (el último de la fila)
        self._cantidad = 0
        self._ultimo_numero = 0

    # ---------- operaciones públicas ----------

    def reportar(self, numero_comentario, reportante, motivo):
        """CA-01, CA-06, CA-07, CA-08, CA-09, CA-10, CA-11: agrega un reporte.

        Devuelve el número del reporte nuevo.
        Lanza ReporteInvalidoError si algún dato no es válido.
        Tiempo: O(1). Espacio: O(1).
        """
        self._validar(numero_comentario, reportante, motivo)

        # Solo gastamos un número cuando ya sabemos que no hubo error (CA-09)
        self._ultimo_numero += 1
        nuevo = Reporte(self._ultimo_numero, numero_comentario, reportante, motivo)

        if self._final is None:
            self._frente = nuevo               # la fila estaba vacía: es el primero
        else:
            self._final.siguiente = nuevo      # se pega detrás del último
        self._final = nuevo                    # y ahora él es el último

        self._cantidad += 1
        return nuevo.numero

    def ver_siguiente(self):
        """CA-04, CA-05: devuelve el reporte más antiguo SIN sacarlo.

        Lanza NoHayReportesError si no hay reportes pendientes.
        Tiempo: O(1). Espacio: O(1).
        """
        if self._frente is None:
            raise NoHayReportesError("No hay reportes pendientes")
        return self._frente

    def atender(self):
        """CA-02, CA-03, CA-10, CA-12: saca y devuelve el reporte más antiguo.

        Lanza NoHayReportesError si no hay reportes pendientes.
        Tiempo: O(1). Espacio: O(1).
        """
        if self._frente is None:
            raise NoHayReportesError("No hay reportes pendientes")

        atendido = self._frente
        self._frente = atendido.siguiente    # el que venía detrás pasa al frente
        if self._frente is None:
            self._final = None               # la fila quedó vacía (CA-10)
        atendido.siguiente = None            # el reporte entregado ya no apunta a la fila

        self._cantidad -= 1
        return atendido

    def cantidad(self):
        """INV-01: cuántos reportes hay pendientes. Tiempo: O(1)."""
        return self._cantidad

    # ---------- funciones internas (empiezan con _) ----------

    def _validar(self, numero_comentario, reportante, motivo):
        """Lanza ReporteInvalidoError si algún dato no es válido."""
        # "type(...) is int" evita que True o False pasen como el número 1 o 0
        if type(numero_comentario) is not int or numero_comentario <= 0:
            raise ReporteInvalidoError(
                "El número del comentario debe ser un entero mayor que 0"
            )
        if not _es_texto_con_contenido(reportante):
            raise ReporteInvalidoError("Quien reporta no puede estar vacío")
        if not _es_texto_con_contenido(motivo):
            raise ReporteInvalidoError("El motivo no puede estar vacío")
