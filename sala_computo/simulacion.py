"""
simulacion.py
-------------
Compara dos escenarios con EXACTAMENTE los mismos trabajos:

  Escenario 1: SIN envejecimiento (prioridad estricta)
  Escenario 2: CON envejecimiento (limite de espera = 20)

Cada trabajo tarda 2 unidades de tiempo en atenderse. Durante 100 unidades
llegan trabajos al azar (mas de ALTA que de otros), asi que el sistema se
satura y los de BAJA sufren. Despues se sigue atendiendo hasta vaciar la cola.

Espera = momento en que empieza a atenderse - momento en que llego.
"""

import random
from cola_prioridad import ColaPrioridad, ALTA, MEDIA, BAJA, NOMBRES_NIVEL

DURACION_LLEGADAS = 100   # durante cuanto tiempo llegan trabajos
TIEMPO_SERVICIO = 2       # lo que tarda atender cada trabajo
LIMITE_ESPERA = 20        # para el escenario con envejecimiento
PROBABILIDADES = [0.30, 0.20, 0.20]   # prob. de que llegue un trabajo ALTA, MEDIA, BAJA en cada instante


def generar_llegadas(semilla=42):
    """Crea la lista de llegadas UNA sola vez, para usarla en ambos escenarios."""
    azar = random.Random(semilla)     # con semilla fija el resultado siempre es igual
    llegadas = []                     # cada elemento: (tiempo, nivel)
    for tiempo in range(DURACION_LLEGADAS):
        for nivel in (ALTA, MEDIA, BAJA):
            if azar.random() < PROBABILIDADES[nivel]:
                llegadas.append((tiempo, nivel))
    return llegadas


def simular(llegadas, limite_espera):
    """Devuelve una lista de 3 listas: las esperas de ALTA, MEDIA y BAJA."""
    cola = ColaPrioridad(limite_espera)
    esperas = [[], [], []]
    posicion = 0                 # por cual llegada vamos
    ocupado_hasta = 0            # cuando se desocupa el servidor
    tiempo = 0

    while posicion < len(llegadas) or not cola.esta_vacia():
        # 1) Los trabajos que llegan en este instante entran a la cola
        while posicion < len(llegadas) and llegadas[posicion][0] == tiempo:
            cola.encolar("trabajo", llegadas[posicion][1], tiempo)
            posicion += 1

        # 2) Si el servidor esta libre y hay alguien esperando, lo atendemos
        if tiempo >= ocupado_hasta and not cola.esta_vacia():
            elemento = cola.desencolar(tiempo)
            espera = tiempo - elemento.tiempo_llegada
            esperas[elemento.nivel_original].append(espera)
            ocupado_hasta = tiempo + TIEMPO_SERVICIO

        tiempo += 1
    return esperas


def promedio(lista):
    if len(lista) == 0:
        return 0.0
    return sum(lista) / len(lista)


def imprimir_tabla(titulo, esperas):
    print(titulo)
    print("  Nivel    Trabajos   Espera media   Peor espera")
    todas = []
    for nivel in (ALTA, MEDIA, BAJA):
        lista = esperas[nivel]
        todas = todas + lista
        print("  %-8s %8d %14.1f %13d" % (NOMBRES_NIVEL[nivel], len(lista), promedio(lista), max(lista)))
    print("  %-8s %8d %14.1f %13d" % ("TODOS", len(todas), promedio(todas), max(todas)))
    print()


if __name__ == "__main__":
    llegadas = generar_llegadas()
    print("Total de trabajos simulados:", len(llegadas))
    print()
    imprimir_tabla("ESCENARIO 1: sin envejecimiento", simular(llegadas, None))
    imprimir_tabla("ESCENARIO 2: con envejecimiento (limite %d)" % LIMITE_ESPERA, simular(llegadas, LIMITE_ESPERA))
