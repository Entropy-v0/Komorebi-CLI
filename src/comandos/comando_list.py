"""Módulo del comando concreto 'list'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_archivos import ServicioArchivos


class ComandoList(ComandoBase):
    """Comando para listar todos los archivos abiertos en la sesión activa."""

    def __init__(self, servicio_archivos: ServicioArchivos) -> None:
        super().__init__(
            nombre="list",
            descripcion="Muestra la lista de archivos abiertos en la sesión (admite filtrar por nombre o ruta).",
            sintaxis="list [nombre_o_ruta]",
        )
        self._servicio_archivos: ServicioArchivos = servicio_archivos

    def ejecutar(self, argumentos: List[str]) -> bool:
        filtro = argumentos[0].strip() if argumentos else None
        archivos = self._servicio_archivos.listar_archivos(filtro)
        if not archivos:
            print("[Información] No hay ningún archivo abierto actualmente en memoria. Usa 'new <nombre>' para crear uno.")
            return True

        print("\n--- Archivos Abiertos en la Sesión ---")
        for idx, archivo, es_activo in archivos:
            indicador = " [ACTIVO] *" if es_activo else ""
            lineas = archivo.conteo_lineas
            fecha = archivo.fecha_modificacion.strftime("%H:%M:%S")
            ruta_mostrada = self._servicio_archivos.obtener_ruta_archivo(archivo)
            etiqueta = f"{archivo.nombre} ({ruta_mostrada})" if ruta_mostrada not in (archivo.nombre, f"/{archivo.nombre}") else archivo.nombre
            print(f"  {idx}. {etiqueta:<26} ({lineas:>2} líneas, mod: {fecha}){indicador}")
        print("---------------------------------------\n")
        return True
