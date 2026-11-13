# Tareas — Índice de comentarios

Plan de referencia: plan.md v1.0 · Especificación: spec.md v1.1

> **En palabras simples:** la lista de pasos pequeños con los que se
> construyó esta pieza. Un paso solo se marca como **Hecha** cuando la
> prueba de su criterio pasa.

| # | Tarea | Criterios | Estado |
|---|-------|-----------|--------|
| T-01 | Errores `NumeroInvalidoError` y `NumeroRepetidoError`; clase `NodoIndice` e `Indice` vacío con `cantidad()` | INV-01, CA-07, CA-08 | Hecha |
| T-02 | `agregar` y `buscar` con casilleros y cadenas (sin agrandar todavía), con pruebas | CA-01, CA-03, CA-04, CA-05 | Hecha |
| T-03 | `existe` y validación del número antes de calcular el casillero, con pruebas | CA-02 | Hecha |
| T-04 | `_agrandar`: duplicar los casilleros y reubicar los nodos, con pruebas | CA-06, CA-09, INV-03 | Hecha |
| T-05 | Verificaciones del plan: cadenas cortas, choques y crecimiento | PLAN-01, PLAN-02, PLAN-03 | Hecha |
| T-06 | Medir tiempos con y sin índice y guardar los resultados | PLAN-04 | Hecha |
| T-07 | Integrar el índice al hilo (ver tarea T-08 del componente 01) | CA-13 (del 01) | Hecha |

Regla: una tarea pasa a **Hecha** solo cuando sus criterios tienen una
prueba que pasa (`python -m pytest`).
