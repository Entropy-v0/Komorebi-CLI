"""Módulo del servicio encargado de administrar el buffer FIFO de peticiones a la IA."""

from typing import Any, Dict, List, Optional
from src.nucleo.contexto_app import ContextoApp
from src.nucleo.peticion_ia import PeticionIA


class ServicioColaIA:
    """Administra el buffer de peticiones de análisis de código hacia la API de IA.
    
    Asegura un despacho estrictamente secuencial (First-In, First-Out) evitando
    la saturación del cliente HTTP o límites de tasa de la API externa.
    """

    def __init__(self, contexto: ContextoApp) -> None:
        self._contexto: ContextoApp = contexto

    @property
    def tamano(self) -> int:
        """Retorna la cantidad actual de peticiones encoladas pendientes."""
        return len(self._contexto.cola_ia)

    def esta_vacia(self) -> bool:
        """Indica si el buffer FIFO no contiene peticiones pendientes."""
        return self._contexto.cola_ia.esta_vacia()

    def encolar(self, codigo: str, nombre_archivo: str = "fragmento.txt") -> PeticionIA:
        """Crea una nueva PeticionIA y la agrega al final de la Cola FIFO."""
        peticion = PeticionIA(codigo=codigo, nombre_archivo=nombre_archivo)
        self._contexto.encolar_peticion_ia(peticion)
        return peticion

    def desencolar_siguiente(self) -> Optional[PeticionIA]:
        """Extrae la siguiente petición al frente de la cola para ser procesada."""
        if self.esta_vacia():
            return None
        return self._contexto.desencolar_peticion_ia()

    def consultar_frente(self) -> Optional[PeticionIA]:
        """Consulta la próxima petición a despachar sin retirarla de la cola."""
        if self.esta_vacia():
            return None
        item = self._contexto.cola_ia.frente()
        return item if isinstance(item, PeticionIA) else None

    def obtener_estado(self) -> Dict[str, Any]:
        """Genera un reporte estructurado del estado de la cola FIFO para el comando queue-status."""
        elementos: List[PeticionIA] = [
            item for item in self._contexto.cola_ia.listar() if isinstance(item, PeticionIA)
        ]
        frente_item = self.consultar_frente()

        return {
            "total_pendientes": len(elementos),
            "proxima_peticion": frente_item.id_peticion if frente_item else None,
            "archivo_proximo": frente_item.nombre_archivo if frente_item else None,
            "peticiones": [
                {
                    "id": p.id_peticion,
                    "archivo": p.nombre_archivo,
                    "estado": p.estado,
                    "timestamp": p.timestamp.strftime("%H:%M:%S"),
                }
                for p in elementos
            ],
        }
