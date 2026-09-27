"""Pruebas unitarias para la estructura Cola FIFO."""

import unittest
from src.estructuras.cola_fifo import ColaFIFO


class TestColaFIFO(unittest.TestCase):
    """Pruebas completas para la clase ColaFIFO."""

    def setUp(self) -> None:
        self.cola = ColaFIFO()

    def test_cola_vacia(self) -> None:
        self.assertTrue(self.cola.esta_vacia())
        self.assertEqual(len(self.cola), 0)
        self.assertEqual(self.cola.tamano, 0)
        self.assertIsNone(self.cola.primer_nodo)
        self.assertEqual(self.cola.listar(), [])

        with self.assertRaises(IndexError):
            self.cola.desencolar()
        with self.assertRaises(IndexError):
            self.cola.frente()

    def test_encolar_y_frente(self) -> None:
        self.cola.encolar("pet_1")
        self.assertFalse(self.cola.esta_vacia())
        self.assertEqual(self.cola.frente(), "pet_1")
        self.assertEqual(len(self.cola), 1)

        self.cola.encolar("pet_2")
        self.assertEqual(self.cola.frente(), "pet_1")
        self.assertEqual(len(self.cola), 2)

    def test_desencolar_fifo(self) -> None:
        self.cola.encolar("peticion_A")
        self.cola.encolar("peticion_B")
        self.cola.encolar("peticion_C")

        self.assertEqual(self.cola.listar(), ["peticion_A", "peticion_B", "peticion_C"])
        self.assertEqual(self.cola.desencolar(), "peticion_A")
        self.assertEqual(self.cola.frente(), "peticion_B")
        self.assertEqual(self.cola.desencolar(), "peticion_B")
        self.assertEqual(self.cola.desencolar(), "peticion_C")
        self.assertTrue(self.cola.esta_vacia())

    def test_limpiar(self) -> None:
        self.cola.encolar("x")
        self.cola.encolar("y")
        self.cola.limpiar()
        self.assertTrue(self.cola.esta_vacia())
        self.assertIsNone(self.cola.primer_nodo)


if __name__ == "__main__":
    unittest.main()
