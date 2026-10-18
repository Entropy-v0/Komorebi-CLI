"""Módulo que define la excepción para nombres duplicados entre hermanos."""

from src.excepciones.error_synthetix import ErrorSynthetix


class NombreDuplicadoError(ErrorSynthetix, ValueError):
    """Se lanza al intentar crear o mover un archivo/carpeta con un nombre ya existente en el mismo directorio."""

    def __init__(self, mensaje: str = "Ya existe un elemento con ese nombre en el directorio actual.") -> None:
        super().__init__(mensaje)

