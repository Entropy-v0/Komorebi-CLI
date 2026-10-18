"""Módulo que define el nodo para el Árbol Binario de Expresiones Aritméticas."""

from typing import Optional


class NodoExpresion:
    """Nodo de un Árbol de Expresiones Aritméticas.
    
    Invariante estructural:
    - Las hojas son exclusivamente operandos numéricos (`izquierdo is None` y `derecho is None`).
    - Los nodos internos son exclusivamente operadores binarios (`+`, `-`, `*`, `/`)
      y poseen exactamente dos hijos (`izquierdo` y `derecho`).
    """

    OPERADORES = {"+", "-", "*", "/"}

    def __init__(
        self,
        valor: str,
        izquierdo: Optional["NodoExpresion"] = None,
        derecho: Optional["NodoExpresion"] = None,
    ) -> None:
        self._valor: str = str(valor).strip()
        self._izquierdo: Optional["NodoExpresion"] = izquierdo
        self._derecho: Optional["NodoExpresion"] = derecho

    @property
    def valor(self) -> str:
        """Retorna el símbolo del operador o el literal numérico del operando."""
        return self._valor

    @property
    def izquierdo(self) -> Optional["NodoExpresion"]:
        """Retorna el subárbol u operando izquierdo."""
        return self._izquierdo

    @izquierdo.setter
    def izquierdo(self, nodo: Optional["NodoExpresion"]) -> None:
        """Asigna el hijo izquierdo."""
        self._izquierdo = nodo

    @property
    def derecho(self) -> Optional["NodoExpresion"]:
        """Retorna el subárbol u operando derecho."""
        return self._derecho

    @derecho.setter
    def derecho(self, nodo: Optional["NodoExpresion"]) -> None:
        """Asigna el hijo derecho."""
        self._derecho = nodo

    @property
    def es_hoja(self) -> bool:
        """Indica si el nodo es una hoja (operando sin hijos)."""
        return self._izquierdo is None and self._derecho is None

    @property
    def es_operador(self) -> bool:
        """Indica si el nodo es un operador interno con dos hijos."""
        return not self.es_hoja and self._valor in self.OPERADORES

    def __repr__(self) -> str:
        return f"NodoExpresion(valor={self._valor!r}, hoja={self.es_hoja})"

