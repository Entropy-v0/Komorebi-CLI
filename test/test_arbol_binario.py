"""Pruebas unitarias para la estructura Árbol Binario (BST)."""

import unittest
from src.estructuras.arbol_binario import ArbolBinario


class TestArbolBinario(unittest.TestCase):
    """Pruebas completas para la clase ArbolBinario."""

    def setUp(self) -> None:
        self.arbol = ArbolBinario()

    def test_arbol_vacio(self) -> None:
        self.assertTrue(self.arbol.esta_vacio())
        self.assertEqual(len(self.arbol), 0)
        self.assertEqual(self.arbol.tamano, 0)
        self.assertIsNone(self.arbol.raiz)
        self.assertEqual(self.arbol.inorden(), [])
        self.assertEqual(self.arbol.preorden(), [])
        self.assertEqual(self.arbol.postorden(), [])

    def test_insertar_y_recorridos(self) -> None:
        # Insertar valores: 50, 30, 70, 20, 40, 60, 80
        valores = [50, 30, 70, 20, 40, 60, 80]
        for v in valores:
            self.assertTrue(self.arbol.insertar(v))

        # No permite duplicados
        self.assertFalse(self.arbol.insertar(50))
        self.assertEqual(len(self.arbol), 7)

        # Inorden debe resultar ordenado ascendentemente
        self.assertEqual(self.arbol.inorden(), [20, 30, 40, 50, 60, 70, 80])
        # Preorden: Raíz, Izq, Der
        self.assertEqual(self.arbol.preorden(), [50, 30, 20, 40, 70, 60, 80])
        # Postorden: Izq, Der, Raíz
        self.assertEqual(self.arbol.postorden(), [20, 40, 30, 60, 80, 70, 50])

    def test_consultar_y_contiene(self) -> None:
        self.arbol.insertar(100)
        self.arbol.insertar(50)
        self.arbol.insertar(150)

        self.assertEqual(self.arbol.consultar(50), 50)
        self.assertTrue(self.arbol.contiene(150))
        self.assertIsNone(self.arbol.consultar(999))
        self.assertFalse(self.arbol.contiene(999))

    def test_modificar(self) -> None:
        self.arbol.insertar(10)
        self.arbol.insertar(5)
        self.arbol.insertar(15)

        # Modificar valor existente
        self.assertTrue(self.arbol.modificar(5, 7))
        self.assertFalse(self.arbol.contiene(5))
        self.assertTrue(self.arbol.contiene(7))
        self.assertEqual(self.arbol.inorden(), [7, 10, 15])

        # Modificar valor inexistente
        self.assertFalse(self.arbol.modificar(999, 1000))

    def test_eliminar_nodo_hoja(self) -> None:
        for v in [50, 30, 70]:
            self.arbol.insertar(v)

        self.assertTrue(self.arbol.eliminar(30))
        self.assertEqual(self.arbol.inorden(), [50, 70])
        self.assertEqual(len(self.arbol), 2)

    def test_eliminar_nodo_un_hijo(self) -> None:
        for v in [50, 30, 70, 20]:
            self.arbol.insertar(v)

        self.assertTrue(self.arbol.eliminar(30))
        self.assertEqual(self.arbol.inorden(), [20, 50, 70])
        self.assertEqual(len(self.arbol), 3)

    def test_eliminar_nodo_dos_hijos(self) -> None:
        for v in [50, 30, 70, 20, 40, 60, 80]:
            self.arbol.insertar(v)

        # Eliminar raíz (50) que tiene dos hijos
        self.assertTrue(self.arbol.eliminar(50))
        self.assertFalse(self.arbol.contiene(50))
        self.assertEqual(self.arbol.inorden(), [20, 30, 40, 60, 70, 80])
        self.assertEqual(len(self.arbol), 6)

    def test_eliminar_inexistente(self) -> None:
        self.arbol.insertar(10)
        self.assertFalse(self.arbol.eliminar(99))


if __name__ == "__main__":
    unittest.main()
