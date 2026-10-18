"""Módulo que define la excepción para movimientos inválidos en el árbol de directorios."""

from src.excepciones.error_synthetix import ErrorSynthetix


class MovimientoInvalidoError(ErrorSynthetix):
    """Se lanza al intentar mover la raíz o mover una carpeta dentro de sí misma o de sus descendientes."""

    def __init__(self, mensaje: str = "Operación de movimiento inválida en la jerarquía de directorios.") -> None:
        super().__init__(mensaje)

