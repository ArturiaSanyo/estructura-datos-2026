"""Pruebas del TAD Carrito para las dos implementaciones."""

import pytest

from carrito_dict import Carrito as CarritoDict
from carrito_lista import Carrito as CarritoLista


@pytest.fixture(params=[CarritoLista, CarritoDict])
def carrito(request):
    return request.param()


def test_carrito_nuevo_esta_vacio(carrito):
    assert carrito.cuanto_llevo() == 0
    assert carrito.cuanto_hay("pan") == 0


def test_meter_producto(carrito):
    carrito.meter("pan", 3)

    assert carrito.cuanto_hay("pan") == 3
    assert carrito.cuanto_llevo() == 3


def test_meter_mismo_producto_acumula(carrito):
    carrito.meter("pan", 2)
    carrito.meter("PAN", 3)

    assert carrito.cuanto_hay("pan") == 5
    assert carrito.cuanto_llevo() == 5


def test_meter_varios_productos(carrito):
    carrito.meter("pan", 2)
    carrito.meter("leche", 4)

    assert carrito.cuanto_hay("pan") == 2
    assert carrito.cuanto_hay("leche") == 4
    assert carrito.cuanto_llevo() == 6


def test_sacar_producto(carrito):
    carrito.meter("pan", 5)
    carrito.sacar("pan", 2)

    assert carrito.cuanto_hay("pan") == 3
    assert carrito.cuanto_llevo() == 3


def test_sacar_todo_elimina_producto(carrito):
    carrito.meter("pan", 3)
    carrito.sacar("pan", 3)

    assert carrito.cuanto_hay("pan") == 0
    assert carrito.cuanto_llevo() == 0


def test_sacar_producto_inexistente_da_error(carrito):
    with pytest.raises(ValueError):
        carrito.sacar("pan", 1)


def test_sacar_mas_de_lo_disponible_no_cambia_el_carrito(carrito):
    carrito.meter("pan", 2)

    with pytest.raises(ValueError):
        carrito.sacar("pan", 3)

    assert carrito.cuanto_hay("pan") == 2
    assert carrito.cuanto_llevo() == 2


def test_nombres_ignoran_mayusculas_y_espacios(carrito):
    carrito.meter("  Pan   Integral ", 2)

    assert carrito.cuanto_hay("pan integral") == 2


@pytest.mark.parametrize("cantidad", [0, -1, 1.5, "2", True, None])
def test_cantidad_invalida(carrito, cantidad):
    with pytest.raises(ValueError):
        carrito.meter("pan", cantidad)


@pytest.mark.parametrize("producto", [None, "", "   ", 10])
def test_producto_invalido(carrito, producto):
    with pytest.raises(ValueError):
        carrito.meter(producto, 1)


def test_dos_carritos_son_independientes(carrito):
    otro = type(carrito)()

    carrito.meter("pan", 3)

    assert otro.cuanto_hay("pan") == 0
    assert carrito.cuanto_hay("pan") == 3
