# Actividad 3 — Lista enlazada

Proyecto completo de la actividad sobre comparación entre `ListaArreglo` y `ListaEnlazada`.

## Requisitos

- Python 3.10 o superior.
- No requiere paquetes externos.

## Ejecutar pruebas

Desde esta carpeta:

```bash
python -m unittest discover -v
```

## Ejecutar la comparación

```bash
python comparacion.py
```

La comparación utiliza una lista de 5.000 canciones y mide las cuatro operaciones solicitadas.

## Archivos

- `lista_arreglo.py`: implementación secuencial.
- `lista_enlazada.py`: implementación con nodos y enlaces.
- `test_lista_arreglo.py`: pruebas del contrato del arreglo.
- `test_lista_enlazada.py`: mismas pruebas para la lista enlazada.
- `test_extremos.py`: cuatro casos límite.
- `nodos_a_mano.md`: Parte A.
- `comparacion.py`: medición de las cuatro operaciones.
- `comparacion.md`: análisis y recomendación.
- `spec.md`, `plan.md`, `task.md`, `constitution.md`: artefactos SDD.
