# Recorridos del arbol de carpetas

## El arbol de prueba

```
servidor
├── Ingenieria
│   ├── Sistemas
│   │   ├── Programacion1
│   │   │   ├── 2025-1
│   │   │   │   ├── tarea1.py
│   │   │   │   └── tarea2.py
│   │   │   └── 2025-2
│   │   │       └── tarea1.py
│   │   └── EstructurasDatos
│   │       └── 2025-2
│   │           ├── taller1.py
│   │           ├── taller2.py
│   │           └── proyecto_final
│   │               ├── main.py
│   │               └── informe.pdf
│   └── Industrial
│       └── Estadistica
│           └── 2025-1
│               └── parcial.pdf
└── Ciencias
    └── Matematicas
        └── Calculo
            └── 2025-1
                ├── taller1.pdf
                └── taller2.pdf
```

Para verificar a mano:
- Entregas bajo `servidor`: 3 + 4 + 1 + 2 = **10**
- Entregas bajo `Ingenieria`: **8**; bajo `Sistemas`: **7**
- Ruta mas profunda: `servidor / Ingenieria / Sistemas / EstructurasDatos / 2025-2 / proyecto_final / main.py`
  (7 nombres, es la unica que llega al nivel 6)

## Recorrido por niveles (con COLA)

```
Nivel 0 : servidor
Nivel 1 : Ingenieria, Ciencias
Nivel 2 : Sistemas, Industrial, Matematicas
Nivel 3 : Programacion1, EstructurasDatos, Estadistica, Calculo
Nivel 4 : 2025-1, 2025-2, 2025-2, 2025-1, 2025-1
Nivel 5 : tarea1.py, tarea2.py, tarea1.py, taller1.py, taller2.py, proyecto_final, parcial.pdf, taller1.pdf, taller2.pdf
Nivel 6 : main.py, informe.pdf
```

## Mismo recorrido con PILA (orden de visita)

```
nivel 0 : servidor
nivel 1 : Ingenieria
nivel 2 : Sistemas
nivel 3 : Programacion1
nivel 4 : 2025-1
nivel 5 : tarea1.py
nivel 5 : tarea2.py
nivel 4 : 2025-2
nivel 5 : tarea1.py
nivel 3 : EstructurasDatos
nivel 4 : 2025-2
nivel 5 : taller1.py
nivel 5 : taller2.py
nivel 5 : proyecto_final
nivel 6 : main.py
nivel 6 : informe.pdf
nivel 2 : Industrial
nivel 3 : Estadistica
nivel 4 : 2025-1
nivel 5 : parcial.pdf
nivel 1 : Ciencias
nivel 2 : Matematicas
nivel 3 : Calculo
nivel 4 : 2025-1
nivel 5 : taller1.pdf
nivel 5 : taller2.pdf
```

## Por que son distintos

- La **cola** es FIFO (el primero que entra es el primero que sale). Los hijos de
  cada carpeta se forman **al final** de la fila, detras de todos los que ya
  estaban esperando. Por eso se atiende todo el nivel 1 antes de tocar el nivel 2,
  y asi sucesivamente: el recorrido va **ancho**, nivel por nivel.
- La **pila** es LIFO (el ultimo que entra es el primero que sale). Los hijos que
  acabamos de apilar quedan **encima**, asi que son los siguientes en salir. El
  recorrido se **mete hasta el fondo** de una rama (servidor → Ingenieria →
  Sistemas → ... → tarea2.py) y solo despues vuelve a las otras ramas. Por eso
  los niveles suben y bajan (5, 5, 4, 5, 3...) en vez de ir en orden.

Misma estructura de datos para guardar pendientes, distinto orden de salida,
distinto recorrido: cola = por niveles (en anchura), pila = por ramas (en profundidad).
