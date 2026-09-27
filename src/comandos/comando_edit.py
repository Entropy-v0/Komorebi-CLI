"""Módulo del comando concreto 'edit'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_historial import ServicioHistorial
from src.servicios.servicio_archivos import ServicioArchivos


class ComandoEdit(ComandoBase):
    """Comando auxiliar para agregar o modificar texto en el archivo activo registrando historial."""

    def __init__(
        self,
        servicio_historial: ServicioHistorial,
        servicio_archivos: ServicioArchivos,
        contexto: ContextoApp,
    ) -> None:
        super().__init__(
            nombre="edit",
            descripcion="Agrega una línea de código al archivo activo registrando el estado previo en la pila Undo.",
            sintaxis="edit <nueva_linea_de_codigo>",
        )
        self._servicio_historial: ServicioHistorial = servicio_historial
        self._servicio_archivos: ServicioArchivos = servicio_archivos
        self._contexto: ContextoApp = contexto

    def ejecutar(self, argumentos: List[str]) -> bool:
        archivo = self._contexto.archivo_activo
        if archivo is None:
            print("[Advertencia] No hay ningún archivo activo para editar. Crea o selecciona uno primero.")
            return False

        if not argumentos:
            print(f"[Error] Debes indicar el texto a insertar. Sintaxis: {self._sintaxis}")
            return False

        nueva_linea = " ".join(argumentos)
        # 1. Registrar snapshot anterior en el historial para soportar Undo
        self._servicio_historial.registrar_modificacion(archivo.contenido)

        # 2. Mutar el archivo activo
        nuevo_contenido = f"{archivo.contenido}\n{nueva_linea}" if archivo.contenido else nueva_linea
        archivo.modificar_contenido(nuevo_contenido)

        # 3. Guardar respaldo en disco
        self._servicio_archivos.guardar_respaldo(archivo)

        print(f"[Éxito] Línea agregada a '{archivo.nombre}'. (Total líneas: {archivo.conteo_lineas})")
        return True
