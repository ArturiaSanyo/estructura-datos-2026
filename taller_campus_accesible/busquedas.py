"""Tres formas de buscar una ruta en el campus: BFS, DFS y A*.

Las tres reciben:  grafo, origen, destino, hora
  - origen y destino son NÚMEROS de punto (use numero_de("Biblioteca") para obtenerlo)
  - hora son los minutos desde la medianoche (use hora_a_minutos("17:45"))
Solo se usan los tramos disponibles a esa hora: accesibles y con la puerta abierta.

Las tres devuelven un diccionario con:
  "algoritmo": el nombre
  "encontrada": True si hay ruta accesible, False si no
  "ruta": lista de números de punto, del origen al destino ([] si no hay ruta)
  "costo": el costo total de la ruta (metros de esfuerzo)
  "distancia": los metros reales que se caminan
  "explorados": lista de los puntos que el algoritmo revisó, en orden

"Explorar un punto" significa sacarlo de la lista de pendientes y revisarlo
(mirar si es el destino y, si no, anotar sus vecinos). Las tres búsquedas cuentan
igual, así que los números se pueden comparar.
"""
import heapq
from collections import deque

from grafo import (NOMBRES, numero_de, hora_a_minutos, minutos_a_hora,
                   distancia_en_linea_recta, construir_grafo, GrafoLista)


# ----------------------------------------------------------------------
# Piezas que usan las tres búsquedas
# ----------------------------------------------------------------------
def vecinos_disponibles(grafo, nodo, hora):
    """Los vecinos de un punto a los que SÍ se puede ir a esa hora."""
    resultado = []
    for vecino, tramo in grafo.vecinos(nodo):
        if tramo.esta_disponible(hora):
            resultado.append((vecino, tramo))
    return resultado


def reconstruir_ruta(padres, destino):
    """Cada punto recuerda de cuál llegamos (su "padre"). Siguiendo esos padres hacia
    atrás desde el destino se obtiene la ruta, y al final se da vuelta la lista."""
    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = padres[actual]
    ruta.reverse()
    return ruta


def costo_y_distancia(grafo, ruta):
    """Suma el costo y los metros de todos los tramos de una ruta."""
    costo = 0
    distancia = 0
    for i in range(len(ruta) - 1):
        tramo = grafo.tramo_entre(ruta[i], ruta[i + 1])
        costo += tramo.costo
        distancia += tramo.distancia
    return costo, distancia


def armar_resultado(algoritmo, grafo, encontrada, padres, destino, explorados):
    if encontrada:
        ruta = reconstruir_ruta(padres, destino)
        costo, distancia = costo_y_distancia(grafo, ruta)
    else:
        ruta = []
        costo = None
        distancia = None
    return {"algoritmo": algoritmo, "encontrada": encontrada, "ruta": ruta,
            "costo": costo, "distancia": distancia, "explorados": explorados}


# ----------------------------------------------------------------------
# BFS: búsqueda en anchura. Revisa primero los puntos más cercanos (en cantidad de tramos).
# ----------------------------------------------------------------------
def buscar_bfs(grafo, origen, destino, hora):
    fila = deque()              # fila de pendientes: el primero en entrar es el primero en salir
    fila.append(origen)
    padres = {origen: None}     # sirve también para saber qué puntos ya se anotaron
    explorados = []

    while len(fila) > 0:
        nodo = fila.popleft()   # sacamos al que lleva más tiempo esperando
        explorados.append(nodo)
        if nodo == destino:
            return armar_resultado("BFS", grafo, True, padres, destino, explorados)
        for vecino, tramo in vecinos_disponibles(grafo, nodo, hora):
            if vecino not in padres:        # solo si no lo habíamos anotado antes
                padres[vecino] = nodo
                fila.append(vecino)

    return armar_resultado("BFS", grafo, False, padres, destino, explorados)


# ----------------------------------------------------------------------
# DFS: búsqueda en profundidad. Se mete lo más lejos posible por un camino antes de probar otro.
# ----------------------------------------------------------------------
def buscar_dfs(grafo, origen, destino, hora):
    pila = [(origen, None)]     # pila de pendientes: el último en entrar es el primero en salir
    padres = {}
    explorados = []

    while len(pila) > 0:
        nodo, padre = pila.pop()        # sacamos al último que se anotó
        if nodo in padres:              # ya lo habíamos revisado por otro camino
            continue
        padres[nodo] = padre
        explorados.append(nodo)
        if nodo == destino:
            return armar_resultado("DFS", grafo, True, padres, destino, explorados)
        for vecino, tramo in vecinos_disponibles(grafo, nodo, hora):
            if vecino not in padres:
                pila.append((vecino, nodo))

    return armar_resultado("DFS", grafo, False, padres, destino, explorados)


