"""Módulo que define el contexto y estado global en vivo de la aplicación Komorebi."""

from typing import List, Optional
from src.estructuras.lista_enlazada import ListaEnlazada
from src.estructuras.cola_fifo import ColaFIFO
from src.nucleo.archivo_codigo import ArchivoCodigo
from src.nucleo.diagnostico import Diagnostico
from src.nucleo.peticion_ia import PeticionIA
from src.nucleo.configuracion_app import ConfiguracionApp


class ContextoApp:
    """Mantiene el estado global de la sesión del Mini IDE en memoria.
    
    Integra la ListaEnlazada de archivos abiertos, la referencia al archivo activo,
    la ColaFIFO de peticiones hacia la IA, la lista de diagnósticos estáticos generados
    y la configuración global activa.
    """

    def __init__(self, configuracion: Optional[ConfiguracionApp] = None) -> None:
        self._archivos_abiertos: ListaEnlazada = ListaEnlazada()
        self._archivo_activo: Optional[ArchivoCodigo] = None
        self._cola_ia: ColaFIFO = ColaFIFO()
        self._diagnosticos: List[Diagnostico] = []
        self._configuracion: ConfiguracionApp = configuracion or ConfiguracionApp()

    @property
    def archivos_abiertos(self) -> ListaEnlazada:
        """Retorna la lista doblemente enlazada de archivos abiertos."""
        return self._archivos_abiertos

    @property
    def archivo_activo(self) -> Optional[ArchivoCodigo]:
        """Retorna la referencia al archivo de código actualmente seleccionado."""
        return self._archivo_activo

    @archivo_activo.setter
    def archivo_activo(self, archivo: Optional[ArchivoCodigo]) -> None:
        """Permite asignar directamente el archivo de código activo."""
        self._archivo_activo = archivo

    @property
    def cola_ia(self) -> ColaFIFO:
        """Retorna la cola FIFO de peticiones de análisis a la IA."""
        return self._cola_ia

    @property
    def diagnosticos(self) -> List[Diagnostico]:
        """Retorna los diagnósticos y alertas generados en el análisis estático actual."""
        return self._diagnosticos

    @diagnosticos.setter
    def diagnosticos(self, nuevos_diagnosticos: List[Diagnostico]) -> None:
        """Actualiza la colección de diagnósticos."""
        self._diagnosticos = [d for d in nuevos_diagnosticos]

    @property
    def configuracion(self) -> ConfiguracionApp:
        """Retorna la configuración activa del sistema."""
        return self._configuracion

    @configuracion.setter
    def configuracion(self, nueva_configuracion: ConfiguracionApp) -> None:
        """Actualiza la configuración del sistema."""
        self._configuracion = nueva_configuracion

    def abrir_archivo(self, archivo: ArchivoCodigo) -> None:
        """Agrega un archivo a la lista enlazada y lo establece como activo si no hay ninguno."""
        self._archivos_abiertos.insertar_al_final(archivo)
        if self._archivo_activo is None:
            self._archivo_activo = archivo

    def buscar_archivo(self, nombre: str) -> Optional[ArchivoCodigo]:
        """Busca un archivo abierto por su nombre en la lista enlazada."""
        return self._archivos_abiertos.buscar(lambda arc: arc.nombre == nombre)

    def cambiar_archivo_activo(self, nombre: str) -> bool:
        """Cambia el archivo activo actual al archivo con el nombre especificado.
        
        Retorna True si el archivo fue encontrado y seleccionado, o False en caso contrario.
        """
        archivo_encontrado = self.buscar_archivo(nombre)
        if archivo_encontrado is None:
            return False

        self._archivo_activo = archivo_encontrado
        return True

    def cerrar_archivo(self, nombre: str) -> bool:
        """Cierra y elimina un archivo de la lista enlazada liberando sus referencias.
        
        Si el archivo eliminado era el activo, reasigna el archivo activo a la nueva cabeza
        de la lista o a None si no quedan archivos.
        """
        eliminado = self._archivos_abiertos.eliminar(lambda arc: arc.nombre == nombre)
        if not eliminado:
            return False

        # Si el archivo activo fue el eliminado, actualizar la referencia activa
        if self._archivo_activo is not None and self._archivo_activo.nombre == nombre:
            if not self._archivos_abiertos.esta_vacia():
                primer_nodo = self._archivos_abiertos.cabeza
                self._archivo_activo = primer_nodo.dato if primer_nodo is not None else None
            else:
                self._archivo_activo = None

        return True

    def listar_archivos(self) -> List[ArchivoCodigo]:
        """Retorna una lista con todos los objetos ArchivoCodigo abiertos."""
        return self._archivos_abiertos.listar()

    def encolar_peticion_ia(self, peticion: PeticionIA) -> None:
        """Encola una nueva petición en el buffer FIFO de IA."""
        self._cola_ia.encolar(peticion)

    def desencolar_peticion_ia(self) -> PeticionIA:
        """Extrae la siguiente petición del buffer FIFO de IA para su procesamiento."""
        return self._cola_ia.desencolar()

    def __repr__(self) -> str:
        activo = self._archivo_activo.nombre if self._archivo_activo else "Ninguno"
        return f"ContextoApp(abiertos={len(self._archivos_abiertos)}, activo={activo!r}, cola_ia={len(self._cola_ia)})"
