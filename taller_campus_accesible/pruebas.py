"""Pruebas del proyecto. Se corren con:  python pruebas.py"""
import heapq

from grafo import (CANTIDAD_NODOS, GrafoMatriz, GrafoLista, GrafoDisperso, construir_grafo,
                   cargar_tramos, numero_de, hora_a_minutos, minutos_a_hora)
from busquedas import buscar_bfs, buscar_dfs, buscar_a_estrella, texto_consulta
from verificar_heuristica import verificar


def vecinos_como_conjunto(grafo, nodo):
    """Los vecinos de un punto como un conjunto de números (para comparar sin importar el orden)."""
    conjunto = set()
    for vecino, tramo in grafo.vecinos(nodo):
        conjunto.add(vecino)
    return conjunto


def test_las_tres_representaciones_dan_los_mismos_vecinos():
    matriz = construir_grafo(GrafoMatriz)
    lista = construir_grafo(GrafoLista)
    disperso = construir_grafo(GrafoDisperso)
    for nodo in range(CANTIDAD_NODOS):
        assert vecinos_como_conjunto(matriz, nodo) == vecinos_como_conjunto(lista, nodo)
        assert vecinos_como_conjunto(lista, nodo) == vecinos_como_conjunto(disperso, nodo)


def test_el_campus_tiene_60_puntos_y_90_tramos():
    assert CANTIDAD_NODOS == 60
    assert len(cargar_tramos()) == 90


def test_horas():
    assert hora_a_minutos("17:45") == 1065
    assert minutos_a_hora(1065) == "17:45"
    assert hora_a_minutos("00:00") == 0


def costo_optimo_de_referencia(grafo, origen, destino, hora):
    """Dijkstra hecho aparte, solo para comprobar a A*."""
    mejor = {origen: 0}
    pendientes = [(0, origen)]
    while len(pendientes) > 0:
        costo, nodo = heapq.heappop(pendientes)
        if nodo == destino:
            return costo
        if costo > mejor[nodo]:
            continue
        for vecino, tramo in grafo.vecinos(nodo):
            if tramo.esta_disponible(hora):
                nuevo = costo + tramo.costo
                if vecino not in mejor or nuevo < mejor[vecino]:
                    mejor[vecino] = nuevo
                    heapq.heappush(pendientes, (nuevo, vecino))
    return None


def test_a_estrella_da_el_costo_optimo_en_todos_los_pares():
    grafo = construir_grafo(GrafoLista)
    for hora_texto in ["12:00", "18:15"]:
        hora = hora_a_minutos(hora_texto)
        for origen in range(CANTIDAD_NODOS):
            for destino in range(CANTIDAD_NODOS):
                esperado = costo_optimo_de_referencia(grafo, origen, destino, hora)
                resultado = buscar_a_estrella(grafo, origen, destino, hora)
                if esperado is None:
                    assert resultado["encontrada"] is False
                else:
                    assert abs(resultado["costo"] - esperado) < 0.000001


def test_bfs_y_dfs_encuentran_ruta_valida():
    grafo = construir_grafo(GrafoLista)
    origen = numero_de("Portería Principal")
    destino = numero_de("Mirador")
    hora = hora_a_minutos("12:00")
    for buscar in [buscar_bfs, buscar_dfs]:
        resultado = buscar(grafo, origen, destino, hora)
        assert resultado["encontrada"]
        ruta = resultado["ruta"]
        assert ruta[0] == origen and ruta[-1] == destino
        for i in range(len(ruta) - 1):          # cada paso debe ser un tramo que existe y se puede usar
            tramo = grafo.tramo_entre(ruta[i], ruta[i + 1])
            assert tramo is not None
            assert tramo.esta_disponible(hora)


def test_la_puerta_de_la_biblioteca():
    grafo = construir_grafo(GrafoLista)
    origen = numero_de("Portería Principal")
    destino = numero_de("Biblioteca")
    assert buscar_a_estrella(grafo, origen, destino, hora_a_minutos("17:45"))["encontrada"]
    assert buscar_a_estrella(grafo, origen, destino, hora_a_minutos("17:59"))["encontrada"] is True
    assert buscar_a_estrella(grafo, origen, destino, hora_a_minutos("18:00"))["encontrada"] is False
    assert buscar_a_estrella(grafo, origen, destino, hora_a_minutos("18:15"))["encontrada"] is False


def test_sin_ruta_se_dice_con_claridad():
    texto = texto_consulta(construir_grafo(GrafoLista), "Portería Principal", "Biblioteca", "18:15")
    assert "NO EXISTE RUTA ACCESIBLE" in texto
    assert "Plazoleta Central -> Biblioteca" in texto


def test_sin_ruta_a_ninguna_hora():
    # Dejamos el punto 'Mirador' sin ningún tramo accesible y comprobamos el mensaje.
    tramos = cargar_tramos()
    mirador = numero_de("Mirador")
    for tramo in tramos:
        if tramo.a == mirador or tramo.b == mirador:
            tramo.accesible = False
    grafo = GrafoLista(CANTIDAD_NODOS, tramos)
    texto = texto_consulta(grafo, "Portería Principal", "Mirador", "12:00")
    assert "NO EXISTE RUTA ACCESIBLE" in texto
    assert "a ninguna hora" in texto


def test_origen_igual_a_destino():
    grafo = construir_grafo(GrafoLista)
    punto = numero_de("Mirador")
    resultado = buscar_a_estrella(grafo, punto, punto, hora_a_minutos("12:00"))
    assert resultado["encontrada"] and resultado["ruta"] == [punto] and resultado["costo"] == 0


def test_nombre_inexistente_da_error_claro():
    try:
        numero_de("Biblioteka")
        assert False, "debió fallar"
    except ValueError as error:
        assert "No existe el punto" in str(error)


def test_la_heuristica_es_admisible():
    assert "admisible (y consistente)" in verificar()


pruebas = [test_las_tres_representaciones_dan_los_mismos_vecinos, test_el_campus_tiene_60_puntos_y_90_tramos,
           test_horas, test_a_estrella_da_el_costo_optimo_en_todos_los_pares, test_bfs_y_dfs_encuentran_ruta_valida,
           test_la_puerta_de_la_biblioteca, test_sin_ruta_se_dice_con_claridad, test_sin_ruta_a_ninguna_hora,
           test_origen_igual_a_destino, test_nombre_inexistente_da_error_claro, test_la_heuristica_es_admisible]

if __name__ == "__main__":
    fallos = 0
    for prueba in pruebas:
        try:
            prueba()
            print("OK    ", prueba.__name__)
        except AssertionError:
            fallos += 1
            print("FALLÓ ", prueba.__name__)
    print()
    if fallos == 0:
        print("Todas las pruebas pasaron.")
    else:
        print(fallos, "prueba(s) fallaron.")
