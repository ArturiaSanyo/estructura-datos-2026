# 1. Clase Nodo (la cajita con el país y las flechas)
class NodoPais:
    def __init__(self, nombre_pais):
        self.pais = nombre_pais
        self.siguiente = None
        self.anterior = None

# 2. Clase Lista Doblemente Enlazada
class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.actual = None  # Aquí guardamos el país donde estamos parados

    def agregar_pais(self, nombre_pais):
        nuevo_nodo = NodoPais(nombre_pais)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
            self.actual = nuevo_nodo # Nos paramos en el primer país agregado
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo

    def ir_siguiente(self):
        if self.actual is None:
            print("La lista está vacía.")
            return
        if self.actual.siguiente is not None:
            self.actual = self.actual.siguiente
            print(f"\n✈️ Viajando al este... Ahora estás en: {self.actual.pais}")
        else:
            print("\n🚫 Ya estás en el último país de la lista. No puedes ir más al este.")

    def ir_anterior(self):
        if self.actual is None:
            print("La lista está vacía.")
            return
        if self.actual.anterior is not None:
            self.actual = self.actual.anterior
            print(f"\n✈️ Viajando al oeste... Ahora estás en: {self.actual.pais}")
        else:
            print("\n🚫 Ya estás en el primer país de la lista. No puedes ir más al oeste.")

    def mostrar_actual(self):
        if self.actual is not None:
            print(f"\n📍 Ubicación actual: {self.actual.pais}")
        else:
            print("\n📍 No estás en ningún país.")

# ==========================================
# 3. PROGRAMA PRINCIPAL (Interacción contigo)
# ==========================================

def main():
    # Primero, creamos la lista y le metemos los 4 países
    mi_viaje = ListaDoblementeEnlazada()
    mi_viaje.agregar_pais("Portugal")
    mi_viaje.agregar_pais("España")
    mi_viaje.agregar_pais("Francia")
    mi_viaje.agregar_pais("Italia")

    print("🌍 ¡Bienvenido a tu viaje por Europa!")
    print("Estás en Portugal. Usa las opciones para moverte.")

    # Este bucle hará que el menú se repita hasta que elijas salir
    while True:
        print("\n--- MENÚ DE VIAJE ---")
        print("1. Ir al siguiente país (Este ➡️)")
        print("2. Regresar al país anterior (Oeste ⬅️)")
        print("3. Ver dónde estoy")
        print("4. Salir del programa")
        
        # input() pausa el programa y espera a que escribas algo y presiones Enter
        opcion = input("Elige una opción (1-4): ")

        if opcion == "1":
            mi_viaje.ir_siguiente()
        elif opcion == "2":
            mi_viaje.ir_anterior()
        elif opcion == "3":
            mi_viaje.mostrar_actual()
        elif opcion == "4":
            print("\n👋 ¡Buen viaje! Saliendo del programa...")
            break # Esta palabra clave rompe el bucle while y termina el programa
        else:
            print("\n❌ Opción no válida. Por favor, escribe un número del 1 al 4.")

# Esta línea asegura que el programa principal se ejecute al iniciar
if __name__ == "__main__":
    main() 