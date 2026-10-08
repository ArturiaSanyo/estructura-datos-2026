# Avataro Natura

**Autor:** Anwar Joseph · **Curso:** Estructuras de Datos · ID 706132 · II-2026
**Universidad Cooperativa de Colombia · Facultad de Ingeniería**
**Temática:** B — Hilos de comentarios

## Contexto narrativo

Avataro Natura es una red social para personas preocupadas por el medio
ambiente en Medellín. Reúne a ciudadanos, organizaciones y colectivos que
quieren organizar actividades locales de pequeña escala (jornadas de
siembra, limpiezas de quebradas, reciclaje comunitario, campañas de
sensibilización) y apoyar con aportes voluntarios a fundaciones dedicadas
al cuidado del entorno.

Cada actividad vive dentro de una comunidad, y alrededor de ella la gente
conversa: propone ideas, discute cómo organizarla, opina sobre lo que se
logró y, cuando hubo dinero de por medio, exige rendición de cuentas.
Esa conversación no es una lista plana. Una opinión recibe respuestas,
esas respuestas reciben otras, y quien llega tarde necesita poder seguir
el hilo completo sin perder el orden. Si el debate se pierde, la
comunidad pierde la confianza que sostiene la plataforma.

Este proyecto implementa en consola el núcleo de esa conversación: el
**mural de opiniones** de cada actividad, organizado como hilos de
comentarios con respuestas anidadas. El usuario puede comentar una
actividad, responder a cualquier comentario, ver el hilo completo con
sangría según la profundidad y moderar contenido inadecuado (el
administrador de la comunidad puede reportarlo).

La idea nace del documento de requisitos de Avataro Natura (v4.0), de
donde se toman los requisitos relacionados con el mural de opiniones, las
comunidades y la moderación. El resto de la plataforma (pagos, noticias,
perfiles, app móvil) queda fuera del alcance de este proyecto
integrador.

## Reglas del proyecto

- Python 3.11 o superior; dependencias: `pytest` (y opcionalmente `matplotlib`).
- Interfaz de consola.
- Las estructuras de datos se implementan desde cero.
- Desarrollo guiado por especificaciones (SDD): la carpeta `specs/` es la
  fuente de verdad y se versiona antes que el código.

## Hitos

| Fecha | Hito |
|---|---|
| Mié 7 oct | Registro en D2L: temática, contexto narrativo y repositorio |
| Mié 14 oct | Entrega 1 — Especificación y diseño |
| Mié 28 oct | Entrega 2 — Avance funcional |
| Mié 11 nov | Entrega final |
| 14 y 21 nov | Sustentación individual |

## Cómo ejecutar

Se completará con las instrucciones de instalación y ejecución cuando
exista código (`python main.py`).
