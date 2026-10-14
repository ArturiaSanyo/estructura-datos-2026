"""
cola_prioridad.py
-----------------
Aqui construimos DOS cosas desde cero (sin heapq ni deque):

1. Cola       -> una cola normal (FIFO: el primero que entra es el primero que sale).
2. ColaPrioridad -> una cola con TRES NIVELES: ALTA, MEDIA y BAJA.

PROBLEMA: si siempre llegan trabajos de prioridad ALTA, los de prioridad BAJA
nunca se atienden. A eso se le llama "espera indefinida" (inanicion).

SOLUCION (mecanismo documentado): ENVEJECIMIENTO
  Cada trabajo recuerda desde que momento esta esperando en su nivel.
  Si lleva esperando 'limite_espera' unidades de tiempo o mas, lo subimos
  un nivel (BAJA -> MEDIA, o MEDIA -> ALTA). Asi, tarde o temprano,
  hasta el trabajo mas humilde llega a ALTA y se atiende.

Si creas la ColaPrioridad con limite_espera=None, el envejecimiento se apaga
(sirve para comparar en simulacion.py).
"""

# Los tres niveles. Usamos numeros: mientras mas pequeno, mas importante.
ALTA = 0
MEDIA = 1
BAJA = 2
NOMBRES_NIVEL = ["ALTA", "MEDIA", "BAJA"]


# ---------------------------------------------------------------
# PARTE 1: la cola normal (hecha con nodos enlazados)
# ---------------------------------------------------------------
class NodoCola:
    """Una cajita que guarda un dato y apunta a la siguiente cajita."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    """Cola FIFO. 'frente' es quien sale primero, 'final' es quien entro ultimo."""

    def __init__(self):
        self.frente = None
        self.final = None
        self.cantidad = 0

    def esta_vacia(self):
        return self.cantidad == 0

    def encolar(self, dato):
        """Mete un dato al final de la cola."""
        nuevo = NodoCola(dato)
        if self.final is None:          # la cola estaba vacia
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self.cantidad += 1

    def desencolar(self):
        """Saca y devuelve el dato del frente."""
        if self.esta_vacia():
            raise IndexError("No se puede desencolar: la cola esta vacia")
        nodo = self.frente
        self.frente = nodo.siguiente
        if self.frente is None:         # la cola quedo vacia
            self.final = None
        self.cantidad -= 1
        return nodo.dato

    def ver_frente(self):
        """Mira quien esta de primero SIN sacarlo."""
        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        return self.frente.dato


# ---------------------------------------------------------------
# PARTE 2: la cola de prioridad con tres niveles
# ---------------------------------------------------------------
class Elemento:
    """Un trabajo que espera en la cola de prioridad."""

    def __init__(self, dato, nivel, tiempo_llegada):
        self.dato = dato
        self.nivel_original = nivel        # nivel con el que llego (no cambia)
        self.nivel = nivel                 # nivel actual (puede subir)
        self.tiempo_llegada = tiempo_llegada   # cuando llego al sistema
        self.tiempo_en_nivel = tiempo_llegada  # desde cuando esta en su nivel actual


class ColaPrioridad:
    def __init__(self, limite_espera=None):
        # Una Cola normal por cada nivel: [ALTA, MEDIA, BAJA]
        self.niveles = [Cola(), Cola(), Cola()]
        self.limite_espera = limite_espera

    def esta_vacia(self):
        for cola in self.niveles:
            if not cola.esta_vacia():
                return False
        return True

    def encolar(self, dato, nivel, tiempo_actual=0):
        """Agrega un trabajo en el nivel indicado (ALTA, MEDIA o BAJA)."""
        elemento = Elemento(dato, nivel, tiempo_actual)
        self.niveles[nivel].encolar(elemento)

    def _envejecer(self, tiempo_actual):
        """
        MECANISMO ANTI-ESPERA-INDEFINIDA.
        Revisa MEDIA y BAJA. Si el que esta de primero ya espero demasiado,
        lo sube un nivel. Solo miramos el frente porque es el que lleva mas
        tiempo esperando en ese nivel.
        """
        if self.limite_espera is None:     # envejecimiento apagado
            return
        for nivel in (MEDIA, BAJA):
            cola = self.niveles[nivel]
            while not cola.esta_vacia():
                primero = cola.ver_frente()
                espera = tiempo_actual - primero.tiempo_en_nivel
                if espera < self.limite_espera:
                    break                  # este aun no cumple; los de atras menos
                cola.desencolar()
                primero.nivel = nivel - 1  # sube un nivel
                primero.tiempo_en_nivel = tiempo_actual
                self.niveles[nivel - 1].encolar(primero)

    def desencolar(self, tiempo_actual=0):
        """Saca el siguiente trabajo: primero ALTA, luego MEDIA, luego BAJA."""
        if self.esta_vacia():
            raise IndexError("No se puede desencolar: la cola esta vacia")
        self._envejecer(tiempo_actual)
        for cola in self.niveles:
            if not cola.esta_vacia():
                return cola.desencolar()


# ---------------------------------------------------------------
# Pequena prueba: python cola_prioridad.py
# ---------------------------------------------------------------
if __name__ == "__main__":
    cp = ColaPrioridad()
    cp.encolar("trabajo baja", BAJA)
    cp.encolar("trabajo alta 1", ALTA)
    cp.encolar("trabajo media", MEDIA)
    cp.encolar("trabajo alta 2", ALTA)
    print("Orden de salida (esperado: alta 1, alta 2, media, baja):")
    while not cp.esta_vacia():
        print(" -", cp.desencolar().dato)
