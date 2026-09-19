# 1. Definimos la clase Nodo. 
# Piensa en un Nodo como una "cajita" que guarda un país y dos flechas (una al anterior, una al siguiente).
class NodoPais:
    def __init__(self, nombre_pais):
        self.pais = nombre_pais  # Aquí guardamos el nombre del país (ej: "España")
        self.siguiente = None    # Apunta al país que viene después (inicialmente vacío)
        self.anterior = None     # Apunta al país que viene antes (inicialmente vacío)

# 2. Definimos la clase ListaDoblementeEnlazada.
# Esta clase maneja los nodos y nos permite movernos entre ellos.
class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None  # El primer país de la lista
        self.cola = None    # El último país de la lista
        self.actual = None  # El país en el que estamos "parados" ahora mismo

    # Método para agregar un país al final de la lista
    def agregar_pais(self, nombre_pais):
        nuevo_nodo = NodoPais(nombre_pais) # Creamos la cajita con el nuevo país
        
        if self.cabeza is None: # Si la lista está vacía...
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
            self.actual = nuevo_nodo # Nos paramos en el primer país
        else: # Si ya hay países en la lista...
            self.cola.siguiente = nuevo_nodo # El último país ahora apunta al nuevo
            nuevo_nodo.anterior = self.cola # El nuevo país apunta hacia atrás al último
            self.cola = nuevo_nodo          # El nuevo país ahora es el último (la cola)

    # Método para ir al siguiente país
    def ir_siguiente(self):
        if self.actual is None:
            print("La lista está vacía.")
            return
        
        if self.actual.siguiente is not None:
            self.actual = self.actual.siguiente # Nos movemos a la siguiente cajita
            print(f"✈️ Viajando al este... Ahora estás en: {self.actual.pais}")
        else:
            print("🚫 Ya estás en el último país de la lista. No puedes ir más al este.")

    # Método para ir al país anterior
    def ir_anterior(self):
        if self.actual is None:
            print("La lista está vacía.")
            return
        
        if self.actual.anterior is not None:
            self.actual = self.actual.anterior # Nos movemos a la cajita anterior
            print(f"✈️ Viajando al oeste... Ahora estás en: {self.actual.pais}")
        else:
            print("🚫 Ya estás en el primer país de la lista. No puedes ir más al oeste.")

    # Método para mostrar dónde estamos parados
    def mostrar_actual(self):
        if self.actual is not None:
            print(f"📍 Ubicación actual: {self.actual.pais}")
        else:
            print("📍 No estás en ningún país.")

# ==========================================
# 3. PRUEBA DEL PROGRAMA (Aquí empieza la ejecución real)
# ==========================================

# Creamos nuestra lista vacía
mi_viaje = ListaDoblementeEnlazada()

# Agregamos 4 países europeos (en orden geográfico de oeste a este para que tenga sentido)
print("--- Creando la ruta de viaje ---")
mi_viaje.agregar_pais("Portugal")
mi_viaje.agregar_pais("España")
mi_viaje.agregar_pais("Francia")
mi_viaje.agregar_pais("Italia")
print("Ruta creada con éxito.\n")

# Empezamos el viaje
mi_viaje.mostrar_actual() # Debería estar en Portugal

# Probamos ir hacia adelante (Siguiente)
print("\n--- Moviéndonos hacia el Este (Siguiente) ---")
mi_viaje.ir_siguiente() # España
mi_viaje.ir_siguiente() # Francia
mi_viaje.mostrar_actual()

# Probamos ir hacia atrás (Anterior)
print("\n--- Moviéndonos hacia el Oeste (Anterior) ---")
mi_viaje.ir_anterior() # España
mi_viaje.ir_anterior() # Portugal
mi_viaje.mostrar_actual()

# Probamos los límites de la lista
print("\n--- Probando los límites ---")
mi_viaje.ir_anterior() # Intenta ir antes de Portugal (debe dar error controlado)
mi_viaje.ir_siguiente() # España
mi_viaje.ir_siguiente() # Francia
mi_viaje.ir_siguiente() # Italia
mi_viaje.ir_siguiente() # Intenta ir después de Italia (debe dar error controlado)