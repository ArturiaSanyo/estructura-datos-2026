# Taller: rutas accesibles en el campus

**Autor:** Anwar Joseph

Herramienta que calcula la ruta accesible de menor esfuerzo entre dos puntos de un campus, teniendo en cuenta
escaleras, obras, pendientes y puertas que cierran a cierta hora.

> El campus incluido es un **campus de ejemplo** (60 puntos, 90 tramos, datos inventados pero coherentes).
> Para usar uno real, cambia solo `campus.py`.

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| `modelo.md` | **Parte A.** Qué es un nodo, qué es un tramo, qué datos lleva, cómo se calcula el costo, y el mapa del campus. |
| `grafo.py` | **Parte B.** Las tres representaciones (matriz, lista y matriz dispersa) y la tabla de memoria con los números del campus. |
| `busquedas.py` | **Parte C.** BFS, DFS y A*, y la tabla de nodos explorados por cada uno. |
| `heuristica.md` | **Parte C.** La heurística de A* y la demostración de que es admisible. |
| `consultas_horario.py` | **Parte D.** La consulta a las 17:45 y a las 18:15, incluido el caso sin ruta accesible. |
| `campus.py` | Los datos del campus (puntos y tramos). Es el único archivo que hay que cambiar para otro campus. |
| `verificar_heuristica.py` | Comprueba con los 3.540 pares de puntos que la heurística nunca sobreestima. |
| `pruebas.py` | Pruebas automáticas. |
| `dibujar_mapa.py` | Redibuja `mapa_campus.png` (opcional, necesita matplotlib). |
| `salida_memoria.txt` | Salida de `python grafo.py`: tabla de memoria. |
| `salida_busquedas.txt` | Salida de `python busquedas.py`: nodos explorados por BFS, DFS y A*. |
| `salida_horarios.txt` | Salida de `python consultas_horario.py`: consultas de las 17:45 y las 18:15. |
| `salida_heuristica.txt` | Salida de `python verificar_heuristica.py`. |
| `mapa_campus.png` | Mapa del campus. |

## Cómo correrlo

Solo hace falta Python 3. Desde la carpeta del proyecto:

```
python grafo.py                    # tabla de memoria
python busquedas.py                # nodos explorados por BFS, DFS y A*  (unos segundos)
python consultas_horario.py        # consultas de las 17:45 y las 18:15
python verificar_heuristica.py     # demostración con números de que la heurística es admisible
python pruebas.py                  # pruebas automáticas
```

## Resumen de resultados

- **Representación elegida: lista de adyacencia.** El campus tiene 60 puntos y 90 tramos, el 5,1 % de los 1.770 pares
  posibles. La matriz usa 3.600 casillas (28.800 bytes) y solo 180 tienen algo; la lista usa 420 (3.360 bytes), el 11,7 %.
  La matriz dispersa usa 421, casi igual que la lista.
- **A* explora en promedio 16,6 puntos; BFS y DFS, 31,0.** Además es el único que siempre da la ruta de menor costo.
- **A las 17:45** hay ruta accesible de la Portería Principal a la Biblioteca (6 tramos, 435 m). **A las 18:15** la puerta
  de la Plazoleta Central ya cerró y la herramienta responde que **no existe ruta accesible**, explicando por qué.
