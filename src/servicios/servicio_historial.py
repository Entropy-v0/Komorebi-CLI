"""Módulo del servicio encargado de la gestión del historial de cambios Undo/Redo."""

from typing import Optional
from src.estructuras.pila import Pila


class ServicioHistorial:
    """Implementa el control de cambios temporal (Undo/Redo) mediante dos pilas LIFO.
    
    Permite registrar snapshots de texto antes de mutaciones, retroceder al estado anterior
    y avanzar a estados revertidos, cumpliendo el requerimiento de dos pilas independientes.
    """

    def __init__(self) -> None:
        self._pila_deshacer: Pila = Pila()
        self._pila_rehacer: Pila = Pila()

    @property
    def puede_deshacer(self) -> bool:
        """Indica si existen estados previos disponibles para retroceder."""
        return not self._pila_deshacer.esta_vacia()

    @property
    def puede_rehacer(self) -> bool:
        """Indica si existen estados posteriores disponibles para avanzar."""
        return not self._pila_rehacer.esta_vacia()

    @property
    def tamano_deshacer(self) -> int:
        """Retorna la cantidad de modificaciones almacenadas en la pila de deshacer."""
        return len(self._pila_deshacer)

    @property
    def tamano_rehacer(self) -> int:
        """Retorna la cantidad de modificaciones almacenadas en la pila de rehacer."""
        return len(self._pila_rehacer)

    def registrar_modificacion(self, contenido_previo: str) -> None:
        """Guarda una instantánea del estado antes de aplicar un cambio.
        
        Limpia la pila de rehacer ya que una nueva mutación invalida el árbol de avance.
        """
        self._pila_deshacer.apilar(contenido_previo)
        self._pila_rehacer.limpiar()

    def deshacer(self, contenido_actual: str) -> Optional[str]:
        """Retrocede al último estado previo apilando el estado actual en la pila de rehacer.
        
        Retorna el contenido restaurado, o None si la pila de deshacer está vacía.
        """
        if not self.puede_deshacer:
            return None

        estado_anterior = self._pila_deshacer.desapilar()
        self._pila_rehacer.apilar(contenido_actual)
        return estado_anterior

    def rehacer(self, contenido_actual: str) -> Optional[str]:
        """Avanza al estado previamente deshecho apilando el estado actual en la pila de deshacer.
        
        Retorna el contenido avanzado, o None si la pila de rehacer está vacía.
        """
        if not self.puede_rehacer:
            return None

        estado_siguiente = self._pila_rehacer.desapilar()
        self._pila_deshacer.apilar(contenido_actual)
        return estado_siguiente

    def limpiar(self) -> None:
        """Vacía ambas pilas liberando la memoria de los snapshots."""
        self._pila_deshacer.limpiar()
        self._pila_rehacer.limpiar()
