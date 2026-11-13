# Especificación — Reportes

**Versión:** 1.0 · **Fecha:** 2026-11-11 · **Autor:** Anwar Joseph

> **En palabras simples:** cuando alguien ve un comentario ofensivo, lo
> reporta. Los reportes se van guardando y la administración los revisa
> de uno en uno, empezando por el que llegó primero, como en la fila de
> un banco: quien llegó antes se atiende antes.

## 1. Propósito

Guardar los reportes de comentarios inadecuados y entregarlos a la
administración en el mismo orden en que llegaron. Cubre HU-05 y la parte de
HU-06 que ordena los reportes.

## 2. Fuera de alcance

- Comprobar que el comentario reportado existe (lo hace el sistema; ver
  `99-sistema/spec.md`). Este componente solo guarda reportes.
- Decidir qué pasa con el comentario reportado (ocultarlo o dejarlo).
- Detectar reportes repetidos de la misma persona.
- Reportes por urgencia o gravedad: todos esperan su turno por igual.
- Guardar en disco.

## 3. Reglas generales

- Cada reporte tiene cuatro datos: **número del reporte**, **número del
  comentario reportado**, **quién reporta** y **motivo**.
- El número del reporte lo asigna este componente: el primero es 1 y cada
  reporte nuevo recibe el siguiente. Nunca se repite ni se salta, aunque
  los reportes anteriores ya se hayan atendido.
- El número del comentario reportado debe ser un número entero mayor que 0
  (1, 2, 3...). El 0, los negativos, los decimales y el texto no valen.
- Quien reporta y el motivo son **vacíos** si no tienen caracteres o solo
  tienen espacios.
- Si una operación falla, todo queda exactamente como estaba.
- Un mismo comentario se puede reportar más de una vez, incluso por la misma
  persona. Cada intento es un reporte distinto y se atiende por separado.

## 4. Operaciones

### `reportar(numero_comentario, reportante, motivo)`
- **Precondiciones:** `numero_comentario` es un entero mayor que 0;
  `reportante` y `motivo` no son vacíos
- **Postcondiciones:** existe un reporte nuevo que será el último en
  atenderse; la cantidad de reportes pendientes aumenta en 1
- **Devuelve:** el número del reporte nuevo
- **Errores:** `ReporteInvalidoError` si alguna precondición no se cumple

### `ver_siguiente()`
- **Precondiciones:** hay al menos un reporte pendiente
- **Postcondiciones:** nada cambia
- **Devuelve:** el reporte más antiguo, sin sacarlo de los pendientes
- **Errores:** `NoHayReportesError` si no hay reportes pendientes

### `atender()`
- **Precondiciones:** hay al menos un reporte pendiente
- **Postcondiciones:** el reporte más antiguo deja de estar pendiente; la
  cantidad baja en 1
- **Devuelve:** ese reporte, con sus cuatro datos
- **Errores:** `NoHayReportesError` si no hay reportes pendientes

### `cantidad()`
- **Devuelve:** cuántos reportes están pendientes

## 5. Invariantes

- INV-01: la cantidad de reportes pendientes es >= 0 en todo momento
- INV-02: los reportes se entregan en el mismo orden en que se recibieron
- INV-03: los números de reporte son únicos y crecientes; un número
  atendido no se vuelve a usar

## 6. Criterios de aceptación

| ID | Criterio | Verificable mediante |
|----|----------|----------------------|
| CA-01 | El primer reporte recibe el número 1 y la cantidad pasa a 1 | test_reportar_primero |
| CA-02 | Los reportes se atienden en el mismo orden en que se hicieron | test_atender_en_orden |
| CA-03 | Atender sin reportes pendientes lanza `NoHayReportesError` | test_atender_vacio |
| CA-04 | `ver_siguiente` devuelve el reporte más antiguo sin sacarlo: la cantidad no cambia y `atender` devuelve el mismo reporte | test_ver_siguiente |
| CA-05 | `ver_siguiente` sin reportes pendientes lanza `NoHayReportesError` | test_ver_siguiente_vacio |
| CA-06 | Un `reportante` vacío o de solo espacios lanza `ReporteInvalidoError` y la cantidad no cambia | test_reportante_vacio |
| CA-07 | Un `motivo` vacío o de solo espacios lanza `ReporteInvalidoError` y la cantidad no cambia | test_motivo_vacio |
| CA-08 | Un número de comentario que no sea un entero mayor que 0 (0, -3, 2.5, "7", True) lanza `ReporteInvalidoError` y la cantidad no cambia | test_numero_comentario_invalido |
| CA-09 | Un reporte fallido no consume número: el siguiente reporte recibe el que correspondía | test_error_no_consume_numero |
| CA-10 | Después de atender todos los reportes se puede volver a reportar, el orden se conserva y el número continúa | test_reportar_despues_de_vaciar |
| CA-11 | Reportar dos veces el mismo comentario genera dos reportes que se atienden por separado | test_mismo_comentario_dos_veces |
| CA-12 | El reporte atendido trae los cuatro datos tal como se registraron | test_reporte_trae_sus_datos |

## 7. Casos extremos considerados

- Sin reportes · un solo reporte · atender el último y volver a reportar
- Reporte con número de comentario inválido (0, negativo, decimal, texto, verdadero/falso)
- Quien reporta o motivo con solo espacios
- El mismo comentario reportado varias veces
- Mirar el siguiente reporte sin atenderlo

## 8. Historial de cambios

| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 2026-11-11 | Versión inicial | Entrega 2: HU-05 y HU-06 |
