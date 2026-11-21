"""Tres formas de guardar el mapa del campus: matriz, lista y matriz dispersa.

Un GRAFO es un conjunto de puntos (nodos) unidos por caminos (aristas).
Aquí cada nodo es un punto del campus (una portería, un edificio, un cruce...) y
cada arista es un TRAMO: el camino que une dos puntos.

Cada punto tiene un número (0, 1, 2, ... 59), que es su posición en la lista
campus.NODOS. Los algoritmos trabajan con esos números, y los nombres solo se
usan para mostrar resultados.

Si ejecutas este archivo (python grafo.py) imprime la tabla de memoria.
"""
import campus

# ----------------------------------------------------------------------
# 1. Los puntos del campus (nombres, posiciones)
# ----------------------------------------------------------------------
NOMBRES = []
TIPOS = []
X = []          # posición en metros, hacia el oriente
Y = []          # posición en metros, hacia el norte
ALTURA = []     # metros sobre la portería principal

for fila in campus.NODOS:
    NOMBRES.append(fila[0])
    TIPOS.append(fila[1])
    X.append(fila[2])
    Y.append(fila[3])
    ALTURA.append(fila[4])

CANTIDAD_NODOS = len(NOMBRES)

INDICE = {}     # de nombre (en minúsculas) a número de punto
for numero in range(CANTIDAD_NODOS):
    INDICE[NOMBRES[numero].lower()] = numero


def numero_de(nombre):
    """Convierte el nombre de un punto en su número. Si no existe, avisa con claridad."""
    clave = nombre.strip().lower()
    if clave in INDICE:
        return INDICE[clave]

    # No existe: buscamos nombres parecidos para ayudar a quien escribió.
    parecidos = []
    for otro in NOMBRES:
        if clave in otro.lower():
            parecidos.append(otro)
    mensaje = "No existe el punto '" + nombre + "' en el campus."
    if len(parecidos) > 0:
        mensaje += " ¿Quisiste decir: " + ", ".join(parecidos) + "?"
    else:
        mensaje += " Revisa que el nombre esté bien escrito (con tildes)."
    raise ValueError(mensaje)


def distancia_en_linea_recta(a, b):
    """Distancia en metros entre dos puntos, mirando el plano (como vuela un pájaro)."""
    dx = X[a] - X[b]
    dy = Y[a] - Y[b]
    return (dx * dx + dy * dy) ** 0.5


# ----------------------------------------------------------------------
# 2. Horas
# ----------------------------------------------------------------------
def hora_a_minutos(texto):
    """'17:45' -> 1065 (minutos desde la medianoche). Así comparar horas es solo comparar números."""
    partes = texto.strip().split(":")
    if len(partes) != 2 or not partes[0].isdigit() or not partes[1].isdigit():
        raise ValueError("La hora '" + texto + "' no es válida. Usa el formato HH:MM, por ejemplo 17:45.")
    horas = int(partes[0])
    minutos = int(partes[1])
    if horas > 23 or minutos > 59:
        raise ValueError("La hora '" + texto + "' no existe. Usa el formato HH:MM, por ejemplo 17:45.")
    return horas * 60 + minutos


def minutos_a_hora(minutos):
    """1065 -> '17:45'."""
    horas = minutos // 60
    resto = minutos % 60
    return str(horas).zfill(2) + ":" + str(resto).zfill(2)


# ----------------------------------------------------------------------
# 3. El costo de un tramo
# ----------------------------------------------------------------------
def factor_por_pendiente(pendiente):
    """Cuánto se "encarece" caminar un tramo según qué tan empinado es.

    Pendiente hasta 5 %  -> factor 1.0  (cómodo: cada metro cuenta como 1)
    Más de 5 % y hasta 8 % -> factor 1.5
    Más de 8 % -> factor 2.5  (muy cansado en silla de ruedas)
    Los tramos con más de 12 % ya se marcan como NO accesibles en campus.py.
    """
    if pendiente <= 5:
        return 1.0
    if pendiente <= 8:
        return 1.5
    return 2.5


