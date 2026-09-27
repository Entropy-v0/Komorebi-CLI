"""Módulo del comando concreto 'analyze'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_cliente_ia import ServicioClienteIA
from src.servicios.servicio_cola_ia import ServicioColaIA


class ComandoAnalyze(ComandoBase):
    """Comando para encolar en el buffer FIFO y analizar el código activo con la API de IA."""

    def __init__(
        self,
        servicio_cola_ia: ServicioColaIA,
        servicio_cliente_ia: ServicioClienteIA,
        contexto: ContextoApp,
    ) -> None:
        super().__init__(
            nombre="analyze",
            descripcion="Encola el código activo en el buffer FIFO y consulta a la IA métricas Big O y refactorización.",
            sintaxis="analyze",
        )
        self._servicio_cola_ia: ServicioColaIA = servicio_cola_ia
        self._servicio_cliente_ia: ServicioClienteIA = servicio_cliente_ia
        self._contexto: ContextoApp = contexto

    def ejecutar(self, argumentos: List[str]) -> bool:
        archivo = self._contexto.archivo_activo
        if archivo is None:
            print("[Advertencia] No hay ningún archivo activo para analizar. Abre o crea uno primero.")
            return False

        if not archivo.contenido.strip():
            print(f"[Advertencia] El archivo '{archivo.nombre}' está vacío. Agrega código antes de analizar.")
            return False

        print(f"[Buffer FIFO] Encolando solicitud de análisis para '{archivo.nombre}'...")
        peticion = self._servicio_cola_ia.encolar(archivo.contenido, archivo.nombre)
        print(f"[Buffer FIFO] Petición encolada con ID: {peticion.id_peticion}. Despachando secuencialmente...")

        # Despacho secuencial desde el buffer
        peticion_a_procesar = self._servicio_cola_ia.desencolar_siguiente()
        if peticion_a_procesar is None:
            return False

        resultado = self._servicio_cliente_ia.procesar_peticion(peticion_a_procesar)

        print("\n================= REPORTE DE ANÁLISIS DE IA =================")
        print(f"  Archivo:               {peticion_a_procesar.nombre_archivo}")
        print(f"  Proveedor:             {resultado.get('proveedor', 'IA')}")
        print(f"  Complejidad Temporal:  {resultado.get('complejidad_temporal', 'N/D')}")
        print(f"  Complejidad Espacial:  {resultado.get('complejidad_espacial', 'N/D')}")
        print(f"  Diagnóstico Técnico:   {resultado.get('analisis', '')}")
        print("  Propuestas de Refactorización:")
        propuestas = resultado.get("propuestas_refactorizacion", [])
        for i, prop in enumerate(propuestas, start=1):
            print(f"    {i}. {prop}")
        print("============================================================\n")
        return True
