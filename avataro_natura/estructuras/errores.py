"""Errores propios del proyecto Avataro Natura.

Un "error propio" es un aviso con nombre específico. En lugar de que el
programa se caiga con un mensaje confuso, lanzamos un error con un nombre
que dice exactamente qué salió mal, y quien usa el programa puede
atraparlo y mostrar un mensaje amable.

Los errores forman una "familia": los de comentarios y los de reportes
heredan de AvataroError. Así el menú puede atrapar a toda la familia
con una sola línea.
"""


class AvataroError(Exception):
    """Error base: todos los errores de este proyecto heredan de este."""


# ---------- errores de comentarios (hilo e índice) ----------

class ComentarioError(AvataroError):
    """Error base de los comentarios."""


class ComentarioInvalidoError(ComentarioError):
    """El autor o el texto del comentario están vacíos."""


class ComentarioNoEncontradoError(ComentarioError):
    """No existe un comentario con ese número."""


class ProfundidadExcedidaError(ComentarioError):
    """Se intentó responder más allá del nivel máximo permitido."""


class NumeroInvalidoError(ComentarioError):
    """El número no es un entero mayor que 0 (lo usa el índice)."""


class NumeroRepetidoError(ComentarioError):
    """Ese número ya estaba guardado en el índice."""


# ---------- errores de reportes ----------

class ReporteError(AvataroError):
    """Error base de los reportes."""


class ReporteInvalidoError(ReporteError):
    """Faltan datos del reporte o el número del comentario no es válido."""


class NoHayReportesError(ReporteError):
    """No hay reportes pendientes."""
