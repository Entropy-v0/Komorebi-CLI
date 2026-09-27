"""Pruebas unitarias para ServicioArchivos."""

import os
import tempfile
import unittest
from src.nucleo.contexto_app import ContextoApp
from src.nucleo.configuracion_app import ConfiguracionApp
from src.servicios.servicio_archivos import ServicioArchivos


class TestServicioArchivos(unittest.TestCase):
    """Pruebas para ServicioArchivos."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cfg = ConfiguracionApp(ruta_respaldos=self.temp_dir.name)
        self.contexto = ContextoApp(configuracion=self.cfg)
        self.servicio = ServicioArchivos(self.contexto)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_crear_archivo_y_respaldo_automatico(self) -> None:
        archivo = self.servicio.crear_archivo("main.cpp", "int main() { return 0; }")
        self.assertEqual(archivo.nombre, "main.cpp")
        self.assertEqual(len(self.contexto.archivos_abiertos), 1)
        self.assertEqual(self.servicio.obtener_archivo_activo(), archivo)

        # Verificar que el archivo de respaldo existe en disco
        ruta_respaldo = os.path.join(self.temp_dir.name, "main.cpp")
        self.assertTrue(os.path.exists(ruta_respaldo))
        with open(ruta_respaldo, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "int main() { return 0; }")

    def test_crear_archivo_duplicado_lanza_error(self) -> None:
        self.servicio.crear_archivo("app.py", "pass")
        with self.assertRaises(ValueError):
            self.servicio.crear_archivo("app.py", "otra cosa")

    def test_cambiar_archivo_activo_por_nombre_e_indice(self) -> None:
        arc1 = self.servicio.crear_archivo("primero.py")
        arc2 = self.servicio.crear_archivo("segundo.py")

        self.assertEqual(self.servicio.obtener_archivo_activo(), arc1)
        # Cambio por nombre
        self.assertTrue(self.servicio.cambiar_archivo_activo("segundo.py"))
        self.assertEqual(self.servicio.obtener_archivo_activo(), arc2)

        # Cambio por índice (1-based: "1" debe ser primero.py)
        self.assertTrue(self.servicio.cambiar_archivo_activo("1"))
        self.assertEqual(self.servicio.obtener_archivo_activo(), arc1)

    def test_cerrar_archivo(self) -> None:
        self.servicio.crear_archivo("f1.py")
        self.servicio.crear_archivo("f2.py")

        self.assertTrue(self.servicio.cerrar_archivo("f1.py"))
        self.assertEqual(len(self.contexto.archivos_abiertos), 1)
        self.assertEqual(self.servicio.obtener_archivo_activo().nombre, "f2.py")

    def test_listar_archivos(self) -> None:
        self.servicio.crear_archivo("a.txt")
        self.servicio.crear_archivo("b.txt")

        lista = self.servicio.listar_archivos()
        self.assertEqual(len(lista), 2)
        idx, arc, es_activo = lista[0]
        self.assertEqual(idx, 1)
        self.assertEqual(arc.nombre, "a.txt")
        self.assertTrue(es_activo)


if __name__ == "__main__":
    unittest.main()
