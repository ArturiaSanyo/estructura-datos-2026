"""Dibuja el mapa del campus en mapa_campus.png (necesita matplotlib: pip install matplotlib).
Es opcional: el resto del proyecto no lo necesita."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from grafo import NOMBRES, TIPOS, X, Y, cargar_tramos

tramos = cargar_tramos()
figura, ejes = plt.subplots(figsize=(17, 10.5))

for tramo in tramos:
    xs = [X[tramo.a], X[tramo.b]]
    ys = [Y[tramo.a], Y[tramo.b]]
    if not tramo.accesible and tramo.motivo == "tramo en obra":
        ejes.plot(xs, ys, color="#e08a00", linewidth=3, linestyle="-.", zorder=1)
    elif not tramo.accesible:
        ejes.plot(xs, ys, color="#d62728", linewidth=2.5, linestyle="--", zorder=1)
    elif tramo.cierra is not None:
        ejes.plot(xs, ys, color="#1f77b4", linewidth=3.5, linestyle=":", zorder=1)
    elif tramo.pendiente > 8:
        ejes.plot(xs, ys, color="#6b8e23", linewidth=4, zorder=1)
    else:
        ejes.plot(xs, ys, color="#2ca02c", linewidth=2, zorder=1)

colores = {"edificio": "#4c72b0", "entrada": "#c44e52", "cruce": "#bbbbbb", "servicio": "#dd8452",
           "deporte": "#55a868", "plazoleta": "#8172b3", "parqueadero": "#937860",
           "transporte": "#da8bc3", "ascensor": "#17becf"}
for i in range(len(NOMBRES)):
    tam = 140 if TIPOS[i] == "cruce" else 330
    ejes.scatter(X[i], Y[i], s=tam, color=colores[TIPOS[i]], edgecolor="black", zorder=3)
    ejes.text(X[i], Y[i], str(i), ha="center", va="center", fontsize=7 if TIPOS[i] == "cruce" else 8,
              color="black" if TIPOS[i] == "cruce" else "white", zorder=4, fontweight="bold")

# Leyenda
from matplotlib.lines import Line2D
elementos = [
    Line2D([0], [0], color="#2ca02c", lw=2, label="Tramo accesible"),
    Line2D([0], [0], color="#6b8e23", lw=4, label="Accesible pero empinado (más de 8 %): cuesta 2,5 veces"),
    Line2D([0], [0], color="#1f77b4", lw=3.5, ls=":", label="Accesible con puerta que cierra (ver modelo.md)"),
    Line2D([0], [0], color="#d62728", lw=2.5, ls="--", label="No accesible (escaleras o pendiente excesiva)"),
    Line2D([0], [0], color="#e08a00", lw=3, ls="-.", label="Tramo en obra"),
]
ejes.legend(handles=elementos, loc="upper left", bbox_to_anchor=(0.0, -0.09), ncol=3, fontsize=9, frameon=False)
ejes.set_title("Campus de ejemplo: 60 puntos y 90 tramos (los números se explican en modelo.md)", fontsize=13)
ejes.set_xlabel("metros hacia el oriente")
ejes.set_ylabel("metros hacia el norte")
ejes.set_aspect("equal")
ejes.grid(alpha=0.2)
figura.tight_layout()
figura.savefig("mapa_campus.png", dpi=110, bbox_inches="tight")
print("Mapa guardado en mapa_campus.png")
