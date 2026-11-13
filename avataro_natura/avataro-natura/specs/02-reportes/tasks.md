# Tareas — Reportes

Plan de referencia: plan.md v1.0 · Especificación: spec.md v1.0

> **En palabras simples:** la lista de pasos pequeños con los que se
> construyó esta pieza. Un paso solo se marca como **Hecha** cuando la
> prueba de su criterio pasa.

| # | Tarea | Criterios | Estado |
|---|-------|-----------|--------|
| T-01 | Errores `ReporteInvalidoError` y `NoHayReportesError`; clase `Reporte` y `Reportes` vacío con `cantidad()` | INV-01 | Hecha |
| T-02 | `reportar` con validación de los tres datos, con pruebas | CA-01, CA-06, CA-07, CA-08, CA-09, CA-11, CA-12 | Hecha |
| T-03 | `atender` y `ver_siguiente` con el orden de llegada, con pruebas | CA-02, CA-03, CA-04, CA-05 | Hecha |
| T-04 | Vaciar la fila y volver a reportar (`_final` en `None`), con pruebas | CA-10, INV-02, INV-03 | Hecha |
| T-05 | Unir con el hilo en `mural.py`: reportar solo comentarios que existen, atender con la decisión de ocultar | CS-02 a CS-08 | Hecha |
| T-06 | Opciones 4 y 5 del menú de consola | CS-09, CS-12 | Hecha |

Regla: una tarea pasa a **Hecha** solo cuando sus criterios tienen una
prueba que pasa (`python -m pytest`).
