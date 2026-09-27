"""Pruebas unitarias para el modelo ContextoApp."""

import unittest
from src.nucleo.contexto_app import ContextoApp
from src.nucleo.archivo_codigo import ArchivoCodigo
from src.nucleo.diagnostico import Diagnostico
from src.nucleo.peticion_ia import PeticionIA


class TestContextoApp(unittest.TestCase):
    """Pruebas completas para la gestión de estado global en ContextoApp."""

    def setUp(self) -> None:
        self.contexto = ContextoApp()

    def test_estado_inicial(self) -> None:
        self.assertTrue(self.contexto.archivos_abiertos.esta_vacia())
        self.assertIsNone(self.contexto.archivo_activo)
        self.assertTrue(self.contexto.cola_ia.esta_vacia())
        self.assertEqual(self.contexto.diagnosticos, [])
        self.assertIsNotNone(self.contexto.configuracion)

    def test_abrir_archivos_y_activo(self) -> None:
        arc1 = ArchivoCodigo("main.py", "print('1')")
        arc2 = ArchivoCodigo("utils.py", "print('2')")

        self.contexto.abrir_archivo(arc1)
        self.assertEqual(self.contexto.archivo_activo, arc1)
        self.assertEqual(len(self.contexto.archivos_abiertos), 1)

        self.contexto.abrir_archivo(arc2)
        # El activo sigue siendo arc1 a menos que se cambie explícitamente
        self.assertEqual(self.contexto.archivo_activo, arc1)
        self.assertEqual(len(self.contexto.archivos_abiertos), 2)

    def test_cambiar_archivo_activo(self) -> None:
        arc1 = ArchivoCodigo("a.txt")
        arc2 = ArchivoCodigo("b.txt")
        self.contexto.abrir_archivo(arc1)
        self.contexto.abrir_archivo(arc2)

        self.assertTrue(self.contexto.cambiar_archivo_activo("b.txt"))
        self.assertEqual(self.contexto.archivo_activo, arc2)

        self.assertFalse(self.contexto.cambiar_archivo_activo("no_existe.txt"))
        self.assertEqual(self.contexto.archivo_activo, arc2)

    def test_cerrar_archivo_activo_reasigna_referencia(self) -> None:
        arc1 = ArchivoCodigo("primero.py")
        arc2 = ArchivoCodigo("segundo.py")
        self.contexto.abrir_archivo(arc1)
        self.contexto.abrir_archivo(arc2)

        # Cerramos el activo actual (arc1)
        self.assertTrue(self.contexto.cerrar_archivo("primero.py"))
        self.assertEqual(len(self.contexto.archivos_abiertos), 1)
        # El activo debe reasignarse automáticamente a arc2
        self.assertEqual(self.contexto.archivo_activo, arc2)

        # Cerramos el último restante
        self.assertTrue(self.contexto.cerrar_archivo("segundo.py"))
        self.assertTrue(self.contexto.archivos_abiertos.esta_vacia())
        self.assertIsNone(self.contexto.archivo_activo)

    def test_cola_ia_en_contexto(self) -> None:
        pet1 = PeticionIA("codigo1")
        pet2 = PeticionIA("codigo2")

        self.contexto.encolar_peticion_ia(pet1)
        self.contexto.encolar_peticion_ia(pet2)
        self.assertEqual(len(self.contexto.cola_ia), 2)

        desencolada = self.contexto.desencolar_peticion_ia()
        self.assertEqual(desencolada.id_peticion, pet1.id_peticion)
        self.assertEqual(len(self.contexto.cola_ia), 1)

    def test_diagnosticos_en_contexto(self) -> None:
        diags = [
            Diagnostico(10, "WARN", "Variable sin usar"),
            Diagnostico(25, "ERROR", "Sintaxis inválida"),
        ]
        self.contexto.diagnosticos = diags
        self.assertEqual(len(self.contexto.diagnosticos), 2)
        self.assertEqual(self.contexto.diagnosticos[0].severidad, "WARN")


if __name__ == "__main__":
    unittest.main()
