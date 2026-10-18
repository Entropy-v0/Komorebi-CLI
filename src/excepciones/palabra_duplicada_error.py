"""Módulo que define la excepción para palabras duplicadas en el diccionario AVL."""

from src.excepciones.error_synthetix import ErrorSynthetix


class PalabraDuplicadaError(ErrorSynthetix):
    """Se lanza al intentar insertar una palabra clave que ya existe en el árbol AVL del diccionario."""

    def __init__(self, mensaje: str = "La palabra clave ya se encuentra registrada en el diccionario.") -> None:
        super().__init__(mensaje)

