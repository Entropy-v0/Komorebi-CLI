"""Módulo del comando concreto 'list'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_archivos import ServicioArchivos


class ComandoList(ComandoBase):
    """Comando para listar todos los archivos abiertos en la sesión activa."""

    def __init__(self, servicio_archivos: ServicioArchivos) -> None:
        super().__init__(
            nombre="list",
            descripcion="Muestra la lista de todos los archivos abiertos en la sesión indicando su posición y estado.",
            sintaxis="list",
        )
        self._servicio_archivos: ServicioArchivos = servicio_archivos

    def ejecutar(self, argumentos: List[str]) -> bool:
        archivos = self._servicio_archivos.listar_archivos()
        if not archivos:
            print("[Información] No hay ningún archivo abierto actualmente en memoria. Usa 'new <nombre>' para crear uno.")
            return True

        print("\n--- Archivos Abiertos en la Sesión ---")
        for idx, archivo, es_activo in archivos:
            indicador = " [ACTIVO] *" if es_activo else ""
            lineas = archivo.conteo_lineas
            fecha = archivo.fecha_modificacion.strftime("%H:%M:%S")
            print(f"  {idx}. {archivo.nombre:<20} ({lineas:>2} líneas, mod: {fecha}){indicador}")
        print("---------------------------------------\n")
        return True
