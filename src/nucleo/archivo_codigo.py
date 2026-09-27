"""Módulo que define el modelo de dominio para archivos de código en memoria."""

from datetime import datetime
from typing import List


class ArchivoCodigo:
    """Representa un archivo o fragmento de código fuente abierto en la sesión del IDE.
    
    Encapsula el nombre del fichero, su contenido textual, y sus metadatos temporales
    de creación y última modificación.
    """

    def __init__(self, nombre: str, contenido: str = "") -> None:
        self._nombre: str = nombre
        self._contenido: str = contenido
        self._fecha_creacion: datetime = datetime.now()
        self._fecha_modificacion: datetime = self._fecha_creacion

    @property
    def nombre(self) -> str:
        """Retorna el nombre o identificador del archivo."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        """Permite renombrar el archivo actualizando su fecha de modificación."""
        self._nombre = nuevo_nombre
        self._fecha_modificacion = datetime.now()

    @property
    def contenido(self) -> str:
        """Retorna el contenido en texto plano del archivo."""
        return self._contenido

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora de creación del archivo en memoria."""
        return self._fecha_creacion

    @property
    def fecha_modificacion(self) -> datetime:
        """Retorna la fecha y hora de la última modificación del archivo."""
        return self._fecha_modificacion

    @property
    def conteo_lineas(self) -> int:
        """Calcula la cantidad total de líneas en el código."""
        if not self._contenido:
            return 0
        return len(self.obtener_lineas())

    @property
    def tamano_bytes(self) -> int:
        """Retorna la longitud en caracteres/bytes del contenido en memoria."""
        return len(self._contenido.encode("utf-8"))

    def modificar_contenido(self, nuevo_contenido: str) -> None:
        """Actualiza el código fuente del archivo y refresca la fecha de modificación."""
        self._contenido = nuevo_contenido
        self._fecha_modificacion = datetime.now()

    def obtener_lineas(self) -> List[str]:
        """Divide el contenido en una lista de líneas individuales."""
        return self._contenido.splitlines()

    def __repr__(self) -> str:
        return f"ArchivoCodigo(nombre={self._nombre!r}, lineas={self.conteo_lineas})"

    def __str__(self) -> str:
        return f"{self._nombre} ({self.conteo_lineas} líneas, modificado: {self._fecha_modificacion.strftime('%Y-%m-%d %H:%M:%S')})"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, ArchivoCodigo):
            return False
        return self._nombre == otro._nombre
