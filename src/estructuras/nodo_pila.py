"""Módulo que define el nodo para pilas (LIFO)."""

from typing import Any, Optional


class NodoPila:
    """Nodo para estructura de datos tipo Pila (LIFO).
    
    Almacena un dato y una referencia al nodo que se encuentra
    por debajo en el tope de la pila.
    """

    def __init__(self, dato: Any) -> None:
        self.dato: Any = dato
        self.siguiente: Optional["NodoPila"] = None

    def __repr__(self) -> str:
        return f"NodoPila(dato={self.dato!r})"
