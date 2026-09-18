import time
from lista_arreglo import ListaArreglo
from lista_enlazada import ListaEnlazada

N = 5000
REPETICIONES = 5


def construir(clase):
    lista = clase()
    for i in range(N):
        lista.insertar_al_final(i)
    return lista


def medir(nombre, operacion):
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        operacion()
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    promedio = sum(tiempos) / len(tiempos)
    print(f"{nombre}: {promedio * 1_000_000:.2f} µs")


def medir_operaciones(clase, etiqueta):
    print(f"\n{etiqueta}")
    medir(
        "Insertar al principio",
        lambda: clase().insertar_al_principio(999999)
    )

    lista = construir(clase)
    medir("Recorrer toda la lista", lambda: sum(1 for _ in lista.recorrer()))

    lista = construir(clase)
    medir("Ir a la canción N", lambda: lista.ir_a(N - 1))

    lista = construir(clase)
    lista.ir_a(N // 2)
    medir("Borrar la canción actual", lambda: lista.borrar_actual())


def main():
    print(f"Comparación con {N} canciones y {REPETICIONES} mediciones por operación.")
    medir_operaciones(ListaArreglo, "LISTA ARREGLO")
    medir_operaciones(ListaEnlazada, "LISTA ENLAZADA")


if __name__ == "__main__":
    main()
