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
- La documentación está escrita en lenguaje cotidiano (hay un glosario en
  `specs/GLOSARIO.md`) y el código está comentado para quien apenas empieza.

## Qué hace el programa

Un menú de consola con seis opciones: comentar, responder, ver el hilo,
reportar un comentario, revisar el siguiente reporte (administración) y
salir. Un comentario reportado y ocultado no se borra: se ve un aviso en su
lugar y sus respuestas siguen visibles.

## Las tres estructuras de datos

| # | Pieza | Estructura | Para qué sirve |
|---|-------|-----------|----------------|
| 01 | Hilo de comentarios | Árbol general | Guardar la conversación con respuestas dentro de respuestas |
| 02 | Reportes | Cola enlazada | Atender los reportes en el orden en que llegaron |
| 03 | Índice de comentarios | Tabla hash con encadenamiento | Encontrar un comentario por su número sin recorrer todo el hilo |

## Hitos

| Fecha | Hito | Estado |
|---|---|---|
| Mié 7 oct | Registro en D2L: temática, contexto narrativo y repositorio | Hecho |
| Mié 14 oct | Entrega 1 — Especificación y diseño (componente 01) | Hecho |
| Mié 28 oct | Entrega 2 — Avance funcional (componentes 01 y 02) | Hecho |
| Mié 11 nov | Entrega final — Sistema completo, análisis e informe (componentes 01, 02 y 03) | Hecho |
| 14 y 21 nov | Sustentación individual | Pendiente |

## Estructura del proyecto

```
avataro-natura/
├── README.md
├── main.py                      # menú de consola
├── mural.py                     # une el hilo con los reportes
├── conftest.py
├── estructuras/
│   ├── errores.py               # los avisos de error con nombre propio
│   ├── hilo.py                  # componente 01: árbol general
│   ├── reportes.py              # componente 02: cola enlazada
│   └── indice.py                # componente 03: tabla hash
├── tests/                       # una prueba por criterio de aceptación
│   ├── test_hilo.py
│   ├── test_reportes.py
│   ├── test_indice.py
│   ├── test_mural.py
│   └── test_consola.py
├── analisis/
│   ├── medir_tiempos.py         # mide los tiempos con y sin índice
│   ├── resultados.txt           # resultado de la medición
│   └── grafica_responder.png
├── specs/                       # fuente de verdad (SDD)
│   ├── CONSTITUTION.md
│   ├── GLOSARIO.md              # palabras técnicas explicadas
│   ├── 00-producto/             # historias, moscow, estructuras
│   ├── 01-hilo-comentarios/     # spec, plan, tasks
│   ├── 02-reportes/             # spec, plan, tasks
│   ├── 03-indice-comentarios/   # spec, plan, tasks
│   ├── 99-sistema/spec.md
│   └── trazabilidad.md          # criterio ↔ prueba ↔ código
└── docs/                        # diseños de Figma del producto original
```

## Cómo ejecutar

Requiere Python 3.11 o superior.

```bash
cd avataro-natura
python main.py                       # programa de consola
pip install pytest
python -m pytest                     # pruebas (53 en total)
python analisis/medir_tiempos.py     # medición de tiempos (tarda unos segundos)
```

En Windows, si `python` no funciona, prueba con `py` en su lugar.
