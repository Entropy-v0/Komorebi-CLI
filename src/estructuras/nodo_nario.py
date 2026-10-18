"""Módulo que define el nodo para el Árbol N-ario del espacio de trabajo (Workspace)."""

from typing import List, Optional
from src.estructuras.lista_enlazada import ListaEnlazada
from src.excepciones.nombre_duplicado_error import NombreDuplicadoError
from src.excepciones.ruta_invalida_error import RutaInvalidaError
from src.nucleo.archivo_codigo import ArchivoCodigo


class NodoNario:
    """Nodo de un Árbol N-ario que representa una carpeta o un archivo en el Workspace.
    
    Reglas de invariante:
    - Solo los nodos de tipo CARPETA pueden contener hijos.
    - Los nodos de tipo ARCHIVO almacenan la referencia directa a la instancia ArchivoCodigo.
    - Los nombres entre nodos hermanos bajo una misma carpeta son estrictamente únicos.
    """

    TIPO_CARPETA = "CARPETA"
    TIPO_ARCHIVO = "ARCHIVO"

    def __init__(
        self,
        nombre: str,
        tipo: str = TIPO_CARPETA,
        padre: Optional["NodoNario"] = None,
        archivo: Optional[ArchivoCodigo] = None,
    ) -> None:
        tipo_normalizado = tipo.upper().strip()
        if tipo_normalizado not in (self.TIPO_CARPETA, self.TIPO_ARCHIVO):
            raise ValueError(f"Tipo de nodo N-ario inválido: '{tipo}'. Use CARPETA o ARCHIVO.")

        if tipo_normalizado == self.TIPO_ARCHIVO and archivo is None:
            raise ValueError("Un nodo de tipo ARCHIVO requiere una referencia a ArchivoCodigo.")

        if tipo_normalizado == self.TIPO_CARPETA and archivo is not None:
            raise ValueError("Un nodo de tipo CARPETA no puede tener asociado un ArchivoCodigo.")

        self._nombre: str = nombre
        self._tipo: str = tipo_normalizado
        self._padre: Optional["NodoNario"] = padre
        self._hijos: ListaEnlazada = ListaEnlazada()
        self._archivo: Optional[ArchivoCodigo] = archivo

    @property
    def nombre(self) -> str:
        """Retorna el nombre del archivo o carpeta."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        """Actualiza el nombre del nodo (y el de su ArchivoCodigo si es un archivo)."""
        nombre_limpio = nuevo_nombre.strip()
        if not nombre_limpio or "/" in nombre_limpio or nombre_limpio in (".", ".."):
            raise RutaInvalidaError(f"Nombre de nodo inválido: '{nuevo_nombre}'.")
        self._nombre = nombre_limpio
        if self._archivo is not None:
            self._archivo.nombre = nombre_limpio

    @property
    def tipo(self) -> str:
        """Retorna el tipo del nodo ('CARPETA' o 'ARCHIVO')."""
        return self._tipo

    @property
    def es_carpeta(self) -> bool:
        """Indica si el nodo representa un directorio."""
        return self._tipo == self.TIPO_CARPETA

    @property
    def es_archivo(self) -> bool:
        """Indica si el nodo representa un archivo de código."""
        return self._tipo == self.TIPO_ARCHIVO

    @property
    def padre(self) -> Optional["NodoNario"]:
        """Retorna la referencia al nodo carpeta padre, o None si es la raíz."""
        return self._padre

    @padre.setter
    def padre(self, nuevo_padre: Optional["NodoNario"]) -> None:
        """Actualiza la referencia al nodo padre."""
        self._padre = nuevo_padre

    @property
    def hijos(self) -> ListaEnlazada:
        """Retorna la ListaEnlazada de nodos hijos."""
        return self._hijos

    @property
    def archivo(self) -> Optional[ArchivoCodigo]:
        """Retorna la referencia al objeto ArchivoCodigo si el nodo es de tipo ARCHIVO."""
        return self._archivo

    def buscar_hijo(self, nombre: str) -> Optional["NodoNario"]:
        """Busca un nodo hijo directo por su nombre exacto."""
        if not self.es_carpeta:
            return None
        return self._hijos.buscar(lambda n: n.nombre == nombre)

    def agregar_hijo(self, nodo_hijo: "NodoNario") -> None:
        """Agrega un nodo hijo verificando que este nodo sea carpeta y no haya duplicados."""
        if not self.es_carpeta:
            raise RutaInvalidaError(
                f"No se puede agregar '{nodo_hijo.nombre}' dentro de '{self._nombre}' porque es un archivo."
            )

        if self.buscar_hijo(nodo_hijo.nombre) is not None:
            ruta_actual = self.obtener_ruta_absoluta()
            raise NombreDuplicadoError(
                f"Ya existe un elemento llamado '{nodo_hijo.nombre}' en '{ruta_actual}'."
            )

        nodo_hijo.padre = self
        self._hijos.insertar_al_final(nodo_hijo)

    def eliminar_hijo(self, nombre: str) -> Optional["NodoNario"]:
        """Desvincula y retorna el nodo hijo con el nombre indicado, o None si no existe."""
        if not self.es_carpeta:
            return None

        hijo = self.buscar_hijo(nombre)
        if hijo is None:
            return None

        self._hijos.eliminar(lambda n: n.nombre == nombre)
        hijo.padre = None
        return hijo

    def listar_hijos(self) -> List["NodoNario"]:
        """Retorna una lista con todos los nodos hijos directos."""
        if not self.es_carpeta:
            return []
        return [nodo for nodo in self._hijos if isinstance(nodo, NodoNario)]

    def obtener_ruta_absoluta(self) -> str:
        """Construye la ruta absoluta desde la raíz '/' hasta este nodo."""
        if self._padre is None:
            return "/"

        segmentos: List[str] = []
        actual: Optional["NodoNario"] = self
        while actual is not None and actual.padre is not None:
            segmentos.append(actual.nombre)
            actual = actual.padre

        segmentos.reverse()
        return "/" + "/".join(segmentos)

    def es_ancestro_de(self, otro_nodo: "NodoNario") -> bool:
        """Verifica si este nodo es igual a `otro_nodo` o es ancestro jerárquico de él."""
        actual: Optional["NodoNario"] = otro_nodo
        while actual is not None:
            if actual is self:
                return True
            actual = actual.padre
        return False

    def __repr__(self) -> str:
        return f"NodoNario(nombre={self._nombre!r}, tipo={self._tipo!r})"

