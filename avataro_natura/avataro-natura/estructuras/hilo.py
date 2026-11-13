"""Hilo de comentarios de una actividad (Componente 01).

Estructura elegida: árbol general, representado con
"primer hijo / siguiente hermano". Está explicada en
specs/01-hilo-comentarios/plan.md

La idea, con una imagen:
    Una conversación es como un árbol. Cada comentario puede tener
    respuestas (sus "hijos"), y cada respuesta puede tener más respuestas.
    Para que cada comentario sepa quiénes son sus respuestas, guarda solo
    dos cosas: cuál es su primera respuesta (primer_hijo) y cuál es su
    última (ultimo_hijo). Y cada respuesta sabe cuál es la siguiente
    respuesta del mismo comentario (siguiente_hermano), formando una cadena.

Además, el hilo usa un Índice (Componente 03) para encontrar rápido
un comentario a partir de su número.
"""

from estructuras.errores import (
    ComentarioInvalidoError,
    ProfundidadExcedidaError,
)
from estructuras.indice import Indice

NIVEL_MAXIMO = 5  # el comentario principal es el nivel 1
AVISO_OCULTO = "[comentario oculto por la administración]"


class Nodo:
    """Un comentario dentro del hilo."""

    def __init__(self, numero, autor, texto, nivel):
        self.numero = numero
        self.autor = autor
        self.texto = texto
        self.nivel = nivel
        self.oculto = False             # True cuando la administración lo oculta
        self.primer_hijo = None         # primera respuesta
        self.ultimo_hijo = None         # última respuesta (para agregar rápido)
        self.siguiente_hermano = None   # el siguiente comentario del mismo nivel


class Hilo:
    """Conversación de una actividad: comentarios con respuestas anidadas."""

    def __init__(self):
        # La raíz es un comentario "falso" (número 0, nivel 0) que no se
        # muestra. Sirve para que los comentarios principales sean sus hijos
        # y no haya que tratarlos como un caso aparte.
        # La raíz NO se anota en el índice: por eso el número 0 "no existe".
        self._raiz = Nodo(0, "", "", 0)
        self._indice = Indice()
        self._cantidad = 0
        self._ultimo_numero = 0

    # ---------- operaciones públicas ----------

    def comentar(self, autor, texto):
        """CA-01, CA-02, CA-07, CA-08: agrega un comentario principal.

        Devuelve el número del comentario nuevo.
        Tiempo: O(1). Espacio: O(1).
        """
        self._validar(autor, texto)
        return self._agregar(self._raiz, autor, texto)

    def responder(self, numero_padre, autor, texto):
        """CA-03, CA-06, CA-09, CA-12, CA-17: responde al comentario numero_padre.

        Devuelve el número de la respuesta nueva.
        Tiempo: O(1) promedio, porque el índice encuentra al padre sin recorrer
        el hilo. Espacio: O(1).
        """
        self._validar(autor, texto)                # primero autor y texto...
        padre = self._encontrar(numero_padre)      # ...luego que el padre exista...
        return self._agregar(padre, autor, texto)  # ...y por último el nivel

    def existe(self, numero):
        """CA-13: True si hay un comentario con ese número, False si no.

        Tiempo: O(1) promedio. Espacio: O(1).
        """
        return self._indice.existe(numero)

    def ocultar(self, numero):
        """CA-14, CA-15, CA-16: oculta el comentario con ese número.

        El comentario no se borra: conserva su número y sus respuestas.
        Ocultar uno que ya estaba oculto no hace nada.
        Tiempo: O(1) promedio. Espacio: O(1).
        """
        comentario = self._encontrar(numero)   # lanza error si no existe
        comentario.oculto = True

    def mostrar(self):
        """CA-04, CA-05, CA-10, CA-14: devuelve el hilo como texto.

        Cada comentario aparece justo después de su padre, con dos espacios
        de sangría por cada nivel. Un hilo vacío devuelve "".
        Tiempo: O(n) comentarios visitados. Espacio: O(n) por el texto.
        """
        return self._recorrer(self._raiz)

    def cantidad(self):
        """INV-01: cuántos comentarios hay en el hilo. Tiempo: O(1)."""
        return self._cantidad

    # ---------- funciones internas (empiezan con _) ----------

    def _validar(self, autor, texto):
        """Lanza ComentarioInvalidoError si autor o texto están vacíos."""
        if not isinstance(autor, str) or autor.strip() == "":
            raise ComentarioInvalidoError("El autor no puede estar vacío")
        if not isinstance(texto, str) or texto.strip() == "":
            raise ComentarioInvalidoError("El texto no puede estar vacío")

    def _encontrar(self, numero):
        """Devuelve el comentario con ese número.

        Se lo pide al índice. Si no existe, el índice lanza
        ComentarioNoEncontradoError (así también el 0 resulta "no existe").
        """
        return self._indice.buscar(numero)

    def _agregar(self, padre, autor, texto):
        """Crea el comentario, lo pone como última respuesta del padre y lo anota en el índice."""
        if padre.nivel >= NIVEL_MAXIMO:
            raise ProfundidadExcedidaError(
                f"No se puede pasar del nivel {NIVEL_MAXIMO}"
            )

        # Solo gastamos un número cuando ya sabemos que no hubo error (CA-11)
        self._ultimo_numero += 1
        nuevo = Nodo(self._ultimo_numero, autor, texto, padre.nivel + 1)

        if padre.primer_hijo is None:
            padre.primer_hijo = nuevo               # es su primera respuesta
        else:
            padre.ultimo_hijo.siguiente_hermano = nuevo  # se pega al final
        padre.ultimo_hijo = nuevo

        self._indice.agregar(nuevo.numero, nuevo)   # lo anotamos en el índice
        self._cantidad += 1
        return nuevo.numero

    def _recorrer(self, nodo):
        """Recorrido en preorden: primero el comentario, luego sus respuestas.

        Esta función se llama a sí misma (recursión): para escribir las
        respuestas de un comentario, se pregunta lo mismo a cada respuesta.
        Como el nivel máximo es 5, nunca se llama a sí misma más de 6 veces
        seguidas, así que no hay riesgo de que se descontrole.
        """
        texto = ""
        hijo = nodo.primer_hijo
        while hijo is not None:           # una vuelta por cada respuesta del nodo
            sangria = "  " * (hijo.nivel - 1)
            if hijo.oculto:
                linea = f"{sangria}#{hijo.numero} {AVISO_OCULTO}"
            else:
                linea = f"{sangria}#{hijo.numero} {hijo.autor}: {hijo.texto}"

            if texto != "":
                texto += "\n"
            texto += linea

            respuestas = self._recorrer(hijo)   # las respuestas de este comentario
            if respuestas != "":
                texto += "\n" + respuestas

            hijo = hijo.siguiente_hermano
        return texto
