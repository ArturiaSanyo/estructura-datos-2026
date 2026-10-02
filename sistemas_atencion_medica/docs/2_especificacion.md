# Especificación (Spec)

## Descripción
Sistema de consola para administrar la atención de pacientes en un centro médico.

## Historias de usuario y criterios de aceptación (HU-CA)

**HU-01: Registrar paciente**
Como recepcionista quiero registrar un paciente para que entre a la cola.
- CA1: Pide nombre y prioridad.
- CA2: No permite nombre vacío ni prioridad inválida.
- CA3: El paciente queda guardado en el archivo.

**HU-02: Definir reglas de priorización**
Como administrador quiero ver las reglas para saber en qué orden se atiende.
- CA1: Muestra las prioridades 1 (Emergencia), 2 (Urgente) y 3 (Normal).

**HU-03: Consultar el siguiente**
Como médico quiero saber quién sigue.
- CA1: Muestra el paciente de menor prioridad; si empatan, el que llegó primero.
- CA2: Si no hay nadie, avisa que la cola está vacía.

**HU-04: Atender paciente**
Como médico quiero atender al siguiente.
- CA1: El paciente sale de la cola y se muestra su información.

**HU-05: Sacar a alguien de la cola**
Como recepcionista quiero retirar un paciente que ya no espera.
- CA1: Se elimina por número de turno.
- CA2: Si el turno no existe, avisa.

**HU-06: Mostrar cuántos faltan**
Como recepcionista quiero ver cuántos faltan.
- CA1: Muestra el total y la lista ordenada.

## Requisitos funcionales (RF)
- RF-01 Registrar pacientes
- RF-02 Definir reglas de priorización
- RF-03 Guardar y cargar datos
- RF-04 Consultar el siguiente
- RF-05 Atender paciente
- RF-06 Sacar de la cola
- RF-07 Mostrar cuántos faltan

## Requisitos no funcionales (RNF)
- RNF-01 Se usa desde la consola con un menú.
- RNF-02 Funciona con Python 3 sin instalar nada extra.
- RNF-03 Código con comentarios y fácil de entender.
- RNF-04 Los datos no se pierden al cerrar el programa.
