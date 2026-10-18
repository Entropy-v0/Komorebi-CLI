"""Módulo del comando concreto 'suggest'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_diccionario import ServicioDiccionario


class ComandoSuggest(ComandoBase):
    """Comando para obtener sugerencias de autocompletado por prefijo desde el Árbol AVL."""

    def __init__(self, servicio_diccionario: ServicioDiccionario) -> None:
        super().__init__(
            nombre="suggest",
            descripcion="Sugiere palabras clave del diccionario AVL que comienzan con el prefijo dado.",
            sintaxis="suggest <prefijo>",
        )
        self._servicio_diccionario: ServicioDiccionario = servicio_diccionario

    def ejecutar(self, argumentos: List[str]) -> bool:
        prefijo = argumentos[0] if argumentos else ""
        print(self._servicio_diccionario.formatear_sugerencias(prefijo))
        return True

