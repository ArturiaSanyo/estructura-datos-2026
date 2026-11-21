"""Parte D: la misma consulta a las 17:45 y a las 18:15.

A las 18:00 se cierran las puertas de algunos tramos. Esta consulta muestra qué
pasa con una ruta que depende de una de esas puertas.

Se ejecuta con:  python consultas_horario.py     (guarda salida_horarios.txt)
"""
from grafo import construir_grafo, GrafoLista
from busquedas import texto_consulta

grafo = construir_grafo(GrafoLista)

consultas = [
    # (1) Consulta pedida: a las 17:45 hay ruta; a las 18:15 la puerta ya cerró y NO hay ruta.
    ("Portería Principal", "Biblioteca", "17:45"),
    ("Portería Principal", "Biblioteca", "18:15"),
    # (2) Otra consulta: aquí la puerta cerrada obliga a dar un rodeo, pero sí hay ruta.
    ("Portería Principal", "Bloque A Ingeniería", "17:45"),
    ("Portería Principal", "Bloque A Ingeniería", "18:15"),
    # (3) Un error de escritura: la herramienta lo dice, no se queda callada.
    ("Portería Principal", "Biblioteka", "17:45"),
    ("Portería Principal", "Biblioteca", "25:99"),
]

titulos = {
    0: "PARTE D - CONSULTA PEDIDA (antes de que cierre la puerta)",
    1: "PARTE D - CONSULTA PEDIDA (después de que cierra la puerta: no hay ruta accesible)",
    2: "OTRO EJEMPLO - con rodeo (antes del cierre)",
    3: "OTRO EJEMPLO - con rodeo (después del cierre: ruta más larga)",
    4: "CASO DE ERROR - nombre mal escrito",
    5: "CASO DE ERROR - hora inválida",
}

partes = []
for numero in range(len(consultas)):
    origen, destino, hora = consultas[numero]
    partes.append("#" * 70)
    partes.append(titulos[numero])
    partes.append("#" * 70)
    partes.append(texto_consulta(grafo, origen, destino, hora))
    partes.append("")

texto = "\n".join(partes)
print(texto)

archivo = open("salida_horarios.txt", "w", encoding="utf-8")
archivo.write(texto + "\n")
archivo.close()
