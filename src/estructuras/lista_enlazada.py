"""Módulo que define la estructura de datos Lista Enlazada Doble."""

from typing import Any, Callable, Generator, List, Optional
from src.estructuras.nodo_lista import NodoLista


class ListaEnlazada:
    """Implementación propia de una Lista Doblemente Enlazada.
    
    Gestiona nodos vinculados bidireccionalmente permitiendo inserciones,
    búsquedas, eliminaciones y liberaciones explícitas de memoria sin
    utilizar métodos ni colecciones nativas de Python.
    """

    def __init__(self) -> None:
        self._cabeza: Optional[NodoLista] = None
        self._cola: Optional[NodoLista] = None
        self._tamano: int = 0

    @property
    def cabeza(self) -> Optional[NodoLista]:
        """Retorna el nodo inicial de la lista."""
        return self._cabeza

    @property
    def cola(self) -> Optional[NodoLista]:
        """Retorna el nodo final de la lista."""
        return self._cola

    @property
    def tamano(self) -> int:
        """Retorna la cantidad actual de elementos en la lista."""
        return self._tamano

    def __len__(self) -> int:
        return self._tamano

    def esta_vacia(self) -> bool:
        """Determina si la lista no contiene elementos."""
        return self._tamano == 0

    def insertar(self, dato: Any, posicion: Optional[int] = None) -> None:
        """Inserta un nuevo elemento en la lista.
        
        Si no se especifica posición o si es mayor/igual al tamaño, se inserta al final.
        Si la posición es menor o igual a 0, se inserta al inicio.
        En caso contrario, se ubica en el índice exacto indicado.
        """
        if posicion is None or posicion >= self._tamano:
            self.insertar_al_final(dato)
            return

        if posicion <= 0:
            self.insertar_al_inicio(dato)
            return

        self._insertar_en_posicion_intermedia(dato, posicion)

    def insertar_al_inicio(self, dato: Any) -> None:
        """Inserta un nuevo dato como primer nodo de la lista."""
        nuevo_nodo = NodoLista(dato)
        if self.esta_vacia():
            self._cabeza = nuevo_nodo
            self._cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self._cabeza
            if self._cabeza is not None:
                self._cabeza.anterior = nuevo_nodo
            self._cabeza = nuevo_nodo
        self._tamano += 1

    def insertar_al_final(self, dato: Any) -> None:
        """Inserta un nuevo dato como último nodo de la lista."""
        nuevo_nodo = NodoLista(dato)
        if self.esta_vacia():
            self._cabeza = nuevo_nodo
            self._cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self._cola
            if self._cola is not None:
                self._cola.siguiente = nuevo_nodo
            self._cola = nuevo_nodo
        self._tamano += 1

    def _insertar_en_posicion_intermedia(self, dato: Any, posicion: int) -> None:
        """Inserta un dato en un índice intermedio válido."""
        actual = self._cabeza
        indice = 0
        while actual is not None and indice < posicion:
            actual = actual.siguiente
            indice += 1

        if actual is not None:
            nuevo_nodo = NodoLista(dato)
            nodo_anterior = actual.anterior

            nuevo_nodo.siguiente = actual
            nuevo_nodo.anterior = nodo_anterior

            if nodo_anterior is not None:
                nodo_anterior.siguiente = nuevo_nodo
            actual.anterior = nuevo_nodo

            self._tamano += 1

    def obtener_por_indice(self, indice: int) -> Any:
        """Retorna el dato ubicado en el índice solicitado (base 0)."""
        nodo = self.obtener_nodo_por_indice(indice)
        if nodo is None:
            raise IndexError("Índice fuera del rango de la lista.")
        return nodo.dato

    def obtener_nodo_por_indice(self, indice: int) -> Optional[NodoLista]:
        """Recorre la lista y retorna el NodoLista en el índice solicitado."""
        if indice < 0 or indice >= self._tamano:
            return None

        actual = self._cabeza
        actual_indice = 0
        while actual is not None:
            if actual_indice == indice:
                return actual
            actual = actual.siguiente
            actual_indice += 1
        return None

    def buscar(self, criterio: Any) -> Optional[Any]:
        """Busca el primer dato que cumpla el criterio (por función predicado o igualdad)."""
        nodo = self.buscar_nodo(criterio)
        return nodo.dato if nodo is not None else None

    def buscar_nodo(self, criterio: Any) -> Optional[NodoLista]:
        """Busca y retorna el NodoLista que cumpla con el criterio especificado."""
        es_predicado = callable(criterio)
        actual = self._cabeza

        while actual is not None:
            coincide = criterio(actual.dato) if es_predicado else actual.dato == criterio
            if coincide:
                return actual
            actual = actual.siguiente

        return None

    def eliminar(self, criterio: Any) -> bool:
        """Elimina el primer nodo que coincida con el criterio y libera sus referencias."""
        nodo_a_eliminar = self.buscar_nodo(criterio)
        if nodo_a_eliminar is None:
            return False

        self._desvincular_nodo(nodo_a_eliminar)
        return True

    def eliminar_por_indice(self, indice: int) -> Any:
        """Elimina el nodo en el índice especificado, liberándolo y retornando su dato."""
        nodo = self.obtener_nodo_por_indice(indice)
        if nodo is None:
            raise IndexError("Índice fuera del rango de la lista.")

        dato = nodo.dato
        self._desvincular_nodo(nodo)
        return dato

    def _desvincular_nodo(self, nodo: NodoLista) -> None:
        """Desconecta el nodo de la lista y limpia sus punteros para liberar memoria.
        
        Aplica pattern matching sobre los enlaces (anterior, siguiente) para
        tratar exhaustivamente los 4 estados topológicos posibles del nodo.
        """
        match (nodo.anterior, nodo.siguiente):
            case (None, None):
                # Único nodo en la lista
                self._cabeza = None
                self._cola = None

            case (None, siguiente):
                # El nodo es la cabeza
                self._cabeza = siguiente
                siguiente.anterior = None

            case (anterior, None):
                # El nodo es la cola
                self._cola = anterior
                anterior.siguiente = None

            case (anterior, siguiente):
                # Nodo intermedio
                anterior.siguiente = siguiente
                siguiente.anterior = anterior

        # Limpieza estricta de referencias internas del nodo para liberación de memoria
        nodo.siguiente = None
        nodo.anterior = None
        self._tamano -= 1

    def listar(self) -> List[Any]:
        """Retorna una lista con todos los datos contenidos en orden secuencial."""
        elementos: List[Any] = []
        actual = self._cabeza
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def limpiar(self) -> None:
        """Libera todos los nodos de la lista desvinculando enlaces."""
        actual = self._cabeza
        while actual is not None:
            siguiente = actual.siguiente
            actual.siguiente = None
            actual.anterior = None
            actual = siguiente

        self._cabeza = None
        self._cola = None
        self._tamano = 0

    def __iter__(self) -> Generator[Any, None, None]:
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __repr__(self) -> str:
        elementos = self.listar()
        return f"ListaEnlazada({elementos!r})"
