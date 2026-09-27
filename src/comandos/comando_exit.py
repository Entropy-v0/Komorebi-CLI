"""Módulo del comando concreto 'exit'."""

import sys
from typing import List
from src.comandos.comando_base import ComandoBase


class ComandoExit(ComandoBase):
    """Comando auxiliar para finalizar ordenadamente la sesión de la consola."""

    def __init__(self) -> None:
        super().__init__(
            nombre="exit",
            descripcion="Finaliza ordenadamente la sesión del Mini IDE Komorebi.",
            sintaxis="exit",
        )

    def ejecutar(self, argumentos: List[str]) -> bool:
        print("[Sesión] Guardando estado y saliendo de Komorebi Mini IDE. ¡Hasta pronto!")
        sys.exit(0)
