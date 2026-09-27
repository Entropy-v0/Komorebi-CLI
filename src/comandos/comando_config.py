"""Módulo del comando concreto 'config'."""

from typing import List
from src.comandos.comando_base import ComandoBase
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_configuracion import ServicioConfiguracion


class ComandoConfig(ComandoBase):
    """Comando para cargar o consultar el archivo de configuración externo (ej. config.json)."""

    def __init__(self, servicio_configuracion: ServicioConfiguracion, contexto: ContextoApp) -> None:
        super().__init__(
            nombre="config",
            descripcion="Carga el archivo de configuración externo o muestra la configuración activa.",
            sintaxis="config [ruta_archivo]",
        )
        self._servicio_configuracion: ServicioConfiguracion = servicio_configuracion
        self._contexto: ContextoApp = contexto

    def ejecutar(self, argumentos: List[str]) -> bool:
        if argumentos:
            ruta = argumentos[0].strip()
            nueva_cfg = self._servicio_configuracion.cargar_configuracion(ruta)
            self._contexto.configuracion = nueva_cfg
            print(f"[Éxito] Configuración cargada satisfactoriamente desde '{ruta}'.")
        else:
            print("[Información] Mostrando configuración activa actual:")

        cfg = self._contexto.configuracion
        print(f"  - Nombre App:        {cfg.nombre_app}")
        print(f"  - Ruta Respaldos:    {cfg.ruta_respaldos}")
        print(f"  - Ruta Logs:         {cfg.ruta_logs}")
        print(f"  - Proveedor IA:      {cfg.proveedor_ia} ({cfg.modelo_ia})")
        print(f"  - URL Completa IA:   {cfg.url_completa_ia}")
        print(f"  - Timeout Ejecución: {cfg.tiempo_maximo_ejecucion}s")
        return True
