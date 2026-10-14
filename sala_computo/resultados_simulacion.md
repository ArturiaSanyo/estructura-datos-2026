# Resultados de la simulacion (semilla 42, 77 trabajos)

Cada trabajo tarda 2 unidades. Tiempos en unidades de tiempo.

| Escenario | Nivel | Trabajos | Espera media | Peor espera |
|---|---|---|---|---|
| 1. Sin envejecimiento | ALTA | 33 | 1.4 | 4 |
| 1. Sin envejecimiento | MEDIA | 22 | 16.6 | 41 |
| 1. Sin envejecimiento | BAJA | 22 | 77.2 | 104 |
| 1. Sin envejecimiento | **TODOS** | 77 | **27.4** | **104** |
| 2. Con envejecimiento (limite 20) | ALTA | 33 | 9.1 | 30 |
| 2. Con envejecimiento (limite 20) | MEDIA | 22 | 25.3 | 43 |
| 2. Con envejecimiento (limite 20) | BAJA | 22 | 56.9 | 70 |
| 2. Con envejecimiento (limite 20) | **TODOS** | 77 | **27.4** | **70** |

## Que muestra la tabla

- El tiempo medio general es igual (27.4): atender los mismos trabajos con un solo
  servidor tarda lo mismo en total; el envejecimiento solo cambia **quien espera**.
- El **peor tiempo de espera baja de 104 a 70**: sin envejecimiento, un trabajo de
  prioridad BAJA espero mas de 100 unidades. Con envejecimiento nadie queda
  olvidado.
- El precio: los trabajos ALTA esperan mas (de 1.4 a 9.1 en promedio), porque
  ahora los viejos les pasan por delante.
