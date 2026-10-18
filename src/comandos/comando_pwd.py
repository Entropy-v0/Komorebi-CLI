"""Módulo del comando concreto 'pwd'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_workspace import ServicioWorkspace


class ComandoPwd(ComandoBase):
    """Comando para mostrar la ruta absoluta del directorio actual en el Workspace."""

    def __init__(self, servicio_workspace: ServicioWorkspace) -> None:
        super().__init__(
            nombre="pwd",
            descripcion="Muestra la ruta absoluta del directorio de trabajo actual.",
            sintaxis="pwd",
        )
        self._servicio_workspace: ServicioWorkspace = servicio_workspace

    def ejecutar(self, argumentos: List[str]) -> bool:
        ruta_actual = self._servicio_workspace.obtener_directorio_actual()
        print(ruta_actual)
        return True

