"""Módulo del comando concreto 'show'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.nucleo.contexto_app import ContextoApp


class ComandoShow(ComandoBase):
    """Comando auxiliar para visualizar el contenido numerado del archivo activo."""

    def __init__(self, contexto: ContextoApp) -> None:
        super().__init__(
            nombre="show",
            descripcion="Muestra el contenido actual del archivo activo con números de línea.",
            sintaxis="show",
        )
        self._contexto: ContextoApp = contexto

    def ejecutar(self, argumentos: List[str]) -> bool:
        archivo = self._contexto.archivo_activo
        if archivo is None:
            print("[Advertencia] No hay ningún archivo activo para mostrar.")
            return False

        print(f"\n--- Contenido de '{archivo.nombre}' ({archivo.conteo_lineas} líneas) ---")
        lineas = archivo.obtener_lineas()
        if not lineas:
            print("  (Archivo vacío)")
        else:
            for num, linea in enumerate(lineas, start=1):
                print(f"  {num:>3} | {linea}")
        print("---------------------------------------------------\n")
        return True
