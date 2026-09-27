"""Módulo que define la clase abstracta base para algoritmos de ordenamiento."""

from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional


class OrdenadorBase(ABC):
    """Clase base abstracta que define el contrato común para algoritmos de ordenamiento.
    
    Garantiza que todas las implementaciones ordenen colecciones de forma manual
    sin invocar métodos nativos prohibidos (como .sort() o sorted()),
    admitiendo criterios de comparación personalizados y dirección ascendente/descendente.
    """

    @abstractmethod
    def ordenar(
        self,
        coleccion: List[Any],
        criterio: Optional[Callable[[Any], Any]] = None,
        ascendente: bool = True,
    ) -> List[Any]:
        """Ordena la colección provista y retorna una nueva lista con los elementos ordenados.
        
        Args:
            coleccion: Lista de elementos u objetos a ordenar.
            criterio: Función opcional para extraer la clave de comparación de cada elemento.
            ascendente: Booleano que define si el orden es ascendente (True) o descendente (False).
            
        Returns:
            Nueva lista con los elementos ordenados.
        """
        pass

    def _es_menor_o_igual(
        self,
        elem_a: Any,
        elem_b: Any,
        criterio: Optional[Callable[[Any], Any]] = None,
        ascendente: bool = True,
    ) -> bool:
        """Compara dos elementos respetando el criterio y la dirección solicitada.
        
        Si ascendente es True, verifica si clave(elem_a) <= clave(elem_b).
        Si ascendente es False, verifica si clave(elem_a) >= clave(elem_b).
        """
        clave_a = criterio(elem_a) if criterio is not None else elem_a
        clave_b = criterio(elem_b) if criterio is not None else elem_b

        if ascendente:
            return clave_a <= clave_b
        return clave_a >= clave_b
