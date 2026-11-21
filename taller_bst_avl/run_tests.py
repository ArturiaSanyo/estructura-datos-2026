"""Corre todas las pruebas sin necesitar pytest:   python run_tests.py"""
import test_bst
import test_avl

modulos = [test_bst, test_avl]
fallos = 0

for modulo in modulos:
    for nombre in dir(modulo):
        if nombre.startswith("test_"):
            prueba = getattr(modulo, nombre)
            try:
                prueba()
                print("OK     ", modulo.__name__, nombre)
            except AssertionError:
                fallos += 1
                print("FALLÓ  ", modulo.__name__, nombre)

print()
if fallos == 0:
    print("Todas las pruebas pasaron.")
else:
    print(fallos, "prueba(s) fallaron.")
