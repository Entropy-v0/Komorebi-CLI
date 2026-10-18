"""Pruebas unitarias para el modelo ArchivoCodigo."""

import unittest
from datetime import datetime
from src.nucleo.archivo_codigo import ArchivoCodigo


class TestArchivoCodigo(unittest.TestCase):
    """Pruebas para la clase ArchivoCodigo."""

    def test_creacion_archivo(self) -> None:
        archivo = ArchivoCodigo("test.py", "print('Hola')\nprint('Mundo')")
        self.assertEqual(archivo.nombre, "test.py")
        self.assertEqual(archivo.contenido, "print('Hola')\nprint('Mundo')")
        self.assertEqual(archivo.conteo_lineas, 2)
        self.assertIsInstance(archivo.fecha_creacion, datetime)
        self.assertIsInstance(archivo.fecha_modificacion, datetime)
        self.assertIn("test.py", repr(archivo))
        self.assertIn("2 líneas", str(archivo))

    def test_modificar_contenido(self) -> None:
        archivo = ArchivoCodigo("main.cpp", "int main() {}")
        fecha_orig = archivo.fecha_modificacion
        archivo.modificar_contenido("int main() {\n    return 0;\n}")
        self.assertEqual(archivo.conteo_lineas, 3)
        self.assertGreaterEqual(archivo.fecha_modificacion, fecha_orig)

    def test_renombrar_archivo(self) -> None:
        archivo = ArchivoCodigo("viejo.txt", "contenido")
        archivo.nombre = "nuevo.txt"
        self.assertEqual(archivo.nombre, "nuevo.txt")

    def test_archivo_vacio(self) -> None:
        archivo = ArchivoCodigo("vacio.py")
        self.assertEqual(archivo.conteo_lineas, 0)
        self.assertEqual(archivo.obtener_lineas(), [])

    def test_id_unico_e_inmutable(self) -> None:
        arc1 = ArchivoCodigo("app.py", "x = 1")
        arc2 = ArchivoCodigo("app.py", "x = 2")
        self.assertTrue(arc1.id_archivo.startswith("file-"))
        self.assertEqual(arc1.id_archivo, arc1.id)
        self.assertNotEqual(arc1.id_archivo, arc2.id_archivo)
        self.assertNotEqual(arc1, arc2)

        with self.assertRaises(AttributeError):
            arc1.id_archivo = "otro-id"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
