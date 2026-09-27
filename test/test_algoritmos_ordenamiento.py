"""Pruebas unitarias para los algoritmos de ordenamiento MergeSort y ShellSort."""

import unittest
from src.algoritmos.mergesort import MergeSort
from src.algoritmos.shellsort import ShellSort


class TestAlgoritmosOrdenamiento(unittest.TestCase):
    """Pruebas comparativas y exhaustivas para MergeSort y ShellSort."""

    def setUp(self) -> None:
        self.algoritmos = [MergeSort(), ShellSort()]

    def test_lista_vacia_y_unitaria(self) -> None:
        for algo in self.algoritmos:
            with self.subTest(algoritmo=algo.__class__.__name__):
                self.assertEqual(algo.ordenar([]), [])
                self.assertEqual(algo.ordenar([42]), [42])

    def test_ordenamiento_numerico_ascendente(self) -> None:
        datos = [64, 34, 25, 12, 22, 11, 90]
        esperado = [11, 12, 22, 25, 34, 64, 90]

        for algo in self.algoritmos:
            with self.subTest(algoritmo=algo.__class__.__name__):
                resultado = algo.ordenar(datos, ascendente=True)
                self.assertEqual(resultado, esperado)
                # Verifica que la lista original no haya sido mutada
                self.assertEqual(datos, [64, 34, 25, 12, 22, 11, 90])

    def test_ordenamiento_numerico_descendente(self) -> None:
        datos = [64, 34, 25, 12, 22, 11, 90]
        esperado = [90, 64, 34, 25, 22, 12, 11]

        for algo in self.algoritmos:
            with self.subTest(algoritmo=algo.__class__.__name__):
                resultado = algo.ordenar(datos, ascendente=False)
                self.assertEqual(resultado, esperado)

    def test_elementos_duplicados_y_negativos(self) -> None:
        datos = [5, -2, 5, 0, -8, 2, 0]
        esperado = [-8, -2, 0, 0, 2, 5, 5]

        for algo in self.algoritmos:
            with self.subTest(algoritmo=algo.__class__.__name__):
                resultado = algo.ordenar(datos, ascendente=True)
                self.assertEqual(resultado, esperado)

    def test_ordenamiento_por_criterio_objeto(self) -> None:
        # Simula objetos de diagnóstico con línea y gravedad
        diagnosticos = [
            {"linea": 45, "gravedad": "WARN", "prioridad": 2},
            {"linea": 12, "gravedad": "ERROR", "prioridad": 3},
            {"linea": 89, "gravedad": "INFO", "prioridad": 1},
            {"linea": 5, "gravedad": "ERROR", "prioridad": 3},
        ]

        for algo in self.algoritmos:
            with self.subTest(algoritmo=algo.__class__.__name__):
                # Ordenar por línea ascendente
                por_linea = algo.ordenar(
                    diagnosticos,
                    criterio=lambda d: d["linea"],
                    ascendente=True,
                )
                lineas = [d["linea"] for d in por_linea]
                self.assertEqual(lineas, [5, 12, 45, 89])

                # Ordenar por prioridad/gravedad descendente
                por_prioridad = algo.ordenar(
                    diagnosticos,
                    criterio=lambda d: d["prioridad"],
                    ascendente=False,
                )
                prioridades = [d["prioridad"] for d in por_prioridad]
                self.assertEqual(prioridades, [3, 3, 2, 1])


if __name__ == "__main__":
    unittest.main()