class Tramo:
    """Un camino entre dos puntos, con toda su información."""

    def __init__(self, a, b, distancia, pendiente, accesible, motivo, cierra):
        self.a = a                      # número del primer punto
        self.b = b                      # número del segundo punto
        self.distancia = distancia      # metros
        self.pendiente = pendiente      # porcentaje
        self.accesible = accesible      # True / False
        self.motivo = motivo            # por qué no es accesible, o "puerta"
        if cierra is None:
            self.cierra = None          # sin horario: siempre abierto
        else:
            self.cierra = hora_a_minutos(cierra)    # minutos desde la medianoche
        # EL COSTO: metros "de esfuerzo". Un tramo cómodo cuesta lo mismo que mide;
        # uno empinado cuesta más que lo que mide.
        self.costo = distancia * factor_por_pendiente(pendiente)

    def esta_disponible(self, hora):
        """¿Se puede usar este tramo a esa hora (en minutos desde la medianoche)?"""
        if not self.accesible:
            return False                # escaleras, obra o pendiente excesiva
        if self.cierra is not None and hora >= self.cierra:
            return False                # la puerta ya cerró (a las 18:00 en punto ya está cerrada)
        return True

    def otro_extremo(self, nodo):
        """Si estoy en un extremo del tramo, devuelve el otro."""
        if nodo == self.a:
            return self.b
        return self.a


def cargar_tramos():
    """Lee campus.TRAMOS y crea los objetos Tramo. Revisa que los datos tengan sentido."""
    tramos = []
    for fila in campus.TRAMOS:
        origen, destino, distancia, pendiente, accesible, motivo, cierra = fila
        a = numero_de(origen)
        b = numero_de(destino)

        # La heurística de A* se apoya en esta regla: un tramo nunca puede medir
        # menos que la línea recta entre sus dos extremos. Si los datos la rompen,
        # lo decimos en vez de dar rutas incorrectas sin avisar.
        recta = distancia_en_linea_recta(a, b)
        if distancia < recta:
            raise ValueError("El tramo " + origen + " - " + destino + " mide " + str(distancia)
                             + " m, pero la línea recta entre los dos puntos es de "
                             + str(round(recta, 1)) + " m. Un camino no puede ser más corto que la "
                             + "línea recta: corrige la distancia en campus.py.")

        tramos.append(Tramo(a, b, distancia, pendiente, accesible, motivo, cierra))
    return tramos


# ----------------------------------------------------------------------
# 4. Representación 1: MATRIZ DE ADYACENCIA
# ----------------------------------------------------------------------
class GrafoMatriz:
    """Una tabla de 60 x 60. La casilla [i][j] guarda el tramo que une i con j,
    o None si no hay tramo. Hay 3.600 casillas aunque solo 180 tengan algo."""

    def __init__(self, cantidad, tramos):
        self.cantidad = cantidad
        self.matriz = []
        for i in range(cantidad):
            fila = []
            for j in range(cantidad):
                fila.append(None)
            self.matriz.append(fila)
        for tramo in tramos:
            self.matriz[tramo.a][tramo.b] = tramo       # ida
            self.matriz[tramo.b][tramo.a] = tramo       # vuelta (el mismo tramo)

    def vecinos(self, nodo):
        """Lista de (vecino, tramo). Hay que mirar TODA la fila, casilla por casilla."""
        resultado = []
        for j in range(self.cantidad):
            if self.matriz[nodo][j] is not None:
                resultado.append((j, self.matriz[nodo][j]))
        return resultado

    def tramo_entre(self, a, b):
        return self.matriz[a][b]

    def casillas_usadas(self):
        """Cuántas casillas ocupa la estructura (esto es lo que se compara en la tabla)."""
        return self.cantidad * self.cantidad

    def casillas_con_datos(self):
        total = 0
        for i in range(self.cantidad):
            for j in range(self.cantidad):
                if self.matriz[i][j] is not None:
                    total += 1
        return total

    def casillas_para_vecinos(self, nodo):
        """Casillas que se leen para saber los vecinos de un punto."""
        return self.cantidad


