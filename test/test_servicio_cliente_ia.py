"""Pruebas unitarias para ServicioClienteIA."""

import unittest
from src.nucleo.configuracion_app import ConfiguracionApp
from src.nucleo.peticion_ia import PeticionIA
from src.servicios.servicio_cliente_ia import ServicioClienteIA


class TestServicioClienteIA(unittest.TestCase):
    """Pruebas para ServicioClienteIA."""

    def test_modo_offline_fallback_estimacion(self) -> None:
        cfg = ConfiguracionApp(api_key_ia="")  # Sin api_key -> modo offline
        cliente = ServicioClienteIA(cfg)

        codigo_cuadratico = """
        for i in range(n):
            for j in range(n):
                print(i, j)
        """
        peticion = PeticionIA(codigo_cuadratico, nombre_archivo="matrices.py")
        resultado = cliente.procesar_peticion(peticion)

        self.assertEqual(peticion.estado, PeticionIA.ESTADO_COMPLETADO)
        self.assertEqual(resultado["complejidad_temporal"], "O(n^2)")
        self.assertIn("propuestas_refactorizacion", resultado)
        self.assertIsInstance(resultado["propuestas_refactorizacion"], list)
        self.assertIn("Offline", resultado["proveedor"])

    def test_analisis_codigo_constante(self) -> None:
        cfg = ConfiguracionApp(api_key_ia="")
        cliente = ServicioClienteIA(cfg)

        codigo_constante = "x = 10\ny = 20\nreturn x + y"
        peticion = PeticionIA(codigo_constante)
        resultado = cliente.procesar_peticion(peticion)

        self.assertEqual(resultado["complejidad_temporal"], "O(1)")


if __name__ == "__main__":
    unittest.main()
