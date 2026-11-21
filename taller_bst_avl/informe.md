# Informe — Matrículas indexadas con BST vs AVL

**Autor:** Anwar Joseph

Todos los números salen de `medir.py` (semilla fija 2026, 10.000 números de documento
aleatorios y sin repetir). La salida completa está en `resultados.txt`. Para que el resultado
no dependa de la máquina uso dos medidas: la **altura** (niveles del árbol, vacío = 0) y los
**pasos por búsqueda** (nodos visitados en promedio al buscar cada una de las 10.000 claves).
El tiempo en microsegundos también se reporta, pero varía de una ejecución a otra (por ejemplo, el
BST desordenado dio 0,91 µs en una corrida y 0,49 µs en otra), así que lo tomo solo como referencia.

## Parte A — Reproducir el problema

Se cargaron los 10.000 documentos en un BST de dos maneras: tal como los exporta la oficina de
registro (ordenados) y mezclados al azar. Después se buscó cada documento.

| Escenario | Altura | Pasos por búsqueda | µs por búsqueda |
| --- | ---: | ---: | ---: |
| BST ordenado | 10.000 | 5.000,5 | 123,83 |
| BST desordenado | 31 | 16,0 | 0,53 |
| AVL ordenado | 14 | 12,4 | 0,36 |
| AVL desordenado | 16 | 12,6 | 0,50 |

Con la carga ordenada, el BST tiene tantos niveles como documentos: 10.000. Buscar un documento
cuesta, en promedio, mirar la mitad del árbol (5.000 nodos), unas 400 veces más pasos que en el
AVL y más de 300 veces más tiempo (124 µs contra 0,36 µs). El mismo código, con los mismos datos
mezclados, baja a 31 niveles y 16 pasos. **Por eso las pruebas pasaban**: con pocos datos de
prueba, o desordenados, el árbol se ve bien; el problema solo aparece con el orden real de producción.

## Parte B — Por qué degenera

La inserción en un BST siempre termina en una hoja: se compara con la raíz y se baja a la
izquierda o a la derecha hasta encontrar un hueco. Si los documentos llegan de menor a mayor,
cada documento nuevo es **mayor que todos los que ya están**, así que en cada nodo la respuesta es
«a la derecha», hasta el final. Nunca se usa el lado izquierdo, y cada inserción solo agrega un nivel.

Los primeros siete documentos ordenados son 1102900, 1240010, 1412081, 1459496, 1535665,
1591445 y 1745621. El árbol resultante (altura 7):

```
1102900
   \
   1240010
      \
      1412081
         \
         1459496
            \
            1535665
               \
               1591445
                  \
                  1745621
```

**Se parece a una lista enlazada**: cada nodo tiene un solo hijo, y encontrar el último documento
obliga a recorrerlos todos, igual que buscar en una lista. Se conserva la propiedad de BST, pero se
pierde la ventaja de dividir el espacio a la mitad en cada paso: la búsqueda pasa de O(log n) a O(n).

## Parte C — Resolver con AVL

El AVL (`avl.py`) es el mismo BST con una regla extra: en todo nodo, las alturas de sus dos
subárboles no pueden diferir en más de 1. La altura se guarda en cada nodo y se actualiza en el
camino de vuelta de la inserción; si un nodo queda con balance fuera de [-1, 1] se rota ahí mismo,
con una de las cuatro rotaciones (LL, RR, LR, RL).

Los mismos siete documentos en el AVL dan un árbol perfecto de 3 niveles, con raíz 1459496, hijos
1240010 y 1591445, y las cuatro hojas abajo. Hicieron falta 4 rotaciones simples a la izquierda.

Con los 10.000 documentos ordenados el AVL quedó en **14 niveles** (el mínimo posible es
14, porque log2(10.000) ≈ 13,3) y 12,4 pasos por búsqueda.

**Rotaciones necesarias:**

| Carga | Rotaciones simples | Detalle por caso |
| --- | ---: | --- |
| Ordenada | 9.986 | LL 0, RR 9.986, LR 0, RL 0 |
| Desordenada | 7.102 | LL 1.112, RR 1.176, LR 1.183, RL 1.224 (4.695 reequilibrios; cada doble cuenta 2 rotaciones) |

