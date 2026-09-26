# Constitución — Actividad 3 (Listas)

Estas son las reglas que no se rompen en ningún momento de esta actividad. Cada una existe para que el ejercicio realmente enseñe algo (no son caprichos):

1. **El archivo de pruebas de la Actividad 2 (`test_lista_arreglo.py`) no se modifica.**
   Si `ListaEnlazada` no lo pasa, el error está en la implementación de `ListaEnlazada` o en que el contrato original estaba mal escrito — no se arregla cambiando la prueba.

2. **`ListaEnlazada` no usa `list` de Python por dentro.**
   Guardar los datos en una lista de Python y solo "envolverla" no es construir una lista enlazada. Los datos viven en `Nodo`s conectados por `siguiente`.

3. **La recomendación de la Parte D sale de los números, no de la intuición.**
   No vale decir "las enlazadas son mejores para insertar" sin más: hay que multiplicar frecuencia real × costo medido y sumar, para las dos estructuras.

4. **Mismo contrato, dos implementaciones.**
   `ListaArreglo` y `ListaEnlazada` deben comportarse exactamente igual desde afuera (mismos métodos, mismos resultados, mismos errores), aunque por dentro sean completamente distintas.
