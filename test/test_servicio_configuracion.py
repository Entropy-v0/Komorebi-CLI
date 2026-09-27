"""Pruebas unitarias para ServicioConfiguracion."""

import os
import tempfile
import unittest
from src.servicios.servicio_configuracion import ServicioConfiguracion


class TestServicioConfiguracion(unittest.TestCase):
    """Pruebas para ServicioConfiguracion."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_cargar_configuracion_existente(self) -> None:
        ruta_cfg = os.path.join(self.temp_dir.name, "test_config.json")
        contenido = (
            '{"nombre_app": "Komorebi Mock", "rutas": {"respaldos": "'
            + os.path.join(self.temp_dir.name, "backups")
            + '", "logs": "'
            + os.path.join(self.temp_dir.name, "logs")
            + '"}}'
        )
        with open(ruta_cfg, "w", encoding="utf-8") as f:
            f.write(contenido)

        servicio = ServicioConfiguracion(ruta_cfg)
        cfg = servicio.cargar_configuracion()
        self.assertEqual(cfg.nombre_app, "Komorebi Mock")
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir.name, "backups")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir.name, "logs")))

    def test_cargar_archivo_inexistente_usa_defaults(self) -> None:
        servicio = ServicioConfiguracion(os.path.join(self.temp_dir.name, "inexistente.json"))
        cfg = servicio.cargar_configuracion()
        self.assertEqual(cfg.nombre_app, "Komorebi Mini IDE")


if __name__ == "__main__":
    unittest.main()
