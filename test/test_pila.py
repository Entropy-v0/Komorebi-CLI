"""Pruebas unitarias para la estructura Pila (LIFO)."""

import unittest
from src.estructuras.pila import Pila


class TestPila(unittest.TestCase):
    """Pruebas completas para la clase Pila."""

    def setUp(self) -> None:
        self.pila = Pila()

    def test_pila_vacia(self) -> None:
        self.assertTrue(self.pila.esta_vacia())
        self.assertEqual(len(self.pila), 0)
        self.assertEqual(self.pila.tamano, 0)
        self.assertIsNone(self.pila.tope)
        self.assertEqual(self.pila.listar(), [])

        with self.assertRaises(IndexError):
            self.pila.desapilar()
        with self.assertRaises(IndexError):
            self.pila.cima()

    def test_apilar_y_cima(self) -> None:
        self.pila.apilar("(")
        self.assertFalse(self.pila.esta_vacia())
        self.assertEqual(self.pila.cima(), "(")
        self.assertEqual(len(self.pila), 1)

        self.pila.apilar("{")
        self.assertEqual(self.pila.cima(), "{")
        self.assertEqual(len(self.pila), 2)

    def test_desapilar_lifo(self) -> None:
        self.pila.apilar("estado_1")
        self.pila.apilar("estado_2")
        self.pila.apilar("estado_3")

        self.assertEqual(self.pila.desapilar(), "estado_3")
        self.assertEqual(self.pila.desapilar(), "estado_2")
        self.assertEqual(self.pila.cima(), "estado_1")
        self.assertEqual(len(self.pila), 1)

        self.assertEqual(self.pila.desapilar(), "estado_1")
        self.assertTrue(self.pila.esta_vacia())

    def test_limpiar(self) -> None:
        self.pila.apilar(1)
        self.pila.apilar(2)
        self.pila.limpiar()
        self.assertTrue(self.pila.esta_vacia())
        self.assertIsNone(self.pila.tope)


if __name__ == "__main__":
    unittest.main()
