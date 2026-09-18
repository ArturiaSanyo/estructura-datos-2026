# CONSTITUTION — Actividad 3

## Principios

### 1. Contrato primero

La estructura enlazada debe cumplir el mismo contrato funcional que la estructura de arreglo.

### 2. Estructura auténtica

La lista enlazada almacena sus elementos mediante objetos `Nodo` conectados por referencias `siguiente`. No se utiliza una lista de Python como almacenamiento oculto.

### 3. Casos extremos obligatorios

Toda implementación debe contemplar explícitamente:

- vacío;
- un elemento;
- eliminación del primero;
- eliminación del último.

### 4. Evidencia antes de recomendar

La elección de estructura se realiza a partir de las frecuencias proporcionadas, el costo teórico y las mediciones. No se decide solamente por la intuición de que las listas enlazadas son mejores para insertar.

### 5. Reproducibilidad

Las pruebas y mediciones deben poder ejecutarse mediante comandos documentados y sin dependencias externas.

### 6. Separación de responsabilidades

La implementación, las pruebas, la comparación y la documentación se mantienen en archivos separados para facilitar la revisión.
