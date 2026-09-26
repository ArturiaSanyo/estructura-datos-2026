"""
CARRUSEL DE IMÁGENES - CULTURA DE PORTUGAL
--------------------------------------------
Este programa muestra un carrusel de imágenes usando el concepto
de LISTA CIRCULAR: cuando llegamos al final de la lista, volvemos
al inicio, y cuando estamos en el inicio y retrocedemos, vamos al final.

La "magia" de la lista circular se logra con el operador módulo (%),
que calcula el resto de una división. Ejemplo con una lista de 5 elementos:

    indice = (indice + 1) % 5

Si indice vale 4 (el último) y sumamos 1 -> 5 % 5 = 0 (volvemos al inicio)
"""

import os
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk, ImageDraw, ImageFont

# -----------------------------------------------------------
# PASO 1: Lista circular de datos (imágenes + descripciones)
# -----------------------------------------------------------
# Cada posición de "imagenes" corresponde a la misma posición en "descripciones"
imagenes = [
    "torre_belem.png",
    "pastel_de_nata.png",
    "fado.png",
    "azulejos.png",
    "cristo_rei.png",
]

descripciones = [
    "Torre de Belém\nMonumento histórico en Lisboa",
    "Pastel de Nata\nDulce típico portugués",
    "Fado\nMúsica tradicional de Portugal",
    "Azulejos\nArte típico de la cerámica portuguesa",
    "Cristo Rei\nEstatua monumental en Lisboa",
]

colores = ["#2E6F95", "#C97B3D", "#5B4B8A", "#2F8F5B", "#B23A48"]

# Índice que indica en qué imagen estamos actualmente
indice_actual = 0


def crear_imagenes_de_ejemplo():
    """
    Crea imágenes de ejemplo con colores y texto si aún no existen.
    Esto es solo para que el programa funcione de inmediato.
    Más adelante puedes reemplazar estos archivos .png por fotos reales.
    """
    for nombre, texto, color in zip(imagenes, descripciones, colores):
        if not os.path.exists(nombre):
            img = Image.new("RGB", (400, 300), color)
            dibujo = ImageDraw.Draw(img)
            titulo = texto.split("\n")[0]
            dibujo.text((30, 130), titulo, fill="white")
            img.save(nombre)


# -----------------------------------------------------------
# PASO 2: Funciones que mueven el índice de forma circular
# -----------------------------------------------------------
def siguiente_imagen():
    global indice_actual
    # Al llegar al final de la lista, el % nos regresa al inicio (posición 0)
    indice_actual = (indice_actual + 1) % len(imagenes)
    mostrar_imagen()


def imagen_anterior():
    global indice_actual
    # Al estar en la posición 0 y retroceder, el % nos manda al final
    indice_actual = (indice_actual - 1) % len(imagenes)
    mostrar_imagen()


def mostrar_imagen():
    """Actualiza la imagen y el texto que se ven en la ventana."""
    ruta = imagenes[indice_actual]
    imagen = Image.open(ruta)
    imagen = imagen.resize((400, 300))
    foto = ImageTk.PhotoImage(imagen)

    etiqueta_imagen.config(image=foto)
    etiqueta_imagen.image = foto  # referencia para que no se borre de memoria
    etiqueta_texto.config(text=descripciones[indice_actual])


# -----------------------------------------------------------
# PASO 3: Construcción de la ventana (interfaz gráfica)
# -----------------------------------------------------------
crear_imagenes_de_ejemplo()

ventana = Tk()
ventana.title("Carrusel - Cultura de Portugal")
ventana.geometry("450x450")
ventana.config(bg="white")

etiqueta_imagen = Label(ventana, bg="white")
etiqueta_imagen.pack(pady=15)

etiqueta_texto = Label(ventana, text="", font=("Arial", 13), bg="white", justify="center")
etiqueta_texto.pack(pady=10)

boton_anterior = Button(ventana, text="<< Anterior", command=imagen_anterior, width=12)
boton_anterior.pack(side="left", padx=40, pady=20)

boton_siguiente = Button(ventana, text="Siguiente >>", command=siguiente_imagen, width=12)
boton_siguiente.pack(side="right", padx=40, pady=20)

mostrar_imagen()  # Mostrar la primera imagen al abrir el programa
ventana.mainloop()
