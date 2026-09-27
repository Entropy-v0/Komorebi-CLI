"""Módulo del comando concreto 'delete'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_archivos import ServicioArchivos


class ComandoDelete(ComandoBase):
    """Comando para eliminar un archivo de la lista y liberar sus nodos en memoria."""

    def __init__(self, servicio_archivos: ServicioArchivos) -> None:
        super().__init__(
            nombre="delete",
            descripcion="Elimina un archivo de la lista y libera correctamente sus nodos en memoria.",
            sintaxis="delete <id/nombre>",
        )
        self._servicio_archivos: ServicioArchivos = servicio_archivos

    def ejecutar(self, argumentos: List[str]) -> bool:
        if not argumentos:
            print(f"[Error] Debes indicar el identificador o nombre a eliminar. Sintaxis: {self._sintaxis}")
            return False

        identificador = argumentos[0].strip()
        exito = self._servicio_archivos.cerrar_archivo(identificador)
        if exito:
            activo = self._servicio_archivos.obtener_archivo_activo()
            nombre_activo = activo.nombre if activo else "Ninguno"
            print(f"[Éxito] Archivo '{identificador}' eliminado de la lista y memoria liberada.")
            print(f"[Información] Archivo activo actual: '{nombre_activo}'.")
            return True
        else:
            print(f"[Error] No se pudo encontrar ni eliminar el archivo '{identificador}'.")
            return False
