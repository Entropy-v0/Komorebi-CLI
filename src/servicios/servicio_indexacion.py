"""Módulo del servicio de indexación global de tokens sobre Árbol B (orden m=4)."""

from typing import Optional
from src.estructuras.arbol_b import ArbolB
from src.estructuras.nodo_nario import NodoNario
from src.estructuras.pila import Pila
from src.nucleo.archivo_codigo import ArchivoCodigo
from src.nucleo.contexto_app import ContextoApp
from src.nucleo.referencia_token import ReferenciaToken
from src.servicios.servicio_logs import ServicioLogs


class ServicioIndexacion:
    """Gestiona la extracción léxica de identificadores y su indexación en un Árbol B.

    Utiliza un tokenizador propio carácter por carácter (sin `re` ni `ast`) que:
    - Ignora comentarios (`# ...`) y contenido literal entre comillas simples o dobles.
    - Extrae identificadores válidos (`[a-zA-Z_][a-zA-Z0-9_]*`).
    - Consulta el `ArbolAVL` en `ContextoApp.diccionario` en O(log n) para descartar
      todas las palabras reservadas del lenguaje.
    - Almacena cada ocurrencia como `ReferenciaToken(archivo_id, linea)` en el `ArbolB`
      alojado en `ContextoApp.indice_global`.
    """

    def __init__(
        self,
        contexto: ContextoApp,
        servicio_logs: Optional[ServicioLogs] = None,
        orden_arbol_b: int = 4,
    ) -> None:
        """Inicializa el servicio de indexación y vincula el `ArbolB` al contexto."""
        self._contexto: ContextoApp = contexto
        self._servicio_logs: Optional[ServicioLogs] = servicio_logs
        self._orden_arbol_b: int = orden_arbol_b

        if self._contexto.indice_global is None:
            self._contexto.indice_global = ArbolB(orden=orden_arbol_b)

    @property
    def indice(self) -> ArbolB:
        """Retorna el `ArbolB` activo en el contexto global."""
        if self._contexto.indice_global is None:
            self._contexto.indice_global = ArbolB(orden=self._orden_arbol_b)
        return self._contexto.indice_global

    # =========================================================================
    # Tokenizador Léxico Propio de Identificadores
    # =========================================================================

    def extraer_tokens_linea(self, linea: str) -> list[str]:
        """Extrae identificadores de código de una línea filtrando keywords del AVL.

        Ignora cadenas literales (`'...'`, `"..."`) y comentarios (`#...`).
        Reconoce nombres de funciones (`def nombre`), parámetros, variables asignadas
        (`nombre = ...`) y referencias a identificadores en expresiones.

        Args:
            linea: Línea de código fuente a analizar.

        Returns:
            Lista de identificadores no reservados encontrados en la línea (sin duplicar
            el mismo token dentro de la misma línea).
        """
        tokens_en_linea: list[str] = []
        n = len(linea)
        i = 0
        en_comilla_simple = False
        en_comilla_doble = False

        while i < n:
            ch = linea[i]

            # Manejo de secuencias de escape dentro de literales de texto
            if (en_comilla_simple or en_comilla_doble) and ch == "\\":
                i += 2
                continue

            if ch == "'" and not en_comilla_doble:
                en_comilla_simple = not en_comilla_simple
                i += 1
                continue

            if ch == '"' and not en_comilla_simple:
                en_comilla_doble = not en_comilla_doble
                i += 1
                continue

            # Ignorar contenido dentro de comillas
            if en_comilla_simple or en_comilla_doble:
                i += 1
                continue

            # Comentario de fin de línea
            if ch == "#":
                break

            # Inicio de identificador: letra o guion bajo
            if ch.isalpha() or ch == "_":
                inicio = i
                i += 1
                while i < n and (linea[i].isalnum() or linea[i] == "_"):
                    i += 1
                identificador = linea[inicio:i]

                if not self._es_palabra_reservada(identificador):
                    if identificador not in tokens_en_linea:
                        tokens_en_linea.append(identificador)
                continue

            i += 1

        return tokens_en_linea

    def _es_palabra_reservada(self, token: str) -> bool:
        """Consulta el Árbol AVL del diccionario para descartar palabras reservadas."""
        diccionario = self._contexto.diccionario
        if diccionario is not None:
            return diccionario.contiene(token)
        return False

    # =========================================================================
    # Indexación del Workspace y Sincronización Incremental
    # =========================================================================

    def indexar_todo(self) -> tuple[int, int]:
        """Reconstruye el índice global B-Tree recorriendo todos los archivos del Workspace.

        Limpia el `ArbolB` antes de reindexar para garantizar que ejecuciones repetidas
        de `index-all` jamás dupliquen referencias ni conserven tokens obsoletos.

        Returns:
            Tupla `(archivos_indexados, tokens_unicos_indexados)`.
        """
        self.indice.limpiar()
        archivos = self._recolectar_archivos_workspace()

        for archivo in archivos:
            self._indexar_lineas_archivo(archivo)

        if self._servicio_logs is not None:
            self._servicio_logs.registrar_info(
                "ServicioIndexacion",
                f"Índice B-Tree reconstruido: {len(archivos)} archivo(s), "
                f"{self.indice.tamanio} token(s) único(s).",
            )
        return len(archivos), self.indice.tamanio

    def reindexar_archivo(self, archivo: ArchivoCodigo) -> None:
        """Actualiza de forma coherente las entradas de `archivo` en el Árbol B."""
        if self._contexto.indice_global is None or self.indice.esta_vacio():
            return
        self.indice.eliminar_referencias_archivo(archivo.id_archivo)
        self._indexar_lineas_archivo(archivo)

    def desindexar_archivo(self, archivo_id: str) -> None:
        """Elimina todas las referencias de un archivo borrado en el Árbol B."""
        if self._contexto.indice_global is None or self.indice.esta_vacio():
            return
        self.indice.eliminar_referencias_archivo(archivo_id)

    def _indexar_lineas_archivo(self, archivo: ArchivoCodigo) -> None:
        """Extrae e inserta en el Árbol B todos los tokens de un `ArchivoCodigo`."""
        for num_linea, texto_linea in enumerate(archivo.obtener_lineas(), start=1):
            tokens = self.extraer_tokens_linea(texto_linea)
            for token in tokens:
                ref = ReferenciaToken(archivo_id=archivo.id_archivo, linea=num_linea)
                self.indice.insertar(token, ref)

    def _recolectar_archivos_workspace(self) -> list[ArchivoCodigo]:
        """Recorre el Árbol N-ario del Workspace (y la lista abierta) sin duplicar IDs."""
        archivos: list[ArchivoCodigo] = []
        ids_vistos: list[str] = []

        workspace = self._contexto.workspace
        if workspace is not None:
            pila: Pila[NodoNario] = Pila()
            pila.apilar(workspace.raiz)
            while not pila.esta_vacia():
                nodo = pila.desapilar()
                if nodo.es_archivo and nodo.archivo is not None:
                    arc = nodo.archivo
                    if arc.id_archivo not in ids_vistos:
                        ids_vistos.append(arc.id_archivo)
                        archivos.append(arc)
                else:
                    hijos = nodo.listar_hijos()
                    for idx in range(len(hijos) - 1, -1, -1):
                        pila.apilar(hijos[idx])

        # Incluir cualquier archivo en la lista enlazada de sesión no presente aún
        for arc in self._contexto.listar_archivos():
            if arc.id_archivo not in ids_vistos:
                ids_vistos.append(arc.id_archivo)
                archivos.append(arc)

        return archivos

    # =========================================================================
    # Búsqueda Global y Resolución de Rutas en el Workspace
    # =========================================================================

    def buscar_global(self, token: str) -> list[tuple[str, list[int]]]:
        """Busca un token en el Árbol B y agrupa sus ocurrencias por ruta del Workspace.

        Args:
            token: Identificador a buscar.

        Returns:
            Lista ordenada de tuplas `(ruta_workspace, [lineas_ordenadas])`.
        """
        referencias = self.indice.buscar(token)
        if not referencias:
            return []

        agrupado_por_ruta: dict[str, list[int]] = {}
        rutas_ordenadas: list[str] = []

        for ref in referencias:
            ruta = self._resolver_ruta_archivo_por_id(ref.archivo_id)
            if ruta is None:
                continue
            if ruta not in agrupado_por_ruta:
                agrupado_por_ruta[ruta] = []
                self._insertar_cadena_ordenada(rutas_ordenadas, ruta)
            self._insertar_entero_ordenado(agrupado_por_ruta[ruta], ref.linea)

        return [(ruta, agrupado_por_ruta[ruta]) for ruta in rutas_ordenadas]

    def formatear_busqueda_global(self, token: str) -> str:
        """Formatea el resultado de `find-global <token>` para la interfaz CLI."""
        token_limpio = token.strip()
        resultados = self.buscar_global(token_limpio)
        if not resultados:
            return (
                f"[Índice B-Tree] El token '{token_limpio}' no fue encontrado en el índice global."
            )

        total_apariciones = sum(len(lineas) for _, lineas in resultados)
        salida = [
            f"--- Resultados Globales B-Tree para '{token_limpio}' "
            f"({total_apariciones} aparición(es) en {len(resultados)} archivo(s)) ---"
        ]
        for ruta, lineas in resultados:
            lineas_str = ", ".join(str(num) for num in lineas)
            salida.append(f"  {ruta:<30} -> Línea(s): {lineas_str}")
        salida.append("-" * len(salida[0]))
        return "\n".join(salida)

    def _resolver_ruta_archivo_por_id(self, archivo_id: str) -> Optional[str]:
        """Resuelve la ruta absoluta en el Workspace para un `archivo_id` dado."""
        workspace = self._contexto.workspace
        if workspace is not None:
            nodo = workspace.buscar_nodo_por_id_archivo(archivo_id)
            if nodo is not None:
                return nodo.obtener_ruta_absoluta()

        archivo = self._contexto.buscar_archivo_por_id(archivo_id)
        if archivo is not None:
            return f"/{archivo.nombre}"
        return None

    def _insertar_cadena_ordenada(self, lista: list[str], valor: str) -> None:
        pos = 0
        n = len(lista)
        while pos < n and lista[pos] < valor:
            pos += 1
        lista.insert(pos, valor)

    def _insertar_entero_ordenado(self, lista: list[int], valor: int) -> None:
        pos = 0
        n = len(lista)
        while pos < n:
            if lista[pos] == valor:
                return
            if lista[pos] > valor:
                break
            pos += 1
        lista.insert(pos, valor)
