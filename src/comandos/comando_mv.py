"""Módulo del comando concreto 'mv'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_workspace import ServicioWorkspace


class ComandoMv(ComandoBase):
    """Comando para mover o renombrar un archivo o directorio en el Workspace."""

    def __init__(self, servicio_workspace: ServicioWorkspace) -> None:
        super().__init__(
            nombre="mv",
            descripcion="Mueve o renombra un archivo o carpeta actualizando el árbol y su respaldo físico.",
            sintaxis="mv <origen> <destino>",
        )
        self._servicio_workspace: ServicioWorkspace = servicio_workspace

    def ejecutar(self, argumentos: List[str]) -> bool:
        if len(argumentos) < 2:
            print(f"[Error] Debes indicar origen y destino. Sintaxis: {self._sintaxis}")
            return False

        origen = argumentos[0].strip()
        destino = argumentos[1].strip()
        nodo_movido = self._servicio_workspace.mover(origen, destino)
        print(f"[Éxito] Elemento movido a '{nodo_movido.obtener_ruta_absoluta()}'.")
        return True

