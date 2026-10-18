"""Módulo del comando concreto 'ls'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_navegacion import ServicioNavegacion


class ComandoLs(ComandoBase):
    """Comando para listar el contenido de un directorio real o del Workspace virtual."""

    FLAGS_OCULTOS = ("-a", "-A", "--all")

    def __init__(self, servicio_navegacion: ServicioNavegacion) -> None:
        super().__init__(
            nombre="ls",
            descripcion=(
                "Lista el contenido del directorio actual o de una ruta "
                "('-a' muestra ocultos; 'ws:ruta' lista el Workspace)."
            ),
            sintaxis="ls [-a] [ruta | ws:ruta]",
        )
        self._servicio_navegacion: ServicioNavegacion = servicio_navegacion

    def ejecutar(self, argumentos: List[str]) -> bool:
        mostrar_ocultos = any(arg in self.FLAGS_OCULTOS for arg in argumentos)
        partes_ruta = [arg for arg in argumentos if arg not in self.FLAGS_OCULTOS]
        ruta = " ".join(partes_ruta).strip() or None

        elementos = self._servicio_navegacion.listar(ruta, mostrar_ocultos)
        if not elementos:
            print("(Directorio vacío)")
            return True

        for nombre, es_directorio in elementos:
            etiqueta = f"{nombre}/" if es_directorio else nombre
            print(f"  {etiqueta}")
        return True
