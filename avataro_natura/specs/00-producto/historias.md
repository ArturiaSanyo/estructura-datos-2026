# Historias de usuario — Avataro Natura

Cada historia dice **qué logra la persona usuaria**. La estructura de datos
aparece en `estructuras.md` y en los planes, nunca aquí.

> **En palabras simples:** una historia de usuario es una frase con tres
> partes: *quién* es la persona, *qué quiere* y *para qué*. Debajo de cada
> historia van los criterios: cosas concretas que se pueden comprobar.

## HU-01 · Comentar una actividad (Must) — Hecha

**Como** persona de la comunidad, **quiero** dejar mi opinión sobre una
actividad ambiental, **para** que los demás sepan lo que pienso.

Criterios:
- El comentario aparece en el mural con mi nombre y recibe un número.
- No puedo publicar un comentario vacío.
- Los comentarios se muestran en el orden en que se publicaron.

## HU-02 · Responder a un comentario (Must) — Hecha

**Como** persona de la comunidad, **quiero** responder a un comentario
concreto, **para** conversar sin perder de qué se está hablando.

Criterios:
- Mi respuesta queda debajo del comentario al que respondo.
- Si el comentario no existe, se me avisa y no se publica nada.
- Las respuestas no se pueden anidar sin límite (máximo 5 niveles).

## HU-03 · Ver la conversación completa (Must) — Hecha

**Como** persona que llega tarde a la actividad, **quiero** ver toda la
conversación en orden, **para** entender qué se discutió y por qué.

Criterios:
- Cada comentario aparece después de aquel al que responde.
- Las respuestas se ven con sangría según su nivel.
- Si aún no hay comentarios, el mural lo indica sin fallar.

## HU-04 · Ir directo a un comentario por su número (Should) — Hecha

**Como** persona de la comunidad, **quiero** responder a un comentario
usando su número, **para** no esperar aunque el mural tenga muchísimos
comentarios.

Criterios:
- Encontrar un comentario por su número tarda casi lo mismo con 10
  comentarios que con 10 000 (se comprueba midiendo, ver `analisis/`).
- Si el número no existe, se me avisa.
- Los criterios comprobables por prueba están en
  `specs/03-indice-comentarios/spec.md`.

## HU-05 · Reportar un comentario inadecuado (Should) — Hecha

**Como** persona de la comunidad, **quiero** reportar un comentario
ofensivo, **para** que la administración lo revise.

Criterios:
- Puedo reportar cualquier comentario que exista, diciendo mi nombre y el
  motivo.
- Si el comentario no existe, se me avisa y no queda ningún reporte.
- No puedo enviar un reporte sin nombre o sin motivo.
- Los criterios comprobables por prueba están en
  `specs/02-reportes/spec.md` y en `specs/99-sistema/spec.md`.

## HU-06 · Revisar los reportes en orden de llegada (Should) — Hecha

**Como** administrador de la comunidad, **quiero** revisar los reportes en
el orden en que llegaron, **para** atender primero lo más antiguo, y decidir
si el comentario se oculta o se deja como está.

Criterios:
- Siempre me aparece primero el reporte más antiguo.
- Si no hay reportes pendientes, se me avisa.
- Al revisar un reporte puedo **ocultar** el comentario o **dejarlo**.
- Un comentario oculto no se borra: conserva su número y sus respuestas
  siguen visibles.
- Los criterios comprobables por prueba están en
  `specs/02-reportes/spec.md` y en `specs/99-sistema/spec.md`.

## HU-07 · Reaccionar a un comentario (Could) — No se hizo

**Como** persona de la comunidad, **quiero** marcar "me gusta" en un
comentario, **para** apoyar una idea sin escribir.

Criterios: sin definir. Quedó fuera por falta de tiempo (ver `moscow.md`).

## Cambios a las historias

| Fecha | Cambio | Motivo |
|-------|--------|--------|
| 2026-11-11 | HU-06 agrega la decisión de ocultar o dejar el comentario | Sin esa decisión, revisar un reporte no tendría ningún efecto: la moderación quedaría vacía |
| 2026-11-11 | HU-04, HU-05 y HU-06 pasan de "criterios por definir" a criterios escritos | Se construyeron los componentes 02 y 03 |
