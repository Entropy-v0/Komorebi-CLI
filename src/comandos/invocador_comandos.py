"""Módulo del invocador central del Patrón Command."""

from typing import Dict, List, Optional
from src.comandos.comando_base import ComandoBase


class InvocadorComandos:
    """Invoker en el Patrón de Diseño Command.
    
    Mantiene el registro de todos los comandos disponibles, valida su existencia
    y despacha la ejecución pasando los argumentos capturados por el CLI.
    """

    def __init__(self) -> None:
        self._comandos: Dict[str, ComandoBase] = {}

    def registrar_comando(self, comando: ComandoBase) -> None:
        """Registra un nuevo objeto comando en el diccionario de comandos activos."""
        clave = comando.nombre.strip().lower()
        self._comandos[clave] = comando

    def obtener_comando(self, nombre: str) -> Optional[ComandoBase]:
        """Recupera la instancia de comando asociada a la palabra clave dada."""
        clave = nombre.strip().lower()
        return self._comandos.get(clave)

    def ejecutar_comando(self, nombre: str, argumentos: List[str]) -> bool:
        """Despacha la ejecución del comando correspondiente.
        
        Retorna False si el comando no está registrado o si la ejecución falló.
        """
        comando = self.obtener_comando(nombre)
        if comando is None:
            print(f"[Error] Comando desconocido: '{nombre}'. Escribe 'help' para ver la lista de comandos.")
            return False

        try:
            return comando.ejecutar(argumentos)
        except Exception as e:
            print(f"[Error en '{nombre}'] {str(e)}")
            return False

    def listar_comandos(self) -> List[ComandoBase]:
        """Retorna todos los comandos registrados ordenados por su nombre."""
        return sorted(self._comandos.values(), key=lambda c: c.nombre)
