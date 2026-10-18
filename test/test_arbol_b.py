"""Pruebas unitarias exhaustivas para Fase 4: Árbol B (m=4) y ServicioIndexacion."""

import io
import os
import random
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout

from src.comandos.comando_find_global import ComandoFindGlobal
from src.comandos.comando_index_all import ComandoIndexAll
from src.estructuras.arbol_b import ArbolB
from src.nucleo.configuracion_app import ConfiguracionApp
from src.nucleo.contexto_app import ContextoApp
from src.nucleo.referencia_token import ReferenciaToken
from src.servicios.servicio_archivos import ServicioArchivos
from src.servicios.servicio_diccionario import ServicioDiccionario
from src.servicios.servicio_indexacion import ServicioIndexacion
from src.servicios.servicio_workspace import ServicioWorkspace


class TestArbolB(unittest.TestCase):
    """Suite de pruebas para NodoB, ArbolB (orden m=4) y ServicioIndexacion."""

    def setUp(self) -> None:
        self._dir_temp = tempfile.mkdtemp(prefix="komorebi_test_btree_")
        self._ruta_respaldos = os.path.join(self._dir_temp, "respaldos")
        self._ruta_logs = os.path.join(self._dir_temp, "logs")

    def tearDown(self) -> None:
        shutil.rmtree(self._dir_temp, ignore_errors=True)

    def test_splits_en_cascada_hasta_la_raiz(self) -> None:
        """Verifica divisiones (splits) en hoja, nodo interno y crecimiento de la raíz."""
        btree = ArbolB(orden=4)
        # Con m=4 (máx 3 claves por nodo), insertar claves en orden fuerza splits sucesivos
        claves = [f"tok_{i:02d}" for i in range(1, 20)]
        altura_anterior = 0

        for idx, clave in enumerate(claves, start=1):
            btree.insertar(clave, ReferenciaToken("file-001", idx))
            self.assertTrue(btree.es_valido())
            self.assertGreaterEqual(btree.altura, altura_anterior)
            altura_anterior = btree.altura

        self.assertEqual(btree.tamanio, 19)
        self.assertGreaterEqual(btree.altura, 3)
        self.assertEqual(btree.inorden(), claves)

    def test_500_inserciones_con_es_valido_tras_cada_paso(self) -> None:
        """Inserta 500 tokens aleatorios verificando es_valido() tras cada inserción/split."""
        rng = random.Random(1337)
        tokens = [f"identificador_{i:04d}" for i in range(500)]
        rng.shuffle(tokens)

        btree = ArbolB(orden=4)
        for num, tok in enumerate(tokens, start=1):
            btree.insertar(tok, ReferenciaToken("file-stress", num))
            self.assertTrue(btree.es_valido())

        self.assertEqual(btree.tamanio, 500)
        recorrido = btree.inorden()
        self.assertEqual(len(recorrido), 500)
        for i in range(len(recorrido) - 1):
            self.assertLess(recorrido[i], recorrido[i + 1])

    def test_token_repetido_en_varios_archivos_sin_duplicar_clave(self) -> None:
        """Verifica que un mismo token en varios archivos agregue referencias sin duplicar clave."""
        btree = ArbolB(orden=4)
        ref1 = ReferenciaToken("file-a", 10)
        ref2 = ReferenciaToken("file-b", 4)
        ref3 = ReferenciaToken("file-a", 25)

        btree.insertar("calcular_total", ref1)
        btree.insertar("calcular_total", ref2)
        btree.insertar("calcular_total", ref3)
        # Intentar insertar exactamente la misma referencia otra vez
        btree.insertar("calcular_total", ReferenciaToken("file-a", 10))

        self.assertEqual(btree.tamanio, 1)
        refs = btree.buscar("calcular_total")
        self.assertEqual(len(refs), 3)
        self.assertEqual(
            [(r.archivo_id, r.linea) for r in refs],
            [("file-a", 10), ("file-a", 25), ("file-b", 4)],
        )
        self.assertTrue(btree.es_valido())

    def test_eliminacion_prestamo_fusion_y_decrecimiento_raiz(self) -> None:
        """Ejercita préstamo izquierdo, préstamo derecho, fusión, nodo interno y reducción de raíz."""
        btree = ArbolB(orden=4)
        claves = [f"k_{i:02d}" for i in range(1, 31)]
        for i, c in enumerate(claves, start=1):
            btree.insertar(c, ReferenciaToken("file-main", i))

        altura_inicial = btree.altura
        self.assertGreaterEqual(altura_inicial, 3)

        # Eliminar claves en un orden que ejercite nodos internos, préstamos y fusiones
        orden_eliminacion = [
            "k_04",  # a menudo separador interno tras splits iniciales
            "k_01",  # extremo izquierdo -> préstamo derecho o fusión
            "k_30",  # extremo derecho -> préstamo izquierdo o fusión
            "k_15",
            "k_08",
            "k_12",
            "k_20",
            "k_25",
        ]
        for c in orden_eliminacion:
            self.assertTrue(btree.eliminar(c))
            self.assertEqual(btree.buscar(c), [])
            self.assertTrue(btree.es_valido())

        # Eliminar el resto hasta vaciar el árbol verificando decrecimiento de altura y validez
        restantes = btree.inorden()
        for c in restantes:
            self.assertTrue(btree.eliminar(c))
            self.assertTrue(btree.es_valido())

        self.assertEqual(btree.tamanio, 0)
        self.assertEqual(btree.altura, 0)
        self.assertTrue(btree.esta_vacio())
        self.assertFalse(btree.eliminar("no_existe"))

    def test_servicio_indexacion_workspace_avl_y_find_global(self) -> None:
        """Verifica extracción léxica, filtrado AVL, index-all idempotente y find-global."""
        config = ConfiguracionApp(
            ruta_respaldos=self._ruta_respaldos, ruta_logs=self._ruta_logs
        )
        contexto = ContextoApp(configuracion=config)
        servicio_archivos = ServicioArchivos(contexto)
        servicio_workspace = ServicioWorkspace(contexto, servicio_archivos)
        ServicioDiccionario(contexto)
        servicio_indexacion = ServicioIndexacion(contexto)
        servicio_archivos.servicio_indexacion = servicio_indexacion

        # Crear jerarquía con dos archivos que comparten un identificador 'contador_global'
        servicio_workspace.crear_carpeta("src")
        servicio_workspace.cambiar_directorio("src")
        arc_app = servicio_archivos.crear_archivo(
            "app.py",
            "def procesar_datos(contador_global):\n"
            "    # comentario con token_falso\n"
            "    mensaje = 'cadena con otro_falso'\n"
            "    if contador_global > 0:\n"
            "        return contador_global\n",
        )
        servicio_workspace.cambiar_directorio("/")
        servicio_workspace.crear_carpeta("utils")
        servicio_workspace.cambiar_directorio("utils")
        servicio_archivos.crear_archivo(
            "helper.py",
            "contador_global = 42\n"
            "def reiniciar():\n"
            "    contador_global = 0\n",
        )

        cmd_index = ComandoIndexAll(servicio_indexacion)
        cmd_find = ComandoFindGlobal(servicio_indexacion)

        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_index.ejecutar([])
            # Ejecutar index-all por segunda vez: no debe duplicar referencias
            cmd_index.ejecutar([])

        self.assertTrue(servicio_indexacion.indice.es_valido())

        # Palabras reservadas de Python ('def', 'if', 'return') NO deben estar en el B-Tree
        self.assertEqual(servicio_indexacion.indice.buscar("def"), [])
        self.assertEqual(servicio_indexacion.indice.buscar("if"), [])
        self.assertEqual(servicio_indexacion.indice.buscar("return"), [])

        # Tokens en comentarios o strings NO deben haberse indexado
        self.assertEqual(servicio_indexacion.indice.buscar("token_falso"), [])
        self.assertEqual(servicio_indexacion.indice.buscar("otro_falso"), [])

        # Verificar ubicaciones de 'contador_global'
        ubicaciones = servicio_indexacion.buscar_global("contador_global")
        self.assertEqual(
            ubicaciones,
            [
                ("/src/app.py", [1, 4, 5]),
                ("/utils/helper.py", [1, 3]),
            ],
        )

        # Verificar salida de find-global para token existente e inexistente
        buf_find = io.StringIO()
        with redirect_stdout(buf_find):
            cmd_find.ejecutar(["contador_global"])
            cmd_find.ejecutar(["token_inexistente_xyz"])
        texto_find = buf_find.getvalue()
        self.assertIn("/src/app.py", texto_find)
        self.assertIn("1, 4, 5", texto_find)
        self.assertIn("/utils/helper.py", texto_find)
        self.assertIn("no fue encontrado en el índice global", texto_find)

        # Mover /src/app.py a /utils/app.py mantiene el índice coherente automáticamente
        servicio_workspace.mover("/src/app.py", "/utils/app.py")
        self.assertEqual(
            servicio_indexacion.buscar_global("procesar_datos"),
            [("/utils/app.py", [1])],
        )

        # Eliminar el archivo purga sus referencias del B-Tree
        contexto.cerrar_archivo_por_id(arc_app.id_archivo)
        self.assertEqual(servicio_indexacion.buscar_global("procesar_datos"), [])
        self.assertEqual(
            servicio_indexacion.buscar_global("contador_global"),
            [("/utils/helper.py", [1, 3])],
        )


if __name__ == "__main__":
    unittest.main()