# ----------------------------------------------------------------------
# A*: revisa primero el punto que parece más prometedor.
# ----------------------------------------------------------------------
def heuristica(nodo, destino):
    """Estimación de lo que falta: la distancia en línea recta hasta el destino.
    Por qué es admisible: ver heuristica.md."""
    return distancia_en_linea_recta(nodo, destino)


def buscar_a_estrella(grafo, origen, destino, hora):
    # Para cada punto guardamos g = lo que cuesta llegar desde el origen (lo mejor que se ha encontrado).
    # La fila de pendientes se ordena por f = g + estimación de lo que falta.
    g = {origen: 0}
    padres = {origen: None}
    pendientes = [(heuristica(origen, destino), origen)]    # heapq mantiene sacando primero el menor f
    ya_explorados = set()
    explorados = []

    while len(pendientes) > 0:
        f, nodo = heapq.heappop(pendientes)
        if nodo in ya_explorados:       # entrada vieja: ya lo revisamos con un costo mejor
            continue
        ya_explorados.add(nodo)
        explorados.append(nodo)
        if nodo == destino:
            return armar_resultado("A*", grafo, True, padres, destino, explorados)

        for vecino, tramo in vecinos_disponibles(grafo, nodo, hora):
            nuevo_g = g[nodo] + tramo.costo
            if vecino not in g or nuevo_g < g[vecino]:      # encontramos un camino mejor hasta el vecino
                g[vecino] = nuevo_g
                padres[vecino] = nodo
                heapq.heappush(pendientes, (nuevo_g + heuristica(vecino, destino), vecino))

    return armar_resultado("A*", grafo, False, padres, destino, explorados)


# ----------------------------------------------------------------------
# Consultas completas con texto explicado (las usa consultas_horario.py)
# ----------------------------------------------------------------------
def explicar_sin_ruta(grafo, origen, destino, hora):
    """Dice POR QUÉ no hay ruta, para no dejar al usuario sin respuesta."""
    texto = []
    # Probamos con la hora 00:00 (todas las puertas abiertas).
    con_todo_abierto = buscar_a_estrella(grafo, origen, destino, 0)
    if con_todo_abierto["encontrada"]:
        texto.append("Sí existe una ruta accesible cuando las puertas están abiertas, pero a esta hora")
        texto.append("tiene tramos con puerta ya cerrada:")
        ruta = con_todo_abierto["ruta"]
        for i in range(len(ruta) - 1):
            tramo = grafo.tramo_entre(ruta[i], ruta[i + 1])
            if tramo.cierra is not None and tramo.cierra <= hora:
                texto.append("  - " + NOMBRES[ruta[i]] + " -> " + NOMBRES[ruta[i + 1]]
                             + " (la puerta cerró a las " + minutos_a_hora(tramo.cierra) + ")")
        texto.append("No hay otro camino accesible: los demás pasan por escaleras sin rampa, obras o pendientes excesivas.")
    else:
        texto.append("No existe ruta accesible entre estos puntos a ninguna hora: todos los caminos")
        texto.append("pasan por escaleras sin rampa, tramos en obra o pendientes excesivas.")
    return texto


def texto_consulta(grafo, nombre_origen, nombre_destino, hora_texto):
    """Calcula la ruta accesible con A* y devuelve el texto de la respuesta."""
    lineas = []
    lineas.append("CONSULTA: " + nombre_origen + " -> " + nombre_destino + " a las " + hora_texto)
    lineas.append("-" * 70)

    # Si el usuario escribe algo mal, se lo decimos claramente (no se falla en silencio).
    try:
        origen = numero_de(nombre_origen)
        destino = numero_de(nombre_destino)
        hora = hora_a_minutos(hora_texto)
    except ValueError as error:
        lineas.append("ERROR EN LA CONSULTA: " + str(error))
        return "\n".join(lineas)

    resultado = buscar_a_estrella(grafo, origen, destino, hora)

    if not resultado["encontrada"]:
        lineas.append("NO EXISTE RUTA ACCESIBLE a las " + hora_texto + ".")
        lineas.extend(explicar_sin_ruta(grafo, origen, destino, hora))
        lineas.append("Puntos revisados por A* antes de concluirlo: " + str(len(resultado["explorados"])))
        return "\n".join(lineas)

    ruta = resultado["ruta"]
    lineas.append("Ruta accesible encontrada: " + str(len(ruta) - 1) + " tramos, "
                  + str(resultado["distancia"]) + " m, costo de esfuerzo " + str(round(resultado["costo"], 1)) + ".")
    lineas.append("")
    puertas = []
    for i in range(len(ruta) - 1):
        tramo = grafo.tramo_entre(ruta[i], ruta[i + 1])
        lineas.append(str(i + 1).rjust(3) + ". " + NOMBRES[ruta[i]] + " -> " + NOMBRES[ruta[i + 1]]
                      + "   " + str(tramo.distancia) + " m, pendiente " + str(tramo.pendiente)
                      + " %, costo " + str(round(tramo.costo, 1)))
        if tramo.cierra is not None:
            puertas.append("    (puerta: cierra a las " + minutos_a_hora(tramo.cierra) + ")")
            lineas.append(puertas[-1])
    lineas.append("")
    lineas.append("Puntos revisados por A*: " + str(len(resultado["explorados"])))
    return "\n".join(lineas)


