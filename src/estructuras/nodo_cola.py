"""Módulo que define el nodo para colas (FIFO)."""

from typing import Any, Optional


class NodoCola:
    """Nodo para estructura de datos tipo Cola FIFO.
    
    Almacena un dato y una referencia al siguiente nodo en la fila
    para despacho secuencial.
    """

    def __init__(self, dato: Any) -> None:
        self.dato: Any = dato
        self.siguiente: Optional["NodoCola"] = None

    def __repr__(self) -> str:
        return f"NodoCola(dato={self.dato!r})"
