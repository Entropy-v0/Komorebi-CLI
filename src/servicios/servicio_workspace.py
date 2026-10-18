"""Módulo del servicio que orquesta el Árbol N-ario del Workspace y su sincronía en disco."""

import os
import shutil
from typing import Any, List, Optional
from src.estructuras.arbol_nario import ArbolNario
from src.estructuras.nodo_nario import NodoNario
from src.excepciones.ruta_invalida_error import RutaInvalidaError
from src.nucleo.archivo_codigo import ArchivoCodigo
from src.nucleo.contexto_app import ContextoApp


class ServicioWorkspace:
    """Orquesta el Árbol N-ario de directorios y archivos en coordinación con ContextoApp y disco.
    
    Garantiza que:
    - El Árbol N-ario sea la fuente de verdad de la jerarquía de rutas.
    - La ListaEnlazada de ContextoApp y los nodos ARCHIVO del árbol compartan exactamente
      la misma referencia de objeto ArchivoCodigo (sin copias duplicadas).
    - Las carpetas y archivos respaldados en `respaldos/` reflejen fielmente la jerarquía
      del árbol ante creaciones, movimientos (`mv`) y eliminaciones (`delete`).
    """

    def __init__(
        self,
        contexto: ContextoApp,
        servicio_archivos: Optional[Any] = None,
        servicio_logs: Optional[Any] = None,
    ) -> None:
        self._contexto: ContextoApp = contexto
        self._servicio_archivos: Optional[Any] = servicio_archivos
        self._servicio_logs: Optional[Any] = servicio_logs

        if not isinstance(self._contexto.workspace, ArbolNario):
            self._contexto.workspace = ArbolNario()
        if not isinstance(self._contexto.directorio_actual, NodoNario):
            self._contexto.directorio_actual = self._contexto.workspace.raiz

    @property
    def arbol(self) -> ArbolNario:
        """Retorna la instancia del Árbol N-ario del workspace."""
        if not isinstance(self._contexto.workspace, ArbolNario):
            self._contexto.workspace = ArbolNario()
            self._contexto.directorio_actual = self._contexto.workspace.raiz
        return self._contexto.workspace

    @property
    def nodo_directorio_actual(self) -> NodoNario:
        """Retorna el NodoNario correspondiente al directorio de trabajo actual."""
        if not isinstance(self._contexto.directorio_actual, NodoNario):
            self._contexto.directorio_actual = self.arbol.raiz
        return self._contexto.directorio_actual

    def obtener_directorio_actual(self) -> str:
        """Retorna la ruta absoluta textual del directorio actual (para el comando 'pwd')."""
        return self.nodo_directorio_actual.obtener_ruta_absoluta()

    def crear_carpeta(self, ruta: str) -> NodoNario:
        """Crea un directorio en el Árbol N-ario y su carpeta equivalente en respaldos."""
        nodo_carpeta = self.arbol.crear_carpeta(ruta, self.nodo_directorio_actual)
        ruta_fisica = self._obtener_ruta_fisica(nodo_carpeta.obtener_ruta_absoluta())
        try:
            os.makedirs(ruta_fisica, exist_ok=True)
            if self._servicio_logs:
                self._servicio_logs.registrar_info(
                    "ServicioWorkspace", f"Carpeta creada: '{nodo_carpeta.obtener_ruta_absoluta()}'"
                )
        except OSError:
            pass
        return nodo_carpeta

    def cambiar_directorio(self, ruta: str = "/") -> NodoNario:
        """Cambia el directorio de trabajo actual resolviendo rutas absolutas, relativas, '.' y '..'."""
        ruta_objetivo = ruta.strip() if ruta and ruta.strip() else "/"
        nodo_destino = self.arbol.resolver_ruta(ruta_objetivo, self.nodo_directorio_actual)
        if not nodo_destino.es_carpeta:
            raise RutaInvalidaError(
                f"No es un directorio: '{nodo_destino.obtener_ruta_absoluta()}' es un archivo."
            )
        self._contexto.directorio_actual = nodo_destino
        return nodo_destino

    def listar_directorio(self, ruta: Optional[str] = None) -> List[NodoNario]:
        """Retorna los nodos hijos directos de la carpeta actual o de la ruta indicada."""
        if ruta and ruta.strip():
            nodo = self.arbol.resolver_ruta(ruta.strip(), self.nodo_directorio_actual)
        else:
            nodo = self.nodo_directorio_actual

        if nodo.es_archivo:
            return [nodo]
        return nodo.listar_hijos()

    def mostrar_arbol(self, ruta: Optional[str] = None) -> List[str]:
        """Genera las líneas del comando 'tree' a partir del directorio actual o de la ruta indicada."""
        if ruta and ruta.strip():
            nodo_inicio = self.arbol.resolver_ruta(ruta.strip(), self.nodo_directorio_actual)
        else:
            nodo_inicio = self.nodo_directorio_actual
        return self.arbol.generar_lineas_tree(nodo_inicio)

    def mover(self, ruta_origen: str, ruta_destino: str) -> NodoNario:
        """Mueve o renombra un archivo o carpeta en el árbol N-ario y sincroniza el respaldo físico."""
        nodo_origen = self.arbol.resolver_ruta(ruta_origen, self.nodo_directorio_actual)
        ruta_abs_antes = nodo_origen.obtener_ruta_absoluta()
        ruta_fisica_antes = self._obtener_ruta_fisica(ruta_abs_antes)

        nodo_movido = self.arbol.mover(ruta_origen, ruta_destino, self.nodo_directorio_actual)
        ruta_abs_despues = nodo_movido.obtener_ruta_absoluta()
        ruta_fisica_despues = self._obtener_ruta_fisica(ruta_abs_despues)

        if ruta_fisica_antes != ruta_fisica_despues:
            self._mover_respaldo_fisico(ruta_fisica_antes, ruta_fisica_despues, nodo_movido)

        if self._servicio_logs:
            self._servicio_logs.registrar_info(
                "ServicioWorkspace", f"Movido '{ruta_abs_antes}' -> '{ruta_abs_despues}'"
            )
        return nodo_movido

    def eliminar(self, ruta: str) -> List[ArchivoCodigo]:
        """Elimina un archivo o carpeta del árbol N-ario, de la ListaEnlazada y del disco de respaldos."""
        nodo = self.arbol.resolver_ruta(ruta, self.nodo_directorio_actual)
        ruta_abs = nodo.obtener_ruta_absoluta()
        ruta_fisica = self._obtener_ruta_fisica(ruta_abs)

        # Si el directorio actual estaba dentro de la carpeta que se va a eliminar, subir al padre
        if nodo.es_carpeta and nodo.es_ancestro_de(self.nodo_directorio_actual):
            self._contexto.directorio_actual = nodo.padre if nodo.padre is not None else self.arbol.raiz

        archivos_eliminados = self.arbol.eliminar(ruta, self.nodo_directorio_actual)
        for arc in archivos_eliminados:
            self._contexto.cerrar_archivo_por_id(arc.id_archivo)

        self._eliminar_respaldo_fisico(ruta_fisica)
        return archivos_eliminados

    def _obtener_ruta_fisica(self, ruta_absoluta_workspace: str) -> str:
        """Convierte una ruta del workspace (ej. '/src/app.py') en ruta dentro de respaldos/."""
        base_respaldos = self._contexto.configuracion.ruta_respaldos
        relativa = ruta_absoluta_workspace.lstrip("/")
        if not relativa:
            return base_respaldos
        return os.path.join(base_respaldos, *relativa.split("/"))

    def _mover_respaldo_fisico(
        self,
        origen_fisico: str,
        destino_fisico: str,
        nodo_movido: NodoNario,
    ) -> None:
        """Sincroniza el movimiento físico en el directorio de respaldos."""
        try:
            os.makedirs(os.path.dirname(destino_fisico), exist_ok=True)
            if os.path.exists(origen_fisico):
                if os.path.isdir(destino_fisico) and os.path.isdir(origen_fisico):
                    shutil.rmtree(destino_fisico, ignore_errors=True)
                shutil.move(origen_fisico, destino_fisico)
            elif nodo_movido.es_archivo and nodo_movido.archivo is not None:
                with open(destino_fisico, "w", encoding="utf-8") as f:
                    f.write(nodo_movido.archivo.contenido)
            elif nodo_movido.es_carpeta:
                os.makedirs(destino_fisico, exist_ok=True)
        except OSError:
            pass

    def _eliminar_respaldo_fisico(self, ruta_fisica: str) -> None:
        """Elimina del disco el respaldo físico asociado al nodo eliminado."""
        try:
            if os.path.isfile(ruta_fisica):
                os.remove(ruta_fisica)
            elif os.path.isdir(ruta_fisica):
                shutil.rmtree(ruta_fisica, ignore_errors=True)
        except OSError:
            pass

