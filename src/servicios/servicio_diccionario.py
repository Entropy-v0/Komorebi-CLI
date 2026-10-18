"""Módulo del servicio de diccionario técnico y autocompletado sobre Árbol AVL."""

from typing import Optional
from src.estructuras.arbol_avl import ArbolAVL
from src.estructuras.nodo_avl import NodoAVL
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_logs import ServicioLogs


class ServicioDiccionario:
    """Gestiona el diccionario de palabras clave y autocompletado en tiempo O(log n + k).

    Al inicializarse, vincula un `ArbolAVL` en `ContextoApp.diccionario` y precarga las
    35 palabras reservadas de Python en un orden deliberadamente desbalanceado para
    ejercitar las cuatro rotaciones (LL, RR, LR, RL) desde el arranque.
    """

    PALABRAS_BASE_PYTHON: tuple[tuple[str, str], ...] = (
        ("return", "Finaliza la ejecución de una función y devuelve un valor."),
        ("def", "Define una función o método en Python."),
        ("while", "Bucle condicional que se ejecuta mientras la expresión sea verdadera."),
        ("assert", "Verifica una condición de depuración y lanza AssertionError si falla."),
        ("async", "Declara una corrutina o función asíncrona."),
        ("break", "Termina inmediatamente el bucle más cercano."),
        ("await", "Suspende la ejecución de una corrutina hasta obtener el resultado."),
        ("class", "Define una nueva clase de objetos."),
        ("from", "Especifica el módulo origen en una importación selectiva."),
        ("continue", "Salta a la siguiente iteración del bucle actual."),
        ("del", "Elimina una referencia a un objeto, variable o elemento."),
        ("elif", "Rama condicional intermedia después de una sentencia if."),
        ("else", "Rama condicional por defecto cuando no se cumplen las anteriores."),
        ("except", "Captura y maneja excepciones dentro de un bloque try."),
        ("False", "Valor booleano literal de falsedad."),
        ("finally", "Bloque que se ejecuta siempre al finalizar una estructura try."),
        ("for", "Bucle iterativo sobre cualquier secuencia o iterable."),
        ("global", "Declara que una variable pertenece al ámbito global del módulo."),
        ("if", "Estructura condicional principal para toma de decisiones."),
        ("import", "Importa un módulo o paquete externo al espacio de nombres."),
        ("in", "Operador de pertenencia o iteración sobre colecciones."),
        ("is", "Operador de identidad referencial entre dos objetos en memoria."),
        ("lambda", "Crea una función anónima en una sola expresión."),
        ("None", "Objeto singleton que representa la ausencia de valor."),
        ("nonlocal", "Vincula una variable con el ámbito envolvente inmediato no global."),
        ("not", "Operador lógico de negación booleana."),
        ("or", "Operador lógico de disyunción con evaluación en cortocircuito."),
        ("pass", "Operación nula utilizada como marcador de posición sintáctico."),
        ("raise", "Lanza explícitamente una excepción en la pila de ejecución."),
        ("True", "Valor booleano literal de verdad."),
        ("try", "Inicia un bloque protegido para captura y manejo de excepciones."),
        ("with", "Gestiona el ciclo de vida de recursos mediante administradores de contexto."),
        ("yield", "Pausa una función generadora y produce un valor al iterador."),
        ("and", "Operador lógico de conjunción con evaluación en cortocircuito."),
        ("as", "Crea un alias en sentencias import, with o except."),
    )

    def __init__(
        self,
        contexto: ContextoApp,
        servicio_logs: Optional[ServicioLogs] = None,
        precargar: bool = True,
    ) -> None:
        """Inicializa el servicio de diccionario y precarga palabras clave de Python.

        Args:
            contexto: Estado global de la sesión donde reside la referencia al `ArbolAVL`.
            servicio_logs: Servicio opcional de bitácora.
            precargar: Si es True y el diccionario está vacío, inserta las keywords base.
        """
        self._contexto: ContextoApp = contexto
        self._servicio_logs: Optional[ServicioLogs] = servicio_logs

        if self._contexto.diccionario is None:
            self._contexto.diccionario = ArbolAVL()

        if precargar and self.arbol.esta_vacio():
            self._precargar_palabras_base()

    @property
    def arbol(self) -> ArbolAVL:
        """Retorna la instancia activa de `ArbolAVL` alojada en el contexto."""
        if self._contexto.diccionario is None:
            self._contexto.diccionario = ArbolAVL()
        return self._contexto.diccionario

    def _precargar_palabras_base(self) -> None:
        """Inserta las palabras reservadas de Python en orden desordenado."""
        for palabra, descripcion in self.PALABRAS_BASE_PYTHON:
            palabra_limpia = palabra.strip()
            if not palabra_limpia or not descripcion:
                continue
            if not self.arbol.contiene(palabra_limpia):
                self.arbol.insertar(palabra_limpia, descripcion)

    def agregar_palabra(
        self,
        palabra: str,
        descripcion: str = "Palabra clave registrada por el usuario.",
    ) -> NodoAVL:
        """Agrega una nueva palabra clave al diccionario AVL.

        Args:
            palabra: Palabra clave a insertar.
            descripcion: Descripción técnica opcional.

        Returns:
            El `NodoAVL` insertado.

        Raises:
            ValueError: Si la palabra está vacía.
            PalabraDuplicadaError: Si la palabra ya existe en el árbol.
        """
        desc_final = (
            descripcion.strip()
            if descripcion and descripcion.strip()
            else "Palabra clave registrada por el usuario."
        )
        nodo = self.arbol.insertar(palabra, desc_final)
        if self._servicio_logs is not None:
            self._servicio_logs.registrar_info(
                "ServicioDiccionario",
                f"Palabra '{nodo.palabra}' insertada (altura={self.arbol.altura}).",
            )
        return nodo

    def eliminar_palabra(self, palabra: str) -> bool:
        """Elimina una palabra clave del diccionario AVL rebalanceando el árbol.

        Args:
            palabra: Palabra clave a eliminar.

        Returns:
            True si fue eliminada, False si no existía.
        """
        eliminado = self.arbol.eliminar(palabra)
        if eliminado and self._servicio_logs is not None:
            self._servicio_logs.registrar_info(
                "ServicioDiccionario",
                f"Palabra '{palabra.strip()}' eliminada (altura={self.arbol.altura}).",
            )
        return eliminado

    def buscar_palabra(self, palabra: str) -> Optional[NodoAVL]:
        """Busca una palabra exacta en el diccionario AVL en O(log n)."""
        return self.arbol.buscar(palabra)

    def es_palabra_reservada(self, palabra: str) -> bool:
        """Indica si `palabra` se encuentra registrada en el diccionario AVL."""
        return self.arbol.contiene(palabra)

    def sugerir(self, prefijo: str) -> list[str]:
        """Retorna sugerencias ordenadas alfabéticamente mediante búsqueda con poda."""
        return self.arbol.sugerir(prefijo)

    def sugerir_detallado(self, prefijo: str) -> list[tuple[str, str]]:
        """Retorna pares (palabra, descripcion) que coinciden con el prefijo dado."""
        return self.arbol.sugerir_detallado(prefijo)

    def formatear_sugerencias(self, prefijo: str) -> str:
        """Genera un bloque formateado con las sugerencias para mostrar en la CLI."""
        coincidencias = self.sugerir_detallado(prefijo)
        etiqueta = f"'{prefijo}'" if prefijo else "(todas)"
        if not coincidencias:
            return (
                f"[Diccionario AVL] Sin coincidencias para el prefijo {etiqueta}."
            )

        lineas = [
            f"--- Sugerencias AVL para {etiqueta} ({len(coincidencias)} coincidencia(s), "
            f"altura árbol={self.arbol.altura}) ---"
        ]
        for palabra, descripcion in coincidencias:
            lineas.append(f"  - {palabra:<15} : {descripcion}")
        lineas.append("-" * len(lineas[0]))
        return "\n".join(lineas)
