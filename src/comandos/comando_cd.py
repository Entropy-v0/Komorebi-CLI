"""Módulo del comando concreto 'cd'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_navegacion import ServicioNavegacion


class ComandoCd(ComandoBase):
    """Comando para cambiar de directorio en el sistema de archivos real o en el Workspace."""

    def __init__(self, servicio_navegacion: ServicioNavegacion) -> None:
        super().__init__(
            nombre="cd",
            descripcion=(
                "Cambia de directorio en el SO (rutas, '~', '..', '-') "
                "o en el Workspace virtual con el prefijo 'ws:'."
            ),
            sintaxis="cd [ruta | ws:ruta | -]",
        )
        self._servicio_navegacion: ServicioNavegacion = servicio_navegacion

    def ejecutar(self, argumentos: List[str]) -> bool:
        destino = " ".join(argumentos).strip()
        ubicacion = self._servicio_navegacion.cambiar_directorio(destino)
        print(f"[Directorio] Ruta actual: {ubicacion}")
        return True
