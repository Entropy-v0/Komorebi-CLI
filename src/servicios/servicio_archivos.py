"""Módulo del servicio encargado de la gestión de archivos de código y respaldos en disco."""

import os
from typing import List, Optional, Tuple
from src.nucleo.archivo_codigo import ArchivoCodigo
from src.nucleo.contexto_app import ContextoApp


class ServicioArchivos:
    """Orquesta las operaciones sobre los archivos abiertos en memoria y su persistencia en disco.
    
    Gestiona la ListaEnlazada de archivos del ContextoApp y realiza respaldos automáticos
    en la ruta configurada cada vez que se crea o modifica un archivo.
    """

    def __init__(self, contexto: ContextoApp) -> None:
        self._contexto: ContextoApp = contexto

    def crear_archivo(self, nombre: str, contenido_inicial: str = "") -> ArchivoCodigo:
        """Crea un nuevo archivo en memoria, lo añade a la lista y genera un respaldo en disco.
        
        Lanza ValueError si ya existe un archivo abierto con el mismo nombre.
        """
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            raise ValueError("El nombre del archivo no puede estar vacío.")

        if self._contexto.buscar_archivo(nombre_limpio) is not None:
            raise ValueError(f"Ya existe un archivo abierto con el nombre '{nombre_limpio}'.")

        if not contenido_inicial and os.path.isfile(nombre_limpio):
            try:
                with open(nombre_limpio, "r", encoding="utf-8") as f:
                    contenido_inicial = f.read()
            except OSError:
                pass

        nuevo_archivo = ArchivoCodigo(nombre_limpio, contenido_inicial)
        self._contexto.abrir_archivo(nuevo_archivo)
        self.guardar_respaldo(nuevo_archivo)
        return nuevo_archivo

    def cambiar_archivo_activo(self, identificador: str) -> bool:
        """Cambia el archivo activo buscando por nombre exacto o por número de índice (1-based)."""
        id_limpio = identificador.strip()
        # Intento de cambio por índice numérico
        if id_limpio.isdigit():
            indice_1_based = int(id_limpio)
            indice_0_based = indice_1_based - 1
            if 0 <= indice_0_based < len(self._contexto.archivos_abiertos):
                archivo = self._contexto.archivos_abiertos.obtener_por_indice(indice_0_based)
                if isinstance(archivo, ArchivoCodigo):
                    self._contexto.archivo_activo = archivo
                    return True

        # Cambio por nombre
        return self._contexto.cambiar_archivo_activo(id_limpio)

    def cerrar_archivo(self, identificador: str) -> bool:
        """Cierra un archivo eliminándolo de la lista enlazada y liberando sus referencias."""
        id_limpio = identificador.strip()
        if id_limpio.isdigit():
            indice_0_based = int(id_limpio) - 1
            if 0 <= indice_0_based < len(self._contexto.archivos_abiertos):
                archivo = self._contexto.archivos_abiertos.obtener_por_indice(indice_0_based)
                if isinstance(archivo, ArchivoCodigo):
                    return self._contexto.cerrar_archivo(archivo.nombre)

        return self._contexto.cerrar_archivo(id_limpio)

    def obtener_archivo_activo(self) -> Optional[ArchivoCodigo]:
        """Retorna la referencia al archivo actualmente seleccionado para edición."""
        return self._contexto.archivo_activo

    def listar_archivos(self) -> List[Tuple[int, ArchivoCodigo, bool]]:
        """Retorna una lista de tuplas (posicion_1_based, archivo, es_activo) de todos los archivos."""
        resultado: List[Tuple[int, ArchivoCodigo, bool]] = []
        activo = self._contexto.archivo_activo

        indice = 1
        for item in self._contexto.archivos_abiertos:
            if isinstance(item, ArchivoCodigo):
                es_activo = (activo is not None and item.nombre == activo.nombre)
                resultado.append((indice, item, es_activo))
                indice += 1

        return resultado

    def guardar_respaldo(self, archivo: Optional[ArchivoCodigo] = None) -> Optional[str]:
        """Escribe una copia física del archivo en el directorio de respaldos configurado.
        
        Si no se pasa archivo, respalda el archivo activo actual.
        """
        objetivo = archivo or self._contexto.archivo_activo
        if objetivo is None:
            return None

        directorio_respaldo = self._contexto.configuracion.ruta_respaldos
        if not os.path.exists(directorio_respaldo):
            os.makedirs(directorio_respaldo, exist_ok=True)

        ruta_destino = os.path.join(directorio_respaldo, objetivo.nombre)
        try:
            with open(ruta_destino, "w", encoding="utf-8") as f:
                f.write(objetivo.contenido)
            return ruta_destino
        except OSError:
            return None
