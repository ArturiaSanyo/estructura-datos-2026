"""Índice de comentarios (Componente 03).

Estructura elegida: tabla de dispersión (hash) con encadenamiento.
Está explicada en specs/03-indice-comentarios/plan.md

La idea, con una imagen:
    Es un archivador con casilleros numerados. Para guardar el comentario
    número 13 en un archivador de 8 casilleros, hacemos la cuenta
    13 % 8 = 5 (el resto de dividir 13 entre 8) y lo dejamos en el
    casillero 5. Para buscarlo, repetimos la cuenta y abrimos ese casillero.
    Si en un mismo casillero caen varios comentarios, quedan unidos en una
    cadena corta, uno detrás de otro.
"""

from estructuras.errores import (
    ComentarioNoEncontradoError,
    NumeroInvalidoError,
    NumeroRepetidoError,
)

TAMANO_INICIAL = 8   # con cuántos casilleros empieza el archivador


def es_numero_valido(numero):
    """Dice si 'numero' es un entero mayor que 0.

    Usamos "type(numero) is int" y no "isinstance" porque en Python
    True y False cuentan como si fueran los números 1 y 0, y no
    queremos que se cuelen como números de comentario.
    """
    return type(numero) is int and numero > 0


class NodoIndice:
    """Una pareja "número -> elemento", unida a la siguiente de su casillero."""

    def __init__(self, numero, elemento):
        self.numero = numero
        self.elemento = elemento
        self.siguiente = None   # el siguiente nodo del mismo casillero


class Indice:
    """Guarda parejas "número -> elemento" y las encuentra muy rápido."""

    def __init__(self):
        # Esta es la ÚNICA lista de Python del componente. Solo hace de
        # "fila de casilleros" con tamaño fijo: nunca le agregamos ni le
        # quitamos elementos (ver la justificación en el plan.md).
        self._tamano = TAMANO_INICIAL
        self._casilleros = [None] * self._tamano   # None = casillero vacío
        self._cantidad = 0

    # ---------- operaciones públicas ----------

    def agregar(self, numero, elemento):
        """CA-01, CA-04, CA-05, CA-06, CA-07, CA-09: guarda una pareja.

        Lanza NumeroInvalidoError si el número no es un entero mayor que 0,
        y NumeroRepetidoError si el número ya estaba guardado.
        Tiempo: O(1) promedio (de vez en cuando la tabla se agranda).
        Espacio: O(1).
        """
        if not es_numero_valido(numero):
            raise NumeroInvalidoError(
                f"El número {numero!r} no es un entero mayor que 0"
            )
        if self._buscar_nodo(numero) is not None:
            raise NumeroRepetidoError(f"El número {numero} ya está en el índice")

        # Si con este número nuevo el archivador quedaría muy lleno,
        # primero lo cambiamos por uno del doble de tamaño.
        if (self._cantidad + 1) * 4 > self._tamano * 3:
            self._agrandar()

        posicion = numero % self._tamano          # la cuenta que elige el casillero
        nuevo = NodoIndice(numero, elemento)
        nuevo.siguiente = self._casilleros[posicion]   # lo que había queda detrás
        self._casilleros[posicion] = nuevo             # el nuevo pasa al inicio
        self._cantidad += 1

    def buscar(self, numero):
        """CA-01, CA-03, CA-08: devuelve el elemento guardado con ese número.

        Lanza ComentarioNoEncontradoError si el número no está.
        Tiempo: O(1) promedio. Espacio: O(1).
        """
        nodo = self._buscar_nodo(numero)
        if nodo is None:
            raise ComentarioNoEncontradoError(f"No existe el comentario #{numero}")
        return nodo.elemento

    def existe(self, numero):
        """CA-02, CA-08: True si el número está guardado, False si no.

        Tiempo: O(1) promedio. Espacio: O(1).
        """
        return self._buscar_nodo(numero) is not None

    def cantidad(self):
        """INV-01, CA-07: cuántos números hay guardados. Tiempo: O(1)."""
        return self._cantidad

    # ---------- funciones internas (empiezan con _) ----------

    def _buscar_nodo(self, numero):
        """Devuelve el nodo con ese número, o None si no está."""
        # Primero validamos: si "numero" fuera un texto, la cuenta del
        # casillero daría un error raro. Un número no válido nunca está.
        if not es_numero_valido(numero):
            return None

        posicion = numero % self._tamano
        nodo = self._casilleros[posicion]
        while nodo is not None:           # recorremos la cadena del casillero
            if nodo.numero == numero:
                return nodo
            nodo = nodo.siguiente
        return None

    def _agrandar(self):
        """Cambia el archivador por uno del doble de tamaño.

        Cada nodo se pasa al casillero que le toca en el archivador nuevo
        (la cuenta cambia porque ahora hay más casilleros). No se crean
        nodos nuevos: solo se cambian de lugar los que ya existen.
        Tiempo: O(n). Espacio: O(n) por la fila nueva de casilleros.
        """
        casilleros_viejos = self._casilleros
        self._tamano = self._tamano * 2
        self._casilleros = [None] * self._tamano

        for casillero in casilleros_viejos:
            nodo = casillero
            while nodo is not None:
                siguiente = nodo.siguiente      # lo guardamos antes de mover el nodo
                posicion = nodo.numero % self._tamano
                nodo.siguiente = self._casilleros[posicion]
                self._casilleros[posicion] = nodo
                nodo = siguiente

    def _cadena_mas_larga(self):
        """Largo de la cadena más larga. Solo la usan las pruebas (PLAN-01)."""
        mayor = 0
        for casillero in self._casilleros:
            largo = 0
            nodo = casillero
            while nodo is not None:
                largo += 1
                nodo = nodo.siguiente
            if largo > mayor:
                mayor = largo
        return mayor
