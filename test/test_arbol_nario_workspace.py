"""Pruebas unitarias y de integración para Fase 1: NodoNario, ArbolNario, ServicioWorkspace y Comandos."""

import os
import tempfile
import unittest

from src.cli.consola_app import ConsolaApp
from src.comandos.comando_cd import ComandoCd
from src.comandos.comando_delete import ComandoDelete
from src.comandos.comando_list import ComandoList
from src.comandos.comando_ls import ComandoLs
from src.comandos.comando_mkdir import ComandoMkdir
from src.comandos.comando_mv import ComandoMv
from src.comandos.comando_new import ComandoNew
from src.comandos.comando_pwd import ComandoPwd
from src.comandos.comando_switch import ComandoSwitch
from src.comandos.comando_tree import ComandoTree
from src.comandos.invocador_comandos import InvocadorComandos
from src.estructuras.arbol_nario import ArbolNario
from src.estructuras.nodo_nario import NodoNario
from src.excepciones.movimiento_invalido_error import MovimientoInvalidoError
from src.excepciones.nombre_duplicado_error import NombreDuplicadoError
from src.excepciones.ruta_invalida_error import RutaInvalidaError
from src.nucleo.archivo_codigo import ArchivoCodigo
from src.nucleo.configuracion_app import ConfiguracionApp
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_archivos import ServicioArchivos
from src.servicios.servicio_navegacion import ServicioNavegacion
from src.servicios.servicio_workspace import ServicioWorkspace


