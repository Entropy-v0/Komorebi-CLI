"""Módulo del comando concreto 'remove-keyword'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_diccionario import ServicioDiccionario


class ComandoRemoveKeyword(ComandoBase):
    """Comando para eliminar una palabra clave del Árbol AVL y rebalancear la estructura."""

    def __init__(self, servicio_diccionario: ServicioDiccionario) -> None:
        super().__init__(
            nombre="remove-keyword",
            descripcion="Elimina una palabra clave del diccionario AVL y rebalancea el árbol.",
            sintaxis="remove-keyword <palabra>",
        )
        self._servicio_diccionario: ServicioDiccionario = servicio_diccionario

    def ejecutar(self, argumentos: List[str]) -> bool:
        if not argumentos:
            print("[Error] Uso esperado: remove-keyword <palabra>")
            return True

        palabra = argumentos[0]
        eliminado = self._servicio_diccionario.eliminar_palabra(palabra)
        if eliminado:
            print(
                f"[Éxito] Palabra clave '{palabra}' eliminada del diccionario AVL "
                f"(total: {self._servicio_diccionario.arbol.tamanio}, "
                f"altura: {self._servicio_diccionario.arbol.altura})."
            )
        else:
            print(f"[Error] La palabra clave '{palabra}' no existe en el diccionario AVL.")
        return True

