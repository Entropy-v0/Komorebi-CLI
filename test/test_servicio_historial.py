"""Pruebas unitarias para ServicioHistorial."""

import unittest
from src.servicios.servicio_historial import ServicioHistorial


class TestServicioHistorial(unittest.TestCase):
    """Pruebas para ServicioHistorial."""

    def setUp(self) -> None:
        self.historial = ServicioHistorial()

    def test_inicialmente_vacio(self) -> None:
        self.assertFalse(self.historial.puede_deshacer)
        self.assertFalse(self.historial.puede_rehacer)
        self.assertIsNone(self.historial.deshacer("actual"))
        self.assertIsNone(self.historial.rehacer("actual"))

    def test_deshacer_y_rehacer(self) -> None:
        # Estado inicial v1
        v1 = "version 1"
        v2 = "version 2"
        v3 = "version 3"

        # Mutación 1: de v1 a v2
        self.historial.registrar_modificacion(v1)
        self.assertTrue(self.historial.puede_deshacer)
        self.assertFalse(self.historial.puede_rehacer)

        # Mutación 2: de v2 a v3
        self.historial.registrar_modificacion(v2)
        self.assertEqual(self.historial.tamano_deshacer, 2)

        # Deshacer desde v3: debe retornar v2
        recuperado = self.historial.deshacer(v3)
        self.assertEqual(recuperado, v2)
        self.assertTrue(self.historial.puede_rehacer)

        # Deshacer nuevamente: debe retornar v1
        recuperado_2 = self.historial.deshacer(v2)
        self.assertEqual(recuperado_2, v1)
        self.assertFalse(self.historial.puede_deshacer)

        # Rehacer: debe retornar v2
        rehacer_1 = self.historial.rehacer(v1)
        self.assertEqual(rehacer_1, v2)

        # Rehacer nuevamente: debe retornar v3
        rehacer_2 = self.historial.rehacer(v2)
        self.assertEqual(rehacer_2, v3)
        self.assertFalse(self.historial.puede_rehacer)

    def test_nueva_modificacion_invalida_rehacer(self) -> None:
        self.historial.registrar_modificacion("v1")
        self.historial.deshacer("v2")
        self.assertTrue(self.historial.puede_rehacer)

        # Nueva edición invalida el camino de rehacer
        self.historial.registrar_modificacion("v1_b")
        self.assertFalse(self.historial.puede_rehacer)


if __name__ == "__main__":
    unittest.main()
