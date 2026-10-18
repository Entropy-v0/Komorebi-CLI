"""Módulo del comando concreto 'mkdir'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_workspace import ServicioWorkspace


class ComandoMkdir(ComandoBase):
    """Comando para crear una carpeta dentro del Árbol N-ario del Workspace."""

    def __init__(self, servicio_workspace: ServicioWorkspace) -> None:
        super().__init__(
            nombre="mkdir",
            descripcion="Crea un nuevo directorio en la ruta especificada del workspace.",
            sintaxis="mkdir <nombre_o_ruta>",
        )
        self._servicio_workspace: ServicioWorkspace = servicio_workspace

    def ejecutar(self, argumentos: List[str]) -> bool:
        if not argumentos:
            print(f"[Error] Debes indicar el nombre o ruta del directorio. Sintaxis: {self._sintaxis}")
            return False

        ruta = argumentos[0].strip()
        nodo = self._servicio_workspace.crear_carpeta(ruta)
        print(f"[Éxito] Directorio '{nodo.obtener_ruta_absoluta()}' creado.")
        return True

