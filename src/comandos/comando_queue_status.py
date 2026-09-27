"""Módulo del comando concreto 'queue-status'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.servicios.servicio_cola_ia import ServicioColaIA


class ComandoQueueStatus(ComandoBase):
    """Comando para consultar el estado actual del buffer FIFO de peticiones de IA."""

    def __init__(self, servicio_cola_ia: ServicioColaIA) -> None:
        super().__init__(
            nombre="queue-status",
            descripcion="Muestra el estado actual de la cola FIFO que administra las solicitudes hacia la API de IA.",
            sintaxis="queue-status",
        )
        self._servicio_cola_ia: ServicioColaIA = servicio_cola_ia

    def ejecutar(self, argumentos: List[str]) -> bool:
        estado = self._servicio_cola_ia.obtener_estado()
        total = estado["total_pendientes"]

        if total == 0:
            print("[Información] La cola FIFO de peticiones está vacía. No hay solicitudes pendientes hacia la IA.")
            return True

        print(f"\n--- Estado del Buffer FIFO de IA ({total} pendiente/s) ---")
        print(f"  Próxima a despachar: {estado['proxima_peticion']} (Archivo: {estado['archivo_proximo']})")
        print("  Elementos en cola (orden de llegada):")
        for i, pet in enumerate(estado["peticiones"], start=1):
            print(f"    {i}. ID: {pet['id']:<14} Archivo: {pet['archivo']:<18} Estado: {pet['estado']} [{pet['timestamp']}]")
        print("----------------------------------------------------------\n")
        return True
