"""Pruebas unitarias para el modelo Diagnostico."""

import unittest
from src.nucleo.diagnostico import Diagnostico


class TestDiagnostico(unittest.TestCase):
    """Pruebas para la clase Diagnostico."""

    def test_creacion_diagnostico(self) -> None:
        diag = Diagnostico(15, "ERROR", "Falta punto y coma", columna=4)
        self.assertEqual(diag.linea, 15)
        self.assertEqual(diag.severidad, "ERROR")
        self.assertEqual(diag.prioridad, 3)
        self.assertEqual(diag.columna, 4)
        self.assertEqual(diag.mensaje, "Falta punto y coma")
        self.assertIn("Línea  15", diag.formato_consola())

    def test_severidad_invalida_defaultea_a_info(self) -> None:
        diag = Diagnostico(1, "DESCONOCIDO", "Mensaje")
        self.assertEqual(diag.severidad, "INFO")
        self.assertEqual(diag.prioridad, 1)

    def test_prioridades_relativas(self) -> None:
        info = Diagnostico(10, "INFO", "Info")
        warn = Diagnostico(10, "WARN", "Warn")
        error = Diagnostico(10, "ERROR", "Error")

        self.assertLess(info.prioridad, warn.prioridad)
        self.assertLess(warn.prioridad, error.prioridad)


if __name__ == "__main__":
    unittest.main()
