"""Módulo que define el modelo de dominio para peticiones de análisis con IA."""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional


class PeticionIA:
    """Modelo para representar una solicitud de análisis de código enviada a la API de IA.
    
    Gestiona el ciclo de vida de la petición dentro del buffer FIFO:
    'PENDIENTE' -> 'EN_PROCESO' -> 'COMPLETADO' | 'FALLIDO'.
    """

    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_EN_PROCESO = "EN_PROCESO"
    ESTADO_COMPLETADO = "COMPLETADO"
    ESTADO_FALLIDO = "FALLIDO"

    def __init__(
        self,
        codigo: str,
        nombre_archivo: str = "fragmento.txt",
        id_peticion: Optional[str] = None,
    ) -> None:
        self._id_peticion: str = id_peticion or f"req-{uuid.uuid4().hex[:8]}"
        self._codigo: str = codigo
        self._nombre_archivo: str = nombre_archivo
        self._timestamp: datetime = datetime.now()
        self._estado: str = self.ESTADO_PENDIENTE
        self._resultado: Optional[Dict[str, Any]] = None
        self._error: Optional[str] = None

    @property
    def id_peticion(self) -> str:
        """Retorna el identificador único de la petición."""
        return self._id_peticion

    @property
    def codigo(self) -> str:
        """Retorna el fragmento de código asociado a la solicitud."""
        return self._codigo

    @property
    def nombre_archivo(self) -> str:
        """Retorna el nombre del archivo de procedencia."""
        return self._nombre_archivo

    @property
    def timestamp(self) -> datetime:
        """Retorna el momento en que la petición fue creada o encolada."""
        return self._timestamp

    @property
    def estado(self) -> str:
        """Retorna el estado actual del procesamiento."""
        return self._estado

    @property
    def resultado(self) -> Optional[Dict[str, Any]]:
        """Retorna la respuesta estructurada de la IA (métricas Big O y refactorización)."""
        return self._resultado

    @property
    def error(self) -> Optional[str]:
        """Retorna el mensaje de error en caso de que la petición haya fallado."""
        return self._error

    def marcar_en_proceso(self) -> None:
        """Transiciona el estado a 'EN_PROCESO'."""
        self._estado = self.ESTADO_EN_PROCESO

    def marcar_completado(self, resultado: Dict[str, Any]) -> None:
        """Registra el resultado exitoso recibido desde el endpoint de IA."""
        self._estado = self.ESTADO_COMPLETADO
        self._resultado = resultado
        self._error = None

    def marcar_fallido(self, mensaje_error: str) -> None:
        """Registra el fallo de conexión o ejecución de la petición."""
        self._estado = self.ESTADO_FALLIDO
        self._error = mensaje_error

    def __repr__(self) -> str:
        return f"PeticionIA(id={self._id_peticion!r}, estado={self._estado!r}, archivo={self._nombre_archivo!r})"

    def __str__(self) -> str:
        hora = self._timestamp.strftime("%H:%M:%S")
        return f"[{self._id_peticion}] {self._nombre_archivo} - Estado: {self._estado} ({hora})"
