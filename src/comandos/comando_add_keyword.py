"""Módulo del comando concreto 'add-keyword'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_diccionario import ServicioDiccionario


class ComandoAddKeyword(ComandoBase):
    """Comando para insertar una nueva palabra clave en el Árbol AVL del diccionario."""

    def __init__(self, servicio_diccionario: ServicioDiccionario) -> None:
        super().__init__(
            nombre="add-keyword",
            descripcion="Agrega una nueva palabra clave y su descripción al diccionario AVL.",
            sintaxis="add-keyword <palabra> [descripcion]",
        )
        self._servicio_diccionario: ServicioDiccionario = servicio_diccionario

    def ejecutar(self, argumentos: List[str]) -> bool:
        if not argumentos:
            print("[Error] Uso esperado: add-keyword <palabra> [descripcion]")
            return True

        palabra = argumentos[0]
        descripcion = " ".join(argumentos[1:]).strip()
        nodo = self._servicio_diccionario.agregar_palabra(palabra, descripcion)
        print(
            f"[Éxito] Palabra clave '{nodo.palabra}' agregada al diccionario AVL "
            f"(total: {self._servicio_diccionario.arbol.tamanio}, "
            f"altura: {self._servicio_diccionario.arbol.altura})."
        )
        return True

