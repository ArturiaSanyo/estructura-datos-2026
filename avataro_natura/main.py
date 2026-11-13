"""Avataro Natura - programa de consola (el menú que ve la persona usuaria).

Este archivo solo habla con la persona: muestra el menú, pide datos y
muestra resultados. Toda la "inteligencia" está en mural.py y en la
carpeta estructuras/.
"""

from estructuras.errores import AvataroError
from mural import Mural


def mostrar_menu(mural):
    print()
    print("=== Avataro Natura · Mural de opiniones ===")
    print("1. Comentar")
    print("2. Responder a un comentario")
    print("3. Ver el hilo")
    print("4. Reportar un comentario")
    print(f"5. Revisar el siguiente reporte (administración) · pendientes: "
          f"{mural.cantidad_reportes()}")
    print("0. Salir")


def pedir_numero(mensaje):
    """Pide un número entero. Devuelve None si el usuario escribe otra cosa."""
    valor = input(mensaje)
    if valor.strip().isdigit():
        return int(valor)
    return None


def opcion_comentar(mural):
    autor = input("Tu nombre: ")
    texto = input("Tu comentario: ")
    numero = mural.comentar(autor, texto)
    print(f"Comentario #{numero} publicado.")


def opcion_responder(mural):
    padre = pedir_numero("Número del comentario a responder: ")
    if padre is None:
        print("Debes escribir un número.")
        return
    autor = input("Tu nombre: ")
    texto = input("Tu respuesta: ")
    numero = mural.responder(padre, autor, texto)
    print(f"Respuesta #{numero} publicada.")


def opcion_ver_hilo(mural):
    if mural.cantidad_comentarios() == 0:
        print("Aún no hay comentarios.")
    else:
        print()
        print(mural.ver_hilo())


def opcion_reportar(mural):
    comentario = pedir_numero("Número del comentario a reportar: ")
    if comentario is None:
        print("Debes escribir un número.")
        return
    reportante = input("Tu nombre: ")
    motivo = input("Motivo del reporte: ")
    numero = mural.reportar(comentario, reportante, motivo)
    print(f"Reporte #{numero} enviado. La administración lo revisará.")


def opcion_revisar_reporte(mural):
    reporte = mural.ver_siguiente_reporte()   # si no hay, lanza NoHayReportesError
    print()
    print(f"Reporte #{reporte.numero}: {reporte.reportante} reportó el "
          f"comentario #{reporte.numero_comentario}.")
    print(f"Motivo: {reporte.motivo}")
    print()
    print("Así se ve el hilo ahora:")
    print(mural.ver_hilo())
    print()

    respuesta = input(
        f"¿Ocultar el comentario #{reporte.numero_comentario}? (s/n): "
    ).strip().lower()

    if respuesta == "s":
        mural.atender_reporte(True)
        print("Comentario ocultado. Reporte atendido.")
    elif respuesta == "n":
        mural.atender_reporte(False)
        print("El comentario se deja como está. Reporte atendido.")
    else:
        print("Respuesta no válida. El reporte sigue pendiente.")


def main():
    mural = Mural()
    print("Actividad: Jornada de siembra en la quebrada La Presidenta")

    opcion = ""
    while opcion != "0":
        mostrar_menu(mural)
        opcion = input("Elige una opción: ").strip()

        try:
            if opcion == "1":
                opcion_comentar(mural)
            elif opcion == "2":
                opcion_responder(mural)
            elif opcion == "3":
                opcion_ver_hilo(mural)
            elif opcion == "4":
                opcion_reportar(mural)
            elif opcion == "5":
                opcion_revisar_reporte(mural)
            elif opcion != "0":
                print("Opción no válida.")

        except AvataroError as error:
            # Cualquier error de comentarios o reportes llega hasta aquí:
            # mostramos el mensaje y el menú sigue funcionando (CS-01).
            print(f"No se pudo: {error}")

    print("¡Hasta pronto!")


if __name__ == "__main__":
    main()
