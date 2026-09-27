"""Módulo que define el nodo para listas enlazadas."""

from typing import Any, Optional


class NodoLista:
    """Nodo para estructura de lista doblemente enlazada.
    
    Almacena el dato y las referencias hacia el nodo siguiente y anterior,
    permitiendo navegación bidireccional y manipulación eficiente en O(1).
    """

    def __init__(self, dato: Any) -> None:
        self.dato: Any = dato
        self.siguiente: Optional["NodoLista"] = None
        self.anterior: Optional["NodoLista"] = None

    def __repr__(self) -> str:
        return f"NodoLista(dato={self.dato!r})"
