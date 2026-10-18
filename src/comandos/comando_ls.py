"""Módulo del comando concreto 'ls'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_workspace import ServicioWorkspace


class ComandoLs(ComandoBase):
    """Comando para listar los elementos hijos del directorio actual o de una ruta."""

    def __init__(self, servicio_workspace: ServicioWorkspace) -> None:
        super().__init__(
            nombre="ls",
            descripcion="Lista las carpetas y archivos contenidos en el directorio actual o ruta.",
            sintaxis="ls [ruta]",
        )
        self._servicio_workspace: ServicioWorkspace = servicio_workspace

    def ejecutar(self, argumentos: List[str]) -> bool:
        ruta = argumentos[0].strip() if argumentos else None
        elementos = self._servicio_workspace.listar_directorio(ruta)
        if not elementos:
            print("(Directorio vacío)")
            return True

        for nodo in elementos:
            etiqueta = f"{nodo.nombre}/" if nodo.es_carpeta else nodo.nombre
            print(f"  {etiqueta}")
        return True

