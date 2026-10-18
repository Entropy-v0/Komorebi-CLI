"""Módulo del Árbol B (B-Tree) multicamino para indexación global de tokens."""

import math
from typing import Optional
from src.estructuras.nodo_b import NodoB
from src.nucleo.referencia_token import ReferenciaToken


class ArbolB:
    """Árbol B balanceado multicamino según la convención de Knuth de orden m (por defecto m=4).

    Invariantes de Knuth para orden `m`:
    1. Todo nodo posee como máximo `m` hijos y `m - 1` claves.
    2. Todo nodo interno distinto de la raíz posee al menos `ceil(m / 2)` hijos
       y `ceil(m / 2) - 1` claves.
    3. Si la raíz no es hoja, posee al menos 2 hijos y 1 clave.
    4. Todas las hojas se encuentran exactamente al mismo nivel (profundidad).
    5. Dentro de cada nodo, las claves están estrictamente ordenadas (`c_0 < c_1 < ... < c_{k-1}`)
       y actúan como separadores estrictos entre los subárboles hijos.
    """

    def __init__(self, orden: int = 4) -> None:
        """Inicializa un Árbol B vacío de orden `orden` (m >= 3).

        Args:
            orden: Grado máximo `m` de ramificación (por defecto 4: nodos 2-3-4).

        Raises:
            ValueError: Si el orden especificado es menor que 3.
        """
        if orden < 3:
            raise ValueError("El orden m de un Árbol B debe ser al menos 3.")
        self._orden: int = orden
        self._max_claves: int = orden - 1
        self._min_hijos: int = math.ceil(orden / 2)
        self._min_claves: int = self._min_hijos - 1
        self._raiz: Optional[NodoB] = None
        self._tamanio: int = 0

    @property
    def orden(self) -> int:
        """Retorna el orden m del Árbol B."""
        return self._orden

    @property
    def max_claves(self) -> int:
        """Retorna el máximo de claves permitidas por nodo (m - 1)."""
        return self._max_claves

    @property
    def min_claves(self) -> int:
        """Retorna el mínimo de claves requerido en nodos no raíz (ceil(m/2) - 1)."""
        return self._min_claves

    @property
    def raiz(self) -> Optional[NodoB]:
        """Retorna el nodo raíz del Árbol B."""
        return self._raiz

    @property
    def tamanio(self) -> int:
        """Retorna el número de tokens únicos almacenados en el Árbol B."""
        return self._tamanio

    @property
    def altura(self) -> int:
        """Calcula la altura actual del Árbol B (0 si está vacío)."""
        nivel = 0
        actual = self._raiz
        while actual is not None:
            nivel += 1
            if actual.es_hoja or not actual.hijos:
                break
            actual = actual.hijos[0]
        return nivel

    def esta_vacio(self) -> bool:
        """Indica si el Árbol B no contiene ninguna clave."""
        return self._raiz is None or len(self._raiz.claves) == 0

    def limpiar(self) -> None:
        """Vacía completamente el Árbol B."""
        self._raiz = None
        self._tamanio = 0

    # =========================================================================
    # Búsqueda O(log n)
    # =========================================================================

    def buscar(self, token: str) -> list[ReferenciaToken]:
        """Busca un token en el Árbol B y devuelve su lista de referencias.

        Args:
            token: Identificador a buscar.

        Returns:
            Lista de `ReferenciaToken` asociadas al token, o lista vacía si no existe.
        """
        token_limpio = token.strip()
        if not token_limpio or self._raiz is None:
            return []

        nodo, idx = self._buscar_en_nodo(self._raiz, token_limpio)
        if nodo is not None and idx >= 0:
            return list(nodo.valores[idx])
        return []

    def contiene(self, token: str) -> bool:
        """Indica si el token existe como clave dentro del Árbol B."""
        token_limpio = token.strip()
        if not token_limpio or self._raiz is None:
            return False
        nodo, _ = self._buscar_en_nodo(self._raiz, token_limpio)
        return nodo is not None

    def _buscar_en_nodo(
        self, nodo: Optional[NodoB], token: str
    ) -> tuple[Optional[NodoB], int]:
        """Desciende por el Árbol B comparando claves lexicográficamente."""
        actual = nodo
        while actual is not None:
            idx = 0
            num_claves = len(actual.claves)
            while idx < num_claves and token > actual.claves[idx]:
                idx += 1

            if idx < num_claves and token == actual.claves[idx]:
                return actual, idx

            if actual.es_hoja:
                return None, -1

            actual = actual.hijos[idx]
        return None, -1

    # =========================================================================
    # Inserción Bottom-Up con División Posterior (Post-Overflow Split)
    # =========================================================================

    def insertar(self, token: str, referencia: ReferenciaToken) -> None:
        """Inserta un token y su `ReferenciaToken` en el Árbol B.

        Algoritmo de Inserción con División Posterior (Bottom-Up):
        ----------------------------------------------------------
        1. Si el `token` ya existe en algún nodo (interno u hoja), NO se crea una nueva
           clave; únicamente se inserta `referencia` de forma ordenada y sin duplicados
           en la lista de valores asociada a dicha clave.
        2. Si el `token` no existe:
           a. Si el árbol está vacío, se crea un nodo raíz hoja con la clave.
           b. De lo contrario, se desciende recursivamente hasta la hoja correspondiente
              y se inserta el par `(token, [referencia])` manteniendo el orden de `claves`.
           c. Al regresar de la recursión (bottom-up), si el hijo visitado supera el máximo
              permitido (`len(hijo.claves) == m > m - 1`), se ejecuta `_dividir_hijo`:
              - La clave mediana sube al nodo padre como nuevo separador.
              - Las claves anteriores a la mediana permanecen en el hijo izquierdo.
              - Las claves posteriores a la mediana pasan a un nuevo nodo hermano derecho.
           d. Si la propagación de divisiones provoca que la raíz misma alcance `m` claves,
              se crea una nueva raíz con la antigua raíz como hijo y se divide, incrementando
              la altura del Árbol B en 1 de manera uniforme para todas las hojas.
        """
        token_limpio = token.strip()
        if not token_limpio:
            raise ValueError("El token a indexar no puede estar vacío.")

        if self._raiz is None:
            self._raiz = NodoB(es_hoja=True)
            self._raiz.claves.append(token_limpio)
            self._raiz.valores.append([referencia])
            self._tamanio = 1
            return

        # 1. Verificar si la clave ya existe en el árbol para agregar solo la referencia
        nodo_existente, idx_existente = self._buscar_en_nodo(self._raiz, token_limpio)
        if nodo_existente is not None and idx_existente >= 0:
            self._agregar_referencia_ordenada(
                nodo_existente.valores[idx_existente], referencia
            )
            return

        # 2. Inserción de nueva clave en hoja con división bottom-up al regresar
        self._insertar_recursivo(self._raiz, token_limpio, referencia)
        self._tamanio += 1

        # 3. Si la raíz se desbordó (alcanzó `m` claves), dividir la raíz y crecer en altura
        if len(self._raiz.claves) > self._max_claves:
            nueva_raiz = NodoB(es_hoja=False)
            nueva_raiz.hijos.append(self._raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self._raiz = nueva_raiz

    def _agregar_referencia_ordenada(
        self, lista_refs: list[ReferenciaToken], nueva: ReferenciaToken
    ) -> None:
        """Inserta `nueva` en `lista_refs` sin duplicados y en orden (archivo_id, linea)."""
        pos = 0
        n = len(lista_refs)
        while pos < n:
            actual = lista_refs[pos]
            if actual == nueva:
                return
            if (actual.archivo_id, actual.linea) > (nueva.archivo_id, nueva.linea):
                break
            pos += 1
        lista_refs.insert(pos, nueva)

    def _insertar_recursivo(
        self, nodo: NodoB, token: str, referencia: ReferenciaToken
    ) -> None:
        """Inserta recursivamente en la hoja y divide al hijo si hubo desbordamiento."""
        pos = 0
        num_claves = len(nodo.claves)
        while pos < num_claves and token > nodo.claves[pos]:
            pos += 1

        if nodo.es_hoja:
            nodo.claves.insert(pos, token)
            nodo.valores.insert(pos, [referencia])
            return

        self._insertar_recursivo(nodo.hijos[pos], token, referencia)

        # Al regresar de la recursión, verificar si el hijo visitado se desbordó (> m - 1 claves)
        if len(nodo.hijos[pos].claves) > self._max_claves:
            self._dividir_hijo(nodo, pos)

    def _dividir_hijo(self, padre: NodoB, idx_hijo: int) -> None:
        """Divide un nodo hijo desbordado (`m` claves) promoviendo la clave mediana al padre."""
        hijo_izq = padre.hijos[idx_hijo]
        mediana = (len(hijo_izq.claves) - 1) // 2

        clave_mediana = hijo_izq.claves[mediana]
        valor_mediana = hijo_izq.valores[mediana]

        # Crear el nuevo hermano derecho con las claves posteriores a la mediana
        hijo_der = NodoB(es_hoja=hijo_izq.es_hoja)
        hijo_der.claves = hijo_izq.claves[mediana + 1 :]
        hijo_der.valores = hijo_izq.valores[mediana + 1 :]

        # Conservar en el hijo izquierdo solo las claves anteriores a la mediana
        hijo_izq.claves = hijo_izq.claves[:mediana]
        hijo_izq.valores = hijo_izq.valores[:mediana]

        # Si el nodo dividido es interno, repartir también sus m + 1 hijos
        if not hijo_izq.es_hoja:
            hijo_der.hijos = hijo_izq.hijos[mediana + 1 :]
            hijo_izq.hijos = hijo_izq.hijos[: mediana + 1]

        # Promover la mediana al padre e insertar el nuevo hijo derecho
        padre.claves.insert(idx_hijo, clave_mediana)
        padre.valores.insert(idx_hijo, valor_mediana)
        padre.hijos.insert(idx_hijo + 1, hijo_der)

    # =========================================================================
    # Eliminación Completa con Préstamo, Fusión y Decrecimiento de Raíz
    # =========================================================================

    def eliminar(self, token: str) -> bool:
        """Elimina completamente un token del Árbol B preservando todas las invariantes.

        Casos cubiertos:
        1. Eliminación directa en nodo hoja.
        2. Eliminación en nodo interno mediante sustitución por el predecesor inorden
           (o sucesor inorden si el hijo derecho posee claves extra) y eliminación
           recursiva en el subárbol correspondiente.
        3. Reparación de subflujo (`len(hijo.claves) < min_claves`) al regresar:
           a. Préstamo desde el hermano izquierdo a través del separador del padre.
           b. Préstamo desde el hermano derecho a través del separador del padre.
           c. Fusión con hermano adyacente + descenso del separador del padre.
        4. Decrecimiento de altura de la raíz cuando la raíz queda sin claves tras una fusión.
        """
        token_limpio = token.strip()
        if not token_limpio or self._raiz is None:
            return False

        eliminado = self._eliminar_en_nodo(self._raiz, token_limpio)
        if not eliminado:
            return False

        self._tamanio -= 1

        # Si la raíz quedó sin claves tras una fusión de sus dos únicos hijos:
        if len(self._raiz.claves) == 0:
            if self._raiz.es_hoja:
                self._raiz = None
            else:
                self._raiz = self._raiz.hijos[0]

        return True

    def eliminar_referencias_archivo(self, archivo_id: str) -> int:
        """Elimina todas las referencias asociadas a `archivo_id` y purga tokens vacíos.

        Args:
            archivo_id: Identificador único inmutable del archivo.

        Returns:
            Cantidad de referencias eliminadas.
        """
        if self._raiz is None:
            return 0

        pares = self.inorden_detallado()
        tokens_a_eliminar: list[str] = []
        referencias_eliminadas = 0

        for token, _ in pares:
            nodo, idx = self._buscar_en_nodo(self._raiz, token)
            if nodo is None or idx < 0:
                continue
            originales = nodo.valores[idx]
            filtradas = [ref for ref in originales if ref.archivo_id != archivo_id]
            eliminadas_en_token = len(originales) - len(filtradas)
            if eliminadas_en_token > 0:
                referencias_eliminadas += eliminadas_en_token
                if filtradas:
                    nodo.valores[idx] = filtradas
                else:
                    tokens_a_eliminar.append(token)

        for token in tokens_a_eliminar:
            self.eliminar(token)

        return referencias_eliminadas

    def _eliminar_en_nodo(self, nodo: NodoB, token: str) -> bool:
        """Elimina recursivamente `token` del subárbol `nodo` y repara subflujos."""
        idx = 0
        num_claves = len(nodo.claves)
        while idx < num_claves and token > nodo.claves[idx]:
            idx += 1

        # Caso A: La clave `token` se encuentra en este nodo en la posición `idx`
        if idx < num_claves and nodo.claves[idx] == token:
            if nodo.es_hoja:
                nodo.claves.pop(idx)
                nodo.valores.pop(idx)
                return True

            # Nodo interno: sustituir por predecesor o sucesor inorden
            if (
                len(nodo.hijos[idx].claves) <= self._min_claves
                and len(nodo.hijos[idx + 1].claves) > self._min_claves
            ):
                # Sustitución por sucesor inorden (mínimo del hijo derecho)
                suc_clave, suc_valor = self._obtener_minimo(nodo.hijos[idx + 1])
                nodo.claves[idx] = suc_clave
                nodo.valores[idx] = list(suc_valor)
                self._eliminar_en_nodo(nodo.hijos[idx + 1], suc_clave)
                if len(nodo.hijos[idx + 1].claves) < self._min_claves:
                    self._reparar_subflujo(nodo, idx + 1)
            else:
                # Sustitución por predecesor inorden (máximo del hijo izquierdo)
                pred_clave, pred_valor = self._obtener_maximo(nodo.hijos[idx])
                nodo.claves[idx] = pred_clave
                nodo.valores[idx] = list(pred_valor)
                self._eliminar_en_nodo(nodo.hijos[idx], pred_clave)
                if len(nodo.hijos[idx].claves) < self._min_claves:
                    self._reparar_subflujo(nodo, idx)
            return True

        # Caso B: La clave no está en este nodo
        if nodo.es_hoja:
            return False

        eliminado = self._eliminar_en_nodo(nodo.hijos[idx], token)
        if eliminado and len(nodo.hijos[idx].claves) < self._min_claves:
            self._reparar_subflujo(nodo, idx)
        return eliminado

    def _obtener_maximo(self, nodo: NodoB) -> tuple[str, list[ReferenciaToken]]:
        """Encuentra la clave máxima (predecesor inorden) en el subárbol dado."""
        actual = nodo
        while not actual.es_hoja:
            actual = actual.hijos[-1]
        return actual.claves[-1], actual.valores[-1]

    def _obtener_minimo(self, nodo: NodoB) -> tuple[str, list[ReferenciaToken]]:
        """Encuentra la clave mínima (sucesor inorden) en el subárbol dado."""
        actual = nodo
        while not actual.es_hoja:
            actual = actual.hijos[0]
        return actual.claves[0], actual.valores[0]

    def _reparar_subflujo(self, padre: NodoB, idx_hijo: int) -> None:
        """Restaura el mínimo de claves en `padre.hijos[idx_hijo]` vía préstamo o fusión."""
        # 1. Intentar préstamo desde el hermano izquierdo si tiene claves de sobra
        if idx_hijo > 0 and len(padre.hijos[idx_hijo - 1].claves) > self._min_claves:
            self._prestar_de_izquierdo(padre, idx_hijo)
            return

        # 2. Intentar préstamo desde el hermano derecho si tiene claves de sobra
        if (
            idx_hijo < len(padre.hijos) - 1
            and len(padre.hijos[idx_hijo + 1].claves) > self._min_claves
        ):
            self._prestar_de_derecho(padre, idx_hijo)
            return

        # 3. Ningún hermano adyacente puede prestar: fusionar con un hermano y el separador
        if idx_hijo < len(padre.hijos) - 1:
            self._fusionar_hijos(padre, idx_hijo)
        else:
            self._fusionar_hijos(padre, idx_hijo - 1)

    def _prestar_de_izquierdo(self, padre: NodoB, idx_hijo: int) -> None:
        """Rota una clave desde el hermano izquierdo a través del separador del padre."""
        hijo = padre.hijos[idx_hijo]
        hermano_izq = padre.hijos[idx_hijo - 1]

        # El separador del padre baja al inicio del hijo con subflujo
        hijo.claves.insert(0, padre.claves[idx_hijo - 1])
        hijo.valores.insert(0, padre.valores[idx_hijo - 1])

        # La última clave del hermano izquierdo sube al padre como nuevo separador
        padre.claves[idx_hijo - 1] = hermano_izq.claves.pop()
        padre.valores[idx_hijo - 1] = hermano_izq.valores.pop()

        # Si son nodos internos, transferir también el último hijo del hermano izquierdo
        if not hijo.es_hoja:
            hijo.hijos.insert(0, hermano_izq.hijos.pop())

    def _prestar_de_derecho(self, padre: NodoB, idx_hijo: int) -> None:
        """Rota una clave desde el hermano derecho a través del separador del padre."""
        hijo = padre.hijos[idx_hijo]
        hermano_der = padre.hijos[idx_hijo + 1]

        # El separador del padre baja al final del hijo con subflujo
        hijo.claves.append(padre.claves[idx_hijo])
        hijo.valores.append(padre.valores[idx_hijo])

        # La primera clave del hermano derecho sube al padre como nuevo separador
        padre.claves[idx_hijo] = hermano_der.claves.pop(0)
        padre.valores[idx_hijo] = hermano_der.valores.pop(0)

        # Si son nodos internos, transferir también el primer hijo del hermano derecho
        if not hijo.es_hoja:
            hijo.hijos.append(hermano_der.hijos.pop(0))

    def _fusionar_hijos(self, padre: NodoB, idx_sep: int) -> None:
        """Fusiona `padre.hijos[idx_sep]` y `padre.hijos[idx_sep + 1]` bajando el separador."""
        hijo_izq = padre.hijos[idx_sep]
        hijo_der = padre.hijos[idx_sep + 1]

        # Bajar la clave separadora desde el padre
        hijo_izq.claves.append(padre.claves.pop(idx_sep))
        hijo_izq.valores.append(padre.valores.pop(idx_sep))

        # Concatenar todas las claves y valores del hermano derecho
        hijo_izq.claves.extend(hijo_der.claves)
        hijo_izq.valores.extend(hijo_der.valores)

        # Si son internos, concatenar los hijos del hermano derecho
        if not hijo_izq.es_hoja:
            hijo_izq.hijos.extend(hijo_der.hijos)

        # Desvincular el hermano derecho del padre
        padre.hijos.pop(idx_sep + 1)

    # =========================================================================
    # Recorridos Inorden y Validación Estructural
    # =========================================================================

    def inorden(self) -> list[str]:
        """Realiza el recorrido inorden multicamino devolviendo los tokens ordenados."""
        resultado: list[str] = []
        self._inorden_recursivo(self._raiz, resultado)
        return resultado

    def inorden_detallado(self) -> list[tuple[str, list[ReferenciaToken]]]:
        """Devuelve pares `(token, referencias)` en orden lexicográfico estricto."""
        resultado: list[tuple[str, list[ReferenciaToken]]] = []
        self._inorden_detallado_recursivo(self._raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo: Optional[NodoB], resultado: list[str]) -> None:
        if nodo is None:
            return
        num_claves = len(nodo.claves)
        for i in range(num_claves):
            if not nodo.es_hoja:
                self._inorden_recursivo(nodo.hijos[i], resultado)
            resultado.append(nodo.claves[i])
        if not nodo.es_hoja and len(nodo.hijos) > num_claves:
            self._inorden_recursivo(nodo.hijos[num_claves], resultado)

    def _inorden_detallado_recursivo(
        self,
        nodo: Optional[NodoB],
        resultado: list[tuple[str, list[ReferenciaToken]]],
    ) -> None:
        if nodo is None:
            return
        num_claves = len(nodo.claves)
        for i in range(num_claves):
            if not nodo.es_hoja:
                self._inorden_detallado_recursivo(nodo.hijos[i], resultado)
            resultado.append((nodo.claves[i], list(nodo.valores[i])))
        if not nodo.es_hoja and len(nodo.hijos) > num_claves:
            self._inorden_detallado_recursivo(nodo.hijos[num_claves], resultado)

    def es_valido(self) -> bool:
        """Verifica todas las invariantes de un Árbol B de orden m:
        1. Orden estricto de claves dentro de cada nodo.
        2. Límites de claves e hijos por nodo (raíz vs nodos internos/hojas).
        3. Todas las hojas ubicadas exactamente al mismo nivel.
        4. Separadores estrictos entre las claves del padre y los subárboles hijos.
        """
        if self._raiz is None:
            return self._tamanio == 0

        niveles_hojas: list[int] = []
        conteo_claves: list[int] = [0]
        valido = self._validar_nodo(
            nodo=self._raiz,
            es_raiz=True,
            nivel_actual=0,
            min_cota=None,
            max_cota=None,
            niveles_hojas=niveles_hojas,
            conteo_claves=conteo_claves,
        )
        if not valido:
            return False

        # Verificar que todas las hojas estén al mismo nivel
        if niveles_hojas:
            primer_nivel = niveles_hojas[0]
            for nivel in niveles_hojas:
                if nivel != primer_nivel:
                    return False

        return conteo_claves[0] == self._tamanio

    def _validar_nodo(
        self,
        nodo: NodoB,
        es_raiz: bool,
        nivel_actual: int,
        min_cota: Optional[str],
        max_cota: Optional[str],
        niveles_hojas: list[int],
        conteo_claves: list[int],
    ) -> bool:
        num_claves = len(nodo.claves)
        if num_claves != len(nodo.valores):
            return False

        # Límites de cantidad de claves
        if es_raiz:
            if num_claves < 1 or num_claves > self._max_claves:
                return False
        else:
            if num_claves < self._min_claves or num_claves > self._max_claves:
                return False

        # Orden estricto y cotas heredadas del padre
        for i in range(num_claves):
            clave = nodo.claves[i]
            if not nodo.valores[i]:
                return False
            if i > 0 and clave <= nodo.claves[i - 1]:
                return False
            if min_cota is not None and clave <= min_cota:
                return False
            if max_cota is not None and clave >= max_cota:
                return False

        conteo_claves[0] += num_claves

        if nodo.es_hoja:
            if len(nodo.hijos) != 0:
                return False
            niveles_hojas.append(nivel_actual)
            return True

        # Nodo interno: debe tener exactamente num_claves + 1 hijos
        if len(nodo.hijos) != num_claves + 1:
            return False
        if not es_raiz and len(nodo.hijos) < self._min_hijos:
            return False

        for i, hijo in enumerate(nodo.hijos):
            cota_inf = min_cota if i == 0 else nodo.claves[i - 1]
            cota_sup = max_cota if i == num_claves else nodo.claves[i]
            if not self._validar_nodo(
                nodo=hijo,
                es_raiz=False,
                nivel_actual=nivel_actual + 1,
                min_cota=cota_inf,
                max_cota=cota_sup,
                niveles_hojas=niveles_hojas,
                conteo_claves=conteo_claves,
            ):
                return False

        return True

