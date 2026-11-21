"""Comprueba con TODOS los pares de puntos que la heurística de A* es admisible.

Admisible = nunca sobreestima: para cualquier punto y cualquier destino, la estimación
(línea recta) es MENOR O IGUAL al costo real del mejor camino.

El argumento teórico está en heuristica.md. Aquí lo comprobamos con números.
Se ejecuta con:  python verificar_heuristica.py
"""
import heapq

from grafo import (NOMBRES, CANTIDAD_NODOS, GrafoLista, construir_grafo,
                   cargar_tramos, distancia_en_linea_recta)
from busquedas import heuristica


def costos_reales_hacia(grafo, destino, hora):
    """Dijkstra desde el destino: el costo real MÍNIMO desde cada punto hasta el destino.
    (Se hace aparte de A*, para que la comprobación no dependa del código que se comprueba.)"""
    mejor = {destino: 0}
    pendientes = [(0, destino)]
    while len(pendientes) > 0:
        costo, nodo = heapq.heappop(pendientes)
        if costo > mejor[nodo]:
            continue
        for vecino, tramo in grafo.vecinos(nodo):
            if not tramo.esta_disponible(hora):
                continue
            nuevo = costo + tramo.costo
            if vecino not in mejor or nuevo < mejor[vecino]:
                mejor[vecino] = nuevo
                heapq.heappush(pendientes, (nuevo, vecino))
    return mejor


def verificar():
    lineas = []
    lineas.append("VERIFICACIÓN DE LA HEURÍSTICA (distancia en línea recta)")
    lineas.append("=" * 70)

    # ---- Comprobación 1: la base del argumento, tramo por tramo -------------
    tramos = cargar_tramos()
    fallos = 0
    for tramo in tramos:
        recta = distancia_en_linea_recta(tramo.a, tramo.b)
        if not (recta <= tramo.distancia <= tramo.costo):
            fallos += 1
    lineas.append("1) En cada uno de los " + str(len(tramos)) + " tramos se cumple:")
    lineas.append("      línea recta <= distancia del tramo <= costo del tramo")
    lineas.append("   Tramos que NO lo cumplen: " + str(fallos))
    lineas.append("")

    # ---- Comprobación 2: admisibilidad con todos los pares -------------------
    # Se usa la hora 00:00 (todas las puertas abiertas): es el caso MÁS FAVORABLE para
    # el costo real. Si la heurística no sobreestima ahí, tampoco lo hace cuando hay
    # puertas cerradas (cerrar puertas solo vuelve los caminos más largos o los quita).
    grafo = construir_grafo(GrafoLista)
    pares = 0
    sobreestima = 0
    mayor_razon = 0
    suma_razon = 0
    peor_par = ""
    for destino in range(CANTIDAD_NODOS):
        reales = costos_reales_hacia(grafo, destino, 0)
        for nodo in range(CANTIDAD_NODOS):
            if nodo == destino:
                continue
            estimado = heuristica(nodo, destino)
            real = reales[nodo]
            pares += 1
            if estimado > real + 0.000001:
                sobreestima += 1
            razon = estimado / real
            suma_razon += razon
            if razon > mayor_razon:
                mayor_razon = razon
                peor_par = NOMBRES[nodo] + " -> " + NOMBRES[destino]
    lineas.append("2) Se comparó la estimación con el costo real de " + str(pares) + " pares (origen, destino):")
    lineas.append("   Pares donde la heurística SOBREESTIMA el costo real: " + str(sobreestima))
    lineas.append("   Razón estimación/costo real: promedio " + str(round(suma_razon / pares, 2))
                  + ", máxima " + str(round(mayor_razon, 2)) + " (" + peor_par + ").")
    lineas.append("   (Una razón <= 1 en todos los pares significa que nunca sobreestima.)")
    lineas.append("")

    # ---- Comprobación 3: consistencia (la que permite no reabrir puntos ya explorados) ----
    violaciones = 0
    revisiones = 0
    for tramo in tramos:
        for destino in range(CANTIDAD_NODOS):
            for desde, hasta in [(tramo.a, tramo.b), (tramo.b, tramo.a)]:
                revisiones += 1
                if heuristica(desde, destino) > tramo.costo + heuristica(hasta, destino) + 0.000001:
                    violaciones += 1
    lineas.append("3) Consistencia: h(A) <= costo(A,B) + h(B) en " + str(revisiones) + " combinaciones")
    lineas.append("   (tramo, sentido, destino). Violaciones: " + str(violaciones))
    lineas.append("")

    if fallos == 0 and sobreestima == 0 and violaciones == 0:
        lineas.append("RESULTADO: la heurística es admisible (y consistente) con los datos del campus.")
    else:
        lineas.append("RESULTADO: ¡hay problemas! Revisa los datos de campus.py.")
    return "\n".join(lineas)


if __name__ == "__main__":
    texto = verificar()
    print(texto)
    archivo = open("salida_heuristica.txt", "w", encoding="utf-8")
    archivo.write(texto + "\n")
    archivo.close()
