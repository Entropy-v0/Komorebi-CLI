"""Pruebas unitarias para el modelo PeticionIA."""

import unittest
from src.nucleo.peticion_ia import PeticionIA


class TestPeticionIA(unittest.TestCase):
    """Pruebas para la clase PeticionIA."""

    def test_creacion_y_estados(self) -> None:
        peticion = PeticionIA("def foo(): pass", nombre_archivo="main.py")
        self.assertEqual(peticion.estado, PeticionIA.ESTADO_PENDIENTE)
        self.assertEqual(peticion.nombre_archivo, "main.py")
        self.assertIsNone(peticion.resultado)
        self.assertIsNone(peticion.error)

        # Transición a EN_PROCESO
        peticion.marcar_en_proceso()
        self.assertEqual(peticion.estado, PeticionIA.ESTADO_EN_PROCESO)

        # Transición a COMPLETADO
        resultado = {"complejidad": "O(1)", "sugerencias": "Código óptimo"}
        peticion.marcar_completado(resultado)
        self.assertEqual(peticion.estado, PeticionIA.ESTADO_COMPLETADO)
        self.assertEqual(peticion.resultado, resultado)

    def test_marcar_fallido(self) -> None:
        peticion = PeticionIA("codigo", id_peticion="req-test")
        peticion.marcar_fallido("Timeout en API")
        self.assertEqual(peticion.estado, PeticionIA.ESTADO_FALLIDO)
        self.assertEqual(peticion.error, "Timeout en API")


if __name__ == "__main__":
    unittest.main()
