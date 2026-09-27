"""Pruebas unitarias para el Patrón Command e Invocador."""

import tempfile
import unittest
from src.nucleo.contexto_app import ContextoApp
from src.nucleo.configuracion_app import ConfiguracionApp
from src.servicios.servicio_configuracion import ServicioConfiguracion
from src.servicios.servicio_archivos import ServicioArchivos
from src.servicios.servicio_sintaxis import ServicioSintaxis
from src.servicios.servicio_historial import ServicioHistorial
from src.servicios.servicio_diagnosticos import ServicioDiagnosticos
from src.servicios.servicio_cola_ia import ServicioColaIA
from src.servicios.servicio_cliente_ia import ServicioClienteIA

from src.comandos.invocador_comandos import InvocadorComandos
from src.comandos.comando_new import ComandoNew
from src.comandos.comando_list import ComandoList
from src.comandos.comando_switch import ComandoSwitch
from src.comandos.comando_delete import ComandoDelete
from src.comandos.comando_config import ComandoConfig
from src.comandos.comando_check import ComandoCheck
from src.comandos.comando_undo import ComandoUndo
from src.comandos.comando_redo import ComandoRedo
from src.comandos.comando_sort import ComandoSort
from src.comandos.comando_queue_status import ComandoQueueStatus
from src.comandos.comando_analyze import ComandoAnalyze
from src.comandos.comando_edit import ComandoEdit
from src.comandos.comando_show import ComandoShow
from src.comandos.comando_help import ComandoHelp


class TestPatronComandos(unittest.TestCase):
    """Pruebas exhaustivas para la integración del Patrón Command."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cfg = ConfiguracionApp(ruta_respaldos=self.temp_dir.name, api_key_ia="")
        self.contexto = ContextoApp(configuracion=self.cfg)

        # Inicialización de servicios
        self.serv_cfg = ServicioConfiguracion()
        self.serv_archivos = ServicioArchivos(self.contexto)
        self.serv_sintaxis = ServicioSintaxis()
        self.serv_historial = ServicioHistorial()
        self.serv_diagnosticos = ServicioDiagnosticos()
        self.serv_cola_ia = ServicioColaIA(self.contexto)
        self.serv_cliente_ia = ServicioClienteIA(self.cfg)

        # Invocador y registro de comandos
        self.invocador = InvocadorComandos()
        self.invocador.registrar_comando(ComandoNew(self.serv_archivos))
        self.invocador.registrar_comando(ComandoList(self.serv_archivos))
        self.invocador.registrar_comando(ComandoSwitch(self.serv_archivos))
        self.invocador.registrar_comando(ComandoDelete(self.serv_archivos))
        self.invocador.registrar_comando(ComandoConfig(self.serv_cfg, self.contexto))
        self.invocador.registrar_comando(ComandoCheck(self.serv_sintaxis, self.contexto))
        self.invocador.registrar_comando(ComandoUndo(self.serv_historial, self.serv_archivos, self.contexto))
        self.invocador.registrar_comando(ComandoRedo(self.serv_historial, self.serv_archivos, self.contexto))
        self.invocador.registrar_comando(ComandoSort(self.serv_diagnosticos, self.contexto))
        self.invocador.registrar_comando(ComandoQueueStatus(self.serv_cola_ia))
        self.invocador.registrar_comando(ComandoAnalyze(self.serv_cola_ia, self.serv_cliente_ia, self.contexto))
        self.invocador.registrar_comando(ComandoEdit(self.serv_historial, self.serv_archivos, self.contexto))
        self.invocador.registrar_comando(ComandoShow(self.contexto))
        self.invocador.registrar_comando(ComandoHelp(self.invocador))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_invocador_comando_desconocido(self) -> None:
        self.assertFalse(self.invocador.ejecutar_comando("desconocido", []))

    def test_flujo_archivos_new_list_switch_delete(self) -> None:
        # 1. new main.py
        self.assertTrue(self.invocador.ejecutar_comando("new", ["main.py", "def foo(): pass"]))
        self.assertEqual(len(self.contexto.archivos_abiertos), 1)
        self.assertEqual(self.contexto.archivo_activo.nombre, "main.py")

        # 2. new utils.py
        self.assertTrue(self.invocador.ejecutar_comando("new", ["utils.py"]))
        self.assertEqual(len(self.contexto.archivos_abiertos), 2)

        # 3. list
        self.assertTrue(self.invocador.ejecutar_comando("list", []))

        # 4. switch utils.py
        self.assertTrue(self.invocador.ejecutar_comando("switch", ["utils.py"]))
        self.assertEqual(self.contexto.archivo_activo.nombre, "utils.py")

        # 5. delete main.py
        self.assertTrue(self.invocador.ejecutar_comando("delete", ["main.py"]))
        self.assertEqual(len(self.contexto.archivos_abiertos), 1)

    def test_flujo_check_y_sort(self) -> None:
        # Crear archivo con error de sintaxis
        self.invocador.ejecutar_comando("new", ["test_sintaxis.py", "arr = [1, 2, 3)\nx = {1: 2]"])
        self.assertFalse(self.invocador.ejecutar_comando("check", []))
        self.assertGreaterEqual(len(self.contexto.diagnosticos), 2)

        # Ordenar diagnósticos por línea con mergesort
        self.assertTrue(self.invocador.ejecutar_comando("sort", ["line", "mergesort"]))
        self.assertTrue(self.invocador.ejecutar_comando("sort", ["severity", "shellsort", "desc"]))

    def test_flujo_edit_undo_redo_show(self) -> None:
        self.invocador.ejecutar_comando("new", ["buffer.txt", "linea 1"])

        # Edit agrega linea 2
        self.assertTrue(self.invocador.ejecutar_comando("edit", ["linea 2"]))
        self.assertEqual(self.contexto.archivo_activo.conteo_lineas, 2)

        # Undo revierte a linea 1
        self.assertTrue(self.invocador.ejecutar_comando("undo", []))
        self.assertEqual(self.contexto.archivo_activo.conteo_lineas, 1)

        # Redo vuelve a linea 2
        self.assertTrue(self.invocador.ejecutar_comando("redo", []))
        self.assertEqual(self.contexto.archivo_activo.conteo_lineas, 2)

        # Show
        self.assertTrue(self.invocador.ejecutar_comando("show", []))

    def test_flujo_queue_status_y_analyze(self) -> None:
        self.invocador.ejecutar_comando("new", ["algoritmo.py", "for i in range(10): print(i)"])
        self.assertTrue(self.invocador.ejecutar_comando("queue-status", []))

        # analyze envía código al buffer y cliente IA
        self.assertTrue(self.invocador.ejecutar_comando("analyze", []))

    def test_comando_help(self) -> None:
        self.assertTrue(self.invocador.ejecutar_comando("help", []))

    def test_comando_config(self) -> None:
        self.assertTrue(self.invocador.ejecutar_comando("config", []))


if __name__ == "__main__":
    unittest.main()
