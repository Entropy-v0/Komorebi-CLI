"""Módulo del Árbol Binario de Búsqueda Autobalanceado (AVL).

Decisión Arquitectónica sobre Herencia (Principio de Sustitución de Liskov - LSP):
---------------------------------------------------------------------------------
`ArbolAVL` se implementa como una clase independiente y autocontenida en lugar de
heredar de `ArbolExpresion` o de un `ArbolBinario` iterativo genérico por dos razones:
1. En el dominio del proyecto, `ArbolExpresion` representa un Árbol de Sintaxis Abstracta
   (AST) donde los nodos internos son operadores y las hojas son operandos numéricos,
   careciendo de la invariante de orden lexicográfico de un Árbol Binario de Búsqueda (BST).
2. Un AVL requiere que `insertar` y `eliminar` propaguen actualizaciones de altura y
   rotaciones de rebalanceo hacia los ancestros durante el desenrollado de la pila de
   recursión, manteniendo la invariante estricta |FB| <= 1 en todo momento. Heredar de
   una estructura sin invariante de balance violaría el Principio de Sustitución de Liskov.
"""

from typing import Optional
from src.estructuras.nodo_avl import NodoAVL
from src.excepciones.palabra_duplicada_error import PalabraDuplicadaError


class ArbolAVL:
    """Árbol Binario de Búsqueda Autobalanceado (AVL) para diccionario y autocompletado.

    Garantiza complejidad temporal O(log n) en el peor caso para búsqueda, inserción
    y eliminación, y O(log n + k) para autocompletado por prefijo mediante poda de ramas.
    Convención de Factor de Balance: FB(nodo) = altura(derecho) - altura(izquierdo).
    """

    def __init__(self) -> None:
        """Inicializa un Árbol AVL vacío."""
        self._raiz: Optional[NodoAVL] = None
        self._tamanio: int = 0

    @property
    def raiz(self) -> Optional[NodoAVL]:
        """Retorna el nodo raíz del Árbol AVL."""
        return self._raiz

    @property
    def tamanio(self) -> int:
        """Retorna la cantidad total de palabras almacenadas en el Árbol AVL."""
        return self._tamanio

    @property
    def altura(self) -> int:
        """Retorna la altura total del árbol (0 si está vacío)."""
        return self._obtener_altura(self._raiz)

    def esta_vacio(self) -> bool:
        """Indica si el árbol no contiene ningún nodo."""
        return self._raiz is None

    # =========================================================================
    # Operaciones Principales O(log n)
    # =========================================================================

    def insertar(self, palabra: str, descripcion: str = "") -> NodoAVL:
        """Inserta una nueva palabra clave en el Árbol AVL manteniendo el balance.

        Args:
            palabra: Clave lexicográfica a insertar.
            descripcion: Descripción técnica asociada a la palabra.

        Returns:
            El NodoAVL recién insertado.

        Raises:
            ValueError: Si la palabra es vacía.
            PalabraDuplicadaError: Si la palabra ya existe en el árbol.
        """
        palabra_limpia = palabra.strip()
        if not palabra_limpia:
            raise ValueError("La palabra clave a insertar no puede estar vacía.")

        nodo_creado: list[NodoAVL] = []
        self._raiz = self._insertar_recursivo(
            self._raiz, palabra_limpia, descripcion.strip(), nodo_creado
        )
        self._tamanio += 1
        return nodo_creado[0]

    def eliminar(self, palabra: str) -> bool:
        """Elimina una palabra clave del Árbol AVL y rebalancea todos los ancestros.

        Soporta los 3 casos clásicos de eliminación en BST (nodo hoja, nodo con 1 hijo,
        nodo con 2 hijos mediante reemplazo por sucesor inorden) seguido de actualización
        de alturas y rotaciones AVL en cada nivel al regresar de la recursión.

        Args:
            palabra: Clave lexicográfica a eliminar.

        Returns:
            True si la palabra existía y fue eliminada; False si no se encontró.
        """
        palabra_limpia = palabra.strip()
        if not palabra_limpia or self._raiz is None:
            return False

        eliminado: list[bool] = [False]
        self._raiz = self._eliminar_recursivo(self._raiz, palabra_limpia, eliminado)
        if eliminado[0]:
            self._tamanio -= 1
        return eliminado[0]

    def buscar(self, palabra: str) -> Optional[NodoAVL]:
        """Busca una palabra clave en tiempo O(log n).

        Args:
            palabra: Clave lexicográfica a buscar.

        Returns:
            El NodoAVL correspondiente si existe, o None si no se encuentra.
        """
        palabra_limpia = palabra.strip()
        actual = self._raiz
        while actual is not None:
            if palabra_limpia == actual.palabra:
                return actual
            if palabra_limpia < actual.palabra:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return None

    def contiene(self, palabra: str) -> bool:
        """Verifica en O(log n) si una palabra existe en el Árbol AVL."""
        return self.buscar(palabra) is not None

    # =========================================================================
    # Autocompletado por Prefijo con Poda O(log n + k)
    # =========================================================================

    def sugerir(self, prefijo: str) -> list[str]:
        """Devuelve todas las palabras que comienzan con `prefijo` en orden alfabético.

        Aplica búsqueda con PODA sobre el Árbol AVL (no realiza recorrido completo
        cuando el prefijo permite descartar subárboles):
        - Si `nodo.palabra` empieza con `prefijo`: explora subárbol izquierdo, agrega
          `nodo.palabra`, y explora subárbol derecho (manteniendo orden inorden).
        - Si `nodo.palabra < prefijo`: poda todo el subárbol izquierdo y explora
          únicamente el subárbol derecho.
        - Si `nodo.palabra > prefijo` (sin empezar con `prefijo`): poda todo el
          subárbol derecho y explora únicamente el subárbol izquierdo.

        Costo temporal: O(log n + k), donde k es el número de coincidencias.

        Args:
            prefijo: Prefijo de búsqueda.

        Returns:
            Lista de palabras coincidentes ordenadas alfabéticamente.
        """
        resultados: list[str] = []
        self._sugerir_con_poda(self._raiz, prefijo, resultados)
        return resultados

    def sugerir_detallado(self, prefijo: str) -> list[tuple[str, str]]:
        """Devuelve pares (palabra, descripcion) que comienzan con `prefijo` usando poda."""
        resultados: list[tuple[str, str]] = []
        self._sugerir_detallado_con_poda(self._raiz, prefijo, resultados)
        return resultados

    # =========================================================================
    # Recorridos y Validación de Invariantes
    # =========================================================================

    def inorden(self) -> list[str]:
        """Retorna todas las palabras del árbol en orden alfabético estricto."""
        resultado: list[str] = []
        self._inorden_recursivo(self._raiz, resultado)
        return resultado

    def inorden_detallado(self) -> list[tuple[str, str]]:
        """Retorna todas las tuplas (palabra, descripcion) en orden alfabético."""
        resultado: list[tuple[str, str]] = []
        self._inorden_detallado_recursivo(self._raiz, resultado)
        return resultado

    def es_valido(self) -> bool:
        """Verifica integralmente las tres invariantes estructurales del Árbol AVL:
        1. Propiedad estricta de Árbol Binario de Búsqueda (izq < nodo < der).
        2. Consistencia exacta del atributo `altura` en cada nodo: 1 + max(h(izq), h(der)).
        3. Condición de balance AVL en cada nodo: |altura(der) - altura(izq)| <= 1.
        """
        return self._validar_nodo(self._raiz, None, None)

    # =========================================================================
    # Métodos Privados de Balanceo y las 4 Rotaciones AVL (LL, RR, LR, RL)
    # =========================================================================

    def _obtener_altura(self, nodo: Optional[NodoAVL]) -> int:
        """Retorna la altura de un nodo en O(1), o 0 si es None."""
        return nodo.altura if nodo is not None else 0

    def _actualizar_altura(self, nodo: NodoAVL) -> None:
        """Recalcula la altura de `nodo` a partir de las alturas de sus dos hijos."""
        altura_izq = self._obtener_altura(nodo.izquierdo)
        altura_der = self._obtener_altura(nodo.derecho)
        nodo.altura = 1 + (altura_izq if altura_izq > altura_der else altura_der)

    def _factor_balance(self, nodo: Optional[NodoAVL]) -> int:
        """Calcula el Factor de Balance según la convención:
        FB(nodo) = altura(derecho) - altura(izquierdo).
        - FB < -1: Subárbol izquierdo pesado (desbalance hacia la izquierda).
        - FB > +1: Subárbol derecho pesado (desbalance hacia la derecha).
        - FB en {-1, 0, +1}: Nodo balanceado.
        """
        if nodo is None:
            return 0
        return self._obtener_altura(nodo.derecho) - self._obtener_altura(nodo.izquierdo)

    def _rotar_ll(self, z: NodoAVL) -> NodoAVL:
        """Rotación Simple a la Derecha para corregir el Caso LL (Izquierda-Izquierda).

        Se invoca cuando FB(z) < -1 y FB(z.izquierdo) <= 0.

                 z                              y
                / \\                            / \\
               y   T4    --(_rotar_ll)-->     x    z
              / \\                                 / \\
             x   T3                              T3  T4

        Reasignación de referencias:
        1. `y` toma el lugar de `z` como nueva raíz del subárbol (`y = z.izquierdo`).
        2. El subárbol derecho de `y` (`T3`) pasa a ser el hijo izquierdo de `z` (`z.izquierdo = T3`).
        3. `z` pasa a ser el hijo derecho de `y` (`y.derecho = z`).

        Orden obligatorio de actualización de alturas:
        1. Primero `z` (que ahora es hijo inferior de `y`).
        2. Después `y` (nueva raíz superior del subárbol, cuya altura depende de `z`).
        """
        y: NodoAVL = z.izquierdo  # type: ignore[assignment]
        t3: Optional[NodoAVL] = y.derecho

        # Reasignación de punteros
        y.derecho = z
        z.izquierdo = t3

        # Actualización de alturas de abajo hacia arriba (primero z, luego y)
        self._actualizar_altura(z)
        self._actualizar_altura(y)
        return y

    def _rotar_rr(self, z: NodoAVL) -> NodoAVL:
        """Rotación Simple a la Izquierda para corregir el Caso RR (Derecha-Derecha).

        Se invoca cuando FB(z) > 1 y FB(z.derecho) >= 0.

               z                                y
              / \\                              / \\
             T1   y      --(_rotar_rr)-->     z    x
                 / \\                         / \\
                T2   x                      T1  T2

        Reasignación de referencias:
        1. `y` toma el lugar de `z` como nueva raíz del subárbol (`y = z.derecho`).
        2. El subárbol izquierdo de `y` (`T2`) pasa a ser el hijo derecho de `z` (`z.derecho = T2`).
        3. `z` pasa a ser el hijo izquierdo de `y` (`y.izquierdo = z`).

        Orden obligatorio de actualización de alturas:
        1. Primero `z` (que ahora es hijo inferior de `y`).
        2. Después `y` (nueva raíz superior del subárbol, cuya altura depende de `z`).
        """
        y: NodoAVL = z.derecho  # type: ignore[assignment]
        t2: Optional[NodoAVL] = y.izquierdo

        # Reasignación de punteros
        y.izquierdo = z
        z.derecho = t2

        # Actualización de alturas de abajo hacia arriba (primero z, luego y)
        self._actualizar_altura(z)
        self._actualizar_altura(y)
        return y

    def _rotar_lr(self, z: NodoAVL) -> NodoAVL:
        """Rotación Doble Izquierda-Derecha para corregir el Caso LR (Izquierda-Derecha).

        Se invoca cuando FB(z) < -1 (izquierda pesada) y FB(z.izquierdo) > 0 (hijo izquierdo
        pesado hacia la derecha).

        Paso 1: Rotación simple a la izquierda (`_rotar_rr`) sobre el hijo izquierdo `y`,
                convirtiendo el caso LR en un caso LL puro.
        Paso 2: Rotación simple a la derecha (`_rotar_ll`) sobre el nodo `z`.
        Las alturas de `y`, `z` y la nueva raíz `x` se actualizan en orden ascendente
        dentro de cada rotación elemental.
        """
        z.izquierdo = self._rotar_rr(z.izquierdo)  # type: ignore[arg-type]
        return self._rotar_ll(z)

    def _rotar_rl(self, z: NodoAVL) -> NodoAVL:
        """Rotación Doble Derecha-Izquierda para corregir el Caso RL (Derecha-Izquierda).

        Se invoca cuando FB(z) > 1 (derecha pesada) y FB(z.derecho) < 0 (hijo derecho
        pesado hacia la izquierda).

        Paso 1: Rotación simple a la derecha (`_rotar_ll`) sobre el hijo derecho `y`,
                convirtiendo el caso RL en un caso RR puro.
        Paso 2: Rotación simple a la izquierda (`_rotar_rr`) sobre el nodo `z`.
        Las alturas de `y`, `z` y la nueva raíz `x` se actualizan en orden ascendente
        dentro de cada rotación elemental.
        """
        z.derecho = self._rotar_ll(z.derecho)  # type: ignore[arg-type]
        return self._rotar_rr(z)

    def _rebalancear(self, nodo: NodoAVL) -> NodoAVL:
        """Actualiza la altura del nodo e identifica si requiere una de las 4 rotaciones."""
        self._actualizar_altura(nodo)
        fb = self._factor_balance(nodo)

        # Desbalance hacia la izquierda (altura(izq) - altura(der) == 2 -> FB == -2)
        if fb < -1:
            if self._factor_balance(nodo.izquierdo) <= 0:
                return self._rotar_ll(nodo)
            return self._rotar_lr(nodo)

        # Desbalance hacia la derecha (altura(der) - altura(izq) == 2 -> FB == +2)
        if fb > 1:
            if self._factor_balance(nodo.derecho) >= 0:
                return self._rotar_rr(nodo)
            return self._rotar_rl(nodo)

        return nodo

    # =========================================================================
    # Auxiliares Recursivos de Inserción, Eliminación y Poda
    # =========================================================================

    def _insertar_recursivo(
        self,
        nodo: Optional[NodoAVL],
        palabra: str,
        descripcion: str,
        nodo_creado: list[NodoAVL],
    ) -> NodoAVL:
        """Inserta recursivamente como en un BST y rebalancea cada ancestro al regresar."""
        if nodo is None:
            nuevo = NodoAVL(palabra, descripcion)
            nodo_creado.append(nuevo)
            return nuevo

        if palabra == nodo.palabra:
            raise PalabraDuplicadaError(
                f"La palabra clave '{palabra}' ya existe en el diccionario AVL."
            )
        if palabra < nodo.palabra:
            nodo.izquierdo = self._insertar_recursivo(
                nodo.izquierdo, palabra, descripcion, nodo_creado
            )
        else:
            nodo.derecho = self._insertar_recursivo(
                nodo.derecho, palabra, descripcion, nodo_creado
            )

        return self._rebalancear(nodo)

    def _eliminar_recursivo(
        self,
        nodo: Optional[NodoAVL],
        palabra: str,
        eliminado: list[bool],
    ) -> Optional[NodoAVL]:
        """Elimina recursivamente el nodo con `palabra` y rebalancea cada ancestro."""
        if nodo is None:
            return None

        if palabra < nodo.palabra:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, palabra, eliminado)
        elif palabra > nodo.palabra:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, palabra, eliminado)
        else:
            eliminado[0] = True
            # Caso 1 y Caso 2: Nodo hoja o con a lo sumo un hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo

            # Caso 3: Nodo con dos hijos -> reemplazar por el sucesor inorden
            # (el nodo mínimo del subárbol derecho)
            sucesor = self._obtener_minimo(nodo.derecho)
            nodo.palabra = sucesor.palabra
            nodo.descripcion = sucesor.descripcion
            dummy: list[bool] = [False]
            nodo.derecho = self._eliminar_recursivo(
                nodo.derecho, sucesor.palabra, dummy
            )

        return self._rebalancear(nodo)

    def _obtener_minimo(self, nodo: NodoAVL) -> NodoAVL:
        """Encuentra el nodo con la clave mínima en el subárbol dado (sucesor inorden)."""
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def _sugerir_con_poda(
        self,
        nodo: Optional[NodoAVL],
        prefijo: str,
        resultados: list[str],
    ) -> None:
        """Recorrido inorden acotado con poda de ramas para autocompletado en O(log n + k)."""
        if nodo is None:
            return

        clave = nodo.palabra
        if clave.startswith(prefijo):
            # La clave coincide con el prefijo: pueden existir coincidencias menores a la
            # izquierda y mayores a la derecha; se explora en inorden para orden alfabético.
            self._sugerir_con_poda(nodo.izquierdo, prefijo, resultados)
            resultados.append(clave)
            self._sugerir_con_poda(nodo.derecho, prefijo, resultados)
        elif clave < prefijo:
            # Toda clave en el subárbol izquierdo es menor que `clave` y por tanto < `prefijo`.
            # Se poda la rama izquierda y solo se explora la derecha.
            self._sugerir_con_poda(nodo.derecho, prefijo, resultados)
        else:
            # `clave > prefijo` y no comienza con `prefijo`: toda clave en el subárbol derecho
            # es mayor que `clave` y tampoco podrá comenzar con `prefijo`.
            # Se poda la rama derecha y solo se explora la izquierda.
            self._sugerir_con_poda(nodo.izquierdo, prefijo, resultados)

    def _sugerir_detallado_con_poda(
        self,
        nodo: Optional[NodoAVL],
        prefijo: str,
        resultados: list[tuple[str, str]],
    ) -> None:
        """Variante de búsqueda con poda que recolecta tuplas (palabra, descripcion)."""
        if nodo is None:
            return

        clave = nodo.palabra
        if clave.startswith(prefijo):
            self._sugerir_detallado_con_poda(nodo.izquierdo, prefijo, resultados)
            resultados.append((clave, nodo.descripcion))
            self._sugerir_detallado_con_poda(nodo.derecho, prefijo, resultados)
        elif clave < prefijo:
            self._sugerir_detallado_con_poda(nodo.derecho, prefijo, resultados)
        else:
            self._sugerir_detallado_con_poda(nodo.izquierdo, prefijo, resultados)

    def _inorden_recursivo(self, nodo: Optional[NodoAVL], resultado: list[str]) -> None:
        if nodo is None:
            return
        self._inorden_recursivo(nodo.izquierdo, resultado)
        resultado.append(nodo.palabra)
        self._inorden_recursivo(nodo.derecho, resultado)

    def _inorden_detallado_recursivo(
        self, nodo: Optional[NodoAVL], resultado: list[tuple[str, str]]
    ) -> None:
        if nodo is None:
            return
        self._inorden_detallado_recursivo(nodo.izquierdo, resultado)
        resultado.append((nodo.palabra, nodo.descripcion))
        self._inorden_detallado_recursivo(nodo.derecho, resultado)

    def _validar_nodo(
        self,
        nodo: Optional[NodoAVL],
        min_clave: Optional[str],
        max_clave: Optional[str],
    ) -> bool:
        """Verifica recursivamente BST estricto, altura exacta y |FB| <= 1."""
        if nodo is None:
            return True

        if min_clave is not None and nodo.palabra <= min_clave:
            return False
        if max_clave is not None and nodo.palabra >= max_clave:
            return False

        altura_izq = self._obtener_altura(nodo.izquierdo)
        altura_der = self._obtener_altura(nodo.derecho)
        altura_esperada = 1 + (altura_izq if altura_izq > altura_der else altura_der)
        if nodo.altura != altura_esperada:
            return False

        fb = altura_der - altura_izq
        if fb < -1 or fb > 1:
            return False

        return self._validar_nodo(
            nodo.izquierdo, min_clave, nodo.palabra
        ) and self._validar_nodo(nodo.derecho, nodo.palabra, max_clave)

