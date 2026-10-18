"""Módulo que define la excepción para divisiones por cero al evaluar expresiones."""

from src.excepciones.error_synthetix import ErrorSynthetix


class DivisionPorCeroError(ErrorSynthetix, ZeroDivisionError):
    """Se lanza cuando durante la evaluación del árbol de expresiones ocurre una división entre cero."""

    def __init__(self, mensaje: str = "Error matemático: división por cero no permitida.") -> None:
        super().__init__(mensaje)

