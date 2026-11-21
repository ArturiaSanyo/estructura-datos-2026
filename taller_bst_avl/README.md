# Taller: matrículas con BST y AVL

Autor: Anwar Joseph

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| `bst.py` | Árbol binario de búsqueda: insertar, buscar y eliminar (hoja, un hijo, dos hijos), más el validador de todo el subárbol. |
| `avl.py` | Árbol AVL con las cuatro rotaciones (LL, RR, LR, RL) y la altura actualizada en el camino de vuelta. |
| `test_bst.py` | Pruebas del BST, incluida la prueba de que sigue siendo BST válido tras borrar un nodo con dos hijos. |
| `test_avl.py` | Pruebas del AVL. |
| `run_tests.py` | Corre todas las pruebas (no necesita instalar nada). |
| `medir.py` | Hace el experimento y muestra las alturas, los pasos y los tiempos. |
| `resultados.txt` | Lo que salió al correr `medir.py`. |
| `informe.md` | Informe con la tabla comparativa, el dibujo del árbol degenerado y la respuesta al jefe de sistemas. |

## Cómo correrlo

Solo hace falta Python 3 (sin instalar nada más). Desde la carpeta del proyecto:

```
python run_tests.py
python medir.py
```

`medir.py` tarda cerca de un minuto, casi todo en el BST con documentos ordenados.
