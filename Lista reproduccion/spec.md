# SPEC — Actividad 3: Lista enlazada

## Objetivo

Construir una implementación de lista enlazada simple que cumpla el mismo contrato de la lista de arreglo y comparar ambas estructuras usando las frecuencias reales del reproductor universitario.

## Alcance

Se implementan:

- `Nodo`.
- `ListaEnlazada`.
- `ListaArreglo`.
- Pruebas del contrato.
- Pruebas de cuatro casos extremos.
- Construcción manual de tres nodos.
- Medición de cuatro operaciones.
- Análisis de costo diario.
- Recomendación condicionada por las frecuencias.

## Contrato común

Ambas listas deben proporcionar:

- `esta_vacia()`
- `tamano()`
- `insertar_al_principio(dato)`
- `insertar_al_final(dato)`
- `obtener(indice)`
- `recorrer()`
- `ir_a(indice)`
- `borrar_actual()`

## Reglas

1. Una lista recién creada está vacía.
2. El tamaño coincide con la cantidad de elementos almacenados.
3. Los elementos se conservan en el orden de inserción.
4. `insertar_al_principio` coloca el dato como primer elemento.
5. `insertar_al_final` coloca el dato como último elemento.
6. `obtener` devuelve el elemento de la posición indicada.
7. `recorrer` visita todos los elementos desde el primero hasta el último.
8. `ir_a` establece la canción actual y devuelve su dato.
9. `borrar_actual` elimina la canción actual y devuelve el dato eliminado.
10. Un índice inválido produce `IndexError`.
11. No se permite almacenar los datos de `ListaEnlazada` en una lista de Python.
12. `ListaEnlazada` debe usar nodos y referencias `siguiente`.
13. La medición se realiza con 5.000 canciones.

## Casos límite

- Lista vacía.
- Lista de un elemento.
- Borrar el primero.
- Borrar el último.
- Borrar el único elemento.

## Criterios de aceptación

- Todas las pruebas del contrato pasan para ambas implementaciones.
- Las pruebas específicas de extremos pasan.
- `ListaEnlazada` no usa `list` de Python como almacenamiento interno.
- La comparación contiene costo teórico, medición y análisis basado en las frecuencias dadas.
