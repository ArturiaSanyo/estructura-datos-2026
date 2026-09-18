import unittest
from lista_enlazada import ListaEnlazada


class TestExtremos(unittest.TestCase):

    def test_lista_vacia(self):
        lista = ListaEnlazada()
        self.assertTrue(lista.esta_vacia())
        self.assertEqual(lista.tamano(), 0)

    def test_lista_un_elemento(self):
        lista = ListaEnlazada()
        lista.insertar_al_final("A")
        self.assertEqual(lista.obtener(0), "A")
        self.assertIs(lista._primero, lista._ultimo)
        self.assertIs(lista._actual, lista._primero)

    def test_borrar_primero(self):
        lista = ListaEnlazada()
        lista.insertar_al_final("A")
        lista.insertar_al_final("B")
        lista.ir_a(0)
        self.assertEqual(lista.borrar_actual(), "A")
        self.assertEqual(list(lista.recorrer()), ["B"])
        self.assertIs(lista._primero, lista._ultimo)

    def test_borrar_ultimo(self):
        lista = ListaEnlazada()
        lista.insertar_al_final("A")
        lista.insertar_al_final("B")
        lista.insertar_al_final("C")
        lista.ir_a(2)
        self.assertEqual(lista.borrar_actual(), "C")
        self.assertEqual(list(lista.recorrer()), ["A", "B"])
        self.assertEqual(lista._ultimo.dato, "B")

    def test_borrar_unico_elemento(self):
        lista = ListaEnlazada()
        lista.insertar_al_final("A")
        lista.ir_a(0)
        lista.borrar_actual()
        self.assertTrue(lista.esta_vacia())
        self.assertIsNone(lista._primero)
        self.assertIsNone(lista._ultimo)
        self.assertIsNone(lista._actual)


if __name__ == "__main__":
    unittest.main()
