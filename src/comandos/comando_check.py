"""Módulo del comando concreto 'check'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_sintaxis import ServicioSintaxis


class ComandoCheck(ComandoBase):
    """Comando para verificar el balanceo sintáctico de (), {}, [] en el código activo usando una Pila."""

    def __init__(self, servicio_sintaxis: ServicioSintaxis, contexto: ContextoApp) -> None:
        super().__init__(
            nombre="check",
            descripcion="Valida el correcto anidamiento de delimitadores () {} [] en el código activo usando una Pila.",
            sintaxis="check",
        )
        self._servicio_sintaxis: ServicioSintaxis = servicio_sintaxis
        self._contexto: ContextoApp = contexto

    def ejecutar(self, argumentos: List[str]) -> bool:
        archivo_activo = self._contexto.archivo_activo
        if archivo_activo is None:
            print("[Advertencia] No hay ningún archivo activo para verificar. Usa 'new' o 'switch'.")
            return False

        print(f"[Análisis] Verificando sintaxis del archivo activo '{archivo_activo.nombre}'...")
        valido, diagnosticos = self._servicio_sintaxis.validar_codigo(archivo_activo.contenido)
        self._contexto.diagnosticos = diagnosticos

        for diag in diagnosticos:
            print(f"  {diag.formato_consola()}")

        if valido:
            print("[Éxito] Verificación sintáctica completada sin errores de balanceo.")
        else:
            print(f"[Fallo] Se detectaron {len(diagnosticos)} discrepancia(s) de delimitadores.")

        return valido
