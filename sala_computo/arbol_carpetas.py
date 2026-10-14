"""
arbol_carpetas.py
-----------------
Modelamos las carpetas del servidor como un ARBOL:
  - Cada Nodo es una carpeta o una entrega (archivo).
  - Una carpeta puede tener hijos. Una entrega no.

Tres consultas:
  1. contar_entregas(nodo)      -> RECURSIVA
  2. ruta_mas_profunda(nodo)    -> RECURSIVA
  3. listar_por_niveles(raiz)   -> SIN recursion, con nuestra propia Cola
"""

from cola_prioridad import Cola   # la cola que construimos nosotros (no deque)


class Nodo:
    def __init__(self, nombre, es_carpeta=True):
        self.nombre = nombre
        self.es_carpeta = es_carpeta   # False significa que es una entrega
        self.hijos = []

    def agregar(self, hijo):
        """Agrega un hijo y lo devuelve (asi podemos seguir armando el arbol)."""
        self.hijos.append(hijo)
        return hijo


# ---------------------------------------------------------------
# Consulta 1: cuantas entregas hay bajo un nodo (recursion)
# ---------------------------------------------------------------
def contar_entregas(nodo):
    # Caso base: si es una entrega, cuenta como 1
    if not nodo.es_carpeta:
        return 1
    # Caso recursivo: sumamos lo que hay en cada hijo
    total = 0
    for hijo in nodo.hijos:
        total = total + contar_entregas(hijo)
    return total


# ---------------------------------------------------------------
# Consulta 2: ruta mas profunda (recursion)
# Devuelve una lista con los nombres desde este nodo hasta el mas hondo.
# ---------------------------------------------------------------
def ruta_mas_profunda(nodo):
    mejor_ruta = []                       # caso base: sin hijos, la lista queda vacia
    for hijo in nodo.hijos:
        ruta = ruta_mas_profunda(hijo)    # pedimos la mejor ruta de cada hijo
        if len(ruta) > len(mejor_ruta):   # nos quedamos con la mas larga
            mejor_ruta = ruta
    return [nodo.nombre] + mejor_ruta     # nosotros + la mejor de abajo


# ---------------------------------------------------------------
# Consulta 3: listado por niveles (SIN recursion, con Cola)
# Devuelve una lista de listas: [[nivel 0], [nivel 1], ...]
# ---------------------------------------------------------------
def listar_por_niveles(raiz):
    niveles = []
    cola = Cola()
    cola.encolar((raiz, 0))               # guardamos el nodo y su nivel
    while not cola.esta_vacia():
        nodo, nivel = cola.desencolar()
        if nivel == len(niveles):         # primera vez que vemos este nivel
            niveles.append([])
        niveles[nivel].append(nodo.nombre)
        for hijo in nodo.hijos:           # los hijos se forman al final de la cola
            cola.encolar((hijo, nivel + 1))
    return niveles


# ---------------------------------------------------------------
# Para la parte D: el MISMO recorrido pero con PILA (lista de Python:
# append = apilar, pop = sacar el ultimo). Devuelve (nivel, nombre) en el
# orden en que se visitan los nodos.
# ---------------------------------------------------------------
def recorrer_con_pila(raiz):
    visitados = []
    pila = [(raiz, 0)]
    while len(pila) > 0:
        nodo, nivel = pila.pop()          # sale el ULTIMO que entro
        visitados.append((nivel, nodo.nombre))
        # Apilamos los hijos al reves para que el primero quede arriba
        for hijo in reversed(nodo.hijos):
            pila.append((hijo, nivel + 1))
    return visitados


# ---------------------------------------------------------------
# El arbol de prueba (esta dibujado en recorridos.md)
# ---------------------------------------------------------------
def construir_arbol_prueba():
    raiz = Nodo("servidor")

    ing = raiz.agregar(Nodo("Ingenieria"))
    sis = ing.agregar(Nodo("Sistemas"))
    prog = sis.agregar(Nodo("Programacion1"))
    s1 = prog.agregar(Nodo("2025-1"))
    s1.agregar(Nodo("tarea1.py", False))
    s1.agregar(Nodo("tarea2.py", False))
    s2 = prog.agregar(Nodo("2025-2"))
    s2.agregar(Nodo("tarea1.py", False))

    est = sis.agregar(Nodo("EstructurasDatos"))
    s3 = est.agregar(Nodo("2025-2"))
    s3.agregar(Nodo("taller1.py", False))
    s3.agregar(Nodo("taller2.py", False))
    final = s3.agregar(Nodo("proyecto_final"))
    final.agregar(Nodo("main.py", False))
    final.agregar(Nodo("informe.pdf", False))

    ind = ing.agregar(Nodo("Industrial"))
    estad = ind.agregar(Nodo("Estadistica"))
    s4 = estad.agregar(Nodo("2025-1"))
    s4.agregar(Nodo("parcial.pdf", False))

    cien = raiz.agregar(Nodo("Ciencias"))
    mat = cien.agregar(Nodo("Matematicas"))
    calc = mat.agregar(Nodo("Calculo"))
    s5 = calc.agregar(Nodo("2025-1"))
    s5.agregar(Nodo("taller1.pdf", False))
    s5.agregar(Nodo("taller2.pdf", False))

    return raiz, ing, sis


if __name__ == "__main__":
    raiz, ing, sis = construir_arbol_prueba()

    print("Entregas bajo 'servidor':  ", contar_entregas(raiz))
    print("Entregas bajo 'Ingenieria':", contar_entregas(ing))
    print("Entregas bajo 'Sistemas':  ", contar_entregas(sis))
    print()
    print("Ruta mas profunda:", " / ".join(ruta_mas_profunda(raiz)))
    print()
    print("Listado por niveles (con cola):")
    for numero, nombres in enumerate(listar_por_niveles(raiz)):
        print("  Nivel", numero, ":", ", ".join(nombres))
    print()
    print("Recorrido con pila (orden de visita):")
    for nivel, nombre in recorrer_con_pila(raiz):
        print("  nivel", nivel, ":", nombre)
