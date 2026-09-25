"""
Menú de consola para probar el Carrito a mano.

Esto NO es parte de lo que se entrega para la nota (no lo pide
el enunciado), es solo una herramienta para que puedas jugar
con el carrito y ver que funciona como dice spec.md.
"""

from carrito_lista import Carrito as CarritoLista
from carrito_dict import Carrito as CarritoDict


def elegir_implementacion():
    print("¿Qué versión del carrito quieres usar?")
    print("1. Lista")
    print("2. Diccionario")
    opcion = input("Elige 1 o 2: ")

    if opcion == "1":
        return CarritoLista()
    else:
        return CarritoDict()


def mostrar_menu():
    print("\n--- Carrito de la tienda ---")
    print("1. Meter producto")
    print("2. Sacar producto")
    print("3. Ver cuánto hay de un producto")
    print("4. Ver cuánto llevo en total")
    print("5. Salir")


def pedir_cantidad():
    """
    Le pide un número al usuario. Si escribe algo que no es
    número, avisa y devuelve None (para no romper el programa).
    """
    texto = input("¿Cuántos? ")
    if texto.isdigit():
        return int(texto)
    else:
        print("Eso no es un número entero válido.")
        return None


def main():
    carrito = elegir_implementacion()

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            producto = input("¿Qué producto quieres meter? ")
            cantidad = pedir_cantidad()
            if cantidad is not None:
                carrito.meter(producto, cantidad)

        elif opcion == "2":
            producto = input("¿Qué producto quieres sacar? ")
            cantidad = pedir_cantidad()
            if cantidad is not None:
                carrito.sacar(producto, cantidad)

        elif opcion == "3":
            producto = input("¿Qué producto quieres consultar? ")
            print("Hay:", carrito.cuanto_hay(producto))

        elif opcion == "4":
            print("Total en el carrito:", carrito.cuanto_llevo())

        elif opcion == "5":
            print("¡Listo, hasta luego!")
            break

        else:
            print("Esa opción no existe, intenta de nuevo.")


if __name__ == "__main__":
    main()
