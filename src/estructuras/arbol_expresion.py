"""Módulo que implementa el Árbol de Expresiones Aritméticas con Shunting-Yard y evaluación postorden."""

from fractions import Fraction
from typing import List, Optional, Tuple, Union
from src.estructuras.nodo_expresion import NodoExpresion
from src.estructuras.pila import Pila
from src.excepciones.division_por_cero_error import DivisionPorCeroError
from src.excepciones.expresion_invalida_error import ExpresionInvalidaError


class ArbolExpresion:
    """Árbol Binario de Expresiones Aritméticas construido desde cero.
    
    Características técnicas:
    - Tokenizador léxico propio carácter por carácter (sin `eval()`, `ast` ni `re`).
    - Construcción mediante el algoritmo Shunting-Yard de Edsger Dijkstra apoyado en dos
      instancias de la `Pila` LIFO propia (pila de operadores y pila de subárboles).
    - Evaluación mediante recorrido en POSTORDEN utilizando `fractions.Fraction` para
      aritmética racional exacta, retornando `int` cuando el denominador es 1 y `float`
      cuando el resultado posee parte fraccionaria.
    """

    TOKEN_NUMERO = "NUMERO"
    TOKEN_OPERADOR = "OPERADOR"
    TOKEN_PAREN_IZQ = "PAREN_IZQ"
    TOKEN_PAREN_DER = "PAREN_DER"

    _PRECEDENCIA = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
    }

    def __init__(self, expresion: Optional[str] = None) -> None:
        self._raiz: Optional[NodoExpresion] = None
        self._expresion_original: str = ""
        if expresion is not None:
            self.construir(expresion)

    @property
    def raiz(self) -> Optional[NodoExpresion]:
        """Retorna el nodo raíz del árbol de expresión."""
        return self._raiz

    @property
    def expresion_original(self) -> str:
        """Retorna la cadena de expresión a partir de la cual se construyó el árbol."""
        return self._expresion_original

    def tokenizar(self, expresion: str) -> List[Tuple[str, str, int]]:
        """Analizador léxico manual que convierte la expresión en tokens `(tipo, valor, posicion)`.
        
        Soporta enteros, decimales, operadores `+ - * /`, paréntesis `()` y signo menos unario.
        Lanza `ExpresionInvalidaError` indicando la posición exacta (base 1) ante errores léxicos.
        """
        if not expresion or not expresion.strip():
            raise ExpresionInvalidaError("La expresión aritmética está vacía.")

        tokens: List[Tuple[str, str, int]] = []
        n = len(expresion)
        i = 0

        while i < n:
            ch = expresion[i]
            pos = i + 1

            # 1. Ignorar espacios en blanco
            if ch in (" ", "\t", "\n", "\r"):
                i += 1
                continue

            # 2. Paréntesis
            if ch == "(":
                tokens.append((self.TOKEN_PAREN_IZQ, "(", pos))
                i += 1
                continue

            if ch == ")":
                tokens.append((self.TOKEN_PAREN_DER, ")", pos))
                i += 1
                continue

            # 3. Detectar si un signo '-' o '+' está en posición unaria
            es_posicion_unaria = (
                len(tokens) == 0
                or tokens[-1][0] in (self.TOKEN_OPERADOR, self.TOKEN_PAREN_IZQ)
            )

            if ch in ("+", "-") and es_posicion_unaria:
                # Mirar el siguiente carácter no blanco
                j = i + 1
                while j < n and expresion[j] in (" ", "\t"):
                    j += 1

                if j >= n:
                    raise ExpresionInvalidaError(
                        f"Operador '{ch}' sin operando en la posición {pos}."
                    )

                sig = expresion[j]
                if ch == "+":
                    # El más unario frente a número o paréntesis es neutro si le sigue operando válido
                    if sig.isdigit() or sig == "." or sig == "(":
                        i += 1
                        continue
                    raise ExpresionInvalidaError(
                        f"Operador '+' inesperado en la posición {pos}."
                    )

                # Caso menos unario ('-')
                if sig.isdigit() or sig == ".":
                    # Leer literal numérico negativo como hoja operando (ej. -5, -3.14)
                    inicio_num = i
                    i = j
                    tiene_punto = False
                    tiene_digito = False
                    while i < n and (expresion[i].isdigit() or expresion[i] == "."):
                        if expresion[i] == ".":
                            if tiene_punto:
                                raise ExpresionInvalidaError(
                                    f"Número decimal inválido con múltiples puntos en la posición {i + 1}."
                                )
                            tiene_punto = True
                        else:
                            tiene_digito = True
                        i += 1

                    if not tiene_digito:
                        raise ExpresionInvalidaError(
                            f"Punto decimal aislado sin dígitos en la posición {pos}."
                        )
                    lexema_neg = "-" + expresion[j:i]
                    tokens.append((self.TOKEN_NUMERO, lexema_neg, inicio_num + 1))
                    continue

                if sig in ("(", "-"):
                    # Menos unario ante paréntesis o doble negación: expandir como '0 - ...'
                    # para preservar que todo nodo operador interno tenga exactamente dos hijos
                    tokens.append((self.TOKEN_NUMERO, "0", pos))
                    tokens.append((self.TOKEN_OPERADOR, "-", pos))
                    i += 1
                    continue

                raise ExpresionInvalidaError(
                    f"Operador '-' sin operando válido en la posición {pos}."
                )

            # 4. Números positivos (enteros o decimales)
            if ch.isdigit() or ch == ".":
                inicio = i
                tiene_punto = False
                tiene_digito = False
                while i < n and (expresion[i].isdigit() or expresion[i] == "."):
                    if expresion[i] == ".":
                        if tiene_punto:
                            raise ExpresionInvalidaError(
                                f"Número decimal mal formado en la posición {i + 1}."
                            )
                        tiene_punto = True
                    else:
                        tiene_digito = True
                    i += 1

                if not tiene_digito:
                    raise ExpresionInvalidaError(
                        f"Punto decimal sin dígitos en la posición {pos}."
                    )

                tokens.append((self.TOKEN_NUMERO, expresion[inicio:i], pos))
                continue

            # 5. Operadores binarios
            if ch in self._PRECEDENCIA:
                tokens.append((self.TOKEN_OPERADOR, ch, pos))
                i += 1
                continue

            # 6. Cualquier otro carácter es inválido
            raise ExpresionInvalidaError(
                f"Carácter inválido '{ch}' en la posición {pos}."
            )

        return tokens

    def construir(self, expresion: str) -> NodoExpresion:
        """Construye el árbol binario de expresión usando Shunting-Yard y dos Pilas propias."""
        self._expresion_original = expresion
        tokens = self.tokenizar(expresion)

        pila_operadores = Pila()
        pila_nodos = Pila()
        tipo_anterior: Optional[str] = None

        for tipo, valor, pos in tokens:
            if tipo == self.TOKEN_NUMERO:
                if tipo_anterior in (self.TOKEN_NUMERO, self.TOKEN_PAREN_DER):
                    raise ExpresionInvalidaError(
                        f"Falta un operador antes de '{valor}' en la posición {pos}."
                    )
                pila_nodos.apilar(NodoExpresion(valor))

            elif tipo == self.TOKEN_PAREN_IZQ:
                if tipo_anterior in (self.TOKEN_NUMERO, self.TOKEN_PAREN_DER):
                    raise ExpresionInvalidaError(
                        f"Falta un operador antes de '(' en la posición {pos}."
                    )
                pila_operadores.apilar((valor, pos))

            elif tipo == self.TOKEN_PAREN_DER:
                if tipo_anterior == self.TOKEN_PAREN_IZQ:
                    raise ExpresionInvalidaError(
                        f"Paréntesis vacíos '()' en la posición {pos}."
                    )
                if tipo_anterior == self.TOKEN_OPERADOR or tipo_anterior is None:
                    raise ExpresionInvalidaError(
                        f"Cierre de paréntesis ')' inesperado en la posición {pos}."
                    )

                encontro_apertura = False
                while not pila_operadores.esta_vacia():
                    op_cima, pos_cima = pila_operadores.cima()
                    if op_cima == "(":
                        pila_operadores.desapilar()
                        encontro_apertura = True
                        break
                    self._reducir_subarbol(pila_operadores, pila_nodos)

                if not encontro_apertura:
                    raise ExpresionInvalidaError(
                        f"Paréntesis de cierre ')' sin apertura en la posición {pos}."
                    )

            elif tipo == self.TOKEN_OPERADOR:
                if tipo_anterior is None or tipo_anterior in (self.TOKEN_OPERADOR, self.TOKEN_PAREN_IZQ):
                    raise ExpresionInvalidaError(
                        f"Operador '{valor}' sin operando izquierdo en la posición {pos}."
                    )

                prec_actual = self._PRECEDENCIA[valor]
                # Asociatividad izquierda: desapilar mientras precedencia en cima >= actual
                while not pila_operadores.esta_vacia():
                    op_cima, _ = pila_operadores.cima()
                    if op_cima == "(":
                        break
                    if self._PRECEDENCIA[op_cima] >= prec_actual:
                        self._reducir_subarbol(pila_operadores, pila_nodos)
                    else:
                        break

                pila_operadores.apilar((valor, pos))

            tipo_anterior = tipo

        if tipo_anterior == self.TOKEN_OPERADOR:
            _, op_final, pos_final = tokens[-1]
            raise ExpresionInvalidaError(
                f"El operador '{op_final}' en la posición {pos_final} carece de operando derecho."
            )

        while not pila_operadores.esta_vacia():
            op_cima, pos_cima = pila_operadores.cima()
            if op_cima == "(":
                raise ExpresionInvalidaError(
                    f"Paréntesis '(' abierto en la posición {pos_cima} nunca fue cerrado."
                )
            self._reducir_subarbol(pila_operadores, pila_nodos)

        if len(pila_nodos) != 1:
            raise ExpresionInvalidaError("La expresión aritmética está incompleta o mal formada.")

        self._raiz = pila_nodos.desapilar()
        return self._raiz

    def _reducir_subarbol(self, pila_operadores: Pila, pila_nodos: Pila) -> None:
        """Extrae un operador y dos subárboles de las pilas para enlazar un nuevo NodoExpresion."""
        op, pos = pila_operadores.desapilar()
        if len(pila_nodos) < 2:
            raise ExpresionInvalidaError(
                f"El operador '{op}' en la posición {pos} requiere dos operandos."
            )
        hijo_derecho: NodoExpresion = pila_nodos.desapilar()
        hijo_izquierdo: NodoExpresion = pila_nodos.desapilar()
        nuevo_nodo = NodoExpresion(op, izquierdo=hijo_izquierdo, derecho=hijo_derecho)
        pila_nodos.apilar(nuevo_nodo)

    def evaluar_exacto(self) -> Fraction:
        """Evalúa el árbol mediante recorrido en POSTORDEN usando aritmética racional exacta (`Fraction`)."""
        if self._raiz is None:
            raise ExpresionInvalidaError("El árbol de expresión está vacío.")
        return self._evaluar_postorden(self._raiz)

    def evaluar(self) -> Union[int, float]:
        """Evalúa el árbol en postorden y retorna `int` si el valor es exacto entero, o `float` si es decimal."""
        fraccion = self.evaluar_exacto()
        if fraccion.denominator == 1:
            return int(fraccion.numerator)
        return float(fraccion)

    def formatear_resultado(self) -> str:
        """Retorna la representación textual limpia del resultado (entero o decimal sin ruido de punto flotante)."""
        valor = self.evaluar()
        if isinstance(valor, int):
            return str(valor)
        # Limpiar posibles colas de representación binaria IEEE 754
        texto = f"{valor:.10f}".rstrip("0").rstrip(".")
        return texto

    def _evaluar_postorden(self, nodo: NodoExpresion) -> Fraction:
        """Recorrido en POSTORDEN (Izquierda -> Derecha -> Raíz) para evaluar subexpresiones."""
        if nodo.es_hoja:
            try:
                return Fraction(nodo.valor)
            except (ValueError, ZeroDivisionError) as e:
                raise ExpresionInvalidaError(f"Operando numérico inválido '{nodo.valor}': {e}")

        if nodo.izquierdo is None or nodo.derecho is None:
            raise ExpresionInvalidaError(
                f"Invariante violado: el operador '{nodo.valor}' no posee exactamente dos hijos."
            )

        # Paso 1: Evaluar subárbol izquierdo
        val_izq = self._evaluar_postorden(nodo.izquierdo)
        # Paso 2: Evaluar subárbol derecho
        val_der = self._evaluar_postorden(nodo.derecho)

        # Paso 3: Procesar raíz (operador)
        match nodo.valor:
            case "+":
                return val_izq + val_der
            case "-":
                return val_izq - val_der
            case "*":
                return val_izq * val_der
            case "/":
                if val_der == 0:
                    raise DivisionPorCeroError("Error matemático: división por cero detectada.")
                return val_izq / val_der
            case _:
                raise ExpresionInvalidaError(f"Operador desconocido '{nodo.valor}'.")

    def preorden(self) -> str:
        """Retorna la notación prefija (Polaca) mediante recorrido Preorden (Raíz, Izquierda, Derecha)."""
        tokens: List[str] = []
        self._preorden_rec(self._raiz, tokens)
        return " ".join(tokens)

    def _preorden_rec(self, nodo: Optional[NodoExpresion], salida: List[str]) -> None:
        if nodo is not None:
            salida.append(nodo.valor)
            self._preorden_rec(nodo.izquierdo, salida)
            self._preorden_rec(nodo.derecho, salida)

    def postorden(self) -> str:
        """Retorna la notación postfija (Polaca Inversa / RPN) mediante recorrido Postorden."""
        tokens: List[str] = []
        self._postorden_rec(self._raiz, tokens)
        return " ".join(tokens)

    def _postorden_rec(self, nodo: Optional[NodoExpresion], salida: List[str]) -> None:
        if nodo is not None:
            self._postorden_rec(nodo.izquierdo, salida)
            self._postorden_rec(nodo.derecho, salida)
            salida.append(nodo.valor)

    def inorden(self) -> str:
        """Retorna la notación infija mediante recorrido Inorden colocando paréntesis solo donde hace falta."""
        if self._raiz is None:
            return ""
        return self._inorden_con_parentesis_minimos(self._raiz)

    def _inorden_con_parentesis_minimos(self, nodo: NodoExpresion) -> str:
        if nodo.es_hoja:
            return nodo.valor

        assert nodo.izquierdo is not None and nodo.derecho is not None
        prec_padre = self._PRECEDENCIA.get(nodo.valor, 0)

        texto_izq = self._inorden_con_parentesis_minimos(nodo.izquierdo)
        if nodo.izquierdo.es_operador:
            prec_izq = self._PRECEDENCIA.get(nodo.izquierdo.valor, 0)
            if prec_izq < prec_padre:
                texto_izq = f"({texto_izq})"

        texto_der = self._inorden_con_parentesis_minimos(nodo.derecho)
        if nodo.derecho.es_operador:
            prec_der = self._PRECEDENCIA.get(nodo.derecho.valor, 0)
            # Para '-' y '/', igual precedencia a la derecha también requiere paréntesis: a - (b - c)
            requiere_por_asociatividad = prec_der == prec_padre and nodo.valor in ("-", "/")
            if prec_der < prec_padre or requiere_por_asociatividad:
                texto_der = f"({texto_der})"

        return f"{texto_izq} {nodo.valor} {texto_der}"

    def dibujar_arbol(self) -> List[str]:
        """Genera una representación visual ASCII del árbol de expresión con conectores ├── y └──."""
        if self._raiz is None:
            return ["(Árbol de expresión vacío)"]

        lineas: List[str] = [self._raiz.valor]
        if not self._raiz.es_hoja:
            hijos = [h for h in (self._raiz.izquierdo, self._raiz.derecho) if h is not None]
            for idx, hijo in enumerate(hijos):
                es_ultimo = (idx == len(hijos) - 1)
                self._dibujar_subarbol(hijo, "", es_ultimo, lineas)
        return lineas

    def _dibujar_subarbol(
        self,
        nodo: NodoExpresion,
        prefijo: str,
        es_ultimo: bool,
        lineas: List[str],
    ) -> None:
        conector = "└── " if es_ultimo else "├── "
        lineas.append(f"{prefijo}{conector}{nodo.valor}")
        if not nodo.es_hoja:
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            hijos = [h for h in (nodo.izquierdo, nodo.derecho) if h is not None]
            for idx, hijo in enumerate(hijos):
                self._dibujar_subarbol(hijo, nuevo_prefijo, idx == len(hijos) - 1, lineas)

