"""Pruebas unitarias para ServicioDiagnosticos."""

import unittest
from src.nucleo.diagnostico import Diagnostico
from src.servicios.servicio_diagnosticos import ServicioDiagnosticos


class TestServicioDiagnosticos(unittest.TestCase):
    """Pruebas para ServicioDiagnosticos."""

    def setUp(self) -> None:
        self.servicio = ServicioDiagnosticos()
        self.diags = [
            Diagnostico(30, "WARN", "Advertencia en 30"),
            Diagnostico(5, "ERROR", "Error crítico en 5"),
            Diagnostico(50, "INFO", "Info en 50"),
            Diagnostico(12, "ERROR", "Otro error en 12"),
        ]

    def test_ordenar_por_linea_mergesort(self) -> None:
        ordenados = self.servicio.ordenar(self.diags, criterio="line", algoritmo="mergesort", ascendente=True)
        lineas = [d.linea for d in ordenados]
        self.assertEqual(lineas, [5, 12, 30, 50])

    def test_ordenar_por_linea_shellsort(self) -> None:
        ordenados = self.servicio.ordenar(self.diags, criterio="linea", algoritmo="shellsort", ascendente=True)
        lineas = [d.linea for d in ordenados]
        self.assertEqual(lineas, [5, 12, 30, 50])

    def test_ordenar_por_gravedad_descendente(self) -> None:
        ordenados = self.servicio.ordenar(self.diags, criterio="severity", algoritmo="mergesort", ascendente=False)
        prioridades = [d.prioridad for d in ordenados]
        # ERROR(3), ERROR(3), WARN(2), INFO(1)
        self.assertEqual(prioridades, [3, 3, 2, 1])

    def test_criterio_o_algoritmo_invalido_lanza_error(self) -> None:
        with self.assertRaises(ValueError):
            self.servicio.ordenar(self.diags, criterio="inexistente", algoritmo="mergesort")
        with self.assertRaises(ValueError):
            self.servicio.ordenar(self.diags, criterio="line", algoritmo="quicksort")


if __name__ == "__main__":
    unittest.main()
