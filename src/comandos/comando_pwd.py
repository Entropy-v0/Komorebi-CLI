"""Módulo del comando concreto 'pwd'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_navegacion import ServicioNavegacion


class ComandoPwd(ComandoBase):
    """Comando para mostrar la ruta del directorio actual (SO real o Workspace virtual)."""

    def __init__(self, servicio_navegacion: ServicioNavegacion) -> None:
        super().__init__(
            nombre="pwd",
            descripcion="Muestra la ruta absoluta del directorio de trabajo actual.",
            sintaxis="pwd",
        )
        self._servicio_navegacion: ServicioNavegacion = servicio_navegacion

    def ejecutar(self, argumentos: List[str]) -> bool:
        print(self._servicio_navegacion.obtener_ubicacion_actual())
        return True
