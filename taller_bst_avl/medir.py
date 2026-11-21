"""Experimento: BST contra AVL con 10.000 documentos, ordenados y desordenados.

Se corre con:  python medir.py     (tarda cerca de un minuto por el BST degenerado)

Se usa una semilla fija para que siempre salgan los mismos documentos y los mismos
resultados. Dos de las medidas (altura y pasos por búsqueda) NO dependen del
computador. El tiempo en microsegundos sí depende, y cambia un poco entre corridas.
"""
import random
import time

from avl import AVL
from bst import BST

CANTIDAD = 10000
SEMILLA = 2026


def generar_documentos():
    """10.000 números de documento distintos, ordenados de menor a mayor."""
    azar = random.Random(SEMILLA)
    documentos = azar.sample(range(1000000, 1200000000), CANTIDAD)
    documentos.sort()
    return documentos


def cargar(clase_arbol, documentos):
    """Crea un árbol (BST o AVL) e inserta los documentos en el orden dado."""
    arbol = clase_arbol()
    inicio = time.perf_counter()
    for documento in documentos:
        arbol.insertar(documento, documento)
    segundos = time.perf_counter() - inicio
    return arbol, segundos


def medir_busqueda(arbol, documentos):
    """Busca cada documento. Devuelve (microsegundos por búsqueda, pasos por búsqueda)."""
    mejor_tiempo = None
    for _ in range(3):                      # se repite 3 veces y se toma la mejor
        inicio = time.perf_counter()
        for documento in documentos:
            arbol.buscar(documento)
        tiempo = time.perf_counter() - inicio
        if mejor_tiempo is None or tiempo < mejor_tiempo:
            mejor_tiempo = tiempo

    total_pasos = 0
    for documento in documentos:
        total_pasos += arbol.pasos_busqueda(documento)

    microsegundos = mejor_tiempo / len(documentos) * 1000000
    pasos = total_pasos / len(documentos)
    return microsegundos, pasos


def parte_a_y_c(ordenados, desordenados):
    print("== Partes A y C:", CANTIDAD, "documentos, semilla", SEMILLA, "==")
    escenarios = [
        ("BST ordenado", BST, ordenados),
        ("BST desordenado", BST, desordenados),
        ("AVL ordenado", AVL, ordenados),
        ("AVL desordenado", AVL, desordenados),
    ]
    for nombre, clase_arbol, orden_de_carga in escenarios:
        arbol, segundos_carga = cargar(clase_arbol, orden_de_carga)
        microsegundos, pasos = medir_busqueda(arbol, orden_de_carga)
        print(nombre.ljust(16),
              "altura =", str(arbol.altura()).rjust(6),
              "| pasos por búsqueda =", str(round(pasos, 1)).rjust(7),
              "| µs por búsqueda =", str(round(microsegundos, 2)).rjust(7),
              "| carga =", round(segundos_carga, 2), "s")
        if clase_arbol is AVL:
            print("                 rotaciones simples =", arbol.total_rotaciones(),
                  "| reequilibrios =", arbol.total_reequilibrios(),
                  "| por caso =", arbol.casos)
        assert arbol.es_valido()


def parte_b(ordenados):
    print()
    print("== Parte B: los primeros siete documentos ordenados ==")
    siete = ordenados[:7]
    print(siete)

    bst = BST()
    avl = AVL()
    for documento in siete:
        bst.insertar(documento)
        avl.insertar(documento)

    print("BST: altura", bst.altura(), "(una cadena: cada nodo tiene un solo hijo)")
    print("AVL: altura", avl.altura(), "| rotaciones simples:", avl.total_rotaciones(),
          "| por caso:", avl.casos)
    raiz = avl.raiz
    print("AVL: raíz", raiz.clave)
    print("     hijos de la raíz:", raiz.izq.clave, "y", raiz.der.clave)
    print("     hojas:", raiz.izq.izq.clave, raiz.izq.der.clave, raiz.der.izq.clave, raiz.der.der.clave)


def generar_tardias(ordenados):
    """Tres formas en que pueden llegar 2.000 matrículas extemporáneas."""
    existentes = set(ordenados)
    minimo = ordenados[0]
    maximo = ordenados[-1]
    azar = random.Random(99)

    # 1) Documentos nuevos repartidos al azar dentro del rango.
    al_azar = set()
    while len(al_azar) < 2000:
        candidato = azar.randint(minimo, maximo)
        if candidato not in existentes:
            al_azar.add(candidato)

    # 2) Un bloque de números consecutivos por encima del mayor documento.
    sobre_el_maximo = []
    for i in range(2000):
        sobre_el_maximo.append(maximo + 1 + i)

    # 3) Un bloque de números consecutivos en la mitad del rango.
    en_el_medio = []
    candidato = ordenados[CANTIDAD // 2]
    while len(en_el_medio) < 2000:
        candidato += 1
        if candidato not in existentes:
            en_el_medio.append(candidato)

    return [
        ("al azar", list(al_azar)),
        ("bloque creciente sobre el máximo", sobre_el_maximo),
        ("bloque creciente dentro del rango", en_el_medio),
    ]


def parte_d(ordenados, desordenados):
    print()
    print("== Parte D: carga inicial DESORDENADA y luego 2.000 matrículas extemporáneas ==")
    for forma_de_llegada, tardias in generar_tardias(ordenados):
        for nombre, clase_arbol in [("BST", BST), ("AVL", AVL)]:
            arbol, _ = cargar(clase_arbol, desordenados)
            altura_antes = arbol.altura()
            for documento in tardias:
                arbol.insertar(documento, documento)
            microsegundos, pasos = medir_busqueda(arbol, tardias)
            print(nombre, "|", forma_de_llegada.ljust(34),
                  "| altura", altura_antes, "->", arbol.altura(),
                  "| pasos (tardías) =", round(pasos, 1),
                  "| µs (tardías) =", round(microsegundos, 2))
            assert arbol.es_valido()


def main():
    ordenados = generar_documentos()

    desordenados = list(ordenados)
    random.Random(SEMILLA + 1).shuffle(desordenados)

    parte_a_y_c(ordenados, desordenados)
    parte_b(ordenados)
    parte_d(ordenados, desordenados)


main()