Con datos ordenados casi cada inserción obliga a una rotación (9.986 de 10.000), y siempre del
mismo tipo (RR): el árbol se desbalancea siempre hacia el mismo lado. Con datos desordenados se
reparte entre los cuatro casos. El costo de rotar es pequeño: cargar 10.000 documentos ordenados tardó
0,04 s en el AVL y 1,7 s en el BST degenerado, porque cada inserción en la lista degenerada recorre toda la cadena.

## Parte D — «¿Por qué no simplemente desordenamos el archivo antes de cargarlo?»

Desordenar arregla la **carga inicial**, pero no el **problema de fondo**: un BST no tiene
ningún mecanismo que lo mantenga equilibrado; su altura depende solamente del orden en que
llegan los datos. Después de la carga inicial, durante el semestre, llegan matrículas extemporáneas y
ese orden ya no lo controlamos nosotros. Un BST inserta siempre en hojas, así que si llega un bloque de
documentos consecutivos (por ejemplo, una cohorte nueva con números de documento seguidos), todos siguen el
mismo camino y forman una cadena colgando de un solo punto del árbol.

Lo medí: cargué los 10.000 documentos **desordenados** (31 niveles) y después inserté 2.000
matrículas extemporáneas de tres maneras:

| Llegada de las 2.000 tardías | Estructura | Altura (antes → después) | Pasos por búsqueda de las tardías | µs por búsqueda de las tardías |
| --- | --- | ---: | ---: | ---: |
| Al azar | BST | 31 → 33 | 18,2 | 0,61 |
| Al azar | AVL | 16 → 16 | 14,0 | 0,54 |
| Bloque creciente por encima del máximo | BST | 31 → 2.009 | 1.009,5 | 27,82 |
| Bloque creciente por encima del máximo | AVL | 16 → 16 | 14,8 | 0,43 |
| Bloque creciente dentro del rango | BST | 31 → 2.018 | 1.018,5 | 24,19 |
| Bloque creciente dentro del rango | AVL | 16 → 16 | 13,4 | 0,34 |

Lo que muestra la medición:

1. **Si las tardías llegaran al azar, desordenar bastaría** (el BST pasó de 31 a 33). El truco de
   desordenar solo funciona bajo el supuesto de que todas las inserciones futuras también serán aleatorias, y
   ese supuesto no lo podemos garantizar.
2. **Con un bloque de documentos consecutivos, el BST se rompe de nuevo**: pasó de 31 a más de 2.000
   niveles, y buscar las matrículas tardías cuesta unos 1.000 pasos, contra unos 14 en el AVL (más de
   cincuenta veces más tiempo). Además, las matrículas más recientes son justo las que el estudiante
   va a consultar al poco de matricularse.
3. **El AVL se mantiene en 16 niveles en los tres casos**, sin importar el orden de llegada: su
   altura nunca supera aproximadamente 1,44·log2(n), por construcción.
4. Aun en el mejor caso, un BST mezclado no es óptimo: 31 niveles frente a 14 del árbol perfecto y 16
   del AVL. La diferencia en pasos promedio es modesta (16,0 contra 12,6); el peligro real no está en la
   carga mezclada sino en que no hay garantía.

Respuesta corta para el jefe de sistemas: desordenar el archivo es un parche que depende de que el
futuro se porte bien. El AVL elimina la causa, porque se equilibra solo con cualquier orden de llegada,
y no hace falta tocar el archivo que entrega la oficina de registro.

## Pruebas y validación

- `test_bst.py` cubre inserción, búsqueda, las tres formas de eliminación (hoja, un hijo, dos hijos),
  y la prueba de que el árbol sigue siendo un BST válido después de borrar un nodo con dos hijos.
  El validador (`es_bst_valido`) revisa **todo el subárbol**, pasando a cada nodo el intervalo
  (mínimo, máximo) heredado de sus ancestros; hay una prueba con un árbol que parece correcto
  mirando solo padre-hijo y que el validador rechaza.
- `test_avl.py` comprueba los cuatro casos de rotación, que la carga ordenada de 127 documentos
  da exactamente 7 niveles y que, con datos aleatorios, se mantienen el orden, las alturas
  guardadas y el balance.
- Ejecuto las 15 pruebas con `python run_tests.py` (en el entorno donde las corrí no estaba `pytest`;
  con pytest instalado, `pytest` las encuentra igual).

## Cómo reproducir

```
python run_tests.py
python medir.py
```
