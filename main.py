"""Punto de entrada principal y bootstrap del Mini IDE Komorebi.

Inicializa el contexto global, carga la configuración externa, instancia los servicios
de negocio, registra los comandos en el Invocador e inicia el bucle interactivo REPL.
"""

import sys
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_configuracion import ServicioConfiguracion
from src.servicios.servicio_archivos import ServicioArchivos
from src.servicios.servicio_sintaxis import ServicioSintaxis
from src.servicios.servicio_historial import ServicioHistorial
from src.servicios.servicio_diagnosticos import ServicioDiagnosticos
from src.servicios.servicio_cola_ia import ServicioColaIA
from src.servicios.servicio_cliente_ia import ServicioClienteIA
from src.servicios.servicio_logs import ServicioLogs

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
from src.comandos.comando_exit import ComandoExit

from src.cli.consola_app import ConsolaApp


def bootstrap(ruta_config: str = "config.json") -> ConsolaApp:
    """Configura y enlaza todas las capas de la arquitectura Komorebi.
    
    Returns:
        Instancia de ConsolaApp lista para iniciar el bucle REPL o ejecutar comandos.
    """
    # 1. Carga de configuración externa
    servicio_configuracion = ServicioConfiguracion(ruta_config)
    configuracion = servicio_configuracion.cargar_configuracion()

    # 2. Inicialización del estado global de la sesión
    contexto = ContextoApp(configuracion=configuracion)

    # 3. Inicialización de los servicios de negocio (Receptores)
    servicio_logs = ServicioLogs(configuracion.ruta_logs)
    servicio_archivos = ServicioArchivos(contexto, servicio_logs)
    servicio_sintaxis = ServicioSintaxis()
    servicio_historial = ServicioHistorial()
    servicio_diagnosticos = ServicioDiagnosticos()
    servicio_cola_ia = ServicioColaIA(contexto)
    servicio_cliente_ia = ServicioClienteIA(configuracion, servicio_logs)

    # 4. Inicialización del despachador y registro de comandos (Patrón Command)
    invocador = InvocadorComandos()
    invocador.registrar_comando(ComandoNew(servicio_archivos))
    invocador.registrar_comando(ComandoList(servicio_archivos))
    invocador.registrar_comando(ComandoSwitch(servicio_archivos))
    invocador.registrar_comando(ComandoDelete(servicio_archivos))
    invocador.registrar_comando(ComandoConfig(servicio_configuracion, contexto))
    invocador.registrar_comando(ComandoCheck(servicio_sintaxis, contexto))
    invocador.registrar_comando(ComandoUndo(servicio_historial, servicio_archivos, contexto))
    invocador.registrar_comando(ComandoRedo(servicio_historial, servicio_archivos, contexto))
    invocador.registrar_comando(ComandoSort(servicio_diagnosticos, contexto))
    invocador.registrar_comando(ComandoQueueStatus(servicio_cola_ia))
    invocador.registrar_comando(ComandoAnalyze(servicio_cola_ia, servicio_cliente_ia, contexto))
    invocador.registrar_comando(ComandoEdit(servicio_historial, servicio_archivos, contexto))
    invocador.registrar_comando(ComandoShow(contexto))
    invocador.registrar_comando(ComandoHelp(invocador))
    invocador.registrar_comando(ComandoExit())

    # 5. Creación de la consola interactiva CLI
    return ConsolaApp(invocador, contexto, servicio_logs=servicio_logs)


def main() -> None:
    """Función de arranque de la aplicación."""
    ruta_config = "config.json"
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-c", "--config") and len(sys.argv) > 2:
            ruta_config = sys.argv[2]
        elif not sys.argv[1].startswith("-"):
            ruta_config = sys.argv[1]

    consola = bootstrap(ruta_config)
    consola.iniciar_repl()


if __name__ == "__main__":
    main()
