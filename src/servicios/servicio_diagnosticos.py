"""Módulo del servicio encargado de la ordenación de diagnósticos mediante algoritmos propios."""

from typing import Callable, Dict, List
from src.algoritmos.ordenador_base import OrdenadorBase
from src.algoritmos.mergesort import MergeSort
from src.algoritmos.shellsort import ShellSort
from src.nucleo.diagnostico import Diagnostico


class ServicioDiagnosticos:
    """Aplica algoritmos de ordenamiento manuales (MergeSort o ShellSort) sobre alertas de código.
    
    Permite ordenar diagnósticos de forma ascendente o descendente según el número de línea
    o el nivel de gravedad/prioridad del diagnóstico.
    """

    def __init__(self) -> None:
        self._algoritmos: Dict[str, OrdenadorBase] = {
            "mergesort": MergeSort(),
            "shellsort": ShellSort(),
        }

    def obtener_algoritmos_disponibles(self) -> List[str]:
        """Retorna los nombres de los algoritmos de ordenamiento soportados."""
        return list(self._algoritmos.keys())

    def ordenar(
        self,
        diagnosticos: List[Diagnostico],
        criterio: str,
        algoritmo: str = "mergesort",
        ascendente: bool = True,
    ) -> List[Diagnostico]:
        """Ordena la colección de diagnósticos según el criterio y algoritmo especificados.
        
        Args:
            diagnosticos: Lista de objetos Diagnostico a ordenar.
            criterio: 'line'/'linea' para ordenar por número de línea, o 'severity'/'gravedad'.
            algoritmo: 'mergesort' o 'shellsort'.
            ascendente: True para orden ascendente (menor a mayor), False para descendente.
            
        Returns:
            Nueva lista con los diagnósticos ordenados.
            
        Raises:
            ValueError: Si el algoritmo o el criterio no son reconocidos.
        """
        nombre_algo = algoritmo.strip().lower()
        if nombre_algo not in self._algoritmos:
            disponibles = ", ".join(self.obtener_algoritmos_disponibles())
            raise ValueError(f"Algoritmo '{algoritmo}' no válido. Opciones: {disponibles}.")

        ordenador = self._algoritmos[nombre_algo]
        funcion_clave = self._resolver_criterio(criterio)

        return ordenador.ordenar(diagnosticos, criterio=funcion_clave, ascendente=ascendente)

    def _resolver_criterio(self, criterio: str) -> Callable[[Diagnostico], int]:
        """Resuelve el criterio textual a una función de extracción de clave."""
        crit_limpio = criterio.strip().lower()
        if crit_limpio in ("line", "linea", "l"):
            return lambda d: d.linea
        elif crit_limpio in ("severity", "gravedad", "prioridad", "s", "g"):
            return lambda d: d.prioridad
        else:
            raise ValueError(f"Criterio '{criterio}' no válido. Opciones: 'line'/'linea' o 'severity'/'gravedad'.")
