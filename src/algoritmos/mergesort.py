"""Módulo que implementa el algoritmo de ordenamiento MergeSort (Divide y Vencerás)."""

from typing import Any, Callable, List, Optional
from src.algoritmos.ordenador_base import OrdenadorBase


class MergeSort(OrdenadorBase):
    """Implementación manual del algoritmo MergeSort.
    
    Aplica la técnica de Divide y Vencerás con una complejidad temporal
    estrictamente garantizada de O(n log n) en el peor, promedio y mejor de los casos.
    Es un algoritmo estable que respeta el orden relativo de elementos equivalentes.
    """

    def ordenar(
        self,
        coleccion: List[Any],
        criterio: Optional[Callable[[Any], Any]] = None,
        ascendente: bool = True,
    ) -> List[Any]:
        """Ordena los elementos utilizando MergeSort de forma recursiva.
        
        Args:
            coleccion: Lista de elementos a ordenar.
            criterio: Función para extraer la clave de comparación.
            ascendente: Define la dirección del ordenamiento.
            
        Returns:
            Nueva lista con los elementos ordenados.
        """
        if len(coleccion) <= 1:
            return [elemento for elemento in coleccion]

        return self._mergesort(coleccion, criterio, ascendente)

    def _mergesort(
        self,
        elementos: List[Any],
        criterio: Optional[Callable[[Any], Any]],
        ascendente: bool = True,
    ) -> List[Any]:
        """Método recursivo que divide la lista y mezcla sus sublistas ordenadas."""
        if len(elementos) <= 1:
            return elementos

        medio = len(elementos) // 2
        izquierda = self._mergesort(elementos[:medio], criterio, ascendente)
        derecha = self._mergesort(elementos[medio:], criterio, ascendente)

        return self._mezclar(izquierda, derecha, criterio, ascendente)

    def _mezclar(
        self,
        izquierda: List[Any],
        derecha: List[Any],
        criterio: Optional[Callable[[Any], Any]],
        ascendente: bool,
    ) -> List[Any]:
        """Intercala dos sublistas previamente ordenadas en una nueva lista combinada."""
        resultado: List[Any] = []
        i = 0
        j = 0
        len_izq = len(izquierda)
        len_der = len(derecha)

        while i < len_izq and j < len_der:
            if self._es_menor_o_igual(izquierda[i], derecha[j], criterio, ascendente):
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        while i < len_izq:
            resultado.append(izquierda[i])
            i += 1

        while j < len_der:
            resultado.append(derecha[j])
            j += 1

        return resultado