# ----------------------------------------------------------------------
# 5. Representación 2: LISTA DE ADYACENCIA
# ----------------------------------------------------------------------
class GrafoLista:
    """Para cada punto, una lista corta con solo SUS vecinos.
    Ejemplo: lista[5] = [(4, tramo), (6, tramo), (15, tramo)] significa que el punto 5
    está conectado con el 4, el 6 y el 15."""

    def __init__(self, cantidad, tramos):
        self.cantidad = cantidad
        self.lista = []
        for i in range(cantidad):
            self.lista.append([])
        for tramo in tramos:
            self.lista[tramo.a].append((tramo.b, tramo))    # ida
            self.lista[tramo.b].append((tramo.a, tramo))    # vuelta

    def vecinos(self, nodo):
        return self.lista[nodo]

    def tramo_entre(self, a, b):
        for vecino, tramo in self.lista[a]:
            if vecino == b:
                return tramo
        return None

    def casillas_usadas(self):
        # 1 casilla por punto (la lista de cada uno) + 2 por cada vecino guardado
        # (el número del vecino y el tramo).
        total = self.cantidad
        for i in range(self.cantidad):
            total += 2 * len(self.lista[i])
        return total

    def casillas_para_vecinos(self, nodo):
        return len(self.lista[nodo])


# ----------------------------------------------------------------------
# 6. Representación 3: MATRIZ DISPERSA (formato CSR, "por filas comprimidas")
# ----------------------------------------------------------------------
class GrafoDisperso:
    """Una matriz donde solo se guardan las casillas que NO están vacías,
    en tres listas largas:

      columnas:    el vecino de cada entrada, fila tras fila
      tramos:      el tramo de cada entrada (en el mismo orden)
      inicio_fila: dónde empieza cada punto dentro de las dos listas anteriores

    Ejemplo con 3 puntos donde 0-1 y 1-2 están unidos:
      columnas    = [1,  0, 2,  1]       (vecinos del 0: [1]; del 1: [0, 2]; del 2: [1])
      inicio_fila = [0, 1, 3, 4]         (el punto 1 usa las posiciones 1 y 2)
    Los vecinos del punto i son las posiciones entre inicio_fila[i] e inicio_fila[i+1].
    """

    def __init__(self, cantidad, tramos):
        self.cantidad = cantidad
        # Primero juntamos los vecinos de cada punto (como en la lista)...
        por_punto = []
        for i in range(cantidad):
            por_punto.append([])
        for tramo in tramos:
            por_punto[tramo.a].append((tramo.b, tramo))
            por_punto[tramo.b].append((tramo.a, tramo))
        # ...y después los aplanamos en las tres listas largas.
        self.columnas = []
        self.tramos = []
        self.inicio_fila = [0]
        for i in range(cantidad):
            ordenados = sorted(por_punto[i], key=_numero_del_vecino)
            for vecino, tramo in ordenados:
                self.columnas.append(vecino)
                self.tramos.append(tramo)
            self.inicio_fila.append(len(self.columnas))

    def vecinos(self, nodo):
        resultado = []
        for posicion in range(self.inicio_fila[nodo], self.inicio_fila[nodo + 1]):
            resultado.append((self.columnas[posicion], self.tramos[posicion]))
        return resultado

    def tramo_entre(self, a, b):
        for posicion in range(self.inicio_fila[a], self.inicio_fila[a + 1]):
            if self.columnas[posicion] == b:
                return self.tramos[posicion]
        return None

    def casillas_usadas(self):
        return len(self.columnas) + len(self.tramos) + len(self.inicio_fila)

    def casillas_para_vecinos(self, nodo):
        # los vecinos del punto + las 2 casillas de inicio_fila que marcan dónde empieza y termina
        return (self.inicio_fila[nodo + 1] - self.inicio_fila[nodo]) + 2


def _numero_del_vecino(par):
    return par[0]


def construir_grafo(clase_de_grafo):
    """Crea el grafo del campus con la representación que se pida.
    Ejemplo: grafo = construir_grafo(GrafoLista)"""
    tramos = cargar_tramos()
    return clase_de_grafo(CANTIDAD_NODOS, tramos)


# ----------------------------------------------------------------------
# 7. Tabla de memoria
# ----------------------------------------------------------------------
BYTES_POR_CASILLA = 8   # suposición: cada casilla guarda un dato de 8 bytes (un número o una referencia)


def con_puntos(numero):
    """12345 -> '12.345' (separador de miles a la española)."""
    return format(numero, ",").replace(",", ".")


