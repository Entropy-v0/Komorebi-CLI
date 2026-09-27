"""Módulo del servicio encargado del registro persistente de logs y errores del sistema."""

from datetime import datetime
import os
from typing import List, Optional


class ServicioLogs:
    """Gestiona el registro de eventos, advertencias y errores en el directorio de logs configurado.
    
    Escribe trazas cronológicas con formato estandarizado garantizando la persistencia
    de incidentes del sistema en archivos físicos sin requerir bibliotecas externas.
    """

    def __init__(self, ruta_directorio_logs: str = "logs") -> None:
        self._ruta_directorio_logs: str = ruta_directorio_logs
        self._nombre_archivo_errores: str = "errores.log"
        self._asegurar_directorio()

    @property
    def ruta_directorio(self) -> str:
        """Retorna la ruta del directorio de logs."""
        return self._ruta_directorio_logs

    @property
    def ruta_archivo_errores(self) -> str:
        """Retorna la ruta completa al archivo de logs de errores."""
        return os.path.join(self._ruta_directorio_logs, self._nombre_archivo_errores)

    def registrar_error(self, origen: str, mensaje: str) -> bool:
        """Escribe una entrada de nivel ERROR en el archivo errores.log."""
        return self._escribir_registro("ERROR", origen, mensaje)

    def registrar_advertencia(self, origen: str, mensaje: str) -> bool:
        """Escribe una entrada de nivel WARNING en el archivo errores.log."""
        return self._escribir_registro("WARNING", origen, mensaje)

    def registrar_info(self, origen: str, mensaje: str) -> bool:
        """Escribe una entrada de nivel INFO en el archivo errores.log."""
        return self._escribir_registro("INFO", origen, mensaje)

    def leer_ultimos_errores(self, limite: int = 10) -> List[str]:
        """Lee y retorna las últimas N líneas del archivo de errores si existe."""
        if not os.path.isfile(self.ruta_archivo_errores):
            return []
        try:
            with open(self.ruta_archivo_errores, "r", encoding="utf-8") as f:
                lineas = [l.rstrip("\n") for l in f if l.strip()]
            return lineas[-limite:] if limite > 0 else lineas
        except OSError:
            return []

    def limpiar_logs(self) -> bool:
        """Vacia el contenido del archivo de logs de errores."""
        try:
            with open(self.ruta_archivo_errores, "w", encoding="utf-8") as f:
                f.write("")
            return True
        except OSError:
            return False

    def _asegurar_directorio(self) -> None:
        """Asegura que el directorio físico para los logs exista en disco."""
        if self._ruta_directorio_logs and not os.path.exists(self._ruta_directorio_logs):
            try:
                os.makedirs(self._ruta_directorio_logs, exist_ok=True)
            except OSError:
                pass

    def _escribir_registro(self, nivel: str, origen: str, mensaje: str) -> bool:
        """Formatea y añade una línea cronológica al archivo de logs de errores."""
        self._asegurar_directorio()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_log = f"[{timestamp}] [{nivel.upper()}] [{origen}] {mensaje}\n"
        try:
            with open(self.ruta_archivo_errores, "a", encoding="utf-8") as f:
                f.write(linea_log)
            return True
        except OSError:
            return False
