"""Módulo que define la estructura de datos Árbol N-ario para el directorio de trabajo."""

from typing import List, Optional, Tuple
from src.estructuras.nodo_nario import NodoNario
from src.estructuras.pila import Pila
from src.excepciones.movimiento_invalido_error import MovimientoInvalidoError
from src.excepciones.nombre_duplicado_error import NombreDuplicadoError
from src.excepciones.ruta_invalida_error import RutaInvalidaError
from src.nucleo.archivo_codigo import ArchivoCodigo


class ArbolNario:
    """Implementación propia de un Árbol N-ario para gestionar el sistema de archivos en memoria.
    
    Soporta resolución de rutas absolutas y relativas (con '.' y '..'), creación de carpetas,
    inserción de archivos, movimiento de subárboles con validación anticiclos, eliminación
    y recorrido en preorden iterativo mediante una Pila LIFO explícita para evitar
    desbordamiento de pila (RecursionError) en jerarquías profundas.
    """

    def __init__(self) -> None:
        self._raiz: NodoNario = NodoNario("/", NodoNario.TIPO_CARPETA)

    @property
    def raiz(self) -> NodoNario:
        """Retorna el nodo raíz ('/') del árbol N-ario."""
        return self._raiz

    def resolver_ruta(
        self,
        ruta: str,
        directorio_base: Optional[NodoNario] = None,
    ) -> NodoNario:
        """Resuelve una ruta absoluta o relativa y retorna el NodoNario correspondiente.
        
        Soporta los segmentos especiales '.' (directorio actual) y '..' (directorio padre).
        Lanza RutaInvalidaError si algún segmento intermedio o final no existe.
        """
        ruta_limpia = ruta.strip()
        if not ruta_limpia:
            raise RutaInvalidaError("La ruta no puede estar vacía.")

        if ruta_limpia.startswith("/"):
            actual = self._raiz
        else:
            actual = directorio_base if directorio_base is not None else self._raiz

        segmentos = [seg for seg in ruta_limpia.split("/") if seg and seg != "."]

        for segmento in segmentos:
            if segmento == "..":
                if actual.padre is not None:
                    actual = actual.padre
                else:
                    actual = self._raiz
            else:
                if not actual.es_carpeta:
                    raise RutaInvalidaError(
                        f"Ruta inválida '{ruta}': '{actual.nombre}' es un archivo, no un directorio."
                    )
                hijo = actual.buscar_hijo(segmento)
                if hijo is None:
                    raise RutaInvalidaError(
                        f"No existe el archivo o directorio '{segmento}' en '{actual.obtener_ruta_absoluta()}'."
                    )
                actual = hijo

        return actual

    def _resolver_padre_y_nombre(
        self,
        ruta: str,
        directorio_base: Optional[NodoNario] = None,
    ) -> Tuple[NodoNario, str]:
        """Separa una ruta en (nodo_carpeta_padre, nombre_elemento_final)."""
        ruta_limpia = ruta.strip()
        if not ruta_limpia or ruta_limpia == "/":
            raise RutaInvalidaError(f"Ruta de destino inválida: '{ruta}'.")

        # Eliminar barra final si la ruta apuntaba a carpeta como "src/"
        if len(ruta_limpia) > 1 and ruta_limpia.endswith("/"):
            ruta_limpia = ruta_limpia.rstrip("/")

        if "/" not in ruta_limpia:
            padre = directorio_base if directorio_base is not None else self._raiz
            nombre_final = ruta_limpia
        else:
            partes = ruta_limpia.rsplit("/", 1)
            ruta_padre = partes[0] if partes[0] else "/"
            nombre_final = partes[1]
            padre = self.resolver_ruta(ruta_padre, directorio_base)

        if not nombre_final or nombre_final in (".", ".."):
            raise RutaInvalidaError(f"Nombre de elemento inválido: '{nombre_final}'.")

        if not padre.es_carpeta:
            raise RutaInvalidaError(
                f"El destino '{padre.obtener_ruta_absoluta()}' es un archivo y no puede contener hijos."
            )

        return padre, nombre_final

    def crear_carpeta(
        self,
        ruta: str,
        directorio_base: Optional[NodoNario] = None,
    ) -> NodoNario:
        """Crea una nueva carpeta en la ruta indicada y retorna su NodoNario."""
        padre, nombre = self._resolver_padre_y_nombre(ruta, directorio_base)
        nueva_carpeta = NodoNario(nombre, NodoNario.TIPO_CARPETA)
        padre.agregar_hijo(nueva_carpeta)
        return nueva_carpeta

    def agregar_archivo(
        self,
        ruta: str,
        archivo: ArchivoCodigo,
        directorio_base: Optional[NodoNario] = None,
    ) -> NodoNario:
        """Inserta un nodo de tipo ARCHIVO asociado a la instancia ArchivoCodigo provista."""
        padre, nombre = self._resolver_padre_y_nombre(ruta, directorio_base)
        archivo.nombre = nombre
        nodo_archivo = NodoNario(nombre, NodoNario.TIPO_ARCHIVO, archivo=archivo)
        padre.agregar_hijo(nodo_archivo)
        return nodo_archivo

    def mover(
        self,
        ruta_origen: str,
        ruta_destino: str,
        directorio_base: Optional[NodoNario] = None,
    ) -> NodoNario:
        """Mueve o renombra un archivo o carpeta hacia la ruta destino.
        
        Reglas:
        - No permite mover la raíz '/'.
        - No permite mover una carpeta dentro de sí misma ni de sus descendientes
          (lanza MovimientoInvalidoError).
        - No permite colisión de nombres entre hermanos (lanza NombreDuplicadoError).
        """
        nodo_origen = self.resolver_ruta(ruta_origen, directorio_base)
        if nodo_origen is self._raiz or nodo_origen.padre is None:
            raise MovimientoInvalidoError("No está permitido mover el directorio raíz '/'.")

        # Intentar verificar si el destino ya existe en el árbol
        nodo_destino_existente: Optional[NodoNario] = None
        try:
            nodo_destino_existente = self.resolver_ruta(ruta_destino, directorio_base)
        except RutaInvalidaError:
            nodo_destino_existente = None

        if nodo_destino_existente is not None:
            if nodo_destino_existente.es_carpeta:
                # Si se mueve hacia una carpeta existente, se ubica como hijo conservando su nombre
                if nodo_destino_existente is nodo_origen:
                    raise MovimientoInvalidoError(
                        f"No se puede mover la carpeta '{nodo_origen.nombre}' dentro de sí misma."
                    )
                nuevo_padre = nodo_destino_existente
                nuevo_nombre = nodo_origen.nombre
            else:
                raise NombreDuplicadoError(
                    f"El destino '{nodo_destino_existente.obtener_ruta_absoluta()}' ya existe y es un archivo."
                )
        else:
            nuevo_padre, nuevo_nombre = self._resolver_padre_y_nombre(ruta_destino, directorio_base)

        # Validación crítica anticiclos: una carpeta no puede moverse a sí misma ni a un descendiente
        if nodo_origen.es_carpeta and nodo_origen.es_ancestro_de(nuevo_padre):
            raise MovimientoInvalidoError(
                f"Movimiento inválido: no se puede mover '{nodo_origen.obtener_ruta_absoluta()}' "
                f"dentro de su propio subárbol '{nuevo_padre.obtener_ruta_absoluta()}'."
            )

        # Si es el mismo padre y mismo nombre, no hay cambios que realizar
        if nuevo_padre is nodo_origen.padre and nuevo_nombre == nodo_origen.nombre:
            return nodo_origen

        # Verificar que no exista otro hermano con el nuevo nombre en el destino
        if nuevo_padre.buscar_hijo(nuevo_nombre) is not None:
            raise NombreDuplicadoError(
                f"Ya existe un elemento llamado '{nuevo_nombre}' en '{nuevo_padre.obtener_ruta_absoluta()}'."
            )

        # Desenganchar del padre actual y enganchar en el nuevo padre
        padre_anterior = nodo_origen.padre
        padre_anterior.eliminar_hijo(nodo_origen.nombre)
        nodo_origen.nombre = nuevo_nombre
        nuevo_padre.agregar_hijo(nodo_origen)
        return nodo_origen

    def eliminar(
        self,
        ruta: str,
        directorio_base: Optional[NodoNario] = None,
    ) -> List[ArchivoCodigo]:
        """Elimina un nodo archivo o carpeta del árbol y retorna los ArchivoCodigo contenidos."""
        nodo = self.resolver_ruta(ruta, directorio_base)
        if nodo is self._raiz or nodo.padre is None:
            raise MovimientoInvalidoError("No se puede eliminar el directorio raíz '/'.")

        archivos_eliminados = self.obtener_archivos_en_subarbol(nodo)
        nodo.padre.eliminar_hijo(nodo.nombre)
        return archivos_eliminados

    def obtener_archivos_en_subarbol(self, nodo_raiz_subarbol: Optional[NodoNario] = None) -> List[ArchivoCodigo]:
        """Recorre en preorden iterativo el subárbol indicado y extrae todos sus ArchivoCodigo."""
        inicio = nodo_raiz_subarbol if nodo_raiz_subarbol is not None else self._raiz
        archivos: List[ArchivoCodigo] = []
        pila = Pila()
        pila.apilar(inicio)

        while not pila.esta_vacia():
            actual: NodoNario = pila.desapilar()
            if actual.es_archivo and actual.archivo is not None:
                archivos.append(actual.archivo)
            elif actual.es_carpeta:
                hijos = actual.listar_hijos()
                for idx in range(len(hijos) - 1, -1, -1):
                    pila.apilar(hijos[idx])

        return archivos

    def RecorridoPreordenTree(self, nodo_inicio: Optional[NodoNario] = None) -> List[str]:
        """Alias descriptivo del recorrido preorden para visualización estilo comando tree."""
        return self.generar_lineas_tree(nodo_inicio)

    def generar_lineas_tree(self, nodo_inicio: Optional[NodoNario] = None) -> List[str]:
        """Genera las líneas visuales estilo Linux 'tree' (├──, └──, │) en preorden iterativo.
        
        Utiliza una Pila LIFO explícita propia (sin recursión del intérprete) para soportar
        árboles de profundidad arbitraria sin riesgo de RecursionError.
        """
        origen = nodo_inicio if nodo_inicio is not None else self._raiz
        etiqueta_raiz = "/" if origen is self._raiz else (f"{origen.nombre}/" if origen.es_carpeta else origen.nombre)
        lineas: List[str] = [etiqueta_raiz]

        if not origen.es_carpeta:
            return lineas

        pila = Pila()
        hijos_raiz = origen.listar_hijos()
        total_raiz = len(hijos_raiz)
        for i in range(total_raiz - 1, -1, -1):
            es_ultimo = (i == total_raiz - 1)
            pila.apilar((hijos_raiz[i], "", es_ultimo))

        while not pila.esta_vacia():
            nodo_actual, prefijo, es_ultimo = pila.desapilar()
            conector = "└── " if es_ultimo else "├── "
            sufijo = "/" if nodo_actual.es_carpeta else ""
            lineas.append(f"{prefijo}{conector}{nodo_actual.nombre}{sufijo}")

            if nodo_actual.es_carpeta:
                hijos = nodo_actual.listar_hijos()
                total_hijos = len(hijos)
                nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
                for i in range(total_hijos - 1, -1, -1):
                    hijo_es_ultimo = (i == total_hijos - 1)
                    pila.apilar((hijos[i], nuevo_prefijo, hijo_es_ultimo))

        return lineas

    def buscar_nodo_por_id_archivo(self, id_archivo: str) -> Optional[NodoNario]:
        """Busca mediante recorrido preorden iterativo el NodoNario que contiene el archivo con id_archivo."""
        pila = Pila()
        pila.apilar(self._raiz)

        while not pila.esta_vacia():
            actual: NodoNario = pila.desapilar()
            if actual.es_archivo and actual.archivo is not None and actual.archivo.id_archivo == id_archivo:
                return actual
            if actual.es_carpeta:
                hijos = actual.listar_hijos()
                for i in range(len(hijos) - 1, -1, -1):
                    pila.apilar(hijos[i])

        return None

    def buscar_nodos_por_nombre(self, nombre: str, solo_archivos: bool = False) -> List[NodoNario]:
        """Busca todos los nodos en el árbol cuyo nombre coincida con el solicitado."""
        coincidencias: List[NodoNario] = []
        pila = Pila()
        pila.apilar(self._raiz)

        while not pila.esta_vacia():
            actual: NodoNario = pila.desapilar()
            if actual is not self._raiz and actual.nombre == nombre:
                if not solo_archivos or actual.es_archivo:
                    coincidencias.append(actual)
            if actual.es_carpeta:
                hijos = actual.listar_hijos()
                for i in range(len(hijos) - 1, -1, -1):
                    pila.apilar(hijos[i])

        return coincidencias

    def listar_todos_los_archivos(self) -> List[Tuple[str, ArchivoCodigo]]:
        """Retorna una lista de tuplas (ruta_absoluta, ArchivoCodigo) en preorden iterativo."""
        resultado: List[Tuple[str, ArchivoCodigo]] = []
        pila = Pila()
        pila.apilar(self._raiz)

        while not pila.esta_vacia():
            actual: NodoNario = pila.desapilar()
            if actual.es_archivo and actual.archivo is not None:
                resultado.append((actual.obtener_ruta_absoluta(), actual.archivo))
            elif actual.es_carpeta:
                hijos = actual.listar_hijos()
                for i in range(len(hijos) - 1, -1, -1):
                    pila.apilar(hijos[i])

        return resultado

