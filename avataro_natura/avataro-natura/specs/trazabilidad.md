# Trazabilidad criterio ↔ prueba ↔ código

> **En palabras simples:** esta tabla permite seguir el hilo en las dos
> direcciones. Si alguien señala un criterio, se ve qué prueba lo comprueba
> y qué código lo cumple. Si alguien señala una función, se ve de qué
> criterio nació.

## Componente 01 · Hilo de comentarios (spec 1.1)

| Componente | Criterio | Prueba | Código |
|------------|----------|--------|--------|
| 01-hilo-comentarios | CA-01 | test_comentar_primero | estructuras/hilo.py · comentar() |
| 01-hilo-comentarios | CA-02 | test_comentarios_en_orden | estructuras/hilo.py · comentar(), mostrar() |
| 01-hilo-comentarios | CA-03 | test_respuesta_queda_bajo_padre | estructuras/hilo.py · responder(), _agregar() |
| 01-hilo-comentarios | CA-04 | test_hilo_en_preorden | estructuras/hilo.py · mostrar(), _recorrer() |
| 01-hilo-comentarios | CA-05 | test_respuestas_en_orden | estructuras/hilo.py · _agregar(), _recorrer() |
| 01-hilo-comentarios | CA-06 | test_responder_inexistente | estructuras/hilo.py · responder(), _encontrar() |
| 01-hilo-comentarios | CA-07 | test_texto_vacio | estructuras/hilo.py · _validar() |
| 01-hilo-comentarios | CA-08 | test_autor_vacio | estructuras/hilo.py · _validar() |
| 01-hilo-comentarios | CA-09 | test_profundidad_maxima | estructuras/hilo.py · _agregar() |
| 01-hilo-comentarios | CA-10 | test_mostrar_vacio | estructuras/hilo.py · mostrar() |
| 01-hilo-comentarios | CA-11 | test_error_no_consume_numero | estructuras/hilo.py · _agregar() |
| 01-hilo-comentarios | CA-12 | test_orden_de_errores | estructuras/hilo.py · responder() |
| 01-hilo-comentarios | CA-13 | test_existe | estructuras/hilo.py · existe() |
| 01-hilo-comentarios | CA-14 | test_ocultar_comentario | estructuras/hilo.py · ocultar(), _recorrer() |
| 01-hilo-comentarios | CA-15 | test_ocultar_inexistente | estructuras/hilo.py · ocultar(), _encontrar() |
| 01-hilo-comentarios | CA-16 | test_ocultar_dos_veces | estructuras/hilo.py · ocultar() |
| 01-hilo-comentarios | CA-17 | test_responder_a_oculto | estructuras/hilo.py · responder(), _agregar() |

## Componente 02 · Reportes (spec 1.0)

| Componente | Criterio | Prueba | Código |
|------------|----------|--------|--------|
| 02-reportes | CA-01 | test_reportar_primero | estructuras/reportes.py · reportar() |
| 02-reportes | CA-02 | test_atender_en_orden | estructuras/reportes.py · reportar(), atender() |
| 02-reportes | CA-03 | test_atender_vacio | estructuras/reportes.py · atender() |
| 02-reportes | CA-04 | test_ver_siguiente | estructuras/reportes.py · ver_siguiente() |
| 02-reportes | CA-05 | test_ver_siguiente_vacio | estructuras/reportes.py · ver_siguiente() |
| 02-reportes | CA-06 | test_reportante_vacio | estructuras/reportes.py · reportar(), _validar() |
| 02-reportes | CA-07 | test_motivo_vacio | estructuras/reportes.py · reportar(), _validar() |
| 02-reportes | CA-08 | test_numero_comentario_invalido | estructuras/reportes.py · _validar() |
| 02-reportes | CA-09 | test_error_no_consume_numero | estructuras/reportes.py · reportar() |
| 02-reportes | CA-10 | test_reportar_despues_de_vaciar | estructuras/reportes.py · atender() |
| 02-reportes | CA-11 | test_mismo_comentario_dos_veces | estructuras/reportes.py · reportar() |
| 02-reportes | CA-12 | test_reporte_trae_sus_datos | estructuras/reportes.py · Reporte, reportar() |

