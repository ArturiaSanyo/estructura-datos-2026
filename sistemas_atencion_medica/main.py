# Sistema de Atención Médica
# Proyecto para principiantes: maneja una cola de pacientes con prioridad.

import json
import os

ARCHIVO = "pacientes.json"

# Reglas de priorización (1 = se atiende primero)
PRIORIDADES = {
    1: "Emergencia",
    2: "Urgente",
    3: "Normal",
}

cola = []           # lista de pacientes esperando
siguiente_id = 1    # número de turno que se le dará al próximo paciente


# ---------- Guardar y cargar datos ----------

def guardar_datos():
    """Guarda la cola en un archivo JSON."""
    datos = {"siguiente_id": siguiente_id, "cola": cola}
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def cargar_datos():
    """Lee la cola desde el archivo JSON (si existe)."""
    global cola, siguiente_id
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
        cola = datos["cola"]
        siguiente_id = datos["siguiente_id"]


# ---------- Funciones principales ----------

def mostrar_reglas():
    """Muestra las reglas de priorización."""
    print("\n--- Reglas de priorización ---")
    for numero, nombre in PRIORIDADES.items():
        print(f"{numero} = {nombre}")
    print("Se atiende primero la prioridad más baja (1).")
    print("Si hay empate, se atiende el que llegó primero.")


def registrar_paciente():
    """Pide los datos y agrega un paciente a la cola."""
    global siguiente_id
    print("\n--- Registrar paciente ---")
    nombre = input("Nombre: ").strip()
    if nombre == "":
        print("El nombre no puede estar vacío.")
        return

    mostrar_reglas()
    try:
        prioridad = int(input("Prioridad (1, 2 o 3): "))
    except ValueError:
        print("Debes escribir un número.")
        return
    if prioridad not in PRIORIDADES:
        print("Prioridad no válida.")
        return

    paciente = {"id": siguiente_id, "nombre": nombre, "prioridad": prioridad}
    cola.append(paciente)
    siguiente_id += 1
    guardar_datos()
    print(f"Paciente registrado con turno #{paciente['id']}.")


def buscar_siguiente():
    """Devuelve el próximo paciente a atender (sin sacarlo de la cola)."""
    if len(cola) == 0:
        return None
    # Ordena por prioridad y, si empatan, por orden de llegada (id)
    return min(cola, key=lambda p: (p["prioridad"], p["id"]))


def consultar_siguiente():
    """Muestra quién es el siguiente."""
    paciente = buscar_siguiente()
    if paciente is None:
        print("\nNo hay pacientes en la cola.")
    else:
        print(f"\nSiguiente: #{paciente['id']} {paciente['nombre']} "
              f"({PRIORIDADES[paciente['prioridad']]})")


def atender_paciente():
    """Atiende al siguiente paciente y lo saca de la cola."""
    paciente = buscar_siguiente()
    if paciente is None:
        print("\nNo hay pacientes para atender.")
        return
    cola.remove(paciente)
    guardar_datos()
    print(f"\nAtendiendo a #{paciente['id']} {paciente['nombre']} "
          f"({PRIORIDADES[paciente['prioridad']]})")


def sacar_de_la_cola():
    """Saca a un paciente de la cola usando su número de turno."""
    if len(cola) == 0:
        print("\nLa cola está vacía.")
        return
    mostrar_cola()
    try:
        turno = int(input("Número de turno a sacar: "))
    except ValueError:
        print("Debes escribir un número.")
        return
    for paciente in cola:
        if paciente["id"] == turno:
            cola.remove(paciente)
            guardar_datos()
            print(f"{paciente['nombre']} fue sacado de la cola.")
            return
    print("No existe ese turno.")


def mostrar_cola():
    """Muestra todos los pacientes que faltan por atender."""
    print(f"\n--- Faltan por atender: {len(cola)} ---")
    for p in sorted(cola, key=lambda p: (p["prioridad"], p["id"])):
        print(f"#{p['id']} {p['nombre']} - {PRIORIDADES[p['prioridad']]}")


# ---------- Menú ----------

def menu():
    cargar_datos()
    while True:
        print("\n===== SISTEMA DE ATENCIÓN MÉDICA =====")
        print("1. Registrar paciente")
        print("2. Ver reglas de priorización")
        print("3. Consultar quién es el siguiente")
        print("4. Atender paciente")
        print("5. Sacar a alguien de la cola")
        print("6. Mostrar cuántos faltan por atender")
        print("0. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            registrar_paciente()
        elif opcion == "2":
            mostrar_reglas()
        elif opcion == "3":
            consultar_siguiente()
        elif opcion == "4":
            atender_paciente()
        elif opcion == "5":
            sacar_de_la_cola()
        elif opcion == "6":
            mostrar_cola()
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
