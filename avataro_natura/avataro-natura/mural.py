"""El mural de una actividad: junta el hilo de comentarios con los reportes.

Aquí está la "pegadura" entre los componentes (ver specs/99-sistema/spec.md).
Esta clase NO guarda datos por su cuenta: solo coordina al Hilo (componente
01, que usa por dentro el Índice, componente 03) y a los Reportes
(componente 02).
"""

from estructuras.errores import ComentarioNoEncontradoError
from estructuras.hilo import Hilo
from estructuras.reportes import Reportes


class Mural:
    """Mural de opiniones: comentarios, respuestas, reportes y moderación."""

    def __init__(self):
        self._hilo = Hilo()
        self._reportes = Reportes()

    # ---------- lo que hace cualquier persona de la comunidad ----------

    def comentar(self, autor, texto):
        """Publica un comentario principal. Devuelve su número."""
        return self._hilo.comentar(autor, texto)

    def responder(self, numero_padre, autor, texto):
        """Responde a un comentario. Devuelve el número de la respuesta."""
        return self._hilo.responder(numero_padre, autor, texto)

    def ver_hilo(self):
        """Devuelve la conversación completa como texto."""
        return self._hilo.mostrar()

    def cantidad_comentarios(self):
        """Cuántos comentarios hay en el mural."""
        return self._hilo.cantidad()

    def reportar(self, numero_comentario, reportante, motivo):
        """CS-02, CS-03, CS-04: reporta un comentario. Devuelve el número del reporte.

        Primero se comprueba que el comentario exista; si no, se lanza
        ComentarioNoEncontradoError y no queda ningún reporte.
        """
        if not self._hilo.existe(numero_comentario):
            raise ComentarioNoEncontradoError(
                f"No existe el comentario #{numero_comentario}"
            )
        return self._reportes.reportar(numero_comentario, reportante, motivo)

    # ---------- lo que hace la administración ----------

    def cantidad_reportes(self):
        """Cuántos reportes esperan ser revisados."""
        return self._reportes.cantidad()

    def ver_siguiente_reporte(self):
        """Devuelve el reporte más antiguo sin atenderlo (lanza NoHayReportesError)."""
        return self._reportes.ver_siguiente()

    def atender_reporte(self, ocultar_comentario):
        """CS-05, CS-06, CS-07, CS-08: atiende el reporte más antiguo.

        Si ocultar_comentario es True, el comentario reportado queda oculto;
        si es False, se deja como está. Devuelve el reporte atendido.
        """
        reporte = self._reportes.atender()      # lanza NoHayReportesError si no hay
        if ocultar_comentario:
            self._hilo.ocultar(reporte.numero_comentario)
        return reporte