## Componente 03 · Índice de comentarios (spec 1.1)

| Componente | Criterio | Prueba | Código |
|------------|----------|--------|--------|
| 03-indice-comentarios | CA-01 | test_agregar_y_buscar | estructuras/indice.py · agregar(), buscar(), _buscar_nodo() |
| 03-indice-comentarios | CA-02 | test_existe | estructuras/indice.py · existe(), es_numero_valido() |
| 03-indice-comentarios | CA-03 | test_buscar_inexistente | estructuras/indice.py · buscar() |
| 03-indice-comentarios | CA-04 | test_agregar_repetido | estructuras/indice.py · agregar() |
| 03-indice-comentarios | CA-05 | test_numero_invalido | estructuras/indice.py · agregar(), es_numero_valido() |
| 03-indice-comentarios | CA-06 | test_muchos_numeros | estructuras/indice.py · agregar(), _agrandar() |
| 03-indice-comentarios | CA-07 | test_cantidad | estructuras/indice.py · cantidad(), agregar() |
| 03-indice-comentarios | CA-08 | test_indice_vacio | estructuras/indice.py · buscar(), existe() |
| 03-indice-comentarios | CA-09 | test_numeros_salteados | estructuras/indice.py · agregar(), _agrandar() |

### Verificaciones del plan 03 (forma y costo)

| Verificación | Prueba o medición | Código |
|--------------|-------------------|--------|
| PLAN-01 · cadenas cortas | test_plan_cadenas_cortas | estructuras/indice.py · _cadena_mas_larga() |
| PLAN-02 · números que chocan | test_plan_numeros_que_chocan | estructuras/indice.py · agregar(), _buscar_nodo() |
| PLAN-03 · la tabla se agranda | test_plan_se_agranda | estructuras/indice.py · _agrandar() |
| PLAN-04 · tiempos medidos | analisis/medir_tiempos.py (resultados en `analisis/resultados.txt`) | estructuras/hilo.py · responder(), _encontrar() |

## Sistema · 99-sistema (spec 1.0)

| Componente | Criterio | Prueba | Código |
|------------|----------|--------|--------|
| 99-sistema | CS-01 | test_error_no_detiene_el_menu | main.py · main() |
| 99-sistema | CS-02 | test_reportar_existente | mural.py · reportar() |
| 99-sistema | CS-03 | test_reportar_inexistente | mural.py · reportar() |
| 99-sistema | CS-04 | test_reportar_orden_de_errores | mural.py · reportar() |
| 99-sistema | CS-05 | test_atender_y_ocultar | mural.py · atender_reporte() |
| 99-sistema | CS-06 | test_atender_sin_ocultar | mural.py · atender_reporte() |
| 99-sistema | CS-07 | test_reportes_en_orden_de_llegada | mural.py · atender_reporte() |
| 99-sistema | CS-08 | test_atender_sin_reportes | mural.py · atender_reporte(), ver_siguiente_reporte() |
| 99-sistema | CS-09 | test_flujo_completo_consola | main.py · opcion_revisar_reporte() |
| 99-sistema | CS-10 | test_numero_con_letras | main.py · pedir_numero(), opcion_responder(), opcion_reportar() |
| 99-sistema | CS-11 | test_salir | main.py · main() |
| 99-sistema | CS-12 | test_respuesta_no_valida_deja_el_reporte | main.py · opcion_revisar_reporte() |

Dónde están las pruebas: `tests/test_hilo.py`, `tests/test_reportes.py`,
`tests/test_indice.py`, `tests/test_mural.py` y `tests/test_consola.py`.
