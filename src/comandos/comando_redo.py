"""Módulo del comando concreto 'redo'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_historial import ServicioHistorial
from src.servicios.servicio_archivos import ServicioArchivos


class ComandoRedo(ComandoBase):
    """Comando para rehacer un cambio deshecho en el código activo usando una Pila LIFO."""

    def __init__(
        self,
        servicio_historial: ServicioHistorial,
        servicio_archivos: ServicioArchivos,
        contexto: ContextoApp,
    ) -> None:
        super().__init__(
            nombre="redo",
            descripcion="Rehace el cambio previamente deshecho utilizando la pila de avance.",
            sintaxis="redo",
        )
        self._servicio_historial: ServicioHistorial = servicio_historial
        self._servicio_archivos: ServicioArchivos = servicio_archivos
        self._contexto: ContextoApp = contexto

    def ejecutar(self, argumentos: List[str]) -> bool:
        archivo = self._contexto.archivo_activo
        if archivo is None:
            print("[Advertencia] No hay ningún archivo activo para rehacer cambios.")
            return False

        if not self._servicio_historial.puede_rehacer:
            print("[Información] No hay cambios deshechos disponibles para rehacer.")
            return False

        contenido_siguiente = self._servicio_historial.rehacer(archivo.contenido)
        if contenido_siguiente is not None:
            archivo.modificar_contenido(contenido_siguiente)
            self._servicio_archivos.guardar_respaldo(archivo)
            print(f"[Éxito] Cambio rehecho en '{archivo.nombre}'. (Líneas: {archivo.conteo_lineas})")
            return True

        return False
