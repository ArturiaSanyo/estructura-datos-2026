import unittest
from lista_arreglo import ListaArreglo


class TestListaArreglo(unittest.TestCase):

    def nueva_lista(self, datos):
        lista = ListaArreglo()
        for dato in datos:
            lista.insertar_al_final(dato)
        return lista

    def test_lista_vacia(self):
        lista = ListaArreglo()
        self.assertTrue(lista.esta_vacia())
        self.assertEqual(lista.tamano(), 0)

    def test_un_elemento(self):
        lista = self.nueva_lista(["A"])
        self.assertEqual(lista.obtener(0), "A")
        self.assertEqual(lista.tamano(), 1)

    def test_insertar_al_principio(self):
        lista = self.nueva_lista(["B", "C"])
        lista.insertar_al_principio("A")
        self.assertEqual(list(lista.recorrer()), ["A", "B", "C"])

    def test_insertar_al_final(self):
        lista = self.nueva_lista(["A", "B"])
        lista.insertar_al_final("C")
        self.assertEqual(list(lista.recorrer()), ["A", "B", "C"])

    def test_ir_a(self):
        lista = self.nueva_lista(["A", "B", "C"])
        self.assertEqual(lista.ir_a(1), "B")
        self.assertEqual(lista.obtener(1), "B")

    def test_borrar_primero(self):
        lista = self.nueva_lista(["A", "B", "C"])
        lista.ir_a(0)
        self.assertEqual(lista.borrar_actual(), "A")
        self.assertEqual(list(lista.recorrer()), ["B", "C"])

    def test_borrar_ultimo(self):
        lista = self.nueva_lista(["A", "B", "C"])
        lista.ir_a(2)
        self.assertEqual(lista.borrar_actual(), "C")
        self.assertEqual(list(lista.recorrer()), ["A", "B"])

    def test_borrar_deja_vacia_la_lista(self):
        lista = self.nueva_lista(["A"])
        lista.ir_a(0)
        self.assertEqual(lista.borrar_actual(), "A")
        self.assertTrue(lista.esta_vacia())
        self.assertEqual(lista.tamano(), 0)

    def test_error_indice(self):
        lista = self.nueva_lista(["A"])
        with self.assertRaises(IndexError):
            lista.ir_a(1)


if __name__ == "__main__":
    unittest.main()
