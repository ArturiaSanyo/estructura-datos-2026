"""
CARRUSEL DE IMÁGENES - CULTURA DE PORTUGAL (Python + tkinter)
-----------------------------------------------------------------
Este programa carga imágenes que ya tienes guardadas en tu carpeta
"imagenes_portugal". No necesita internet para nada.

IMPORTANTE: este programa abre una ventana gráfica, así que debes
ejecutarlo en tu propia computadora (con pantalla). No funcionará
dentro de un Codespace o servidor sin interfaz gráfica.

LISTA CIRCULAR:
Usamos una lista (array) normal + un índice que se mueve con el
operador módulo (%). Así, al llegar al final volvemos al inicio,
y al estar en el inicio y retroceder, vamos al final.

    indice = (indice + 1) % len(lista)   -> avanzar
    indice = (indice - 1) % len(lista)   -> retroceder
"""

from tkinter import Tk, Label, Button
from PIL import Image, ImageTk

# -----------------------------------------------------------
# PASO 1: Lista circular de datos.
# Cada elemento apunta a una imagen dentro de la carpeta
# "imagenes_portugal" (debe estar junto a este archivo .py)
# -----------------------------------------------------------
imagenes = [
    {
        "archivo": "imagenes_portugal/festa_campinos_santarem.jpg",
        "titulo": "Festa dos Campinos - Santarém",
        "descripcion": "Jinetes tradicionales (campinos) del Ribatejo, guiando ganado."
    },
    {
        "archivo": "imagenes_portugal/festa_campinos_ribatejo.jpg",
        "titulo": "Fiesta tradicional del Ribatejo",
        "descripcion": "Desfile a caballo típico de las fiestas populares portuguesas."
    },
    {
        "archivo": "imagenes_portugal/palacio_pena_sintra.jpg",
        "titulo": "Palacio da Pena",
        "descripcion": "Palacio del siglo XIX en Sintra, Patrimonio de la Humanidad."
    },
    {
        "archivo": "imagenes_portugal/porto_rio_duero.jpg",
        "titulo": "Oporto y el río Duero",
        "descripcion": "Vista de la ciudad de Oporto a orillas del río Duero."
    },
    {
        "archivo": "imagenes_portugal/puente_dom_luis_porto.jpg",
        "titulo": "Puente Dom Luís I",
        "descripcion": "Icónico puente de hierro que conecta Oporto y Vila Nova de Gaia."
    },
    {
        "archivo": "imagenes_portugal/pozo_iniciatico_sintra.jpg",
        "titulo": "Pozo Iniciático - Quinta da Regaleira",
        "descripcion": "Torre subterránea en espiral, en Sintra."
    },
    {
        "archivo": "imagenes_portugal/convento_cristo_tomar.jpg",
        "titulo": "Convento de Cristo",
        "descripcion": "Antiguo monasterio en Tomar, fundado por la Orden del Temple."
    },
    {
        "archivo": "imagenes_portugal/tranvia_lisboa.jpg",
        "titulo": "Tranvía 28",
        "descripcion": "El famoso tranvía amarillo que recorre las calles de Lisboa."
    },
]

# Índice que indica en qué imagen estamos ahora mismo
indice_actual = 0


# -----------------------------------------------------------
# PASO 2: Función que dibuja en pantalla la imagen actual
# -----------------------------------------------------------
def mostrar_imagen():
    item = imagenes[indice_actual]

    imagen = Image.open(item["archivo"]).resize((400, 300))
    foto = ImageTk.PhotoImage(imagen)

    etiqueta_imagen.config(image=foto)
    etiqueta_imagen.image = foto  # referencia para que no se borre de memoria
    etiqueta_texto.config(text=f"{item['titulo']}\n{item['descripcion']}")
    etiqueta_contador.config(text=f"{indice_actual + 1} de {len(imagenes)}")


# -----------------------------------------------------------
# PASO 3: Lista circular con el operador módulo (%)
# -----------------------------------------------------------
def siguiente_imagen():
    global indice_actual
    # Al llegar al final de la lista, el % nos regresa al inicio
    indice_actual = (indice_actual + 1) % len(imagenes)
    mostrar_imagen()


def imagen_anterior():
    global indice_actual
    # Al estar en el inicio y retroceder, el % nos manda al final
    indice_actual = (indice_actual - 1) % len(imagenes)
    mostrar_imagen()


# -----------------------------------------------------------
# PASO 4: Construcción de la ventana (interfaz gráfica)
# -----------------------------------------------------------
ventana = Tk()
ventana.title("Carrusel - Cultura de Portugal")
ventana.geometry("450x480")
ventana.config(bg="white")

etiqueta_imagen = Label(ventana, bg="white")
etiqueta_imagen.pack(pady=15)

etiqueta_texto = Label(ventana, text="", font=("Arial", 13), bg="white", justify="center")
etiqueta_texto.pack(pady=10)

etiqueta_contador = Label(ventana, text="", font=("Arial", 10), bg="white", fg="#888")
etiqueta_contador.pack()

boton_anterior = Button(ventana, text="<< Anterior", command=imagen_anterior, width=12)
boton_anterior.pack(side="left", padx=40, pady=20)

boton_siguiente = Button(ventana, text="Siguiente >>", command=siguiente_imagen, width=12)
boton_siguiente.pack(side="right", padx=40, pady=20)

mostrar_imagen()  # Mostrar la primera imagen al abrir el programa
ventana.mainloop()
