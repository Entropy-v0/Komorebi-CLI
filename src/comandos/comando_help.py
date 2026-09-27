"""Módulo del comando concreto 'help'."""

from typing import Any, List
from src.comandos.comando_base import ComandoBase


class ComandoHelp(ComandoBase):
    """Comando auxiliar para mostrar la ayuda de todos los comandos registrados en el sistema."""

    def __init__(self, invocador: Any) -> None:
        super().__init__(
            nombre="help",
            descripcion="Muestra el listado de todos los comandos disponibles y su sintaxis.",
            sintaxis="help",
        )
        self._invocador = invocador

    def ejecutar(self, argumentos: List[str]) -> bool:
        comandos = self._invocador.listar_comandos()
        print("\n================== KOMOREBI MINI IDE - COMANDOS DISPONIBLES ==================")
        for cmd in comandos:
            print(f"  {cmd.sintaxis:<36} : {cmd.descripcion}")
        print("==============================================================================\n")
        return True
