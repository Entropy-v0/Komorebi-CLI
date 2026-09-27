"""Pruebas unitarias para el bootstrap global en main.py."""

import unittest
from main import bootstrap
from src.cli.consola_app import ConsolaApp


class TestBootstrap(unittest.TestCase):
    """Pruebas para la inicialización completa en main.py."""

    def test_bootstrap_inicializacion_completa(self) -> None:
        consola = bootstrap("config.json")
        self.assertIsInstance(consola, ConsolaApp)
        self.assertIsNotNone(consola.contexto)
        self.assertIsNotNone(consola.invocador)

        # Verificar que todos los comandos clave están registrados
        comandos_esperados = [
            "new", "list", "switch", "delete", "config", "check",
            "undo", "redo", "sort", "queue-status", "analyze",
            "edit", "show", "help", "exit"
        ]
        for cmd in comandos_esperados:
            self.assertIsNotNone(
                consola.invocador.obtener_comando(cmd),
                f"El comando '{cmd}' debe estar registrado en el Invocador."
            )

    def test_bootstrap_ejecutar_comandos(self) -> None:
        consola = bootstrap("config.json")
        self.assertTrue(consola.ejecutar_linea("new demo.py def test(): pass"))
        self.assertTrue(consola.ejecutar_linea("check"))
        self.assertTrue(consola.ejecutar_linea("list"))


if __name__ == "__main__":
    unittest.main()
