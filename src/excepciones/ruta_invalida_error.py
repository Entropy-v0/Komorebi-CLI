"""Módulo que define la excepción para rutas inválidas o inexistentes."""

from src.excepciones.error_synthetix import ErrorSynthetix


class RutaInvalidaError(ErrorSynthetix):
    """Se lanza cuando una ruta del workspace es inválida, no existe o no es del tipo esperado."""

    def __init__(self, mensaje: str = "La ruta especificada no es válida o no existe.") -> None:
        super().__init__(mensaje)

