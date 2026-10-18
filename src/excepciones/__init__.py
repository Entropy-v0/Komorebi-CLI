"""Paquete de excepciones de dominio propias del sistema."""

from src.excepciones.error_synthetix import ErrorSynthetix
from src.excepciones.ruta_invalida_error import RutaInvalidaError
from src.excepciones.nombre_duplicado_error import NombreDuplicadoError
from src.excepciones.movimiento_invalido_error import MovimientoInvalidoError
from src.excepciones.expresion_invalida_error import ExpresionInvalidaError
from src.excepciones.division_por_cero_error import DivisionPorCeroError
from src.excepciones.palabra_duplicada_error import PalabraDuplicadaError

ErrorKomorebi = ErrorSynthetix

__all__ = [
    "ErrorSynthetix",
    "ErrorKomorebi",
    "RutaInvalidaError",
    "NombreDuplicadoError",
    "MovimientoInvalidoError",
    "ExpresionInvalidaError",
    "DivisionPorCeroError",
    "PalabraDuplicadaError",
]

