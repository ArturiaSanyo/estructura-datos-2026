"""Mide cuánto tardan las operaciones cuando el mural crece (PLAN-04).

Cómo usarlo, desde la carpeta del proyecto:

    python analisis/medir_tiempos.py

Qué hace, en palabras simples:
    1. Arma murales de 1 000, 2 000, 4 000, 8 000 y 16 000 comentarios.
    2. Mide cuánto tarda responder al ÚLTIMO comentario (el caso más lento
       para quien busca recorriendo), una vez con el índice (versión final)
       y otra recorriendo todo el hilo (cómo era antes del índice).
    3. Mide cuánto tarda ver el hilo completo y atender reportes.
    4. Guarda los resultados en analisis/resultados.txt y, si está instalado
       matplotlib, dibuja una gráfica en analisis/grafica_responder.png.

Los tiempos cambian un poco de un computador a otro, pero la FORMA de los
resultados (qué crece y qué no) es siempre la misma.
"""

import os
import sys
import time

# Para poder importar la carpeta "estructuras" aunque se corra desde otro sitio
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from estructuras.errores import ComentarioNoEncontradoError  # noqa: E402
from estructuras.hilo import Hilo  # noqa: E402
from estructuras.reportes import Reportes  # noqa: E402

TAMANOS = [1000, 2000, 4000, 8000, 16000]   # cantidad de comentarios
RESPUESTAS = 200      # cuántas respuestas medimos en cada tamaño
REPETICIONES = 3      # se repite cada medición y se toma la más rápida


def buscar_recorriendo(nodo, numero):
    """La búsqueda "de antes": recorre el árbol comentario por comentario."""
    if nodo.numero == numero:
        return nodo
    hijo = nodo.primer_hijo
    while hijo is not None:
        encontrado = buscar_recorriendo(hijo, numero)
        if encontrado is not None:
            return encontrado
        hijo = hijo.siguiente_hermano
    return None


class HiloSinIndice(Hilo):
    """El mismo hilo, pero encontrando comentarios como antes (sin índice).

    Solo cambia UNA función (_encontrar). Todo lo demás es idéntico, así la
    comparación es justa.
    """

    def _encontrar(self, numero):
        nodo = buscar_recorriendo(self._raiz, numero)
        if nodo is None or nodo.numero == 0:
            raise ComentarioNoEncontradoError(f"No existe el comentario #{numero}")
        return nodo


def armar_hilo(clase, cantidad):
    """Crea un hilo con 'cantidad' comentarios principales."""
    hilo = clase()
    for i in range(cantidad):
        hilo.comentar("Ana", f"comentario {i + 1}")
    return hilo


def tiempo_en_ms(funcion):
    """Corre la función varias veces y devuelve el menor tiempo, en milisegundos."""
    mejor = None
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        funcion()
        total = (time.perf_counter() - inicio) * 1000
        if mejor is None or total < mejor:
            mejor = total
    return mejor


def medir_responder(clase):
    """Tiempo (ms) de RESPUESTAS respuestas al último comentario, para cada tamaño."""
    resultados = []
    for cantidad in TAMANOS:
        hilo = armar_hilo(clase, cantidad)

        def responder_muchas():
            for _ in range(RESPUESTAS):
                hilo.responder(cantidad, "Luis", "respuesta")

        resultados.append(tiempo_en_ms(responder_muchas))
    return resultados


def medir_mostrar():
    """Tiempo (ms) de mostrar el hilo completo, para cada tamaño."""
    resultados = []
    for cantidad in TAMANOS:
        hilo = armar_hilo(Hilo, cantidad)
        resultados.append(tiempo_en_ms(hilo.mostrar))
    return resultados


def medir_reportes():
    """Tiempo (microsegundos) por operación al reportar y atender, para cada tamaño."""
    resultados = []
    for cantidad in TAMANOS:
        reportes = Reportes()

        def reportar_todos():
            for _ in range(cantidad):
                reportes.reportar(1, "Ana", "motivo")

        def atender_todos():
            for _ in range(cantidad):
                reportes.atender()

        ms_reportar = tiempo_en_ms(reportar_todos)
        # ya hay reportes de la última repetición; los atendemos todos
        pendientes = reportes.cantidad()
        inicio = time.perf_counter()
        for _ in range(pendientes):
            reportes.atender()
        ms_atender = (time.perf_counter() - inicio) * 1000
        resultados.append((ms_reportar * 1000 / cantidad,
                           ms_atender * 1000 / pendientes))
    return resultados


def main():
    con_indice = medir_responder(Hilo)
    sin_indice = medir_responder(HiloSinIndice)
    mostrar = medir_mostrar()
    reportes = medir_reportes()

    lineas = []
    lineas.append("RESULTADOS DE LA MEDICIÓN DE TIEMPOS")
    lineas.append("")
    lineas.append(f"1) Responder {RESPUESTAS} veces al último comentario (milisegundos, menos es mejor)")
    lineas.append(f"{'Comentarios':>12} {'Sin índice':>12} {'Con índice':>12} {'Veces más rápido':>18}")
    for i, cantidad in enumerate(TAMANOS):
        veces = sin_indice[i] / con_indice[i]
        lineas.append(f"{cantidad:>12} {sin_indice[i]:>12.2f} {con_indice[i]:>12.2f} {veces:>18.0f}")
    lineas.append("")
    lineas.append("2) Mostrar el hilo completo (milisegundos)")
    lineas.append(f"{'Comentarios':>12} {'Tiempo':>12}")
    for i, cantidad in enumerate(TAMANOS):
        lineas.append(f"{cantidad:>12} {mostrar[i]:>12.2f}")
    lineas.append("")
    lineas.append("3) Reportes: tiempo por operación (microsegundos)")
    lineas.append(f"{'Reportes':>12} {'reportar':>12} {'atender':>12}")
    for i, cantidad in enumerate(TAMANOS):
        lineas.append(f"{cantidad:>12} {reportes[i][0]:>12.3f} {reportes[i][1]:>12.3f}")
    lineas.append("")
    lineas.append("Cómo leerlo: si al duplicar los comentarios el tiempo también se")
    lineas.append("duplica, el costo crece en proporción (O(n)). Si el tiempo casi no")
    lineas.append("cambia, el costo es casi constante (O(1)).")

    texto = "\n".join(lineas)
    print(texto)

    ruta = os.path.join(RAIZ, "analisis", "resultados.txt")
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto + "\n")
    print(f"\nResultados guardados en {ruta}")

    # La gráfica es opcional: solo se dibuja si matplotlib está instalado.
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(matplotlib no está instalado: no se dibuja la gráfica)")
        return

    plt.figure(figsize=(7, 4))
    plt.plot(TAMANOS, sin_indice, marker="o", label="Sin índice (recorriendo)")
    plt.plot(TAMANOS, con_indice, marker="o", label="Con índice (tabla hash)")
    plt.xlabel("Comentarios en el mural")
    plt.ylabel(f"Tiempo de {RESPUESTAS} respuestas (ms)")
    plt.title("Responder: con y sin índice")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RAIZ, "analisis", "grafica_responder.png"), dpi=150)
    print("Gráfica guardada en analisis/grafica_responder.png")


if __name__ == "__main__":
    main()
