"""Módulo del comando concreto 'switch'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_archivos import ServicioArchivos


class ComandoSwitch(ComandoBase):
    """Comando para alternar el archivo activo actual por nombre o por índice."""

    def __init__(self, servicio_archivos: ServicioArchivos) -> None:
        super().__init__(
            nombre="switch",
            descripcion="Cambia el archivo activo actual para visualizar o editar su contenido.",
            sintaxis="switch <id/nombre>",
        )
        self._servicio_archivos: ServicioArchivos = servicio_archivos

    def ejecutar(self, argumentos: List[str]) -> bool:
        if not argumentos:
            print(f"[Error] Debes indicar el número o nombre del archivo. Sintaxis: {self._sintaxis}")
            return False

        identificador = argumentos[0].strip()
        exito = self._servicio_archivos.cambiar_archivo_activo(identificador)
        if exito:
            activo = self._servicio_archivos.obtener_archivo_activo()
            nombre = activo.nombre if activo else identificador
            print(f"[Éxito] Archivo activo cambiado a '{nombre}'.")
            return True
        else:
            print(f"[Error] No se encontró ningún archivo con el identificador o nombre '{identificador}'.")
            return False
