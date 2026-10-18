"""Módulo del comando concreto 'index-all'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_indexacion import ServicioIndexacion


class ComandoIndexAll(ComandoBase):
    """Comando para reconstruir el índice global de tokens en el Árbol B."""

    def __init__(self, servicio_indexacion: ServicioIndexacion) -> None:
        super().__init__(
            nombre="index-all",
            descripcion="Indexa todos los identificadores de los archivos del Workspace en el Árbol B.",
            sintaxis="index-all",
        )
        self._servicio_indexacion: ServicioIndexacion = servicio_indexacion

    def ejecutar(self, argumentos: List[str]) -> bool:
        archivos_proc, tokens_unicos = self._servicio_indexacion.indexar_todo()
        print(
            f"[Índice B-Tree] Indexación completada: {archivos_proc} archivo(s) escaneado(s), "
            f"{tokens_unicos} token(s) único(s) registrado(s) (orden m={self._servicio_indexacion.indice.orden}, "
            f"altura={self._servicio_indexacion.indice.altura})."
        )
        return True

