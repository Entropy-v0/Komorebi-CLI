"""Pruebas unitarias para la capa de interfaz CLI."""

import tempfile
import unittest
from src.nucleo.contexto_app import ContextoApp
from src.nucleo.configuracion_app import ConfiguracionApp
from src.nucleo.archivo_codigo import ArchivoCodigo
from src.comandos.invocador_comandos import InvocadorComandos
from src.comandos.comando_new import ComandoNew
from src.servicios.servicio_archivos import ServicioArchivos
from src.cli.analizador_comandos import AnalizadorComandos
from src.cli.consola_app import ConsolaApp


class TestCLI(unittest.TestCase):
    """Pruebas unitarias para AnalizadorComandos y ConsolaApp."""

    def setUp(self) -> None:
        self.analizador = AnalizadorComandos()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cfg = ConfiguracionApp(ruta_respaldos=self.temp_dir.name)
        self.contexto = ContextoApp(configuracion=self.cfg)
        self.invocador = InvocadorComandos()
        self.serv_archivos = ServicioArchivos(self.contexto)
        self.invocador.registrar_comando(ComandoNew(self.serv_archivos))
        self.consola = ConsolaApp(self.invocador, self.contexto, self.analizador)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_analizador_tokenizacion_simple(self) -> None:
        cmd, args = self.analizador.parsear("new main.py")
        self.assertEqual(cmd, "new")
        self.assertEqual(args, ["main.py"])

    def test_analizador_con_comillas(self) -> None:
        cmd, args = self.analizador.parsear('edit "print(\'Hola Mundo\')"')
        self.assertEqual(cmd, "edit")
        self.assertEqual(args, ["print('Hola Mundo')"])

    def test_analizador_mayusculas_y_espacios(self) -> None:
        cmd, args = self.analizador.parsear("   CHECK   ")
        self.assertEqual(cmd, "check")
        self.assertEqual(args, [])

    def test_analizador_entrada_vacia(self) -> None:
        cmd, args = self.analizador.parsear("   ")
        self.assertEqual(cmd, "")
        self.assertEqual(args, [])

    def test_prompt_dinamico(self) -> None:
        # Inicialmente sin archivo
        self.assertEqual(self.consola.generar_prompt(), "Komorebi [sin-archivo]> ")

        # Al abrir archivo activo
        self.contexto.archivo_activo = ArchivoCodigo("demo.py")
        self.assertEqual(self.consola.generar_prompt(), "Komorebi [demo.py]> ")

    def test_consola_ejecutar_linea(self) -> None:
        self.assertTrue(self.consola.ejecutar_linea("new main.cpp int main(){}"))
        self.assertEqual(self.contexto.archivo_activo.nombre, "main.cpp")
        self.assertEqual(self.consola.generar_prompt(), "Komorebi [main.cpp]> ")

        # Línea vacía no debe fallar
        self.assertTrue(self.consola.ejecutar_linea("   "))


if __name__ == "__main__":
    unittest.main()
