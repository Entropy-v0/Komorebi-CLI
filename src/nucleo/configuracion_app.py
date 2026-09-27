"""Módulo que define el modelo de configuración externa del sistema."""

import os
from typing import Any, Dict, List, Optional


class ConfiguracionApp:
    """Encapsula los parámetros de configuración leídos desde el archivo externo config.json.
    
    Gestiona las rutas locales de respaldos y logs, los límites de tiempo de ejecución,
    el proveedor de IA (ej. Google Gemini o mock offline) y los endpoints de conexión.
    """

    def __init__(
        self,
        ruta_respaldos: str = "respaldos",
        ruta_logs: str = "logs",
        url_ia: str = "https://generativelanguage.googleapis.com/v1beta/models",
        endpoint_analisis: str = "/analizar",
        tiempo_maximo_ejecucion: int = 15,
        nombre_app: str = "Komorebi Mini IDE",
        puerto: int = 8000,
        proveedor_ia: str = "gemini",
        modelo_ia: str = "gemini-3.8-flash",
        api_key_ia: Optional[str] = None,
    ) -> None:
        self._ruta_respaldos: str = ruta_respaldos
        self._ruta_logs: str = ruta_logs
        self._url_ia: str = url_ia
        self._endpoint_analisis: str = endpoint_analisis
        self._tiempo_maximo_ejecucion: int = max(1, tiempo_maximo_ejecucion)
        self._nombre_app: str = nombre_app
        self._puerto: int = puerto
        self._proveedor_ia: str = proveedor_ia
        self._modelo_ia: str = modelo_ia
        if api_key_ia is None:
            self._api_key_ia: str = os.environ.get("GEMINI_API_KEY", "")
        elif isinstance(api_key_ia, str) and api_key_ia.startswith("${") and api_key_ia.endswith("}"):
            nombre_var = api_key_ia[2:-1].strip()
            self._api_key_ia: str = os.environ.get(nombre_var, "")
        else:
            self._api_key_ia: str = api_key_ia

    @property
    def ruta_respaldos(self) -> str:
        """Retorna la ruta del directorio destinado a respaldos automáticos."""
        return self._ruta_respaldos

    @property
    def ruta_logs(self) -> str:
        """Retorna la ruta del directorio para almacenamiento de logs y errores."""
        return self._ruta_logs

    @property
    def url_ia(self) -> str:
        """Retorna la URL base de conexión hacia la API de IA."""
        return self._url_ia

    @property
    def endpoint_analisis(self) -> str:
        """Retorna el endpoint relativo para el envío de código a analizar."""
        return self._endpoint_analisis

    @property
    def proveedor_ia(self) -> str:
        """Retorna el identificador del proveedor de IA ('gemini', 'mock', etc.)."""
        return self._proveedor_ia

    @property
    def modelo_ia(self) -> str:
        """Retorna el identificador del modelo LLM configurado."""
        return self._modelo_ia

    @property
    def api_key_ia(self) -> str:
        """Retorna la clave de API para la llamada a la IA (si está configurada)."""
        if self._api_key_ia.startswith("${") and self._api_key_ia.endswith("}"):
            nombre_var = self._api_key_ia[2:-1].strip()
            return os.environ.get(nombre_var, "")
        return self._api_key_ia

    @property
    def api_key_enmascarada(self) -> str:
        """Retorna una versión enmascarada de la API key para visualización segura en la consola."""
        key = self.api_key_ia
        if not key:
            return "[No configurada / Modo Offline]"
        if len(key) <= 8:
            return "******** (cargada desde .env)"
        return f"{key[:6]}...{key[-4:]} (cargada desde .env)"

    @property
    def url_completa_ia(self) -> str:
        """Retorna la URL completa combinando la URL base y el endpoint o modelo."""
        if self._proveedor_ia.lower() == "gemini":
            base = self._url_ia.rstrip("/")
            modelo = self._modelo_ia.strip("/")
            return f"{base}/{modelo}:generateContent"

        url_base = self._url_ia.rstrip("/")
        endpoint = self._endpoint_analisis if self._endpoint_analisis.startswith("/") else f"/{self._endpoint_analisis}"
        return f"{url_base}{endpoint}"

    @property
    def tiempo_maximo_ejecucion(self) -> int:
        """Retorna el timeout máximo en segundos para peticiones externas."""
        return self._tiempo_maximo_ejecucion

    @property
    def nombre_app(self) -> str:
        """Retorna el nombre formal de la aplicación."""
        return self._nombre_app

    @property
    def puerto(self) -> int:
        """Retorna el puerto de conexión configurado."""
        return self._puerto

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "ConfiguracionApp":
        """Construye una instancia a partir de un diccionario parseado de JSON.
        
        Admite formatos anidados y planos con valores por defecto seguros.
        """
        rutas = datos.get("rutas", {})
        ia = datos.get("ia", {})
        servidor = datos.get("servidor", {})

        ruta_respaldos = rutas.get("respaldos", datos.get("ruta_respaldos", "respaldos"))
        ruta_logs = rutas.get("logs", datos.get("ruta_logs", "logs"))
        url_ia = ia.get("url_base", datos.get("url_ia", "https://generativelanguage.googleapis.com/v1beta/models"))
        endpoint_analisis = ia.get("endpoint_analisis", datos.get("endpoint_analisis", "/analizar"))
        tiempo_max = ia.get("timeout_segundos", datos.get("tiempo_maximo_ejecucion", 15))
        proveedor_ia = ia.get("proveedor", datos.get("proveedor_ia", "gemini"))
        modelo_ia = ia.get("modelo", datos.get("modelo_ia", "gemini-3.8-flash"))
        api_key_raw = ia.get("api_key", datos.get("api_key_ia", None))
        api_key_ia = None if api_key_raw == "" else api_key_raw
        nombre_app = datos.get("nombre_app", "Komorebi Mini IDE")
        puerto = servidor.get("puerto", datos.get("puerto", 8000))

        return cls(
            ruta_respaldos=ruta_respaldos,
            ruta_logs=ruta_logs,
            url_ia=url_ia,
            endpoint_analisis=endpoint_analisis,
            tiempo_maximo_ejecucion=int(tiempo_max),
            nombre_app=nombre_app,
            puerto=int(puerto),
            proveedor_ia=proveedor_ia,
            modelo_ia=modelo_ia,
            api_key_ia=api_key_ia,
        )

    def a_diccionario(self) -> Dict[str, Any]:
        """Serializa la configuración a un diccionario estructurado."""
        return {
            "nombre_app": self._nombre_app,
            "rutas": {
                "respaldos": self._ruta_respaldos,
                "logs": self._ruta_logs,
            },
            "ia": {
                "proveedor": self._proveedor_ia,
                "modelo": self._modelo_ia,
                "api_key": self._api_key_ia,
                "url_base": self._url_ia,
                "endpoint_analisis": self._endpoint_analisis,
                "timeout_segundos": self._tiempo_maximo_ejecucion,
            },
            "servidor": {
                "puerto": self._puerto,
            },
        }

    def validar(self) -> List[str]:
        """Valida la coherencia de los valores configurados y retorna una lista de advertencias o errores."""
        errores: List[str] = []
        if not self._ruta_respaldos.strip():
            errores.append("La ruta de respaldos no puede estar vacía.")
        if not self._ruta_logs.strip():
            errores.append("La ruta de logs no puede estar vacía.")
        if not self._url_ia.strip():
            errores.append("La URL de la API de IA no puede estar vacía.")
        if self._tiempo_maximo_ejecucion <= 0:
            errores.append("El tiempo máximo de ejecución debe ser un número positivo.")
        return errores

    def __repr__(self) -> str:
        return f"ConfiguracionApp(app={self._nombre_app!r}, proveedor={self._proveedor_ia!r}, modelo={self._modelo_ia!r})"
