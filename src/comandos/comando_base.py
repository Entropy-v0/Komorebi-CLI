"""Módulo que define la interfaz base abstracta del Patrón Command."""

from abc import ABC, abstractmethod
from typing import List


class ComandoBase(ABC):
    """Clase base abstracta para todos los comandos del sistema Komorebi.
    
    Encapsula una acción sobre el sistema desacoplando la invocación en la consola
    CLI de la lógica real ejecutada en los servicios de negocio (receptores).
    """

    def __init__(self, nombre: str, descripcion: str, sintaxis: str) -> None:
        self._nombre: str = nombre
        self._descripcion: str = descripcion
        self._sintaxis: str = sintaxis

    @property
    def nombre(self) -> str:
        """Retorna el identificador o palabra clave que invoca el comando."""
        return self._nombre

    @property
    def descripcion(self) -> str:
        """Retorna una explicación breve del propósito del comando."""
        return self._descripcion

    @property
    def sintaxis(self) -> str:
        """Retorna la signatura o ejemplo de uso de los argumentos del comando."""
        return self._sintaxis

    @abstractmethod
    def ejecutar(self, argumentos: List[str]) -> bool:
        """Ejecuta la acción encapsulada utilizando los argumentos provistos.
        
        Args:
            argumentos: Lista de parámetros posicionales tokenizados.
            
        Returns:
            True si el comando se ejecutó satisfactoriamente, False si ocurrió un error.
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nombre={self._nombre!r})"
