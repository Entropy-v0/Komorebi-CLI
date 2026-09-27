"""Módulo de la consola interactiva REPL de la aplicación Komorebi."""

import sys
from typing import Optional
from src.cli.analizador_comandos import AnalizadorComandos
from src.comandos.invocador_comandos import InvocadorComandos
from src.nucleo.contexto_app import ContextoApp


class ConsolaApp:
    """Gestiona el bucle interactivo de terminal (REPL - Read, Eval, Print Loop).
    
    Genera el prompt dinámico indicando el archivo activo: 'Komorebi [archivo_activo]> ',
    sin menús de opciones numéricos para cumplir estrictamente con los requisitos de la cátedra.
    """

    def __init__(
        self,
        invocador: InvocadorComandos,
        contexto: ContextoApp,
        analizador: Optional[AnalizadorComandos] = None,
    ) -> None:
        self._invocador: InvocadorComandos = invocador
        self._contexto: ContextoApp = contexto
        self._analizador: AnalizadorComandos = analizador or AnalizadorComandos()
        self._en_ejecucion: bool = False

    @property
    def invocador(self) -> InvocadorComandos:
        """Retorna el despachador de comandos asociado."""
        return self._invocador

    @property
    def contexto(self) -> ContextoApp:
        """Retorna el contexto de estado de la aplicación."""
        return self._contexto

    def generar_prompt(self) -> str:
        """Genera el texto del prompt dinámico según el archivo activo actual."""
        archivo_activo = self._contexto.archivo_activo
        nombre_mostrado = archivo_activo.nombre if archivo_activo else "sin-archivo"
        return f"Komorebi [{nombre_mostrado}]> "

    def ejecutar_linea(self, linea: str) -> bool:
        """Procesa una única línea de comando (útil para pruebas y modo por lotes)."""
        nombre_cmd, args = self._analizador.parsear(linea)
        if not nombre_cmd:
            return True
        return self._invocador.ejecutar_comando(nombre_cmd, args)

    def iniciar_repl(self) -> None:
        """Inicia el ciclo continuo de terminal hasta que el usuario invoque 'exit' o Ctrl+D."""
        self._imprimir_bienvenida()
        self._en_ejecucion = True

        while self._en_ejecucion:
            try:
                linea = input(self.generar_prompt())
                self.ejecutar_linea(linea)
            except (KeyboardInterrupt, EOFError):
                print("\n[Sesión] Finalizando Komorebi Mini IDE por interrupción del usuario.")
                self._en_ejecucion = False
                break
            except SystemExit:
                self._en_ejecucion = False
                break
            except Exception as e:
                print(f"[Error no controlado] {str(e)}")

    def _imprimir_bienvenida(self) -> None:
        """Imprime la cabecera informativa de inicio del Mini IDE."""
        app_nombre = self._contexto.configuracion.nombre_app
        print("=" * 68)
        print(f"  {app_nombre.upper()} - Algoritmos y Estructuras II")
        print("  Patrón Command • Estructuras desde Cero • Sin Menús Numéricos")
        print("  Escribe 'help' para ver la lista de comandos disponibles.")
        print("  Escribe 'exit' para cerrar la sesión.")
        print("=" * 68)
