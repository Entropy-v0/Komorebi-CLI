"""Módulo del comando concreto 'sort'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_diagnosticos import ServicioDiagnosticos


class ComandoSort(ComandoBase):
    """Comando para ordenar los diagnósticos y alertas usando MergeSort o ShellSort."""

    def __init__(self, servicio_diagnosticos: ServicioDiagnosticos, contexto: ContextoApp) -> None:
        super().__init__(
            nombre="sort",
            descripcion="Ordena las alertas del código activo usando MergeSort o ShellSort por línea o gravedad.",
            sintaxis="sort <criterio: line|severity> <algoritmo: mergesort|shellsort> [asc|desc]",
        )
        self._servicio_diagnosticos: ServicioDiagnosticos = servicio_diagnosticos
        self._contexto: ContextoApp = contexto

    def ejecutar(self, argumentos: List[str]) -> bool:
        if len(argumentos) < 2:
            print(f"[Error] Parámetros insuficientes. Sintaxis: {self._sintaxis}")
            return False

        criterio = argumentos[0].strip().lower()
        algoritmo = argumentos[1].strip().lower()
        direccion = argumentos[2].strip().lower() if len(argumentos) > 2 else "asc"
        ascendente = direccion not in ("desc", "descendente", "d")

        diags_actuales = self._contexto.diagnosticos
        if not diags_actuales:
            print("[Información] No hay diagnósticos activos para ordenar. Ejecuta primero 'check'.")
            return True

        try:
            diags_ordenados = self._servicio_diagnosticos.ordenar(
                diags_actuales,
                criterio=criterio,
                algoritmo=algoritmo,
                ascendente=ascendente,
            )
            self._contexto.diagnosticos = diags_ordenados

            dir_texto = "ascendente" if ascendente else "descendente"
            print(f"\n--- Diagnósticos Ordenados ({algoritmo.upper()} por {criterio.upper()}, {dir_texto}) ---")
            for diag in diags_ordenados:
                print(f"  {diag.formato_consola()}")
            print("-------------------------------------------------------------------------\n")
            return True
        except ValueError as e:
            print(f"[Error] {str(e)}")
            return False
