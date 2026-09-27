"""Módulo del comando concreto 'undo'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_historial import ServicioHistorial
from src.servicios.servicio_archivos import ServicioArchivos


class ComandoUndo(ComandoBase):
    """Comando para deshacer la última modificación en el código activo usando una Pila LIFO."""

    def __init__(
        self,
        servicio_historial: ServicioHistorial,
        servicio_archivos: ServicioArchivos,
        contexto: ContextoApp,
    ) -> None:
        super().__init__(
            nombre="undo",
            descripcion="Deshace el último cambio realizado sobre el código utilizando la pila de retroceso.",
            sintaxis="undo",
        )
        self._servicio_historial: ServicioHistorial = servicio_historial
        self._servicio_archivos: ServicioArchivos = servicio_archivos
        self._contexto: ContextoApp = contexto

    def ejecutar(self, argumentos: List[str]) -> bool:
        archivo = self._contexto.archivo_activo
        if archivo is None:
            print("[Advertencia] No hay ningún archivo activo para deshacer cambios.")
            return False

        if not self._servicio_historial.puede_deshacer:
            print("[Información] No hay más estados previos para deshacer en el historial.")
            return False

        contenido_anterior = self._servicio_historial.deshacer(archivo.contenido)
        if contenido_anterior is not None:
            archivo.modificar_contenido(contenido_anterior)
            self._servicio_archivos.guardar_respaldo(archivo)
            print(f"[Éxito] Cambio deshecho en '{archivo.nombre}'. (Líneas: {archivo.conteo_lineas})")
            return True

        return False
