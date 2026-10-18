"""Pruebas unitarias exhaustivas para Fase 3: Árbol AVL y ServicioDiccionario."""

import io
import math
import random
import unittest
from contextlib import redirect_stdout

from src.comandos.comando_add_keyword import ComandoAddKeyword
from src.comandos.comando_remove_keyword import ComandoRemoveKeyword
from src.comandos.comando_suggest import ComandoSuggest
from src.estructuras.arbol_avl import ArbolAVL
from src.excepciones.palabra_duplicada_error import PalabraDuplicadaError
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_diccionario import ServicioDiccionario


class TestArbolAVL(unittest.TestCase):
    """Suite de pruebas para NodoAVL, ArbolAVL, rotaciones, poda y ServicioDiccionario."""

    def test_rotacion_ll_izquierda_izquierda(self) -> None:
        """Verifica la rotación simple derecha (Caso LL) ante inserción descendente."""
        avl = ArbolAVL()
        avl.insertar("c", "tercero")
        avl.insertar("b", "segundo")
        avl.insertar("a", "primero")

        self.assertIsNotNone(avl.raiz)
        self.assertEqual(avl.raiz.palabra, "b")
        self.assertEqual(avl.raiz.izquierdo.palabra, "a")
        self.assertEqual(avl.raiz.derecho.palabra, "c")
        self.assertEqual(avl.altura, 2)
        self.assertTrue(avl.es_valido())

    def test_rotacion_rr_derecha_derecha(self) -> None:
        """Verifica la rotación simple izquierda (Caso RR) ante inserción ascendente."""
        avl = ArbolAVL()
        avl.insertar("a", "primero")
        avl.insertar("b", "segundo")
        avl.insertar("c", "tercero")

        self.assertIsNotNone(avl.raiz)
        self.assertEqual(avl.raiz.palabra, "b")
        self.assertEqual(avl.raiz.izquierdo.palabra, "a")
        self.assertEqual(avl.raiz.derecho.palabra, "c")
        self.assertEqual(avl.altura, 2)
        self.assertTrue(avl.es_valido())

    def test_rotacion_lr_izquierda_derecha(self) -> None:
        """Verifica la rotación doble izquierda-derecha (Caso LR)."""
        avl = ArbolAVL()
        avl.insertar("c", "tercero")
        avl.insertar("a", "primero")
        avl.insertar("b", "segundo")

        self.assertIsNotNone(avl.raiz)
        self.assertEqual(avl.raiz.palabra, "b")
        self.assertEqual(avl.raiz.izquierdo.palabra, "a")
        self.assertEqual(avl.raiz.derecho.palabra, "c")
        self.assertEqual(avl.altura, 2)
        self.assertTrue(avl.es_valido())

    def test_rotacion_rl_derecha_izquierda(self) -> None:
        """Verifica la rotación doble derecha-izquierda (Caso RL)."""
        avl = ArbolAVL()
        avl.insertar("a", "primero")
        avl.insertar("c", "tercero")
        avl.insertar("b", "segundo")

        self.assertIsNotNone(avl.raiz)
        self.assertEqual(avl.raiz.palabra, "b")
        self.assertEqual(avl.raiz.izquierdo.palabra, "a")
        self.assertEqual(avl.raiz.derecho.palabra, "c")
        self.assertEqual(avl.altura, 2)
        self.assertTrue(avl.es_valido())

    def test_inserciones_ascendentes_quedan_balanceadas(self) -> None:
        """Verifica que N inserciones en orden ascendente no degeneren en lista."""
        avl = ArbolAVL()
        n = 127
        for i in range(1, n + 1):
            avl.insertar(f"item_{i:04d}", f"Item {i}")

        self.assertEqual(avl.tamanio, n)
        self.assertTrue(avl.es_valido())
        # Con 127 inserciones estrictamente ascendentes, las rotaciones RR mantienen
        # un árbol perfectamente balanceado de altura log2(127+1) = 7 (frente a 127 en BST).
        cota_teorica_avl = math.ceil(1.44 * math.log2(n + 2))
        self.assertLessEqual(avl.altura, cota_teorica_avl)
        self.assertEqual(avl.altura, 7)

    def test_palabra_duplicada_lanza_excepcion(self) -> None:
        """Verifica que insertar una clave repetida lance PalabraDuplicadaError."""
        avl = ArbolAVL()
        avl.insertar("async", "Corrutina")
        with self.assertRaises(PalabraDuplicadaError):
            avl.insertar("async", "Duplicada")

    def test_eliminacion_tres_casos_y_rebalanceo(self) -> None:
        """Verifica eliminación de hoja, nodo con 1 hijo, nodo con 2 hijos y rebalanceo."""
        avl = ArbolAVL()
        palabras = ["m", "f", "t", "c", "h", "p", "x", "a", "d", "g", "j", "r", "z"]
        for p in palabras:
            avl.insertar(p, f"Desc {p}")
            self.assertTrue(avl.es_valido())

        # 1. Eliminar hoja ("a")
        self.assertTrue(avl.eliminar("a"))
        self.assertFalse(avl.contiene("a"))
        self.assertTrue(avl.es_valido())

        # 2. Eliminar nodo con un solo hijo ("c" ahora solo tiene hijo derecho "d")
        self.assertTrue(avl.eliminar("c"))
        self.assertFalse(avl.contiene("c"))
        self.assertTrue(avl.contiene("d"))
        self.assertTrue(avl.es_valido())

        # 3. Eliminar nodo con dos hijos (la raíz "m")
        self.assertTrue(avl.eliminar("m"))
        self.assertFalse(avl.contiene("m"))
        self.assertTrue(avl.es_valido())

        # 4. Eliminar el resto verificando invariantes en cada paso
        restantes = avl.inorden()
        for p in restantes:
            self.assertTrue(avl.eliminar(p))
            self.assertTrue(avl.es_valido())

        self.assertEqual(avl.tamanio, 0)
        self.assertEqual(avl.altura, 0)
        self.assertFalse(avl.eliminar("inexistente"))

    def test_1000_inserciones_aleatorias_y_es_valido(self) -> None:
        """Prueba de estrés con 1000 inserciones aleatorias y validación estructural."""
        rng = random.Random(42)
        universo = [f"kw_{i:05d}" for i in range(1000)]
        rng.shuffle(universo)

        avl = ArbolAVL()
        for palabra in universo:
            avl.insertar(palabra, "Generada aleatoriamente")

        self.assertEqual(avl.tamanio, 1000)
        self.assertTrue(avl.es_valido())

        recorrido = avl.inorden()
        self.assertEqual(len(recorrido), 1000)
        for idx in range(len(recorrido) - 1):
            self.assertLess(recorrido[idx], recorrido[idx + 1])

        # Eliminar 300 elementos aleatorios y comprobar que sigue siendo un AVL válido
        for palabra in universo[:300]:
            self.assertTrue(avl.eliminar(palabra))
        self.assertEqual(avl.tamanio, 700)
        self.assertTrue(avl.es_valido())

    def test_sugerir_con_poda_casos_borde(self) -> None:
        """Verifica autocompletado con prefijo válido, sin coincidencias y prefijo vacío."""
        contexto = ContextoApp()
        servicio = ServicioDiccionario(contexto)

        # 35 palabras reservadas de Python precargadas y árbol válido
        self.assertEqual(servicio.arbol.tamanio, 35)
        self.assertTrue(servicio.arbol.es_valido())

        # Prefijo con múltiples coincidencias ordenadas alfabéticamente
        sug_in = servicio.sugerir("in")
        self.assertEqual(sug_in, ["in"])

        sug_as = servicio.sugerir("as")
        self.assertEqual(sug_as, ["as", "assert", "async"])

        # Prefijo sin coincidencias
        self.assertEqual(servicio.sugerir("xyz_inexistente"), [])

        # Prefijo vacío devuelve todas las palabras en orden alfabético
        todas = servicio.sugerir("")
        self.assertEqual(len(todas), 35)
        self.assertEqual(todas, servicio.arbol.inorden())

    def test_comandos_cli_diccionario(self) -> None:
        """Verifica los comandos add-keyword, suggest y remove-keyword."""
        contexto = ContextoApp()
        servicio = ServicioDiccionario(contexto)
        cmd_add = ComandoAddKeyword(servicio)
        cmd_sug = ComandoSuggest(servicio)
        cmd_rem = ComandoRemoveKeyword(servicio)

        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_add.ejecutar(["struct", "Estructura", "de", "datos", "compuesta."])
            cmd_sug.ejecutar(["st"])
        salida = buf.getvalue()
        self.assertIn("struct", salida)
        self.assertIn("Estructura de datos compuesta.", salida)

        buf_rem = io.StringIO()
        with redirect_stdout(buf_rem):
            cmd_rem.ejecutar(["struct"])
        self.assertIn("eliminada", buf_rem.getvalue())
        self.assertFalse(servicio.es_palabra_reservada("struct"))


if __name__ == "__main__":
    unittest.main()

