"""Módulo del servicio encargado de la verificación de sintaxis y balanceo de delimitadores."""

from typing import Dict, List, Tuple
from src.estructuras.pila import Pila
from src.nucleo.diagnostico import Diagnostico


class ServicioSintaxis:
    """Valida el anidamiento y equilibrio de símbolos de agrupación: (), {}, [].
    
    Emplea internamente una Pila LIFO desarrollada desde cero para reportar con precisión
    el número de línea y columna exacta ante cualquier desbalance o delimitador sin cerrar.
    """

    _PAREJAS: Dict[str, str] = {
        ")": "(",
        "}": "{",
        "]": "[",
    }
    _APERTURAS = set(_PAREJAS.values())
    _CIERRES = set(_PAREJAS.keys())

    def __init__(self) -> None:
        self._pila: Pila = Pila()

    def validar_codigo(self, codigo: str) -> Tuple[bool, List[Diagnostico]]:
        """Analiza el código y retorna una tupla (es_valido, lista_diagnosticos).
        
        Si los delimitadores están balanceados, retorna True y un diagnóstico INFO.
        Si hay discrepancias, retorna False y diagnósticos de nivel ERROR detallando
        línea y carácter del fallo.
        """
        self._pila.limpiar()
        diagnosticos: List[Diagnostico] = []

        lineas = codigo.splitlines(keepends=True)
        for num_linea, linea_texto in enumerate(lineas, start=1):
            for num_col, caracter in enumerate(linea_texto, start=1):
                if caracter in self._APERTURAS:
                    # Apila una tupla con el símbolo, línea y columna
                    self._pila.apilar((caracter, num_linea, num_col))

                elif caracter in self._CIERRES:
                    esperado = self._PAREJAS[caracter]

                    if self._pila.esta_vacia():
                        msg = f"Símbolo de cierre inesperado '{caracter}' sin apertura correspondiente."
                        diagnosticos.append(Diagnostico(num_linea, "ERROR", msg, columna=num_col))
                    else:
                        apertura, linea_ap, col_ap = self._pila.desapilar()
                        if apertura != esperado:
                            msg = (
                                f"Desbalance de delimitadores: se cerró con '{caracter}' "
                                f"pero se esperaba el cierre de '{apertura}' (abierto en línea {linea_ap}, col {col_ap})."
                            )
                            diagnosticos.append(Diagnostico(num_linea, "ERROR", msg, columna=num_col))

        # Verificar si quedaron delimitadores abiertos sin cerrar en la pila
        while not self._pila.esta_vacia():
            apertura, linea_ap, col_ap = self._pila.desapilar()
            msg = f"Delimitador sin cerrar: '{apertura}' abierto en línea {linea_ap}, col {col_ap} nunca fue cerrado."
            diagnosticos.append(Diagnostico(linea_ap, "ERROR", msg, columna=col_ap))

        if not diagnosticos:
            diag_exito = Diagnostico(
                1, "INFO", "Sintaxis balanceada: todos los delimitadores () {} [] están en equilibrio."
            )
            return True, [diag_exito]

        return False, diagnosticos
