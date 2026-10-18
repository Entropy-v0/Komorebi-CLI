"""Prueba de integración de extremo a extremo (E2E) para la Fase 2 de Komorebi Mini IDE."""

import ast
import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout

from main import bootstrap


class TestIntegracionFase2(unittest.TestCase):
    """Ejecuta un escenario completo por el REPL integrando las 4 estructuras arbóreas."""

    def setUp(self) -> None:
        self._dir_temp = tempfile.mkdtemp(prefix="komorebi_e2e_")
        self._ruta_config = os.path.join(self._dir_temp, "config_e2e.json")
        self._ruta_respaldos = os.path.join(self._dir_temp, "respaldos")
        self._ruta_logs = os.path.join(self._dir_temp, "logs")

        with open(self._ruta_config, "w", encoding="utf-8") as f:
            f.write(
                "{\n"
                f'  "ruta_respaldos": "{self._ruta_respaldos}",\n'
                f'  "ruta_logs": "{self._ruta_logs}",\n'
                '  "api_key_ia": ""\n'
                "}\n"
            )

    def tearDown(self) -> None:
        shutil.rmtree(self._dir_temp, ignore_errors=True)

    def test_escenario_completo_repl_y_coherencia_estructuras(self) -> None:
        """Ejecuta el flujo completo por ConsolaApp verificando N-ario, Lista, AVL, B-Tree y disco."""
        consola = bootstrap(self._ruta_config)
        contexto = consola._contexto  # acceso de inspección para la prueba E2E

        comandos_repl = [
            "mkdir src",
            "cd ws:/src",
            "pwd",
            "new app.py",
            'edit "def calcular(tasa_interes):"',
            'edit "    monto_final = (4 + 8) * 3"',
            'edit "    return monto_final"',
            'eval "(4+8)*3" --tree',
            'add-keyword struct "Estructura de datos compuesta"',
            "suggest st",
            "index-all",
            "find-global monto_final",
            "cd ws:/",
            "mkdir core",
            "mv /src/app.py /core/app.py",
            "tree",
            "find-global monto_final",
            "clear",
            "cls",
            "help",
        ]

        buffer_salida = io.StringIO()
        with redirect_stdout(buffer_salida):
            for linea in comandos_repl:
                continuar = consola.ejecutar_linea(linea)
                self.assertTrue(continuar, f"El comando '{linea}' detuvo el REPL inesperadamente.")

        salida = buffer_salida.getvalue()

        # 1. Verificación del evaluador de expresiones (Árbol Binario de Expresiones)
        self.assertIn("36", salida)
        self.assertIn("4 + 8", salida)

        # 2. Verificación del diccionario y autocompletado con poda (Árbol AVL)
        self.assertIn("struct", salida)
        self.assertTrue(contexto.diccionario.es_valido())
        self.assertIn("struct", contexto.diccionario.sugerir("st"))

        # 3. Verificación del índice global (Árbol B de orden m=4)
        self.assertTrue(contexto.indice_global.es_valido())
        self.assertIn("/core/app.py", salida)
        self.assertIn("2, 3", salida)

        # 4. Coherencia estricta entre Árbol N-ario, ListaEnlazada y respaldos en disco
        nodo_en_core = contexto.workspace.resolver_ruta("/core/app.py")
        self.assertTrue(nodo_en_core.es_archivo)
        archivo_nario = nodo_en_core.archivo
        archivo_lista = contexto.buscar_archivo("app.py")

        self.assertIsNotNone(archivo_nario)
        self.assertIs(
            archivo_nario,
            archivo_lista,
            "El nodo del Árbol N-ario y la ListaEnlazada deben referenciar el mismo objeto ArchivoCodigo.",
        )

        ruta_fisica_esperada = os.path.join(self._ruta_respaldos, "core", "app.py")
        ruta_fisica_antigua = os.path.join(self._ruta_respaldos, "src", "app.py")
        self.assertTrue(os.path.isfile(ruta_fisica_esperada))
        self.assertFalse(os.path.exists(ruta_fisica_antigua))

    def test_auditoria_reglas_arquitectonicas(self) -> None:
        """Verifica una clase por archivo y ausencia de estructuras/funciones prohibidas."""
        raiz_repo = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        for carpeta in ("src", "test", "scripts"):
            ruta_carpeta = os.path.join(raiz_repo, carpeta)
            for root, _, files in os.walk(ruta_carpeta):
                for fname in files:
                    if not fname.endswith(".py"):
                        continue
                    ruta_py = os.path.join(root, fname)
                    with open(ruta_py, "r", encoding="utf-8") as f:
                        codigo = f.read()
                    arbol_ast = ast.parse(codigo, filename=ruta_py)
                    clases = [
                        n.name for n in ast.walk(arbol_ast) if isinstance(n, ast.ClassDef)
                    ]
                    self.assertLessEqual(
                        len(clases),
                        1,
                        f"Violación de 'una clase por archivo' en {ruta_py}: {clases}",
                    )
                    for nodo in ast.walk(arbol_ast):
                        if isinstance(nodo, ast.Call):
                            if isinstance(nodo.func, ast.Name):
                                self.assertNotIn(
                                    nodo.func.id,
                                    ("eval", "sorted"),
                                    f"Función prohibida '{nodo.func.id}' en {ruta_py}:{nodo.lineno}",
                                )
                            if isinstance(nodo.func, ast.Attribute):
                                self.assertNotEqual(
                                    nodo.func.attr,
                                    "sort",
                                    f"Método prohibido '.sort()' en {ruta_py}:{nodo.lineno}",
                                )


if __name__ == "__main__":
    unittest.main()

