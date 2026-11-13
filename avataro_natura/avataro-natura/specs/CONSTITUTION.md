# Constitución del proyecto — Avataro Natura

**Autor:** Anwar Joseph · **Temática:** B (Hilos de comentarios)

> **En palabras simples:** esta página es el "reglamento" que me puse a mí
> mismo antes de empezar. Cada vez que dudo sobre cómo hacer algo, vuelvo
> a leerla. Si una regla me estorba, no la ignoro: la cambio de forma
> explícita y anoto por qué (ver el final de esta página).

## Principios

1. Toda estructura de datos que elegí se construye desde cero. No uso
   `list`, `dict`, `set`, `deque` ni `heapq` como sustituto de esa
   estructura; si uso alguno como apoyo interno, lo justifico en el
   `plan.md` del componente.
   *(Traducción: las "cajas" donde guardo la información las armo yo
   mismo, pieza por pieza, para demostrar que entiendo cómo funcionan.)*
2. Ninguna operación pública está terminada sin una explicación escrita
   (docstring) que diga cuánto cuesta (su complejidad) y sin pruebas del
   caso normal y de los casos extremos.
3. La especificación va antes que el código. Si cambia el comportamiento,
   primero cambia el `spec.md`, en su propio commit.
4. Cada prueba dice en su docstring qué criterio de aceptación verifica.
5. *(Agregado el 2026-11-11, ver tabla de cambios.)* Toda la documentación
   se escribe en lenguaje cotidiano, y el código se escribe y comenta
   pensando en alguien que apenas está aprendiendo a programar.

## Restricciones

- Lenguaje: Python 3.11 o superior.
- Dependencias permitidas: `pytest` y, opcionalmente, `matplotlib`.
- Interfaz: consola. Debe ejecutarse en una máquina limpia siguiendo el
  README.
- Alcance: solo el mural de opiniones (hilos de comentarios) y lo que lo
  apoya (reportes y moderación). Pagos, noticias, perfiles y app móvil
  quedan fuera (ver `00-producto/moscow.md`).

## Definición de terminado

Una funcionalidad está terminada cuando:

- [x] Todos sus criterios de aceptación tienen prueba y pasan
- [x] La complejidad real coincide con la declarada en el plan
- [x] Revisé el código contra la spec antes de integrarlo
- [x] `spec.md`, `plan.md` y `tasks.md` reflejan el estado real

## Uso de asistentes de IA

Permitido para: redactar borradores de documentos de especificación y
proponer ejemplos de código que luego leo, ejecuto, pruebo y corrijo yo.

No permitido para: entregar código que no pueda explicar línea por línea.

## Cambios a la constitución

| Fecha | Cambio | Motivo |
|-------|--------|--------|
| 2026-11-11 | Se agrega el principio 5 (lenguaje cotidiano y código para principiantes) | La documentación debe poder entenderla cualquier persona, no solo quien sabe de tecnología |
| 2026-11-11 | En el principio 1 queda aclarado que un arreglo de tamaño fijo puede usarse como apoyo interno si se justifica en el plan | La tabla de dispersión del componente 03 necesita "casilleros" numerados; se justifica en `03-indice-comentarios/plan.md` |
