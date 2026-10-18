"""Módulo del comando concreto 'find-global'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_indexacion import ServicioIndexacion


class ComandoFindGlobal(ComandoBase):
    """Comando para buscar un identificador en todo el proyecto mediante el Árbol B."""

    def __init__(self, servicio_indexacion: ServicioIndexacion) -> None:
        super().__init__(
            nombre="find-global",
            descripcion="Busca un identificador en el índice global B-Tree mostrando archivos y líneas.",
            sintaxis="find-global <token>",
        )
        self._servicio_indexacion: ServicioIndexacion = servicio_indexacion

    def ejecutar(self, argumentos: List[str]) -> bool:
        if not argumentos:
            print("[Error] Uso esperado: find-global <token>")
            return True

        token = argumentos[0]
        print(self._servicio_indexacion.formatear_busqueda_global(token))
        return True

