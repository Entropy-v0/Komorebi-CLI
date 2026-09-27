"""Pruebas unitarias para ServicioSintaxis."""

import unittest
from src.servicios.servicio_sintaxis import ServicioSintaxis


class TestServicioSintaxis(unittest.TestCase):
    """Pruebas para ServicioSintaxis."""

    def setUp(self) -> None:
        self.servicio = ServicioSintaxis()

    def test_codigo_balanceado(self) -> None:
        codigo = """
        def sumar(a, b):
            datos = [1, 2, {3: 4}]
            return (a + b)
        """
        valido, diags = self.servicio.validar_codigo(codigo)
        self.assertTrue(valido)
        self.assertEqual(len(diags), 1)
        self.assertEqual(diags[0].severidad, "INFO")

    def test_desbalance_cierre_incorrecto(self) -> None:
        codigo = "arr = [1, 2, 3)"
        valido, diags = self.servicio.validar_codigo(codigo)
        self.assertFalse(valido)
        self.assertEqual(diags[0].severidad, "ERROR")
        self.assertIn("Desbalance", diags[0].mensaje)

    def test_delimitador_sin_cerrar(self) -> None:
        codigo = "def foo():\n    if (x > 0: pass"
        valido, diags = self.servicio.validar_codigo(codigo)
        self.assertFalse(valido)
        self.assertIn("sin cerrar", diags[0].mensaje)

    def test_cierre_sin_apertura(self) -> None:
        codigo = "x = 5}\n"
        valido, diags = self.servicio.validar_codigo(codigo)
        self.assertFalse(valido)
        self.assertIn("inesperado", diags[0].mensaje)


if __name__ == "__main__":
    unittest.main()
