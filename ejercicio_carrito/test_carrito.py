"""
Pruebas del TAD Carrito.

Estas pruebas se basan en las reglas escritas en spec.md.
Se ejecutan DOS VECES: una con la implementación de lista
(carrito_lista.py) y otra con la de diccionario (carrito_dict.py).

Esto se logra con @pytest.mark.parametrize: en vez de escribir
cada prueba dos veces, le decimos a pytest "corre esta misma
prueba usando primero esta clase, y luego esta otra".

Nivel básico: aquí no se usan errores (no hay raise ni ValueError).
Cuando algo es inválido, solo revisamos que el carrito
NO haya cambiado (el mensaje impreso no se revisa).

IMPORTANTE: este archivo no se debe modificar después de escrito.
"""

import pytest

from carrito_lista import Carrito as CarritoLista
from carrito_dict import Carrito as CarritoDict


# Lista de clases contra las que se van a correr todas las pruebas.
IMPLEMENTACIONES = [CarritoLista, CarritoDict]
IDS = ["lista", "dict"]


# ---------------------------------------------------------
# Pruebas de un carrito vacío
# ---------------------------------------------------------

@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_carrito_nuevo_esta_vacio(ClaseCarrito):
    carrito = ClaseCarrito()
    assert carrito.cuanto_llevo() == 0


@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_producto_que_no_existe_devuelve_cero(ClaseCarrito):
    carrito = ClaseCarrito()
    assert carrito.cuanto_hay("pan") == 0


# ---------------------------------------------------------
# Pruebas de meter productos
# ---------------------------------------------------------

@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_meter_un_producto(ClaseCarrito):
    carrito = ClaseCarrito()
    carrito.meter("pan", 2)
    assert carrito.cuanto_hay("pan") == 2
    assert carrito.cuanto_llevo() == 2


@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_meter_el_mismo_producto_dos_veces_se_acumula(ClaseCarrito):
    carrito = ClaseCarrito()
    carrito.meter("pan", 2)
    carrito.meter("pan", 3)
    assert carrito.cuanto_hay("pan") == 5


@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_meter_normaliza_mayusculas_y_espacios(ClaseCarrito):
    carrito = ClaseCarrito()
    carrito.meter("  Pan   Integral ", 2)
    assert carrito.cuanto_hay("pan integral") == 2
    assert carrito.cuanto_hay("PAN INTEGRAL") == 2


@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_tildes_hacen_productos_diferentes(ClaseCarrito):
    carrito = ClaseCarrito()
    carrito.meter("café", 1)
    carrito.meter("cafe", 1)
    assert carrito.cuanto_hay("café") == 1
    assert carrito.cuanto_hay("cafe") == 1


@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
@pytest.mark.parametrize("cantidad_invalida", [0, -1, 1.5, "3"])
def test_meter_cantidad_invalida_no_agrega_nada(ClaseCarrito, cantidad_invalida):
    carrito = ClaseCarrito()
    carrito.meter("pan", cantidad_invalida)
    assert carrito.cuanto_hay("pan") == 0
    assert carrito.cuanto_llevo() == 0


@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_meter_producto_vacio_no_agrega_nada(ClaseCarrito):
    carrito = ClaseCarrito()
    carrito.meter("   ", 1)
    assert carrito.cuanto_llevo() == 0


# ---------------------------------------------------------
# Pruebas de sacar productos
# ---------------------------------------------------------

@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_sacar_reduce_la_cantidad(ClaseCarrito):
    carrito = ClaseCarrito()
    carrito.meter("pan", 5)
    carrito.sacar("pan", 2)
    assert carrito.cuanto_hay("pan") == 3


@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_sacar_todo_elimina_el_producto(ClaseCarrito):
    carrito = ClaseCarrito()
    carrito.meter("pan", 3)
    carrito.sacar("pan", 3)
    assert carrito.cuanto_hay("pan") == 0
    assert carrito.cuanto_llevo() == 0


@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_sacar_producto_que_no_existe_no_cambia_nada(ClaseCarrito):
    carrito = ClaseCarrito()
    carrito.sacar("pan", 1)
    assert carrito.cuanto_hay("pan") == 0
    assert carrito.cuanto_llevo() == 0


@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_sacar_mas_de_lo_que_hay_no_cambia_nada(ClaseCarrito):
    carrito = ClaseCarrito()
    carrito.meter("pan", 2)
    carrito.sacar("pan", 5)
    assert carrito.cuanto_hay("pan") == 2


# ---------------------------------------------------------
# Pruebas del total
# ---------------------------------------------------------

@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_cuanto_llevo_suma_varios_productos(ClaseCarrito):
    carrito = ClaseCarrito()
    carrito.meter("pan", 2)
    carrito.meter("leche", 1)
    carrito.meter("huevos", 6)
    assert carrito.cuanto_llevo() == 9


# ---------------------------------------------------------
# La prueba clave: independencia entre carritos
# (esta es la que detecta el error de "las dos cajas
# comparten el mismo carrito" que pide la Parte D)
# ---------------------------------------------------------

@pytest.mark.parametrize("ClaseCarrito", IMPLEMENTACIONES, ids=IDS)
def test_dos_carritos_son_independientes(ClaseCarrito):
    carrito_1 = ClaseCarrito()
    carrito_2 = ClaseCarrito()

    carrito_1.meter("pan", 5)

    assert carrito_2.cuanto_hay("pan") == 0
    assert carrito_2.cuanto_llevo() == 0
    assert carrito_1.cuanto_hay("pan") == 5
