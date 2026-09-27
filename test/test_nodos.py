"""Pruebas unitarias para las clases de nodos atómicos."""

import unittest
from src.estructuras.nodo_lista import NodoLista
from src.estructuras.nodo_pila import NodoPila
from src.estructuras.nodo_cola import NodoCola
from src.estructuras.nodo_arbol import NodoArbol


class TestNodos(unittest.TestCase):
    """Conjunto de pruebas para validar el comportamiento de los nodos."""

    def test_nodo_lista_inicializacion(self) -> None:
        nodo = NodoLista("archivo.py")
        self.assertEqual(nodo.dato, "archivo.py")
        self.assertIsNone(nodo.siguiente)
        self.assertIsNone(nodo.anterior)
        self.assertIn("archivo.py", repr(nodo))

    def test_nodo_pila_inicializacion(self) -> None:
        nodo = NodoPila("{")
        self.assertEqual(nodo.dato, "{")
        self.assertIsNone(nodo.siguiente)
        self.assertIn("{", repr(nodo))

    def test_nodo_cola_inicializacion(self) -> None:
        nodo = NodoCola({"id": 1, "prompt": "Analizar"})
        self.assertEqual(nodo.dato["id"], 1)
        self.assertIsNone(nodo.siguiente)
        self.assertIn("prompt", repr(nodo))

    def test_nodo_arbol_inicializacion(self) -> None:
        nodo = NodoArbol(42)
        self.assertEqual(nodo.valor, 42)
        self.assertIsNone(nodo.izquierda)
        self.assertIsNone(nodo.derecha)
        self.assertIn("42", repr(nodo))


if __name__ == "__main__":
    unittest.main()
