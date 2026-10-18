"""Módulo del nodo multipágina para el Árbol B (B-Tree)."""

from src.nucleo.referencia_token import ReferenciaToken


class NodoB:
    """Representa un nodo (página) dentro de un Árbol B de orden m.

    Mantiene claves ordenadas lexicográficamente, una lista paralela de listas de
    `ReferenciaToken` por cada clave, y hasta `m` referencias a nodos hijos cuando
    es un nodo interno.
    """

    def __init__(self, es_hoja: bool = True) -> None:
        """Inicializa un nodo del Árbol B.

        Args:
            es_hoja: True si el nodo no posee hijos; False si es un nodo interno.
        """
        self._claves: list[str] = []
        self._valores: list[list[ReferenciaToken]] = []
        self._hijos: list["NodoB"] = []
        self._es_hoja: bool = es_hoja

    @property
    def claves(self) -> list[str]:
        """Retorna la lista ordenada de tokens (claves) almacenados en el nodo."""
        return self._claves

    @claves.setter
    def claves(self, nuevas_claves: list[str]) -> None:
        """Actualiza la lista de claves del nodo."""
        self._claves = nuevas_claves

    @property
    def valores(self) -> list[list[ReferenciaToken]]:
        """Retorna la lista paralela de listas de ReferenciaToken por cada clave."""
        return self._valores

    @valores.setter
    def valores(self, nuevos_valores: list[list[ReferenciaToken]]) -> None:
        """Actualiza la lista paralela de valores del nodo."""
        self._valores = nuevos_valores

    @property
    def hijos(self) -> list["NodoB"]:
        """Retorna la lista de nodos hijos."""
        return self._hijos

    @hijos.setter
    def hijos(self, nuevos_hijos: list["NodoB"]) -> None:
        """Actualiza la lista de nodos hijos."""
        self._hijos = nuevos_hijos

    @property
    def es_hoja(self) -> bool:
        """Indica si el nodo es una hoja."""
        return self._es_hoja

    @es_hoja.setter
    def es_hoja(self, valor: bool) -> None:
        """Actualiza el indicador de hoja del nodo."""
        self._es_hoja = valor

    def __repr__(self) -> str:
        return f"NodoB(claves={self._claves!r}, es_hoja={self._es_hoja})"

