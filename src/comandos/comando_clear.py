"""Módulo del comando concreto 'clear' para limpiar la pantalla de la consola."""

import os
import sys
from typing import List
from src.comandos.comando_base import ComandoBase


class ComandoClear(ComandoBase):
    """Comando auxiliar para despejar el historial visual de la terminal interactiva."""

    def __init__(self) -> None:
        super().__init__(
            nombre="clear",
            descripcion="Limpia la pantalla de la terminal (alias: cls).",
            sintaxis="clear",
        )

    def ejecutar(self, argumentos: List[str]) -> bool:
        if sys.stdout.isatty():
            os.system("cls" if os.name == "nt" else "clear")
        print("\033[2J\033[H", end="", flush=True)
        return True

