"""Módulo del comando concreto 'new'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_archivos import ServicioArchivos


class ComandoNew(ComandoBase):
    """Comando para crear un nuevo archivo de código en memoria con respaldo en disco."""

    def __init__(self, servicio_archivos: ServicioArchivos) -> None:
        super().__init__(
            nombre="new",
            descripcion="Crea un nuevo archivo en memoria con el nombre indicado y contenido inicial opcional.",
            sintaxis="new <nombre_archivo> [contenido_inicial]",
        )
        self._servicio_archivos: ServicioArchivos = servicio_archivos

    def ejecutar(self, argumentos: List[str]) -> bool:
        if not argumentos:
            print(f"[Error] Falta el nombre del archivo. Sintaxis: {self._sintaxis}")
            return False

        nombre_archivo = argumentos[0].strip()
        contenido_inicial = " ".join(argumentos[1:]) if len(argumentos) > 1 else ""

        try:
            archivo = self._servicio_archivos.crear_archivo(nombre_archivo, contenido_inicial)
            print(f"[Éxito] Archivo '{archivo.nombre}' creado y establecido como activo (respaldo en disco guardado).")
            return True
        except ValueError as e:
            print(f"[Error] {str(e)}")
            return False
