"""Programa sencillo para probar el carrito desde la terminal."""

from carrito_dict import Carrito


def mostrar(carrito):
    print("\n--- CARRITO ---")
    if carrito.cuanto_llevo() == 0:
        print("El carrito está vacío.")
    else:
        for producto, cantidad in carrito.productos.items():
            print(f"{producto}: {cantidad}")
        print(f"Total de unidades: {carrito.cuanto_llevo()}")


def main():
    carrito = Carrito()

    while True:
        mostrar(carrito)
        print("\n1. Meter producto")
        print("2. Sacar producto")
        print("3. Consultar producto")
        print("0. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "0":
            print("Hasta luego.")
            break

        try:
            if opcion == "1":
                producto = input("Producto: ")
                cantidad = int(input("Cantidad: "))
                carrito.meter(producto, cantidad)

            elif opcion == "2":
                producto = input("Producto: ")
                cantidad = int(input("Cantidad: "))
                carrito.sacar(producto, cantidad)

            elif opcion == "3":
                producto = input("Producto: ")
                print("Cantidad:", carrito.cuanto_hay(producto))

            else:
                print("Opción no válida.")

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
