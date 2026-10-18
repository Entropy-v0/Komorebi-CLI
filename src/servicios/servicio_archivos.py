"""Módulo del servicio encargado de la gestión de archivos de código y respaldos en disco."""

import os
import shutil
from typing import Any, List, Optional, Tuple
from src.estructuras.arbol_nario import ArbolNario
from src.estructuras.nodo_nario import NodoNario
from src.excepciones.nombre_duplicado_error import NombreDuplicadoError
from src.excepciones.ruta_invalida_error import RutaInvalidaError
from src.nucleo.archivo_codigo import ArchivoCodigo
from src.nucleo.contexto_app import ContextoApp


class ServicioArchivos:
    """Orquesta las operaciones sobre los archivos abiertos en memoria y su persistencia en disco.
    
    Coordina la ListaEnlazada de archivos abiertos del ContextoApp con el Árbol N-ario
    del Workspace (cuando está activo) garantizando que ambos apunten al mismo objeto
    ArchivoCodigo y que los respaldos físicos reflejen la jerarquía de directorios.
    """

    def __init__(
        self,
        contexto: ContextoApp,
        servicio_logs: Optional[Any] = None,
        servicio_indexacion: Optional[Any] = None,
    ) -> None:
        self._contexto: ContextoApp = contexto
        self._servicio_logs: Optional[Any] = servicio_logs
        self._servicio_indexacion: Optional[Any] = servicio_indexacion

    @property
    def servicio_indexacion(self) -> Optional[Any]:
        """Retorna el servicio de indexación vinculado, si existe."""
        return self._servicio_indexacion

    @servicio_indexacion.setter
    def servicio_indexacion(self, servicio: Optional[Any]) -> None:
        """Vincula el servicio de indexación para refresco automático tras ediciones."""
        self._servicio_indexacion = servicio

    def crear_archivo(self, nombre: str, contenido_inicial: str = "") -> ArchivoCodigo:
        """Crea un nuevo archivo en el directorio actual (o ruta), lo añade a la lista y respalda en disco.
        
        Lanza NombreDuplicadoError si ya existe un archivo con el mismo nombre en el mismo directorio.
        """
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            raise ValueError("El nombre del archivo no puede estar vacío.")

        if isinstance(self._contexto.workspace, ArbolNario):
            arbol = self._contexto.workspace
            dir_base = (
                self._contexto.directorio_actual
                if isinstance(self._contexto.directorio_actual, NodoNario)
                else arbol.raiz
            )
            padre, nombre_hoja = arbol._resolver_padre_y_nombre(nombre_limpio, dir_base)
            if padre.buscar_hijo(nombre_hoja) is not None:
                raise NombreDuplicadoError(
                    f"Ya existe un archivo o carpeta con el nombre '{nombre_hoja}' en '{padre.obtener_ruta_absoluta()}'."
                )

            nuevo_archivo = ArchivoCodigo(nombre_hoja, contenido_inicial)
            arbol.agregar_archivo(nombre_limpio, nuevo_archivo, dir_base)
            self._contexto.abrir_archivo(nuevo_archivo)
            self.guardar_respaldo(nuevo_archivo)
            return nuevo_archivo

        if self._contexto.buscar_archivo(nombre_limpio) is not None:
            raise NombreDuplicadoError(f"Ya existe un archivo abierto con el nombre '{nombre_limpio}'.")

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
        """Cambia el archivo activo buscando por índice (1-based), nombre o ruta del workspace.
        
        Si existen múltiples archivos con el mismo nombre en distintas carpetas y solo se
        provee el nombre, lanza RutaInvalidaError pidiendo especificar la ruta.
        """
        id_limpio = identificador.strip()
        if not id_limpio:
            return False

        # 1. Cambio por índice numérico (1-based)
        if id_limpio.isdigit():
            indice_0_based = int(id_limpio) - 1
            if 0 <= indice_0_based < len(self._contexto.archivos_abiertos):
                archivo = self._contexto.archivos_abiertos.obtener_por_indice(indice_0_based)
                if isinstance(archivo, ArchivoCodigo):
                    self._contexto.archivo_activo = archivo
                    return True

        # 2. Resolución con Árbol N-ario si está activo
        if isinstance(self._contexto.workspace, ArbolNario):
            arbol = self._contexto.workspace
            dir_base = (
                self._contexto.directorio_actual
                if isinstance(self._contexto.directorio_actual, NodoNario)
                else arbol.raiz
            )

            if "/" in id_limpio:
                nodo = arbol.resolver_ruta(id_limpio, dir_base)
                if not nodo.es_archivo or nodo.archivo is None:
                    raise RutaInvalidaError(
                        f"La ruta '{id_limpio}' es un directorio, no un archivo seleccionable."
                    )
                self._contexto.archivo_activo = nodo.archivo
                return True

            coincidencias = arbol.buscar_nodos_por_nombre(id_limpio, solo_archivos=True)
            if len(coincidencias) > 1:
                rutas = ", ".join(n.obtener_ruta_absoluta() for n in coincidencias)
                raise RutaInvalidaError(
                    f"Ambigüedad: existen varios archivos llamados '{id_limpio}'. Especifica la ruta ({rutas})."
                )
            if len(coincidencias) == 1 and coincidencias[0].archivo is not None:
                self._contexto.archivo_activo = coincidencias[0].archivo
                return True
            return False

        # 3. Modo plano sin workspace
        coincidencias_planas = self._contexto.buscar_archivos_por_nombre(id_limpio)
        if len(coincidencias_planas) > 1:
            raise RutaInvalidaError(
                f"Ambigüedad: existen múltiples archivos con el nombre '{id_limpio}'. Especifica la ruta."
            )
        return self._contexto.cambiar_archivo_activo(id_limpio)

    def cerrar_archivo(self, identificador: str) -> bool:
        """Cierra y desengancha un archivo tanto del Árbol N-ario como de la ListaEnlazada."""
        id_limpio = identificador.strip()
        if not id_limpio:
            return False

        # 1. Eliminación por índice numérico (1-based)
        if id_limpio.isdigit():
            indice_0_based = int(id_limpio) - 1
            if 0 <= indice_0_based < len(self._contexto.archivos_abiertos):
                archivo = self._contexto.archivos_abiertos.obtener_por_indice(indice_0_based)
                if isinstance(archivo, ArchivoCodigo):
                    if isinstance(self._contexto.workspace, ArbolNario):
                        nodo = self._contexto.workspace.buscar_nodo_por_id_archivo(archivo.id_archivo)
                        if nodo is not None and nodo.padre is not None:
                            ruta_rel = nodo.obtener_ruta_absoluta().lstrip("/")
                            nodo.padre.eliminar_hijo(nodo.nombre)
                            self._eliminar_respaldo_relativo(ruta_rel)
                    return self._contexto.cerrar_archivo_por_id(archivo.id_archivo)

        # 2. Eliminación coordinada con Árbol N-ario
        if isinstance(self._contexto.workspace, ArbolNario):
            arbol = self._contexto.workspace
            dir_base = (
                self._contexto.directorio_actual
                if isinstance(self._contexto.directorio_actual, NodoNario)
                else arbol.raiz
            )

            if "/" in id_limpio:
                nodo = arbol.resolver_ruta(id_limpio, dir_base)
                ruta_rel = nodo.obtener_ruta_absoluta().lstrip("/")
                if nodo.es_carpeta and nodo.es_ancestro_de(dir_base):
                    self._contexto.directorio_actual = nodo.padre if nodo.padre is not None else arbol.raiz
                archivos_eliminados = arbol.eliminar(id_limpio, dir_base)
                for arc in archivos_eliminados:
                    self._contexto.cerrar_archivo_por_id(arc.id_archivo)
                self._eliminar_respaldo_relativo(ruta_rel)
                return True

            # Si no tiene '/', verificar primero si es archivo(s) por nombre
            coincidencias_arch = arbol.buscar_nodos_por_nombre(id_limpio, solo_archivos=True)
            if len(coincidencias_arch) > 1:
                rutas = ", ".join(n.obtener_ruta_absoluta() for n in coincidencias_arch)
                raise RutaInvalidaError(
                    f"Ambigüedad: existen varios archivos llamados '{id_limpio}'. Especifica la ruta ({rutas})."
                )
            if len(coincidencias_arch) == 1:
                nodo_unico = coincidencias_arch[0]
                ruta_rel = nodo_unico.obtener_ruta_absoluta().lstrip("/")
                if nodo_unico.padre is not None:
                    nodo_unico.padre.eliminar_hijo(nodo_unico.nombre)
                if nodo_unico.archivo is not None:
                    self._contexto.cerrar_archivo_por_id(nodo_unico.archivo.id_archivo)
                self._eliminar_respaldo_relativo(ruta_rel)
                return True

            # Verificar si es una carpeta hija en el directorio actual
            hijo_local = dir_base.buscar_hijo(id_limpio)
            if hijo_local is not None:
                ruta_rel = hijo_local.obtener_ruta_absoluta().lstrip("/")
                archivos_eliminados = arbol.eliminar(id_limpio, dir_base)
                for arc in archivos_eliminados:
                    self._contexto.cerrar_archivo_por_id(arc.id_archivo)
                self._eliminar_respaldo_relativo(ruta_rel)
                return True

            return False

        return self._contexto.cerrar_archivo(id_limpio)

    def obtener_archivo_activo(self) -> Optional[ArchivoCodigo]:
        """Retorna la referencia al archivo actualmente seleccionado para edición."""
        return self._contexto.archivo_activo

    def obtener_ruta_archivo(self, archivo: ArchivoCodigo) -> str:
        """Retorna la ruta absoluta en el workspace para el archivo dado, o su nombre si no hay árbol."""
        if isinstance(self._contexto.workspace, ArbolNario):
            nodo = self._contexto.workspace.buscar_nodo_por_id_archivo(archivo.id_archivo)
            if nodo is not None:
                return nodo.obtener_ruta_absoluta()
        return archivo.nombre

    def listar_archivos(self, filtro: Optional[str] = None) -> List[Tuple[int, ArchivoCodigo, bool]]:
        """Retorna una lista de tuplas (posicion_1_based, archivo, es_activo) de los archivos abiertos.
        
        Si se especifica `filtro` (nombre o ruta), filtra las coincidencias o lanza
        RutaInvalidaError si el nombre es ambiguo entre varios directorios.
        """
        resultado_completo: List[Tuple[int, ArchivoCodigo, bool]] = []
        activo = self._contexto.archivo_activo

        indice = 1
        for item in self._contexto.archivos_abiertos:
            if isinstance(item, ArchivoCodigo):
                es_activo = (activo is not None and item.id_archivo == activo.id_archivo)
                resultado_completo.append((indice, item, es_activo))
                indice += 1

        if not filtro or not filtro.strip():
            return resultado_completo

        filtro_limpio = filtro.strip()
        if isinstance(self._contexto.workspace, ArbolNario):
            arbol = self._contexto.workspace
            dir_base = (
                self._contexto.directorio_actual
                if isinstance(self._contexto.directorio_actual, NodoNario)
                else arbol.raiz
            )

            if "/" not in filtro_limpio:
                coincidencias = arbol.buscar_nodos_por_nombre(filtro_limpio, solo_archivos=True)
                if len(coincidencias) > 1:
                    rutas = ", ".join(n.obtener_ruta_absoluta() for n in coincidencias)
                    raise RutaInvalidaError(
                        f"Ambigüedad: existen varios archivos llamados '{filtro_limpio}'. Especifica la ruta ({rutas})."
                    )
                if len(coincidencias) == 1 and coincidencias[0].archivo is not None:
                    id_obj = coincidencias[0].archivo.id_archivo
                    return [t for t in resultado_completo if t[1].id_archivo == id_obj]

            nodo_filtro = arbol.resolver_ruta(filtro_limpio, dir_base)
            archivos_sub = arbol.obtener_archivos_en_subarbol(nodo_filtro)
            ids_validos = {a.id_archivo for a in archivos_sub}
            return [t for t in resultado_completo if t[1].id_archivo in ids_validos]

        # Sin workspace activo, filtrar por nombre
        filtrados = [t for t in resultado_completo if t[1].nombre == filtro_limpio]
        if len(filtrados) > 1:
            raise RutaInvalidaError(
                f"Ambigüedad: existen varios archivos llamados '{filtro_limpio}'. Especifica la ruta."
            )
        if not filtrados:
            raise RutaInvalidaError(f"No se encontró ningún archivo con el nombre '{filtro_limpio}'.")
        return filtrados

    def guardar_respaldo(self, archivo: Optional[ArchivoCodigo] = None) -> Optional[str]:
        """Escribe una copia física del archivo en el directorio de respaldos reflejando su jerarquía."""
        objetivo = archivo or self._contexto.archivo_activo
        if objetivo is None:
            return None

        if self._servicio_indexacion is not None:
            self._servicio_indexacion.reindexar_archivo(objetivo)

        directorio_respaldo = self._contexto.configuracion.ruta_respaldos
        if not os.path.exists(directorio_respaldo):
            os.makedirs(directorio_respaldo, exist_ok=True)

        ruta_relativa = objetivo.nombre
        if isinstance(self._contexto.workspace, ArbolNario):
            nodo = self._contexto.workspace.buscar_nodo_por_id_archivo(objetivo.id_archivo)
            if nodo is not None:
                ruta_relativa = nodo.obtener_ruta_absoluta().lstrip("/")

        partes_ruta = [p for p in ruta_relativa.split("/") if p]
        ruta_destino = os.path.join(directorio_respaldo, *partes_ruta) if partes_ruta else os.path.join(directorio_respaldo, objetivo.nombre)
        try:
            os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
            with open(ruta_destino, "w", encoding="utf-8") as f:
                f.write(objetivo.contenido)
            if self._servicio_logs:
                self._servicio_logs.registrar_info("ServicioArchivos", f"Respaldo generado exitosamente: '{ruta_destino}'")
            return ruta_destino
        except OSError as e:
            if self._servicio_logs:
                self._servicio_logs.registrar_error("ServicioArchivos", f"Error al generar respaldo de '{objetivo.nombre}': {str(e)}")
            return None

    def _eliminar_respaldo_relativo(self, ruta_relativa: str) -> None:
        """Elimina del disco el respaldo físico asociado a una ruta relativa del workspace."""
        if not ruta_relativa:
            return
        directorio_respaldo = self._contexto.configuracion.ruta_respaldos
        ruta_fisica = os.path.join(directorio_respaldo, *ruta_relativa.split("/"))
        try:
            if os.path.isfile(ruta_fisica):
                os.remove(ruta_fisica)
            elif os.path.isdir(ruta_fisica):
                shutil.rmtree(ruta_fisica, ignore_errors=True)
        except OSError:
            pass
