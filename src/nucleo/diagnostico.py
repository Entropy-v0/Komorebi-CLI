"""Módulo que define el modelo de dominio para diagnósticos y alertas de código."""

from typing import Dict


class Diagnostico:
    """Representa una advertencia, error o información producida por el análisis estático.
    
    Admite ordenamiento por número de línea o por nivel de severidad/prioridad,
    cumpliendo con los requerimientos del motor de ordenamiento (MergeSort/ShellSort).
    """

    _PRIORIDADES: Dict[str, int] = {
        "INFO": 1,
        "WARN": 2,
        "ERROR": 3,
    }

    def __init__(self, linea: int, severidad: str, mensaje: str, columna: int = 1) -> None:
        self._linea: int = max(1, linea)
        self._severidad: str = severidad.upper()
        if self._severidad not in self._PRIORIDADES:
            self._severidad = "INFO"
        self._mensaje: str = mensaje
        self._columna: int = max(1, columna)

    @property
    def linea(self) -> int:
        """Retorna el número de línea donde se detectó el diagnóstico (base 1)."""
        return self._linea

    @property
    def severidad(self) -> str:
        """Retorna la etiqueta de severidad ('INFO', 'WARN', 'ERROR')."""
        return self._severidad

    @property
    def mensaje(self) -> str:
        """Retorna la descripción detallada del diagnóstico."""
        return self._mensaje

    @property
    def columna(self) -> int:
        """Retorna el número de columna o posición del carácter."""
        return self._columna

    @property
    def prioridad(self) -> int:
        """Mapea el nivel de gravedad a un valor numérico para comparaciones y ordenamiento.
        
        ERROR: 3 (mayor gravedad)
        WARN:  2 (gravedad media)
        INFO:  1 (menor gravedad)
        """
        return self._PRIORIDADES.get(self._severidad, 1)

    def formato_consola(self) -> str:
        """Formatea el diagnóstico para su presentación tabular o en la consola del CLI."""
        return f"[{self._severidad:<5}] Línea {self._linea:>3}, Col {self._columna:>2}: {self._mensaje}"

    def __repr__(self) -> str:
        return f"Diagnostico(linea={self._linea}, severidad={self._severidad!r}, mensaje={self._mensaje!r})"

    def __str__(self) -> str:
        return self.formato_consola()

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Diagnostico):
            return False
        return (
            self._linea == otro._linea
            and self._severidad == otro._severidad
            and self._mensaje == otro._mensaje
        )
