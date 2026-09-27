"""Módulo que define la estructura de datos Cola FIFO."""

from typing import Any, List, Optional
from src.estructuras.nodo_cola import NodoCola


class ColaFIFO:
    """Implementación propia de una Cola FIFO (First In, First Out).
    
    Gestiona elementos organizados secuencialmente mediante punteros
    frente y final, utilizada para el buffer de peticiones a la API de IA.
    """

    def __init__(self) -> None:
        self._frente: Optional[NodoCola] = None
        self._final: Optional[NodoCola] = None
        self._tamano: int = 0

    @property
    def primer_nodo(self) -> Optional[NodoCola]:
        """Retorna la referencia al nodo del frente de la cola."""
        return self._frente

    @property
    def tamano(self) -> int:
        """Retorna la cantidad actual de elementos en la cola."""
        return self._tamano

    def __len__(self) -> int:
        return self._tamano

    def esta_vacia(self) -> bool:
        """Verifica si la cola no contiene elementos pendientes."""
        return self._tamano == 0

    def encolar(self, elemento: Any) -> None:
        """Inserta un nuevo elemento al final de la cola (operación enqueue)."""
        nuevo_nodo = NodoCola(elemento)
        if self.esta_vacia():
            self._frente = nuevo_nodo
            self._final = nuevo_nodo
        else:
            if self._final is not None:
                self._final.siguiente = nuevo_nodo
            self._final = nuevo_nodo
        self._tamano += 1

    def desencolar(self) -> Any:
        """Extrae y retorna el elemento al frente de la cola (operación dequeue).
        
        Libera la referencia del nodo desencolado para gestión estricta de memoria.
        Lanza IndexError si la cola se encuentra vacía.
        """
        if self.esta_vacia() or self._frente is None:
            raise IndexError("No se puede desencolar de una cola vacía.")

        nodo_extraido = self._frente
        self._frente = nodo_extraido.siguiente

        if self._frente is None:
            self._final = None

        # Desvinculación de puntero para liberar memoria
        nodo_extraido.siguiente = None
        self._tamano -= 1

        return nodo_extraido.dato

    def frente(self) -> Any:
        """Consulta el dato ubicado al inicio de la cola sin extraerlo (operación front/peek).
        
        Lanza IndexError si la cola se encuentra vacía.
        """
        if self.esta_vacia() or self._frente is None:
            raise IndexError("La cola está vacía, no hay elemento en el frente.")
        return self._frente.dato

    def limpiar(self) -> None:
        """Vacía la cola liberando secuencialmente cada uno de sus nodos."""
        actual = self._frente
        while actual is not None:
            siguiente = actual.siguiente
            actual.siguiente = None
            actual = siguiente

        self._frente = None
        self._final = None
        self._tamano = 0

    def listar(self) -> List[Any]:
        """Retorna los datos de la cola en orden de llegada (del frente al final)."""
        elementos: List[Any] = []
        actual = self._frente
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __repr__(self) -> str:
        return f"ColaFIFO(frente={self.frente() if not self.esta_vacia() else None!r}, tamano={self._tamano})"
