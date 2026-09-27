"""Módulo del servicio encargado de la carga y validación de la configuración externa."""

import json
import os
from typing import Optional
from src.nucleo.configuracion_app import ConfiguracionApp


class ServicioConfiguracion:
    """Gestiona la lectura, validación y persistencia de configuración del sistema.
    
    Verifica la existencia y accesibilidad de los directorios de respaldos y logs,
    creándolos automáticamente en el sistema de archivos si no existen.
    """

    def __init__(self, ruta_archivo_config: str = "config.json") -> None:
        self._ruta_archivo_config: str = ruta_archivo_config
        self._configuracion_actual: ConfiguracionApp = ConfiguracionApp()

    @property
    def configuracion(self) -> ConfiguracionApp:
        """Retorna la instancia de configuración actualmente cargada."""
        return self._configuracion_actual

    @property
    def ruta_archivo(self) -> str:
        """Retorna la ruta hacia el archivo de configuración activo."""
        return self._ruta_archivo_config

    def cargar_configuracion(self, ruta_archivo: Optional[str] = None) -> ConfiguracionApp:
        """Carga y parsea el archivo de configuración JSON.
        
        Si el archivo no existe o está corrupto, carga la configuración por defecto
        y asegura la creación de las carpetas locales requeridas.
        """
        self._cargar_variables_entorno_desde_dotenv()
        if ruta_archivo:
            self._ruta_archivo_config = ruta_archivo

        if not os.path.exists(self._ruta_archivo_config):
            self._configuracion_actual = ConfiguracionApp()
            self._asegurar_directorios()
            return self._configuracion_actual

        try:
            with open(self._ruta_archivo_config, "r", encoding="utf-8") as f:
                datos = json.load(f)
            self._configuracion_actual = ConfiguracionApp.desde_diccionario(datos)
        except (json.JSONDecodeError, OSError):
            self._configuracion_actual = ConfiguracionApp()

        self._asegurar_directorios()
        return self._configuracion_actual

    def guardar_configuracion(self, ruta_archivo: Optional[str] = None) -> bool:
        """Persiste la configuración actual a un archivo JSON en disco."""
        destino = ruta_archivo or self._ruta_archivo_config
        try:
            with open(destino, "w", encoding="utf-8") as f:
                json.dump(self._configuracion_actual.a_diccionario(), f, indent=2, ensure_ascii=False)
            return True
        except OSError:
            return False

    def _asegurar_directorios(self) -> None:
        """Garantiza la creación física en disco de las carpetas de respaldos y logs."""
        for ruta in [self._configuracion_actual.ruta_respaldos, self._configuracion_actual.ruta_logs]:
            if ruta and not os.path.exists(ruta):
                os.makedirs(ruta, exist_ok=True)

    def _cargar_variables_entorno_desde_dotenv(self) -> None:
        """Carga variables desde el archivo .env si existe en el entorno local."""
        candidatos = [
            os.path.join(os.getcwd(), ".env"),
            os.path.join(os.path.dirname(os.path.abspath(self._ruta_archivo_config)), ".env"),
        ]
        for ruta_env in candidatos:
            if os.path.exists(ruta_env):
                try:
                    with open(ruta_env, "r", encoding="utf-8") as f:
                        for linea in f:
                            linea_limpia = linea.strip()
                            if linea_limpia and not linea_limpia.startswith("#") and "=" in linea_limpia:
                                clave, valor = linea_limpia.split("=", 1)
                                clave = clave.strip()
                                valor = valor.strip().strip('"').strip("'")
                                os.environ[clave] = valor
                    break
                except OSError:
                    pass
