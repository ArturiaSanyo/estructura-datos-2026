# Tareas — Hilo de comentarios

Plan de referencia: plan.md v2.0 · Especificación: spec.md v1.1

> **En palabras simples:** la lista de pasos pequeños con los que se
> construyó esta pieza. Un paso solo se marca como **Hecha** cuando la
> prueba de su criterio pasa.

| # | Tarea | Criterios | Estado |
|---|-------|-----------|--------|
| T-01 | `errores.py`, clase `Nodo` y `Hilo` vacío con `cantidad()` y `mostrar()` | CA-10, INV-01 | Hecha |
| T-02 | `comentar` con validación de autor y texto, con pruebas | CA-01, CA-02, CA-07, CA-08, CA-11 | Hecha |
| T-03 | `responder` con búsqueda del padre, con pruebas | CA-03, CA-06, CA-12 | Hecha |
| T-04 | `mostrar` en preorden con sangría, con pruebas | CA-04, CA-05 | Hecha |
| T-05 | Nivel máximo en `responder`, con pruebas | CA-09, INV-03 | Hecha |
| T-06 | Menú de consola en `main.py` | CS-01 (ver 99-sistema) | Hecha |
| T-07 | `existe` y `ocultar`, aviso de oculto en `mostrar`, con pruebas (spec 1.1) | CA-13, CA-14, CA-15, CA-16, CA-17 | Hecha |
| T-08 | Cambiar la búsqueda por recorrido por el índice (plan 2.0) y quitar `_buscar`; todas las pruebas anteriores deben seguir pasando sin tocarlas | CA-03, CA-06, CA-12, CA-13, CA-15 | Hecha |

Regla: una tarea pasa a **Hecha** solo cuando sus criterios tienen una
prueba que pasa (`python -m pytest`).
