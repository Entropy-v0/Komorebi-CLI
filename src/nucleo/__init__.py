"""Módulo de modelos de dominio y contexto compartido de la aplicación."""

from src.nucleo.archivo_codigo import ArchivoCodigo
from src.nucleo.diagnostico import Diagnostico
from src.nucleo.peticion_ia import PeticionIA
from src.nucleo.configuracion_app import ConfiguracionApp
from src.nucleo.contexto_app import ContextoApp

__all__ = [
    "ArchivoCodigo",
    "Diagnostico",
    "PeticionIA",
    "ConfiguracionApp",
    "ContextoApp",
]
