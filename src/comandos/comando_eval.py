"""Módulo del comando concreto 'eval'."""

from typing import List, Optional
from src.comandos.comando_base import ComandoBase
from src.nucleo.contexto_app import ContextoApp
from src.servicios.servicio_expresiones import ServicioExpresiones


class ComandoEval(ComandoBase):
    """Comando para evaluar expresiones aritméticas mediante un Árbol de Expresiones en postorden."""

    def __init__(
        self,
        servicio_expresiones: ServicioExpresiones,
        contexto: Optional[ContextoApp] = None,
    ) -> None:
        super().__init__(
            nombre="eval",
            descripcion="Evalúa una expresión aritmética en postorden (usa --tree para ver el árbol y postfija).",
            sintaxis='eval "<expresion>" [--tree]',
        )
        self._servicio_expresiones: ServicioExpresiones = servicio_expresiones
        self._contexto: Optional[ContextoApp] = contexto

    def ejecutar(self, argumentos: List[str]) -> bool:
        mostrar_arbol = False
        partes_expresion: List[str] = []

        for arg in argumentos:
            if arg.strip() == "--tree":
                mostrar_arbol = True
            else:
                partes_expresion.append(arg)

        # Modo opcional sin expresión: buscar expresiones aritméticas en el archivo activo
        if not partes_expresion:
            if self._contexto is None or self._contexto.archivo_activo is None:
                print(f"[Error] Debes indicar una expresión o tener un archivo activo. Sintaxis: {self._sintaxis}")
                return False

            archivo = self._contexto.archivo_activo
            hallazgos = self._servicio_expresiones.evaluar_en_codigo(archivo.contenido)
            if not hallazgos:
                print(f"[Información] No se encontraron expresiones aritméticas puras en '{archivo.nombre}'.")
                return True

            print(f"\n--- Expresiones Evaluadas en '{archivo.nombre}' ---")
            for item in hallazgos:
                print(f"  Línea {item['linea']:>3}: {item['linea_original']}  ==>  {item['resultado_texto']}")
                if mostrar_arbol:
                    print(f"    Postfija: {item['postorden']}")
                    for l_arb in item["lineas_arbol"]:
                        print(f"      {l_arb}")
            print("---------------------------------------------------\n")
            return True

        expresion = " ".join(partes_expresion)
        datos = self._servicio_expresiones.evaluar_expresion(expresion)

        print(f"Resultado: {datos['resultado_texto']}")
        if mostrar_arbol:
            print(f"Notación Inorden:   {datos['inorden']}")
            print(f"Notación Preorden:  {datos['preorden']}")
            print(f"Notación Postfija:  {datos['postorden']}")
            print("Árbol de Expresión:")
            for linea in datos["lineas_arbol"]:
                print(f"  {linea}")

        return True

