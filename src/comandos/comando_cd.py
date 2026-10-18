"""Módulo del comando concreto 'cd'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_workspace import ServicioWorkspace


class ComandoCd(ComandoBase):
    """Comando para cambiar el directorio actual en el Árbol N-ario del Workspace."""

    def __init__(self, servicio_workspace: ServicioWorkspace) -> None:
        super().__init__(
            nombre="cd",
            descripcion="Cambia el directorio actual en el workspace (soporta '.', '..' y rutas).",
            sintaxis="cd <ruta>",
        )
        self._servicio_workspace: ServicioWorkspace = servicio_workspace

    def ejecutar(self, argumentos: List[str]) -> bool:
        ruta = argumentos[0].strip() if argumentos else "/"
        nodo = self._servicio_workspace.cambiar_directorio(ruta)
        print(f"[Directorio] Ruta actual: {nodo.obtener_ruta_absoluta()}")
        return True

