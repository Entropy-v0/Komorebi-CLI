"""Módulo que define la estructura de datos Árbol Binario de Búsqueda."""

from typing import Any, List, Optional
from src.estructuras.nodo_arbol import NodoArbol


class ArbolBinario:
    """Implementación de un Árbol Binario de Búsqueda (BST).
    
    Estructura jerárquica no lineal que cumple con los requerimientos de la cátedra:
    raíz y métodos fundamentales (insertar, eliminar, modificar, consultar),
    así como recorridos estándar (inorden, preorden, postorden).
    """

    def __init__(self) -> None:
        self._raiz: Optional[NodoArbol] = None
        self._tamano: int = 0

    @property
    def raiz(self) -> Optional[NodoArbol]:
        """Retorna la referencia al nodo raíz del árbol."""
        return self._raiz

    @property
    def tamano(self) -> int:
        """Retorna el número de elementos contenidos en el árbol."""
        return self._tamano

    def __len__(self) -> int:
        return self._tamano

    def esta_vacio(self) -> bool:
        """Indica si el árbol no tiene ningún nodo."""
        return self._raiz is None

    def insertar(self, valor: Any) -> bool:
        """Inserta un nuevo valor en el árbol respetando la propiedad de búsqueda.
        
        Retorna True si fue insertado exitosamente, o False si el valor ya existe.
        """
        if self._raiz is None:
            self._raiz = NodoArbol(valor)
            self._tamano += 1
            return True

        insertado = self._insertar_recursivo(self._raiz, valor)
        if insertado:
            self._tamano += 1
        return insertado

    def _insertar_recursivo(self, actual: NodoArbol, valor: Any) -> bool:
        """Inserta recursivamente navegando a la izquierda o derecha."""
        if valor < actual.valor:
            if actual.izquierda is None:
                actual.izquierda = NodoArbol(valor)
                return True
            return self._insertar_recursivo(actual.izquierda, valor)
        elif valor > actual.valor:
            if actual.derecha is None:
                actual.derecha = NodoArbol(valor)
                return True
            return self._insertar_recursivo(actual.derecha, valor)
        else:
            # El valor ya existe en el árbol
            return False

    def consultar(self, valor: Any) -> Optional[Any]:
        """Busca un valor en el árbol y lo retorna si existe, o None en caso contrario."""
        nodo = self._buscar_nodo(self._raiz, valor)
        return nodo.valor if nodo is not None else None

    def contiene(self, valor: Any) -> bool:
        """Indica mediante un booleano si el valor consultado se encuentra en el árbol."""
        return self._buscar_nodo(self._raiz, valor) is not None

    def _buscar_nodo(self, actual: Optional[NodoArbol], valor: Any) -> Optional[NodoArbol]:
        """Búsqueda binaria recursiva sobre el árbol."""
        if actual is None:
            return None
        if valor == actual.valor:
            return actual
        elif valor < actual.valor:
            return self._buscar_nodo(actual.izquierda, valor)
        else:
            return self._buscar_nodo(actual.derecha, valor)

    def modificar(self, valor_viejo: Any, valor_nuevo: Any) -> bool:
        """Modifica un valor existente en el árbol.
        
        Para preservar estrictamente el invariante del Árbol Binario de Búsqueda,
        se elimina el valor anterior y se reinserta el nuevo valor.
        Retorna True si la modificación fue exitosa, o False si el valor_viejo no existía.
        """
        if not self.contiene(valor_viejo):
            return False

        self.eliminar(valor_viejo)
        self.insertar(valor_nuevo)
        return True

    def eliminar(self, valor: Any) -> bool:
        """Elimina un valor del árbol reconfigurando enlaces y liberando memoria.
        
        Maneja los 3 casos clásicos: nodo hoja, nodo con 1 hijo, y nodo con 2 hijos.
        Retorna True si el elemento fue encontrado y eliminado, o False en caso contrario.
        """
        if not self.contiene(valor):
            return False

        self._raiz = self._eliminar_recursivo(self._raiz, valor)
        self._tamano -= 1
        return True

    def _eliminar_recursivo(self, actual: Optional[NodoArbol], valor: Any) -> Optional[NodoArbol]:
        """Elimina recursivamente un nodo y retorna la nueva raíz del subárbol."""
        if actual is None:
            return None

        if valor < actual.valor:
            actual.izquierda = self._eliminar_recursivo(actual.izquierda, valor)
        elif valor > actual.valor:
            actual.derecha = self._eliminar_recursivo(actual.derecha, valor)
        else:
            # Caso 1: Nodo sin hijos (hoja)
            if actual.izquierda is None and actual.derecha is None:
                return None

            # Caso 2: Nodo con un solo hijo
            if actual.izquierda is None:
                temporal = actual.derecha
                actual.derecha = None  # Liberación de enlace
                return temporal
            elif actual.derecha is None:
                temporal = actual.izquierda
                actual.izquierda = None  # Liberación de enlace
                return temporal

            # Caso 3: Nodo con dos hijos
            # Obtenemos el sucesor inorden (el mínimo del subárbol derecho)
            sucesor = self._obtener_minimo(actual.derecha)
            actual.valor = sucesor.valor
            actual.derecha = self._eliminar_recursivo(actual.derecha, sucesor.valor)

        return actual

    def _obtener_minimo(self, actual: NodoArbol) -> NodoArbol:
        """Encuentra el nodo con el valor más pequeño a partir del nodo dado."""
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def inorden(self) -> List[Any]:
        """Recorrido Inorden (Izquierda, Raíz, Derecha). Retorna lista ordenada."""
        resultado: List[Any] = []
        self._inorden_recursivo(self._raiz, resultado)
        return resultado

    def _inorden_recursivo(self, actual: Optional[NodoArbol], resultado: List[Any]) -> None:
        if actual is not None:
            self._inorden_recursivo(actual.izquierda, resultado)
            resultado.append(actual.valor)
            self._inorden_recursivo(actual.derecha, resultado)

    def preorden(self) -> List[Any]:
        """Recorrido Preorden (Raíz, Izquierda, Derecha)."""
        resultado: List[Any] = []
        self._preorden_recursivo(self._raiz, resultado)
        return resultado

    def _preorden_recursivo(self, actual: Optional[NodoArbol], resultado: List[Any]) -> None:
        if actual is not None:
            resultado.append(actual.valor)
            self._preorden_recursivo(actual.izquierda, resultado)
            self._preorden_recursivo(actual.derecha, resultado)

    def postorden(self) -> List[Any]:
        """Recorrido Postorden (Izquierda, Derecha, Raíz)."""
        resultado: List[Any] = []
        self._postorden_recursivo(self._raiz, resultado)
        return resultado

    def _postorden_recursivo(self, actual: Optional[NodoArbol], resultado: List[Any]) -> None:
        if actual is not None:
            self._postorden_recursivo(actual.izquierda, resultado)
            self._postorden_recursivo(actual.derecha, resultado)
            resultado.append(actual.valor)

    def limpiar(self) -> None:
        """Limpia todo el árbol liberando las referencias de los nodos."""
        self._limpiar_recursivo(self._raiz)
        self._raiz = None
        self._tamano = 0

    def _limpiar_recursivo(self, actual: Optional[NodoArbol]) -> None:
        if actual is not None:
            self._limpiar_recursivo(actual.izquierda)
            self._limpiar_recursivo(actual.derecha)
            actual.izquierda = None
            actual.derecha = None

    def __repr__(self) -> str:
        return f"ArbolBinario(raiz={self._raiz.valor if self._raiz else None}, tamano={self._tamano})"
