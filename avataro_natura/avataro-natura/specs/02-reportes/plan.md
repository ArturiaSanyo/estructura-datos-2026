# Plan técnico — Reportes

**Especificación de referencia:** spec.md v1.0 · **Versión del plan:** 1.0

> **En palabras simples:** los reportes se guardan como una cadena de
> eslabones, en el orden en que llegaron. El programa recuerda cuál es el
> primer eslabón (el más antiguo) y cuál es el último (el más nuevo).
> Para atender, se saca el primero. Para reportar, se pega uno nuevo al
> final. Ninguna de las dos operaciones necesita recorrer la cadena, por
> eso son rápidas sin importar cuántos reportes haya.
> **O(1)** = tarda lo mismo con 5 reportes que con 5 000.

## 1. Estructura de datos elegida

**Cola enlazada** con una referencia al frente (`_frente`, el reporte más
antiguo) y otra al final (`_final`, el más nuevo). Cada `Reporte` guarda
sus cuatro datos y una referencia `siguiente` al reporte que llegó justo
después. El mismo objeto `Reporte` sirve como eslabón de la cadena.

Las dos referencias hacen que **reportar** (pegar al final) y **atender**
(sacar del frente) cuesten O(1).

No se usa ninguna `list`, `dict` ni `deque` (constitución, principio 1).

## 2. Alternativas consideradas

| Alternativa | Ventaja | Por qué se descartó |
|-------------|---------|---------------------|
| Arreglo dinámico (`list` de Python) | Muy fácil de escribir | Sacar del inicio obliga a correr todos los elementos: O(n). Además viola la constitución (principio 1) |
| Cola enlazada con solo el frente | Un poco menos de código | Pegar al final exige recorrer toda la cadena: O(n) |
| Pila (el último que llega sale primero) | Muy simple | Entrega el orden al revés: HU-06 pide atender primero lo más antiguo |
| Cola circular de tamaño fijo | O(1) y poca memoria | Hay que fijar un máximo de reportes de antemano; si se llena, hay que rechazar o reorganizar |
| Cola de prioridad (montículo) | Permitiría atender por urgencia | No se necesita: todos los reportes esperan su turno por igual. Si más adelante se pide urgencia, cambia el plan, no la spec |

## 3. Complejidad esperada

| Operación | Tiempo | Espacio | Justificación |
|-----------|--------|---------|---------------|
| `reportar` | O(1) | O(1) | Se pega un eslabón nuevo después de `_final` |
| `ver_siguiente` | O(1) | O(1) | Se mira `_frente` |
| `atender` | O(1) | O(1) | Se saca `_frente` y se avanza al siguiente |
| `cantidad` | O(1) | O(1) | Se guarda un contador |

Memoria total del componente: O(n), un eslabón por reporte pendiente.

## 4. Diseño interno

- `_frente`: el reporte más antiguo (o `None` si no hay ninguno)
- `_final`: el reporte más nuevo (o `None` si no hay ninguno)
- `_cantidad`: contador de reportes pendientes
- `_ultimo_numero`: último número de reporte entregado; solo avanza cuando
  el reporte se creó sin error
- Al sacar un reporte, su referencia `siguiente` se borra (`None`) para que
  el reporte entregado no arrastre al resto de la fila
- **Invariante de representación:** `_cantidad` = número de reportes
  alcanzables desde `_frente`; si `_frente` es `None`, entonces `_final`
  también es `None` y `_cantidad` es 0; el `siguiente` de `_final` es `None`

## 5. Riesgos técnicos

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Al sacar el último reporte, olvidar poner `_final` en `None`; el siguiente reporte se pegaría a un eslabón viejo y se perdería | Alto | Prueba CA-10 (vaciar y volver a reportar) |
| Gastar un número de reporte cuando la operación falla | Medio | Validar todo antes de incrementar `_ultimo_numero` (CA-09) |
| Aceptar `True` como número de comentario porque en Python `True` vale 1 | Medio | Comprobar el tipo exacto (`type(x) is int`) y probar con `True` (CA-08) |
| Entregar un reporte que todavía apunta al siguiente | Bajo | Borrar `siguiente` al atender |

## 6. Historial de cambios del plan

| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 2026-11-11 | Versión inicial | Entrega 2 |
