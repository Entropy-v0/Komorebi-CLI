"""Pruebas de navegación híbrida: sistema de archivos real del SO y Workspace virtual."""

import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout

from main import bootstrap
from src.excepciones.ruta_invalida_error import RutaInvalidaError
from src.nucleo.configuracion_app import ConfiguracionApp
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_navegacion import ServicioNavegacion
from src.servicios.servicio_workspace import ServicioWorkspace


class TestNavegacionHibrida(unittest.TestCase):
    """Verifica `cd`, `ls` y `pwd` sobre el SO real y el Workspace virtual (`ws:`)."""

    def setUp(self) -> None:
        self._raiz = os.path.realpath(tempfile.mkdtemp(prefix="komorebi_nav_"))
        os.makedirs(os.path.join(self._raiz, "proyecto", "src"))
        os.makedirs(os.path.join(self._raiz, "otro"))
        with open(os.path.join(self._raiz, "proyecto", "leeme.txt"), "w", encoding="utf-8") as f:
            f.write("hola")
        with open(os.path.join(self._raiz, "proyecto", ".oculto"), "w", encoding="utf-8") as f:
            f.write("x")

        self._contexto = ContextoApp()
        self._contexto.ubicacion_real = self._raiz
        self._servicio = ServicioNavegacion(
            self._contexto,
            ServicioWorkspace(self._contexto),
            iniciar_en_sistema_real=True,
        )

    def tearDown(self) -> None:
        shutil.rmtree(self._raiz, ignore_errors=True)

    def test_cd_absoluto_relativo_padre_y_anterior(self) -> None:
        destino = os.path.join(self._raiz, "proyecto")
        self.assertEqual(self._servicio.cambiar_directorio(destino), destino)
        self.assertEqual(self._servicio.cambiar_directorio("src"), os.path.join(destino, "src"))
        self.assertEqual(self._servicio.cambiar_directorio("../.."), self._raiz)
        self.assertEqual(self._servicio.cambiar_directorio("-"), os.path.join(destino, "src"))
        self.assertEqual(self._servicio.obtener_ubicacion_actual(), os.path.join(destino, "src"))

    def test_cd_sin_argumento_va_al_directorio_personal(self) -> None:
        self.assertEqual(
            self._servicio.cambiar_directorio(""), os.path.normpath(os.path.expanduser("~"))
        )

    def test_cd_permite_salir_hacia_la_raiz_del_sistema(self) -> None:
        self.assertEqual(self._servicio.cambiar_directorio("/"), os.path.abspath(os.sep))
        self.assertEqual(self._servicio.cambiar_directorio(".."), os.path.abspath(os.sep))

    def test_cd_errores_descriptivos(self) -> None:
        with self.assertRaises(RutaInvalidaError):
            self._servicio.cambiar_directorio("no_existe_jamas")
        with self.assertRaises(RutaInvalidaError):
            self._servicio.cambiar_directorio(os.path.join("proyecto", "leeme.txt"))
        with self.assertRaises(RutaInvalidaError):
            self._servicio.cambiar_directorio("-")  # aún no hay directorio anterior

    def test_ls_ordenado_oculto_y_ruta_explicita(self) -> None:
        self._servicio.cambiar_directorio("proyecto")
        self.assertEqual(self._servicio.listar(), [("leeme.txt", False), ("src", True)])
        self.assertEqual(
            self._servicio.listar(mostrar_ocultos=True),
            [(".oculto", False), ("leeme.txt", False), ("src", True)],
        )
        self.assertEqual(self._servicio.listar(".."), [("otro", True), ("proyecto", True)])

    def test_workspace_virtual_con_prefijo_ws(self) -> None:
        contexto = ContextoApp(
            configuracion=ConfiguracionApp(ruta_respaldos=os.path.join(self._raiz, "respaldos"))
        )
        contexto.ubicacion_real = self._raiz
        servicio_ws = ServicioWorkspace(contexto)
        servicio_ws.crear_carpeta("virtual")
        servicio = ServicioNavegacion(contexto, servicio_ws, iniciar_en_sistema_real=True)

        self.assertEqual(servicio.cambiar_directorio("ws:/virtual"), "ws:/virtual")
        self.assertEqual(contexto.modo_navegacion, ContextoApp.MODO_WORKSPACE)
        self.assertEqual(servicio.listar("ws:/"), [("virtual", True)])
        self.assertEqual(servicio.cambiar_directorio("@ws"), "ws:/")

        # Volver al SO real conserva el cursor real previo
        self.assertEqual(servicio.cambiar_directorio(self._raiz), self._raiz)
        self.assertEqual(contexto.modo_navegacion, ContextoApp.MODO_REAL)

    def test_repl_bootstrap_navegacion_prompt_y_comandos(self) -> None:
        ruta_config = os.path.join(self._raiz, "config.json")
        with open(ruta_config, "w", encoding="utf-8") as f:
            f.write(
                "{\n"
                f'  "ruta_respaldos": "{os.path.join(self._raiz, "respaldos")}",\n'
                f'  "ruta_logs": "{os.path.join(self._raiz, "logs")}"\n'
                "}\n"
            )
        consola = bootstrap(ruta_config)
        self.assertTrue(consola.generar_prompt().startswith("Komorebi ["))

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.assertTrue(consola.ejecutar_linea(f'cd "{self._raiz}"'))
            self.assertEqual(consola.generar_prompt(), f"Komorebi [{self._raiz}]> ")
            self.assertTrue(consola.ejecutar_linea("ls"))
            self.assertTrue(consola.ejecutar_linea("cd proyecto"))
            self.assertTrue(consola.ejecutar_linea("pwd"))
            self.assertTrue(consola.ejecutar_linea("ls -a"))
            self.assertFalse(consola.ejecutar_linea("cd carpeta_inexistente"))
            self.assertTrue(consola.ejecutar_linea("cd ws:/"))
            self.assertEqual(consola.generar_prompt(), "Komorebi [ws:/]> ")

        salida = buffer.getvalue()
        self.assertIn("otro/", salida)
        self.assertIn(os.path.join(self._raiz, "proyecto"), salida)
        self.assertIn(".oculto", salida)
        self.assertIn("No existe el directorio", salida)


if __name__ == "__main__":
    unittest.main()

