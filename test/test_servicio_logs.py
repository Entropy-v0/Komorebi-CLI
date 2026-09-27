"""Pruebas unitarias para el ServicioLogs."""

import os
import tempfile
import unittest
from src.servicios.servicio_logs import ServicioLogs


class TestServicioLogs(unittest.TestCase):
    """Pruebas para ServicioLogs."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ruta_logs = os.path.join(self.temp_dir.name, "mis_logs")
        self.servicio = ServicioLogs(self.ruta_logs)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_inicializacion_crea_directorio(self) -> None:
        self.assertTrue(os.path.isdir(self.ruta_logs))
        self.assertEqual(self.servicio.ruta_directorio, self.ruta_logs)
        self.assertEqual(
            self.servicio.ruta_archivo_errores,
            os.path.join(self.ruta_logs, "errores.log")
        )

    def test_registrar_error_y_leer(self) -> None:
        self.servicio.registrar_error("ModuloPrueba", "Error critico simulado")
        self.assertTrue(os.path.isfile(self.servicio.ruta_archivo_errores))

        lineas = self.servicio.leer_ultimos_errores()
        self.assertEqual(len(lineas), 1)
        self.assertIn("[ERROR]", lineas[0])
        self.assertIn("[ModuloPrueba]", lineas[0])
        self.assertIn("Error critico simulado", lineas[0])

    def test_registrar_multiples_niveles(self) -> None:
        self.servicio.registrar_info("Init", "Sistema iniciado")
        self.servicio.registrar_advertencia("Buffer", "Capacidad al 80%")
        self.servicio.registrar_error("Red", "Timeout de conexion")

        lineas = self.servicio.leer_ultimos_errores()
        self.assertEqual(len(lineas), 3)
        self.assertIn("[INFO]", lineas[0])
        self.assertIn("[WARNING]", lineas[1])
        self.assertIn("[ERROR]", lineas[2])

    def test_leer_con_limite(self) -> None:
        for i in range(5):
            self.servicio.registrar_error("Bucle", f"Fallo {i}")

        ultimos_dos = self.servicio.leer_ultimos_errores(limite=2)
        self.assertEqual(len(ultimos_dos), 2)
        self.assertIn("Fallo 3", ultimos_dos[0])
        self.assertIn("Fallo 4", ultimos_dos[1])

    def test_limpiar_logs(self) -> None:
        self.servicio.registrar_error("Modulo", "Error previo")
        self.assertEqual(len(self.servicio.leer_ultimos_errores()), 1)

        self.servicio.limpiar_logs()
        self.assertEqual(len(self.servicio.leer_ultimos_errores()), 0)


if __name__ == "__main__":
    unittest.main()
