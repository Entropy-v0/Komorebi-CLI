"""Pruebas unitarias para el modelo ConfiguracionApp."""

import unittest
from src.nucleo.configuracion_app import ConfiguracionApp


class TestConfiguracionApp(unittest.TestCase):
    """Pruebas para la clase ConfiguracionApp."""

    def test_valores_por_defecto(self) -> None:
        cfg = ConfiguracionApp()
        self.assertEqual(cfg.ruta_respaldos, "respaldos")
        self.assertEqual(cfg.ruta_logs, "logs")
        self.assertEqual(cfg.tiempo_maximo_ejecucion, 15)
        self.assertEqual(cfg.proveedor_ia, "gemini")
        self.assertEqual(cfg.modelo_ia, "gemini-3.8-flash")
        self.assertIn("gemini-3.8-flash:generateContent", cfg.url_completa_ia)
        self.assertEqual(cfg.validar(), [])

    def test_desde_diccionario_anidado(self) -> None:
        datos = {
            "nombre_app": "Komorebi Test",
            "rutas": {"respaldos": "backups", "logs": "error_logs"},
            "ia": {
                "proveedor": "generico",
                "url_base": "https://api.ia.com",
                "endpoint_analisis": "/v1/check",
                "timeout_segundos": 30,
            },
            "servidor": {"puerto": 9000},
        }
        cfg = ConfiguracionApp.desde_diccionario(datos)
        self.assertEqual(cfg.nombre_app, "Komorebi Test")
        self.assertEqual(cfg.ruta_respaldos, "backups")
        self.assertEqual(cfg.ruta_logs, "error_logs")
        self.assertEqual(cfg.tiempo_maximo_ejecucion, 30)
        self.assertEqual(cfg.url_completa_ia, "https://api.ia.com/v1/check")
        self.assertEqual(cfg.puerto, 9000)

    def test_validar_errores(self) -> None:
        cfg = ConfiguracionApp(ruta_respaldos="", ruta_logs="", url_ia="", tiempo_maximo_ejecucion=-5)
        errores = cfg.validar()
        self.assertEqual(len(errores), 3)  # Respaldos, logs, url_ia (tiempo se normaliza a min 1)


if __name__ == "__main__":
    unittest.main()
