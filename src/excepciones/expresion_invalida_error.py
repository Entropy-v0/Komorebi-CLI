"""Módulo que define la excepción para expresiones aritméticas inválidas."""

from src.excepciones.error_synthetix import ErrorSynthetix


class ExpresionInvalidaError(ErrorSynthetix):
    """Se lanza cuando una expresión matemática contiene errores léxicos o sintácticos."""

    def __init__(self, mensaje: str = "La expresión aritmética proporcionada no es válida.") -> None:
        super().__init__(mensaje)

