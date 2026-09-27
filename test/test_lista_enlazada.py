"""Pruebas unitarias para la Lista Enlazada Doble."""

import unittest
from src.estructuras.lista_enlazada import ListaEnlazada


class TestListaEnlazada(unittest.TestCase):
    """Pruebas completas para la implementación propia de ListaEnlazada."""

    def setUp(self) -> None:
        self.lista = ListaEnlazada()

    def test_lista_vacia(self) -> None:
        self.assertTrue(self.lista.esta_vacia())
        self.assertEqual(len(self.lista), 0)
        self.assertEqual(self.lista.tamano, 0)
        self.assertIsNone(self.lista.cabeza)
        self.assertIsNone(self.lista.cola)
        self.assertEqual(self.lista.listar(), [])

    def test_insertar_al_final_y_al_inicio(self) -> None:
        self.lista.insertar_al_final("segundo.py")
        self.lista.insertar_al_inicio("primero.py")
        self.lista.insertar_al_final("tercero.py")

        self.assertFalse(self.lista.esta_vacia())
        self.assertEqual(len(self.lista), 3)
        self.assertEqual(self.lista.listar(), ["primero.py", "segundo.py", "tercero.py"])
        self.assertEqual(self.lista.cabeza.dato, "primero.py")
        self.assertEqual(self.lista.cola.dato, "tercero.py")
        self.assertEqual(self.lista.cabeza.siguiente.dato, "segundo.py")
        self.assertEqual(self.lista.cola.anterior.dato, "segundo.py")

    def test_insertar_con_posicion(self) -> None:
        self.lista.insertar("A")
        self.lista.insertar("C")
        self.lista.insertar("B", posicion=1)

        self.assertEqual(self.lista.listar(), ["A", "B", "C"])
        self.lista.insertar("Z", posicion=0)
        self.assertEqual(self.lista.cabeza.dato, "Z")
        self.lista.insertar("FINAL", posicion=100)
        self.assertEqual(self.lista.cola.dato, "FINAL")

    def test_obtener_por_indice(self) -> None:
        self.lista.insertar_al_final("a.txt")
        self.lista.insertar_al_final("b.txt")
        self.assertEqual(self.lista.obtener_por_indice(0), "a.txt")
        self.assertEqual(self.lista.obtener_por_indice(1), "b.txt")

        with self.assertRaises(IndexError):
            self.lista.obtener_por_indice(2)
        with self.assertRaises(IndexError):
            self.lista.obtener_por_indice(-1)

    def test_buscar(self) -> None:
        self.lista.insertar_al_final({"id": 1, "nombre": "main.py"})
        self.lista.insertar_al_final({"id": 2, "nombre": "utils.py"})

        resultado = self.lista.buscar(lambda item: item["nombre"] == "utils.py")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["id"], 2)

        no_encontrado = self.lista.buscar(lambda item: item["nombre"] == "inexistente.py")
        self.assertIsNone(no_encontrado)

    def test_eliminar_por_valor(self) -> None:
        self.lista.insertar_al_final("uno")
        self.lista.insertar_al_final("dos")
        self.lista.insertar_al_final("tres")

        # Eliminar elemento intermedio
        eliminado = self.lista.eliminar("dos")
        self.assertTrue(eliminado)
        self.assertEqual(self.lista.listar(), ["uno", "tres"])
        self.assertEqual(len(self.lista), 2)
        self.assertEqual(self.lista.cabeza.siguiente.dato, "tres")
        self.assertEqual(self.lista.cola.anterior.dato, "uno")

        # Eliminar cabeza
        self.assertTrue(self.lista.eliminar("uno"))
        self.assertEqual(self.lista.cabeza.dato, "tres")
        self.assertEqual(len(self.lista), 1)

        # Eliminar cola restante
        self.assertTrue(self.lista.eliminar("tres"))
        self.assertTrue(self.lista.esta_vacia())
        self.assertIsNone(self.lista.cabeza)
        self.assertIsNone(self.lista.cola)

        # Eliminar inexistente
        self.assertFalse(self.lista.eliminar("no_existe"))

    def test_eliminar_por_indice(self) -> None:
        self.lista.insertar_al_final("x")
        self.lista.insertar_al_final("y")
        self.lista.insertar_al_final("z")

        eliminado = self.lista.eliminar_por_indice(1)
        self.assertEqual(eliminado, "y")
        self.assertEqual(self.lista.listar(), ["x", "z"])

        with self.assertRaises(IndexError):
            self.lista.eliminar_por_indice(5)

    def test_iterador(self) -> None:
        valores = [10, 20, 30]
        for v in valores:
            self.lista.insertar_al_final(v)

        recolectados = [v for v in self.lista]
        self.assertEqual(recolectados, valores)

    def test_limpiar(self) -> None:
        self.lista.insertar_al_final("a")
        self.lista.insertar_al_final("b")
        self.lista.limpiar()
        self.assertTrue(self.lista.esta_vacia())
        self.assertEqual(len(self.lista), 0)
        self.assertIsNone(self.lista.cabeza)
        self.assertIsNone(self.lista.cola)


if __name__ == "__main__":
    unittest.main()
