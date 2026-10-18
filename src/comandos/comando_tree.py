"""Módulo del comando concreto 'tree'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_workspace import ServicioWorkspace


class ComandoTree(ComandoBase):
    """Comando para imprimir la jerarquía del Workspace en formato árbol estilo Linux."""

    def __init__(self, servicio_workspace: ServicioWorkspace) -> None:
        super().__init__(
            nombre="tree",
            descripcion="Muestra en preorden la jerarquía de carpetas y archivos estilo comando tree.",
            sintaxis="tree [ruta]",
        )
        self._servicio_workspace: ServicioWorkspace = servicio_workspace

    def ejecutar(self, argumentos: List[str]) -> bool:
        ruta = argumentos[0].strip() if argumentos else None
        lineas = self._servicio_workspace.mostrar_arbol(ruta)
        for linea in lineas:
            print(linea)
        return True