class TestArbolNarioWorkspace(unittest.TestCase):
    """Pruebas exhaustivas para el Árbol N-ario y su coordinación con ServicioArchivos y disco."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cfg = ConfiguracionApp(ruta_respaldos=self.temp_dir.name)
        self.contexto = ContextoApp(configuracion=self.cfg)
        self.serv_archivos = ServicioArchivos(self.contexto)
        self.serv_workspace = ServicioWorkspace(self.contexto, self.serv_archivos)

        self.serv_navegacion = ServicioNavegacion(self.contexto, self.serv_workspace)

        self.invocador = InvocadorComandos()
        self.invocador.registrar_comando(ComandoNew(self.serv_archivos))
        self.invocador.registrar_comando(ComandoList(self.serv_archivos))
        self.invocador.registrar_comando(ComandoSwitch(self.serv_archivos))
        self.invocador.registrar_comando(ComandoDelete(self.serv_archivos))
        self.invocador.registrar_comando(ComandoMkdir(self.serv_workspace))
        self.invocador.registrar_comando(ComandoCd(self.serv_navegacion))
        self.invocador.registrar_comando(ComandoPwd(self.serv_navegacion))
        self.invocador.registrar_comando(ComandoLs(self.serv_navegacion))
        self.invocador.registrar_comando(ComandoTree(self.serv_workspace))
        self.invocador.registrar_comando(ComandoMv(self.serv_workspace))
        self.consola = ConsolaApp(self.invocador, self.contexto)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_nodo_archivo_no_puede_tener_hijos(self) -> None:
        arc = ArchivoCodigo("main.py", "print(1)")
        nodo_arch = NodoNario("main.py", NodoNario.TIPO_ARCHIVO, archivo=arc)
        sub = NodoNario("sub", NodoNario.TIPO_CARPETA)
        with self.assertRaises(RutaInvalidaError):
            nodo_arch.agregar_hijo(sub)

    def test_nombres_duplicados_entre_hermanos(self) -> None:
        self.serv_workspace.crear_carpeta("src")
        with self.assertRaises(NombreDuplicadoError):
            self.serv_workspace.crear_carpeta("src")

        self.serv_archivos.crear_archivo("src/app.py", "x = 1")
        with self.assertRaises(NombreDuplicadoError):
            self.serv_archivos.crear_archivo("src/app.py", "x = 2")

    def test_mover_carpeta_a_si_misma_o_descendiente_lanza_error(self) -> None:
        self.serv_workspace.crear_carpeta("a")
        self.serv_workspace.crear_carpeta("a/b")
        self.serv_workspace.crear_carpeta("a/b/c")

        with self.assertRaises(MovimientoInvalidoError):
            self.serv_workspace.mover("/a", "/a")

        with self.assertRaises(MovimientoInvalidoError):
            self.serv_workspace.mover("/a", "/a/b/c")

    def test_cd_rutas_relativas_absolutas_E_inexistentes(self) -> None:
        self.serv_workspace.crear_carpeta("src")
        self.serv_workspace.crear_carpeta("src/nucleo")
        self.serv_archivos.crear_archivo("src/app.py", "pass")

        self.assertEqual(self.consola.generar_prompt(), "Komorebi [/]> ")
        self.serv_workspace.cambiar_directorio("src")
        self.assertEqual(self.consola.generar_prompt(), "Komorebi [/src]> ")

        self.serv_workspace.cambiar_directorio("./nucleo")
        self.assertEqual(self.serv_workspace.obtener_directorio_actual(), "/src/nucleo")

        self.serv_workspace.cambiar_directorio("..")
        self.assertEqual(self.serv_workspace.obtener_directorio_actual(), "/src")

        # No se puede hacer cd a un archivo
        with self.assertRaises(RutaInvalidaError):
            self.serv_workspace.cambiar_directorio("app.py")

        # No se puede hacer cd a ruta inexistente
        with self.assertRaises(RutaInvalidaError):
            self.serv_workspace.cambiar_directorio("/no_existe/jamás")

    def test_tree_con_carpetas_vacias_y_archivos(self) -> None:
        self.serv_workspace.crear_carpeta("src")
        self.serv_workspace.crear_carpeta("docs_vacio")
        self.serv_archivos.crear_archivo("src/main.py", "pass")
        self.serv_archivos.crear_archivo("README.md", "# titulo")

        lineas = self.serv_workspace.mostrar_arbol("/")
        esperado = [
            "/",
            "├── src/",
            "│   └── main.py",
            "├── docs_vacio/",
            "└── README.md",
        ]
        self.assertEqual(lineas, esperado)

    def test_anidamiento_profundo_sin_recursion_error(self) -> None:
        arbol = ArbolNario()
        actual = arbol.raiz
        profundidad = 1200
        for i in range(profundidad):
            nuevo = NodoNario(f"dir_{i}", NodoNario.TIPO_CARPETA)
            actual.agregar_hijo(nuevo)
            actual = nuevo

        lineas = arbol.generar_lineas_tree()
        self.assertEqual(len(lineas), profundidad + 1)
        self.assertIn("└── dir_1199/", lineas[-1])

    def test_sincronia_arbol_lista_y_disco_con_mv_y_delete(self) -> None:
        self.assertTrue(self.consola.ejecutar_linea("mkdir src"))
        self.assertTrue(self.consola.ejecutar_linea("mkdir lib"))
        self.assertTrue(self.consola.ejecutar_linea("cd ws:/src"))
        self.assertTrue(self.consola.ejecutar_linea("new app.py print('hola')"))

        # Verificar que el objeto ArchivoCodigo en ListaEnlazada y en ArbolNario es EL MISMO (idéntica referencia)
        archivo_en_lista = self.contexto.archivos_abiertos.obtener_por_indice(0)
        nodo_en_arbol = self.serv_workspace.arbol.resolver_ruta("/src/app.py")
        self.assertIs(archivo_en_lista, nodo_en_arbol.archivo)

        # Verificar respaldo físico en respaldos/src/app.py
        ruta_fisica_orig = os.path.join(self.temp_dir.name, "src", "app.py")
        self.assertTrue(os.path.isfile(ruta_fisica_orig))

        # Mover /src/app.py a /lib/modulo.py
        self.assertTrue(self.consola.ejecutar_linea("mv /src/app.py /lib/modulo.py"))
        ruta_fisica_nueva = os.path.join(self.temp_dir.name, "lib", "modulo.py")
        self.assertFalse(os.path.exists(ruta_fisica_orig))
        self.assertTrue(os.path.isfile(ruta_fisica_nueva))
        self.assertEqual(archivo_en_lista.nombre, "modulo.py")

        # Eliminar archivo con delete
        self.assertTrue(self.consola.ejecutar_linea("delete /lib/modulo.py"))
        self.assertEqual(len(self.contexto.archivos_abiertos), 0)
        self.assertFalse(os.path.exists(ruta_fisica_nueva))
        with self.assertRaises(RutaInvalidaError):
            self.serv_workspace.arbol.resolver_ruta("/lib/modulo.py")

    def test_ambiguedad_mismo_nombre_en_distintas_carpetas(self) -> None:
        self.consola.ejecutar_linea("mkdir src")
        self.consola.ejecutar_linea("mkdir test")
        self.consola.ejecutar_linea("new /src/app.py x=1")
        self.consola.ejecutar_linea("new /test/app.py x=2")

        # switch sin ruta debe fallar por ambigüedad (capturado por ConsolaApp retornando False)
        self.assertFalse(self.consola.ejecutar_linea("switch app.py"))
        self.assertFalse(self.consola.ejecutar_linea("list app.py"))

        # switch indicando ruta completa funciona sin ambigüedad
        self.assertTrue(self.consola.ejecutar_linea("switch /test/app.py"))
        self.assertEqual(self.contexto.archivo_activo.contenido, "x=2")


if __name__ == "__main__":
    unittest.main()

