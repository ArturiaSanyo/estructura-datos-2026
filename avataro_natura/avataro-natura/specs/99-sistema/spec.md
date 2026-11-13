# Especificación del sistema — Avataro Natura

**Versión:** 1.0 · **Fecha:** 2026-11-11 · **Autor:** Anwar Joseph

> **En palabras simples:** Avataro Natura es un mural donde la gente de
> Medellín conversa sobre actividades ambientales (sembrar árboles, limpiar
> quebradas...). Cualquiera puede opinar y responder; si alguien ve algo
> ofensivo, lo reporta; y la administración revisa los reportes uno por uno,
> el más antiguo primero, y decide si oculta el comentario. Esta página
> explica cómo encajan las tres piezas del programa.

## 1. Propósito

Mural de opiniones para actividades ambientales de Medellín: la gente
comenta y responde, y la administración modera. Esta especificación
describe el sistema completo y cómo encajan los contratos de cada
componente.

## 2. Componentes y contratos

| # | Componente | Qué promete al resto del sistema | Spec |
|---|------------|----------------------------------|------|
| 01 | Hilo de comentarios | Dar un número a cada comentario, mostrar la conversación en orden, decir si un número existe y ocultar un comentario | `01-hilo-comentarios/spec.md` (v1.1) |
| 02 | Reportes | Entregar los reportes en el orden en que llegaron | `02-reportes/spec.md` (v1.0) |
| 03 | Índice de comentarios | Decir rápido si un número existe y a qué comentario corresponde | `03-indice-comentarios/spec.md` (v1.1) |

Cómo encajan (en lenguaje cotidiano):

- El **hilo** da un número a cada comentario nuevo y lo anota en el **índice**.
  Gracias al índice, el hilo encuentra cualquier comentario por su número
  sin recorrer toda la conversación. El índice no se ofrece a las personas:
  solo lo usa el hilo.
- Un **reporte** solo puede referirse a un número que existe en el hilo. Los
  reportes no saben nada de comentarios: quien lo comprueba es el sistema,
  preguntándole primero al hilo (`existe`) y solo entonces guardando el
  reporte.
- Cuando la administración atiende un reporte, el sistema le saca el reporte
  más antiguo a **reportes** y, si se decide ocultar, le pide al **hilo**
  que oculte ese comentario.
- Ningún componente conoce a los otros dos de forma directa, salvo el hilo,
  que usa el índice. La coordinación vive en `mural.py`.

## 3. Interfaz de consola

Menú con las opciones: **1** comentar, **2** responder, **3** ver el hilo,
**4** reportar un comentario, **5** revisar el siguiente reporte
(administración) y **0** salir. El menú muestra cuántos reportes hay
pendientes. Los errores se muestran como un mensaje que empieza con
"No se pudo:" y el programa continúa.

Al revisar un reporte, la consola muestra quién reportó, el motivo y el hilo
completo, y pregunta si se oculta el comentario (s/n). Con cualquier otra
respuesta, el reporte sigue pendiente.

## 4. Criterios de aceptación del sistema

| ID | Criterio | Verificable mediante |
|----|----------|----------------------|
| CS-01 | Un error (comentario vacío, comentario inexistente, nivel excedido, reporte de un comentario inexistente o revisar sin reportes) muestra un mensaje "No se pudo: ..." y el menú sigue funcionando | test_error_no_detiene_el_menu |
| CS-02 | Reportar un comentario que existe deja un reporte pendiente y devuelve su número | test_reportar_existente |
| CS-03 | Reportar un comentario que no existe (incluido el 0) lanza `ComentarioNoEncontradoError` y no queda ningún reporte pendiente | test_reportar_inexistente |
| CS-04 | Si el comentario no existe y además quien reporta o el motivo están vacíos, se avisa primero que el comentario no existe | test_reportar_orden_de_errores |
| CS-05 | Atender un reporte pidiendo ocultar hace que el hilo muestre el aviso en lugar del comentario, y las respuestas siguen visibles | test_atender_y_ocultar |
| CS-06 | Atender un reporte pidiendo no ocultar deja el hilo exactamente igual | test_atender_sin_ocultar |
| CS-07 | Los reportes se atienden en el orden en que llegaron, sin importar a qué comentario se refieren | test_reportes_en_orden_de_llegada |
| CS-08 | Atender o mirar el siguiente reporte sin reportes pendientes lanza `NoHayReportesError` | test_atender_sin_reportes |
| CS-09 | Desde el menú se puede comentar, responder, reportar, revisar el reporte y ocultar el comentario, y luego el hilo lo muestra oculto | test_flujo_completo_consola |
| CS-10 | Si un número se escribe con letras, la consola avisa "Debes escribir un número." y el menú sigue | test_numero_con_letras |
| CS-11 | La opción 0 termina el programa con un saludo | test_salir |
| CS-12 | Si al revisar un reporte la respuesta no es s ni n, el reporte sigue pendiente | test_respuesta_no_valida_deja_el_reporte |

## 5. Fuera de alcance

Pagos, noticias, perfiles, mensajes directos, aplicación móvil y web,
inicio de sesión, distinguir quién es administrador, editar o borrar
comentarios y guardar los datos al cerrar el programa.

## 6. Historial de cambios

| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 0.1 | 2026-10-17 | Versión inicial con el componente 01 | — |
| 0.2 | 2026-11-11 | Se agrega el componente 02 (reportes), las opciones 4 y 5 del menú y los criterios CS-02 a CS-08 | Entrega 2: HU-05 y HU-06 |
| 1.0 | 2026-11-11 | Se agrega el componente 03 (índice); CS-01 pasa de ejecución manual a prueba automática y se amplía; se agregan CS-09 a CS-12; el documento se reescribe en lenguaje cotidiano | Entrega final. La prueba manual no dejaba evidencia y la consola ahora se puede probar sin que nadie escriba |