def tabla_memoria():
    """Devuelve el texto de la tabla de memoria con los números reales del campus."""
    tramos = cargar_tramos()
    matriz = GrafoMatriz(CANTIDAD_NODOS, tramos)
    lista = GrafoLista(CANTIDAD_NODOS, tramos)
    disperso = GrafoDisperso(CANTIDAD_NODOS, tramos)

    n = CANTIDAD_NODOS
    a = len(tramos)
    posibles = n * (n - 1) // 2
    lineas = []
    lineas.append("MEMORIA DE LAS TRES REPRESENTACIONES")
    lineas.append("=" * 70)
    lineas.append("Campus: " + str(n) + " puntos y " + str(a) + " tramos.")
    lineas.append("Pares posibles de puntos: " + con_puntos(posibles) + ". Tramos reales: " + str(a)
                  + " (" + str(round(100.0 * a / posibles, 1)) + " % de los posibles).")
    lineas.append("Cada tramo se guarda 2 veces (ida y vuelta): " + str(2 * a) + " entradas.")
    lineas.append("Suposición: cada casilla ocupa " + str(BYTES_POR_CASILLA) + " bytes.")
    lineas.append("La información de cada tramo (distancia, pendiente...) es igual en las tres")
    lineas.append("y se guarda una sola vez, así que no se cuenta aquí.")
    lineas.append("")

    encabezado = "Representación".ljust(22) + "Casillas".rjust(10) + "Bytes".rjust(10) + "  % de la matriz"
    lineas.append(encabezado)
    lineas.append("-" * 70)
    base = matriz.casillas_usadas()
    for nombre, grafo in [("Matriz", matriz), ("Lista de adyacencia", lista), ("Matriz dispersa (CSR)", disperso)]:
        casillas = grafo.casillas_usadas()
        porcentaje = 100.0 * casillas / base
        lineas.append(nombre.ljust(22) + con_puntos(casillas).rjust(10)
                      + con_puntos(casillas * BYTES_POR_CASILLA).rjust(10)
                      + "  " + str(round(porcentaje, 1)) + " %")
    lineas.append("")
    lineas.append("De las " + con_puntos(base) + " casillas de la matriz, solo " + str(matriz.casillas_con_datos())
                  + " tienen un tramo (" + str(round(100.0 * matriz.casillas_con_datos() / base, 1))
                  + " %). El resto son ceros guardados para nada.")
    lineas.append("")

    # Cuántas casillas hay que leer para saber los vecinos de un punto (promedio de los 60 puntos)
    lineas.append("CASILLAS QUE SE LEEN PARA PEDIR LOS VECINOS DE UN PUNTO (promedio)")
    lineas.append("-" * 70)
    for nombre, grafo in [("Matriz", matriz), ("Lista de adyacencia", lista), ("Matriz dispersa (CSR)", disperso)]:
        suma = 0
        for nodo in range(n):
            suma += grafo.casillas_para_vecinos(nodo)
        lineas.append(nombre.ljust(22) + str(round(suma / n, 1)).rjust(6))
    lineas.append("")

    # Qué pasa si el campus crece (mismo promedio de 3 vecinos por punto: tramos = 1,5 x puntos)
    lineas.append("SI EL CAMPUS CRECE (con la misma forma: 1,5 tramos por punto)")
    lineas.append("-" * 70)
    lineas.append("Puntos".rjust(8) + "Matriz (casillas)".rjust(20) + "Lista".rjust(12) + "CSR".rjust(12)
                  + "Matriz en bytes".rjust(18))
    for puntos in [60, 600, 6000, 60000]:
        tramos_aprox = puntos * 3 // 2
        c_matriz = puntos * puntos
        c_lista = puntos + 4 * tramos_aprox
        c_csr = 4 * tramos_aprox + puntos + 1
        lineas.append(con_puntos(puntos).rjust(8) + con_puntos(c_matriz).rjust(20)
                      + con_puntos(c_lista).rjust(12) + con_puntos(c_csr).rjust(12)
                      + con_puntos(c_matriz * BYTES_POR_CASILLA).rjust(18))
    lineas.append("")
    lineas.append("La matriz crece con el CUADRADO de los puntos (n x n); la lista y la dispersa")
    lineas.append("crecen en línea recta con los puntos y los tramos.")
    return "\n".join(lineas)


if __name__ == "__main__":
    texto = tabla_memoria()
    print(texto)
    archivo = open("salida_memoria.txt", "w", encoding="utf-8")
    archivo.write(texto + "\n")
    archivo.close()
