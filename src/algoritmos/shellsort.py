"""Módulo que implementa el algoritmo de ordenamiento ShellSort."""

from typing import Any, Callable, List, Optional
from src.algoritmos.ordenador_base import OrdenadorBase


class ShellSort(OrdenadorBase):
    """Implementación manual del algoritmo ShellSort.
    
    Mejora el algoritmo de ordenamiento por inserción al comparar elementos
    separados por un intervalo decreciente (gap sequence).
    Utiliza la secuencia de intervalos de Knuth (h = 3*h + 1), optimizando
    el desplazamiento de elementos distantes hacia su posición final.
    """

    def ordenar(
        self,
        coleccion: List[Any],
        criterio: Optional[Callable[[Any], Any]] = None,
        ascendente: bool = True,
    ) -> List[Any]:
        """Ordena los elementos aplicando ShellSort con secuencia de saltos.
        
        Args:
            coleccion: Lista de elementos a ordenar.
            criterio: Función opcional para extraer la clave de comparación.
            ascendente: Define la dirección del ordenamiento.
            
        Returns:
            Nueva lista con los elementos ordenados.
        """
        resultado = [elemento for elemento in coleccion]
        n = len(resultado)
        if n <= 1:
            return resultado

        # Cálculo del intervalo inicial óptimo según la secuencia de Knuth
        intervalo = 1
        while intervalo < n // 3:
            intervalo = 3 * intervalo + 1

        # Proceso de inserción con intervalos decrecientes
        while intervalo >= 1:
            for i in range(intervalo, n):
                elemento_actual = resultado[i]
                j = i
                
                # Desplaza elementos que no cumplan la condición de orden hacia adelante
                while j >= intervalo and not self._es_menor_o_igual(
                    resultado[j - intervalo], elemento_actual, criterio, ascendente
                ):
                    resultado[j] = resultado[j - intervalo]
                    j -= intervalo

                resultado[j] = elemento_actual

            intervalo //= 3

        return resultado
