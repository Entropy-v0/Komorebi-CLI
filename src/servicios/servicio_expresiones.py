"""Módulo del servicio encargado de la construcción y evaluación de Árboles de Expresión."""

from typing import Any, Dict, List
from src.estructuras.arbol_expresion import ArbolExpresion
from src.excepciones.error_synthetix import ErrorSynthetix


class ServicioExpresiones:
    """Orquesta la construcción del Árbol de Expresiones, sus recorridos y evaluación postorden.
    
    Admite tanto la evaluación directa de una expresión aritmética provista por consola
    como la inspección línea por línea de expresiones aritméticas dentro del archivo activo.
    """

    def evaluar_expresion(self, expresion: str) -> Dict[str, Any]:
        """Construye el ArbolExpresion, lo evalúa en postorden y retorna métricas y recorridos."""
        arbol = ArbolExpresion(expresion)
        resultado_num = arbol.evaluar()
        resultado_str = arbol.formatear_resultado()

        return {
            "expresion": expresion,
            "resultado": resultado_num,
            "resultado_texto": resultado_str,
            "fraccion": arbol.evaluar_exacto(),
            "preorden": arbol.preorden(),
            "inorden": arbol.inorden(),
            "postorden": arbol.postorden(),
            "lineas_arbol": arbol.dibujar_arbol(),
        }

    def evaluar_en_codigo(self, contenido: str) -> List[Dict[str, Any]]:
        """Busca y evalúa expresiones aritméticas línea por línea dentro de un código fuente."""
        hallazgos: List[Dict[str, Any]] = []
        lineas = contenido.splitlines()

        for num_linea, linea in enumerate(lineas, start=1):
            sin_comentario = linea.split("#", 1)[0].strip()
            if not sin_comentario:
                continue

            candidato = sin_comentario
            if "=" in sin_comentario and not any(op in sin_comentario for op in ("==", "!=", "<=", ">=")):
                partes = sin_comentario.split("=", 1)
                candidato = partes[1].strip()

            if not any(op in candidato for op in ("+", "-", "*", "/")):
                continue

            try:
                info = self.evaluar_expresion(candidato)
                info["linea"] = num_linea
                info["linea_original"] = sin_comentario
                hallazgos.append(info)
            except ErrorSynthetix:
                continue

        return hallazgos

