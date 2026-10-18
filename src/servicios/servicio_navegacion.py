"""Módulo del servicio de navegación híbrida: sistema de archivos real del SO y Workspace virtual."""

import os
from typing import List, Optional, Tuple
from src.excepciones.ruta_invalida_error import RutaInvalidaError
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_workspace import ServicioWorkspace


class ServicioNavegacion:
    """Resuelve `cd`, `ls` y `pwd` sobre el sistema de archivos real o el Workspace virtual.

    Reglas de resolución del destino:
    - `ws:<ruta>` (o `@ws`, `@ws/<ruta>`): navega en el Workspace virtual (Árbol N-ario).
    - Cualquier otro texto: navega en el sistema de archivos real (rutas absolutas,
      relativas, `~`, `$VARIABLES`, `.`, `..` y `-` para el directorio anterior).

    El cursor real se almacena en `ContextoApp.ubicacion_real` y NO se invoca `os.chdir`,
    de modo que las rutas relativas de respaldos y logs del IDE permanezcan estables.
    """

    PREFIJO_WORKSPACE = "ws:"
    ALIAS_WORKSPACE = "@ws"

    def __init__(
        self,
        contexto: ContextoApp,
        servicio_workspace: ServicioWorkspace,
        iniciar_en_sistema_real: bool = False,
    ) -> None:
        """Inicializa el servicio y, opcionalmente, ubica la sesión en el directorio real actual.

        Args:
            contexto: Estado global de la sesión.
            servicio_workspace: Servicio que gestiona el Workspace virtual.
            iniciar_en_sistema_real: Si es True, el modo inicial es el sistema de archivos real.
        """
        self._contexto: ContextoApp = contexto
        self._servicio_workspace: ServicioWorkspace = servicio_workspace
        self._ubicacion_anterior: Optional[str] = None

        if self._contexto.ubicacion_real is None:
            self._contexto.ubicacion_real = os.getcwd()
        if iniciar_en_sistema_real:
            self._contexto.modo_navegacion = ContextoApp.MODO_REAL

    # =========================================================================
    # Operaciones públicas
    # =========================================================================

    def cambiar_directorio(self, destino: str = "") -> str:
        """Cambia la ubicación actual y retorna su representación textual.

        Args:
            destino: Ruta destino. Vacío equivale al directorio personal (`~`) del usuario.

        Raises:
            RutaInvalidaError: Si la ruta no existe, no es un directorio o no es accesible.
        """
        es_workspace, ruta = self._interpretar_destino(destino)
        if es_workspace:
            self._servicio_workspace.cambiar_directorio(ruta)
            self._contexto.modo_navegacion = ContextoApp.MODO_WORKSPACE
            return self.obtener_ubicacion_actual()
        return self._cambiar_directorio_real(ruta)

    def obtener_ubicacion_actual(self) -> str:
        """Retorna la ruta del modo activo: real, o `ws:/ruta` si se navega en el Workspace."""
        modo = self._contexto.modo_navegacion
        if modo == ContextoApp.MODO_REAL:
            return self._ubicacion_real_segura()

        ruta_workspace = self._servicio_workspace.obtener_directorio_actual()
        if modo == ContextoApp.MODO_WORKSPACE:
            return f"{self.PREFIJO_WORKSPACE}{ruta_workspace}"
        return ruta_workspace

    def listar(
        self, destino: Optional[str] = None, mostrar_ocultos: bool = False
    ) -> List[Tuple[str, bool]]:
        """Lista el contenido de un directorio como pares `(nombre, es_directorio)`.

        Sin destino, lista la ubicación del modo activo. Los elementos del sistema real
        se devuelven en orden alfabético sin distinguir mayúsculas.

        Raises:
            RutaInvalidaError: Si la ruta no existe o no se puede leer.
        """
        if destino is None or not destino.strip():
            if self._contexto.modo_navegacion == ContextoApp.MODO_REAL:
                return self._listar_real(self._ubicacion_real_segura(), mostrar_ocultos)
            return self._listar_workspace(None)

        es_workspace, ruta = self._interpretar_destino(destino)
        if es_workspace:
            return self._listar_workspace(ruta)
        return self._listar_real(self._resolver_ruta_real(ruta), mostrar_ocultos)

    # =========================================================================
    # Interpretación y resolución de rutas
    # =========================================================================

    def _interpretar_destino(self, destino: str) -> Tuple[bool, str]:
        """Separa el prefijo de Workspace (si existe) y retorna `(es_workspace, ruta)`."""
        texto = destino.strip() if destino else ""
        if texto == self.ALIAS_WORKSPACE:
            return True, "/"
        if texto.startswith(self.ALIAS_WORKSPACE + "/"):
            return True, texto[len(self.ALIAS_WORKSPACE):]
        if texto.startswith(self.PREFIJO_WORKSPACE):
            resto = texto[len(self.PREFIJO_WORKSPACE):].strip()
            return True, resto if resto else "/"
        return False, texto

    def _ubicacion_real_segura(self) -> str:
        """Retorna el cursor real, inicializándolo con el directorio de trabajo si es necesario."""
        if self._contexto.ubicacion_real is None:
            self._contexto.ubicacion_real = os.getcwd()
        return self._contexto.ubicacion_real

    def _resolver_ruta_real(self, texto: str) -> str:
        """Convierte `texto` en ruta absoluta normalizada respecto al cursor real."""
        ruta = os.path.expandvars(os.path.expanduser(texto)) if texto else os.path.expanduser("~")
        if not os.path.isabs(ruta):
            ruta = os.path.join(self._ubicacion_real_segura(), ruta)
        return os.path.normpath(ruta)

    def _validar_directorio_real(self, ruta_absoluta: str) -> None:
        """Verifica que la ruta exista, sea un directorio y permita acceso de lectura."""
        if not os.path.exists(ruta_absoluta):
            raise RutaInvalidaError(f"No existe el directorio: '{ruta_absoluta}'.")
        if not os.path.isdir(ruta_absoluta):
            raise RutaInvalidaError(f"No es un directorio: '{ruta_absoluta}'.")
        if not os.access(ruta_absoluta, os.R_OK | os.X_OK):
            raise RutaInvalidaError(f"Permiso denegado: '{ruta_absoluta}'.")

    def _cambiar_directorio_real(self, ruta: str) -> str:
        """Mueve el cursor real al directorio indicado (soporta `-` para el anterior)."""
        if ruta == "-":
            if self._ubicacion_anterior is None:
                raise RutaInvalidaError("No existe un directorio anterior al cual volver.")
            ruta_absoluta = self._ubicacion_anterior
        else:
            ruta_absoluta = self._resolver_ruta_real(ruta)

        self._validar_directorio_real(ruta_absoluta)

        actual = self._ubicacion_real_segura()
        if ruta_absoluta != actual:
            self._ubicacion_anterior = actual
        self._contexto.ubicacion_real = ruta_absoluta
        self._contexto.modo_navegacion = ContextoApp.MODO_REAL
        return ruta_absoluta

    # =========================================================================
    # Listados
    # =========================================================================

    def _listar_workspace(self, ruta: Optional[str]) -> List[Tuple[str, bool]]:
        """Lista el contenido de una carpeta del Workspace virtual."""
        nodos = self._servicio_workspace.listar_directorio(ruta)
        return [(nodo.nombre, nodo.es_carpeta) for nodo in nodos]

    def _listar_real(
        self, ruta_absoluta: str, mostrar_ocultos: bool
    ) -> List[Tuple[str, bool]]:
        """Lista el contenido de un directorio real ordenado alfabéticamente."""
        if not os.path.exists(ruta_absoluta):
            raise RutaInvalidaError(f"No existe la ruta: '{ruta_absoluta}'.")
        if not os.path.isdir(ruta_absoluta):
            return [(os.path.basename(ruta_absoluta), False)]

        resultado: List[Tuple[str, bool]] = []
        try:
            with os.scandir(ruta_absoluta) as entradas:
                for entrada in entradas:
                    if not mostrar_ocultos and entrada.name.startswith("."):
                        continue
                    self._insertar_ordenado(resultado, (entrada.name, entrada.is_dir()))
        except PermissionError:
            raise RutaInvalidaError(f"Permiso denegado: '{ruta_absoluta}'.")
        except OSError as error:
            raise RutaInvalidaError(f"No se pudo leer '{ruta_absoluta}': {error.strerror}.")
        return resultado

    def _insertar_ordenado(
        self, lista: List[Tuple[str, bool]], elemento: Tuple[str, bool]
    ) -> None:
        """Inserta `elemento` en `lista` manteniendo orden alfabético (insensible a mayúsculas)."""
        clave = elemento[0].lower()
        pos = 0
        while pos < len(lista) and lista[pos][0].lower() <= clave:
            pos += 1
        lista.insert(pos, elemento)

