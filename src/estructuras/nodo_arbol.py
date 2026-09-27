"""Módulo que define el nodo para árboles binarios."""

from typing import Any, Optional


class NodoArbol:
    """Nodo para estructura de datos tipo Árbol Binario.
    
    Almacena un valor y punteros hacia los subárboles izquierdo y derecho.
    """

    def __init__(self, valor: Any) -> None:
        self.valor: Any = valor
        self.izquierda: Optional["NodoArbol"] = None
        self.derecha: Optional["NodoArbol"] = None

    def __repr__(self) -> str:
        return f"NodoArbol(valor={self.valor!r})"
