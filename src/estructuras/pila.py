"""Módulo que define la estructura de datos Pila (LIFO)."""

from typing import Any, List, Optional
from src.estructuras.nodo_pila import NodoPila


class Pila:
    """Implementación propia de una estructura Pila (LIFO - Last In, First Out).
    
    Gestiona elementos apilados en memoria mediante nodos enlazados,
    utilizada para el balanceo de delimitadores y el historial Undo/Redo.
    """

    def __init__(self) -> None:
        self._tope: Optional[NodoPila] = None
        self._tamano: int = 0

    @property
    def tope(self) -> Optional[NodoPila]:
        """Retorna el nodo ubicado en la cima de la pila."""
        return self._tope

    @property
    def tamano(self) -> int:
        """Retorna el número de elementos contenidos en la pila."""
        return self._tamano

    def __len__(self) -> int:
        return self._tamano

    def esta_vacia(self) -> bool:
        """Indica si la pila no posee elementos."""
        return self._tamano == 0

    def apilar(self, elemento: Any) -> None:
        """Inserta un nuevo elemento en la cima de la pila (operación push)."""
        nuevo_nodo = NodoPila(elemento)
        nuevo_nodo.siguiente = self._tope
        self._tope = nuevo_nodo
        self._tamano += 1

    def desapilar(self) -> Any:
        """Extrae y retorna el elemento en la cima de la pila (operación pop).
        
        Libera la referencia del nodo desapilado para gestión estricta de memoria.
        Lanza IndexError si la pila se encuentra vacía.
        """
        if self.esta_vacia() or self._tope is None:
            raise IndexError("No se puede desapilar de una pila vacía.")

        nodo_extraido = self._tope
        self._tope = nodo_extraido.siguiente

        # Desvinculación de puntero para liberar memoria
        nodo_extraido.siguiente = None
        self._tamano -= 1

        return nodo_extraido.dato

    def cima(self) -> Any:
        """Consulta el dato ubicado en el tope sin extraerlo (operación peek).
        
        Lanza IndexError si la pila se encuentra vacía.
        """
        if self.esta_vacia() or self._tope is None:
            raise IndexError("La pila está vacía, no hay elemento en la cima.")
        return self._tope.dato

    def limpiar(self) -> None:
        """Vacía la pila liberando secuencialmente cada uno de sus nodos."""
        actual = self._tope
        while actual is not None:
            siguiente = actual.siguiente
            actual.siguiente = None
            actual = siguiente

        self._tope = None
        self._tamano = 0

    def listar(self) -> List[Any]:
        """Retorna los datos de la pila en orden desde el tope hacia la base."""
        elementos: List[Any] = []
        actual = self._tope
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __repr__(self) -> str:
        return f"Pila(tope={self.cima() if not self.esta_vacia() else None!r}, tamano={self._tamano})"
