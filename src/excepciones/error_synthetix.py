"""Módulo que define la excepción base del sistema."""


class ErrorSynthetix(Exception):
    """Excepción base para todos los errores de dominio en el Mini IDE Komorebi/Synthetix.
    
    Permite capturar cualquier error controlado del sistema desde la capa CLI
    para presentar un mensaje claro sin interrumpir abruptamente el bucle REPL.
    """

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self._mensaje: str = mensaje

    @property
    def mensaje(self) -> str:
        """Retorna la descripción detallada del error ocurrido."""
        return self._mensaje

