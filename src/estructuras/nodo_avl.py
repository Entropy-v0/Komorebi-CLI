"""Módulo del nodo para el Árbol Binario de Búsqueda Autobalanceado (AVL)."""

from typing import Optional


class NodoAVL:
    """Representa un nodo dentro de un Árbol AVL de diccionario técnico.

    Almacena una palabra clave (identificador o keyword), su descripción asociada,
    referencias a sus subárboles izquierdo y derecho, y su altura cacheada para
    calcular el factor de balance en tiempo O(1).
    """

    def __init__(self, palabra: str, descripcion: str = "") -> None:
        """Inicializa un nuevo nodo hoja del Árbol AVL con altura 1.

        Args:
            palabra: Clave lexicográfica única almacenada en el nodo.
            descripcion: Descripción semántica o técnica de la palabra clave.
        """
        self._palabra: str = palabra
        self._descripcion: str = descripcion
        self._izquierdo: Optional["NodoAVL"] = None
        self._derecho: Optional["NodoAVL"] = None
        self._altura: int = 1

    @property
    def palabra(self) -> str:
        """Retorna la palabra clave almacenada en el nodo."""
        return self._palabra

    @palabra.setter
    def palabra(self, valor: str) -> None:
        """Actualiza la palabra clave del nodo (usado en reemplazo por sucesor inorden)."""
        self._palabra = valor

    @property
    def descripcion(self) -> str:
        """Retorna la descripción técnica asociada a la palabra clave."""
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        """Actualiza la descripción técnica asociada a la palabra clave."""
        self._descripcion = valor

    @property
    def izquierdo(self) -> Optional["NodoAVL"]:
        """Retorna la referencia al hijo izquierdo."""
        return self._izquierdo

    @izquierdo.setter
    def izquierdo(self, nodo: Optional["NodoAVL"]) -> None:
        """Establece la referencia al hijo izquierdo."""
        self._izquierdo = nodo

    @property
    def derecho(self) -> Optional["NodoAVL"]:
        """Retorna la referencia al hijo derecho."""
        return self._derecho

    @derecho.setter
    def derecho(self, nodo: Optional["NodoAVL"]) -> None:
        """Establece la referencia al hijo derecho."""
        self._derecho = nodo

    @property
    def altura(self) -> int:
        """Retorna la altura actual del subárbol enraizado en este nodo."""
        return self._altura

    @altura.setter
    def altura(self, valor: int) -> None:
        """Actualiza la altura del subárbol enraizado en este nodo."""
        self._altura = valor

    def __repr__(self) -> str:
        return f"NodoAVL(palabra={self._palabra!r}, altura={self._altura})"

