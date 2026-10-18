"""Pruebas unitarias para los componentes base de la Fase 0 (Excepciones, ReferenciaToken y captura CLI)."""

import io
from contextlib import redirect_stdout
from typing import List
import unittest

from src.cli.consola_app import ConsolaApp
from src.comandos.comando_cd import ComandoCd
from src.comandos.invocador_comandos import InvocadorComandos
from src.excepciones import (
    DivisionPorCeroError,
    ErrorKomorebi,
    ErrorSynthetix,
    ExpresionInvalidaError,
    MovimientoInvalidoError,
    NombreDuplicadoError,
    PalabraDuplicadaError,
    RutaInvalidaError,
)
from src.nucleo.contexto_app import ContextoApp
from src.nucleo.referencia_token import ReferenciaToken
from src.servicios.servicio_workspace import ServicioWorkspace


class TestFase0Base(unittest.TestCase):
    """Pruebas unitarias para Excepciones de dominio, ReferenciaToken y captura en ConsolaApp."""

    def test_jerarquia_excepciones_propias(self) -> None:
        self.assertIs(ErrorKomorebi, ErrorSynthetix)
        derivadas = [
            RutaInvalidaError("ruta mala"),
            NombreDuplicadoError("duplicado"),
            MovimientoInvalidoError("movimiento ilegal"),
            ExpresionInvalidaError("expresión rota"),
            DivisionPorCeroError("división entre 0"),
            PalabraDuplicadaError("palabra repetida"),
        ]
        for exc in derivadas:
            self.assertIsInstance(exc, ErrorSynthetix)
            self.assertTrue(len(exc.mensaje) > 0)
            self.assertEqual(str(exc), exc.mensaje)

    def test_referencia_token_inmutable_y_comparable(self) -> None:
        ref1 = ReferenciaToken("file-abc12345", 10)
        ref2 = ReferenciaToken("file-abc12345", 10)
        ref3 = ReferenciaToken("file-abc12345", 25)

        self.assertEqual(ref1.id_archivo, "file-abc12345")
        self.assertEqual(ref1.linea, 10)
        self.assertEqual(ref1, ref2)
        self.assertEqual(hash(ref1), hash(ref2))
        self.assertNotEqual(ref1, ref3)
        self.assertTrue(ref1 < ref3)
        self.assertIn("file-abc12345", repr(ref1))
        self.assertEqual(str(ref1), "file-abc12345:10")

        with self.assertRaises(AttributeError):
            ref1.linea = 99  # type: ignore[misc]
        with self.assertRaises(AttributeError):
            ref1.id_archivo = "otro"  # type: ignore[misc]

    def test_referencia_token_validaciones(self) -> None:
        with self.assertRaises(ValueError):
            ReferenciaToken("", 1)
        with self.assertRaises(ValueError):
            ReferenciaToken("file-123", 0)
        with self.assertRaises(ValueError):
            ReferenciaToken("file-123", -5)

    def test_consola_captura_error_synthetix_y_muestra_mensaje(self) -> None:
        contexto = ContextoApp()
        invocador = InvocadorComandos()
        invocador.registrar_comando(ComandoCd(ServicioWorkspace(contexto)))
        consola = ConsolaApp(invocador, contexto)

        buffer_salida = io.StringIO()
        with redirect_stdout(buffer_salida):
            exito = consola.ejecutar_linea("cd /inexistente")

        salida = buffer_salida.getvalue()
        self.assertFalse(exito)
        self.assertIn("inexistente", salida)


if __name__ == "__main__":
    unittest.main()

