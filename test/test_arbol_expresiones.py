"""Pruebas unitarias para la Fase 2: NodoExpresion, ArbolExpresion, ServicioExpresiones y ComandoEval."""

import io
from contextlib import redirect_stdout
import unittest

from src.comandos.comando_eval import ComandoEval
from src.estructuras.arbol_expresion import ArbolExpresion
from src.estructuras.nodo_expresion import NodoExpresion
from src.excepciones.division_por_cero_error import DivisionPorCeroError
from src.excepciones.expresion_invalida_error import ExpresionInvalidaError
from src.nucleo.archivo_codigo import ArchivoCodigo
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_expresiones import ServicioExpresiones


class TestArbolExpresiones(unittest.TestCase):
    """Pruebas exhaustivas para el Árbol de Expresiones Aritméticas."""

    def setUp(self) -> None:
        self.servicio = ServicioExpresiones()

    def _verificar_invariante_binario_estricto(self, nodo: NodoExpresion) -> None:
        """Verifica recursivamente que hojas sean operandos y nodos internos tengan exactamente 2 hijos."""
        if nodo.es_hoja:
            self.assertIsNone(nodo.izquierdo)
            self.assertIsNone(nodo.derecho)
            self.assertFalse(nodo.es_operador)
        else:
            self.assertTrue(nodo.es_operador)
            self.assertIsNotNone(nodo.izquierdo)
            self.assertIsNotNone(nodo.derecho)
            self._verificar_invariante_binario_estricto(nodo.izquierdo)
            self._verificar_invariante_binario_estricto(nodo.derecho)

    def test_precedencia_y_asociatividad_izquierda(self) -> None:
        arbol1 = ArbolExpresion("2 + 3 * 4")
        self.assertEqual(arbol1.evaluar(), 14)
        self.assertIsInstance(arbol1.evaluar(), int)
        self._verificar_invariante_binario_estricto(arbol1.raiz)

        # Asociatividad izquierda: 8 - 3 - 2 = (8 - 3) - 2 = 3 (no 8 - (3 - 2) = 7)
        arbol2 = ArbolExpresion("8-3-2")
        self.assertEqual(arbol2.evaluar(), 3)

        # Asociatividad izquierda en división: 16 / 4 / 2 = (16 / 4) / 2 = 2
        arbol3 = ArbolExpresion("16 / 4 / 2")
        self.assertEqual(arbol3.evaluar(), 2)
        self.assertIsInstance(arbol3.evaluar(), int)

    def test_parentesis_anidados_y_menos_unario(self) -> None:
        arbol = ArbolExpresion("((4 + 8) * (5 - 2)) / 6")
        self.assertEqual(arbol.evaluar(), 6)
        self._verificar_invariante_binario_estricto(arbol.raiz)

        # Menos unario frente a números y frente a paréntesis
        self.assertEqual(ArbolExpresion("-5 + 3").evaluar(), -2)
        self.assertEqual(ArbolExpresion("4 * -2.5").evaluar(), -10)
        arbol_paren_neg = ArbolExpresion("-(3 + 2) * 4")
        self.assertEqual(arbol_paren_neg.evaluar(), -20)
        self._verificar_invariante_binario_estricto(arbol_paren_neg.raiz)

    def test_decimales_y_precision_exacta_fraction(self) -> None:
        # En punto flotante estándar 0.1 + 0.2 = 0.30000000000000004; con Fraction es 3/10 exacto
        arbol = ArbolExpresion("0.1 + 0.2")
        self.assertEqual(arbol.formatear_resultado(), "0.3")

        arbol_div = ArbolExpresion("5 / 2")
        self.assertEqual(arbol_div.evaluar(), 2.5)
        self.assertEqual(arbol_div.formatear_resultado(), "2.5")

        arbol_entero = ArbolExpresion("7.5 + 2.5")
        self.assertEqual(arbol_entero.evaluar(), 10)
        self.assertIsInstance(arbol_entero.evaluar(), int)
        self.assertEqual(arbol_entero.formatear_resultado(), "10")

    def test_tres_recorridos_sobre_5_mas_3_por_2(self) -> None:
        arbol = ArbolExpresion("(5+3)*2")
        self.assertEqual(arbol.evaluar(), 16)
        self.assertEqual(arbol.preorden(), "* + 5 3 2")
        self.assertEqual(arbol.postorden(), "5 3 + 2 *")
        self.assertEqual(arbol.inorden(), "(5 + 3) * 2")

        # En 5 + 3 * 2, el inorden NO requiere paréntesis porque * tiene mayor precedencia
        arbol_sin_paren = ArbolExpresion("5 + 3 * 2")
        self.assertEqual(arbol_sin_paren.inorden(), "5 + 3 * 2")

        # En 8 - (3 - 2), el inorden conserva paréntesis a la derecha por asociatividad
        arbol_resta_der = ArbolExpresion("8 - (3 - 2)")
        self.assertEqual(arbol_resta_der.inorden(), "8 - (3 - 2)")
        self.assertEqual(arbol_resta_der.evaluar(), 7)

    def test_division_por_cero_lanza_excepcion_propia(self) -> None:
        arbol = ArbolExpresion("10 / (5 - 5)")
        with self.assertRaises(DivisionPorCeroError):
            arbol.evaluar()

    def test_errores_sintaxis_y_posicion(self) -> None:
        expresiones_invalidas = [
            "",
            "   ",
            "(5 + 3",
            "5 + 3)",
            "()",
            "5 +",
            "* 5",
            "5 3",
            "5 + $",
            "3.1.4 + 1",
            ". + 2",
            "5 + * 3",
        ]
        for expr in expresiones_invalidas:
            with self.subTest(expresion=expr):
                with self.assertRaises(ExpresionInvalidaError):
                    ArbolExpresion(expr)

    def test_comando_eval_con_tree_y_en_archivo_activo(self) -> None:
        contexto = ContextoApp()
        contexto.archivo_activo = ArchivoCodigo(
            "calculos.py",
            "a = (4 + 8) * 3\nb = 10 / 4\n# comentario\ntexto = 'hola'",
        )
        cmd = ComandoEval(self.servicio, contexto)

        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertTrue(cmd.ejecutar(["(5+3)*2", "--tree"]))
        salida = buf.getvalue()
        self.assertIn("Resultado: 16", salida)
        self.assertIn("5 3 + 2 *", salida)
        self.assertIn("├── +", salida)

        # Eval sin argumentos analiza el archivo activo línea por línea
        buf_archivo = io.StringIO()
        with redirect_stdout(buf_archivo):
            self.assertTrue(cmd.ejecutar([]))
        salida_arch = buf_archivo.getvalue()
        self.assertIn("36", salida_arch)
        self.assertIn("2.5", salida_arch)


if __name__ == "__main__":
    unittest.main()

