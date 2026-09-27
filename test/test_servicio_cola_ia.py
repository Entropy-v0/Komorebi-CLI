"""Pruebas unitarias para ServicioColaIA."""

import unittest
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_cola_ia import ServicioColaIA


class TestServicioColaIA(unittest.TestCase):
    """Pruebas para ServicioColaIA."""

    def setUp(self) -> None:
        self.contexto = ContextoApp()
        self.servicio = ServicioColaIA(self.contexto)

    def test_encolar_y_estado(self) -> None:
        self.assertTrue(self.servicio.esta_vacia())
        self.assertEqual(self.servicio.tamano, 0)

        pet1 = self.servicio.encolar("codigo 1", "f1.py")
        pet2 = self.servicio.encolar("codigo 2", "f2.py")

        self.assertFalse(self.servicio.esta_vacia())
        self.assertEqual(self.servicio.tamano, 2)
        self.assertEqual(self.servicio.consultar_frente().id_peticion, pet1.id_peticion)

        estado = self.servicio.obtener_estado()
        self.assertEqual(estado["total_pendientes"], 2)
        self.assertEqual(estado["proxima_peticion"], pet1.id_peticion)
        self.assertEqual(estado["archivo_proximo"], "f1.py")

    def test_desencolar_secuencial(self) -> None:
        pet1 = self.servicio.encolar("c1")
        pet2 = self.servicio.encolar("c2")

        extraido_1 = self.servicio.desencolar_siguiente()
        self.assertEqual(extraido_1.id_peticion, pet1.id_peticion)
        self.assertEqual(self.servicio.tamano, 1)

        extraido_2 = self.servicio.desencolar_siguiente()
        self.assertEqual(extraido_2.id_peticion, pet2.id_peticion)
        self.assertTrue(self.servicio.esta_vacia())
        self.assertIsNone(self.servicio.desencolar_siguiente())


if __name__ == "__main__":
    unittest.main()