# ----------------------------------------------------------------------
# Comparación de nodos explorados (python busquedas.py)
# ----------------------------------------------------------------------
def comparar(grafo, nombre_origen, nombre_destino, hora_texto):
    """Corre las tres búsquedas sobre la misma consulta y devuelve sus resultados."""
    origen = numero_de(nombre_origen)
    destino = numero_de(nombre_destino)
    hora = hora_a_minutos(hora_texto)
    return [buscar_bfs(grafo, origen, destino, hora),
            buscar_dfs(grafo, origen, destino, hora),
            buscar_a_estrella(grafo, origen, destino, hora)]


def tabla_de_exploracion():
    grafo = construir_grafo(GrafoLista)
    consultas = [
        ("Portería Principal", "Biblioteca", "12:00"),
        ("Portería Principal", "Bloque A Ingeniería", "17:45"),
        ("Portería Norte", "Cafetería Central", "12:00"),
        ("Portería Deportiva", "Admisiones y Registro", "12:00"),
        ("Mirador", "Portería Principal", "12:00"),
    ]
    lineas = []
    lineas.append("NODOS EXPLORADOS POR CADA BÚSQUEDA PARA LA MISMA CONSULTA")
    lineas.append("(Entre paréntesis: costo de la ruta encontrada; el menor es el óptimo)")
    lineas.append("=" * 100)
    lineas.append("Consulta".ljust(52) + "BFS".rjust(15) + "DFS".rjust(15) + "A*".rjust(15))
    lineas.append("-" * 100)
    for origen, destino, hora in consultas:
        resultados = comparar(grafo, origen, destino, hora)
        etiqueta = (origen + " -> " + destino + " (" + hora + ")")
        fila = etiqueta.ljust(52)
        for r in resultados:
            celda = str(len(r["explorados"])) + " (" + str(round(r["costo"])) + ")"
            fila += celda.rjust(15)
        lineas.append(fila)

    # Promedio sobre TODAS las consultas posibles (60 x 59 pares de puntos, a las 12:00)
    hora = hora_a_minutos("12:00")
    suma = {"BFS": 0, "DFS": 0, "A*": 0}
    optimas = {"BFS": 0, "DFS": 0, "A*": 0}
    sobrecosto = {"BFS": 0, "DFS": 0, "A*": 0}
    consultas_totales = 0
    for origen in range(len(NOMBRES)):
        for destino in range(len(NOMBRES)):
            if origen == destino:
                continue
            a_estrella = buscar_a_estrella(grafo, origen, destino, hora)
            for resultado in [buscar_bfs(grafo, origen, destino, hora),
                              buscar_dfs(grafo, origen, destino, hora), a_estrella]:
                nombre = resultado["algoritmo"]
                suma[nombre] += len(resultado["explorados"])
                if resultado["costo"] <= a_estrella["costo"] + 0.000001:
                    optimas[nombre] += 1
                sobrecosto[nombre] += resultado["costo"] / a_estrella["costo"]
            consultas_totales += 1
    lineas.append("-" * 100)
    fila = ("Promedio de las " + str(consultas_totales) + " consultas posibles (12:00)").ljust(52)
    for nombre in ["BFS", "DFS", "A*"]:
        fila += str(round(suma[nombre] / consultas_totales, 1)).rjust(15)
    lineas.append(fila)
    lineas.append("")
    lineas.append("¿Qué tan buena es la ruta que encuentra cada uno? (las " + str(consultas_totales) + " consultas)")
    lineas.append("-" * 100)
    for nombre in ["BFS", "DFS", "A*"]:
        porcentaje = 100.0 * optimas[nombre] / consultas_totales
        promedio = sobrecosto[nombre] / consultas_totales
        lineas.append(nombre.ljust(5) + "encuentra la ruta de menor costo en el " + str(round(porcentaje, 1))
                      + " % de las consultas; en promedio su ruta cuesta " + str(round(promedio, 2)) + " veces la óptima.")
    return "\n".join(lineas)


if __name__ == "__main__":
    texto = tabla_de_exploracion()
    print(texto)
    archivo = open("salida_busquedas.txt", "w", encoding="utf-8")
    archivo.write(texto + "\n")
    archivo.close()
