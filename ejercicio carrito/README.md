# Ejercicio Carrito

Ejercicio sencillo del TAD `Carrito` en Python.

## Archivos

- `spec.md`: especificación del comportamiento.
- `carrito_dict.py`: implementación con diccionario.
- `carrito_lista.py`: implementación con lista.
- `test_carrito.py`: pruebas automáticas para las dos implementaciones.
- `menu.py`: programa sencillo para probar el carrito desde la terminal.

## Requisitos

Python 3 y `pytest`.

Instalar pytest:

```bash
python -m pip install pytest
```

## Ejecutar las pruebas

Desde esta carpeta:

```bash
python -m pytest -v
```

## Ejecutar el programa

```bash
python menu.py
```

## Idea principal

Las dos clases implementan el mismo comportamiento. Solo cambia la forma interna de guardar los productos.
