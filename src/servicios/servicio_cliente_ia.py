"""Módulo del servicio cliente HTTP para conexión con la API de Inteligencia Artificial."""

import json
import re
import urllib.error
import urllib.request
from typing import Any, Dict, Optional
from src.nucleo.configuracion_app import ConfiguracionApp
from src.nucleo.peticion_ia import PeticionIA


class ServicioClienteIA:
    """Gestiona la comunicación HTTP con la API de IA (Google Gemini REST o Mock Offline).
    
    Extrae métricas de complejidad algorítmica (Big O temporal y espacial)
    y propuestas de refactorización de código sin requerir librerías externas de terceros.
    """

    def __init__(self, configuracion: ConfiguracionApp) -> None:
        self._configuracion: ConfiguracionApp = configuracion

    def procesar_peticion(self, peticion: PeticionIA) -> Dict[str, Any]:
        """Procesa una PeticionIA conectándose al endpoint configurado o aplicando fallback.
        
        Actualiza el estado de la PeticionIA a COMPLETADO o FALLIDO y retorna el resultado.
        """
        peticion.marcar_en_proceso()

        api_key = self._configuracion.api_key_ia
        proveedor = self._configuracion.proveedor_ia.lower()

        # Si está configurado Gemini y existe API Key, intentar conexión HTTP real
        if proveedor == "gemini" and api_key:
            try:
                resultado = self._llamar_gemini_api(peticion.codigo, api_key)
                peticion.marcar_completado(resultado)
                return resultado
            except Exception as e:
                # Fallback inteligente ante errores de red o cuota en la defensa
                resultado_fallback = self._analisis_estatico_local(
                    peticion.codigo,
                    nota=f"Conexión con Gemini no disponible ({str(e)}). Activado modo seguro offline.",
                )
                peticion.marcar_completado(resultado_fallback)
                return resultado_fallback

        # Modo Offline / Simulado (ideal para entornos sin internet o sin API key)
        resultado_local = self._analisis_estatico_local(
            peticion.codigo,
            nota="Modo seguro offline (sin API Key configurada).",
        )
        peticion.marcar_completado(resultado_local)
        return resultado_local

    def _llamar_gemini_api(self, codigo: str, api_key: str) -> Dict[str, Any]:
        """Efectúa una petición HTTP POST directa a la API REST de Google Gemini."""
        url = f"{self._configuracion.url_completa_ia}?key={api_key}"
        timeout = self._configuracion.tiempo_maximo_ejecucion

        prompt = (
            "Eres un evaluador de algoritmos y complejidad para un Mini IDE. "
            "Analiza el siguiente código fuente y responde ÚNICAMENTE con un JSON válido "
            "que contenga las siguientes claves exactas: "
            "'complejidad_temporal' (ej. O(1), O(n), O(n log n), O(n^2)), "
            "'complejidad_espacial' (ej. O(1), O(n)), "
            "'analisis' (resumen técnico de 1 a 2 oraciones), y "
            "'propuestas_refactorizacion' (lista de 2 o 3 recomendaciones de mejora).\n\n"
            f"Código:\n{codigo}"
        )

        cuerpo = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json"
            },
        }

        datos_bytes = json.dumps(cuerpo).encode("utf-8")
        solicitud = urllib.request.Request(
            url,
            data=datos_bytes,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(solicitud, timeout=timeout) as respuesta:
            respuesta_bytes = respuesta.read()
            datos_respuesta = json.loads(respuesta_bytes.decode("utf-8"))

        return self._extraer_json_gemini(datos_respuesta)

    def _extraer_json_gemini(self, datos_api: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae el contenido textual y lo convierte en el diccionario estándar de métricas."""
        candidatos = datos_api.get("candidates", [])
        if not candidatos:
            raise ValueError("La API de Gemini no retornó ningún candidato de respuesta.")

        texto = candidatos[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        # Limpieza de bloques de markdown si vinieron incluidos
        texto_limpio = re.sub(r"^```json\s*", "", texto.strip(), flags=re.MULTILINE)
        texto_limpio = re.sub(r"^```\s*$", "", texto_limpio.strip(), flags=re.MULTILINE)

        resultado = json.loads(texto_limpio)
        return {
            "complejidad_temporal": resultado.get("complejidad_temporal", "O(n)"),
            "complejidad_espacial": resultado.get("complejidad_espacial", "O(1)"),
            "analisis": resultado.get("analisis", "Análisis completado satisfactoriamente por Gemini."),
            "propuestas_refactorizacion": resultado.get("propuestas_refactorizacion", []),
            "proveedor": "Google Gemini (Online)",
        }

    def _analisis_estatico_local(self, codigo: str, nota: str = "") -> Dict[str, Any]:
        """Estimación estática local de complejidad (Modo a prueba de fallos).
        
        Inspecciona bucles anidados y recursión para estimar Big O y brindar sugerencias
        incluso si no hay internet o API Key durante la defensa.
        """
        lineas = codigo.splitlines()
        conteo_for = sum(1 for linea in lineas if re.search(r"\b(for|while)\b", linea))
        es_recursivo = any("recursiv" in linea.lower() or "def " in linea and "(" in linea for linea in lineas)

        # Estimación de Big O temporal
        if conteo_for >= 2:
            temporal = "O(n^2)"
            espacial = "O(1)"
            analisis = "Se detectaron múltiples estructuras de iteración anidadas."
        elif conteo_for == 1:
            temporal = "O(n)"
            espacial = "O(1)"
            analisis = "Iteración lineal simple sobre el conjunto de datos."
        elif es_recursivo:
            temporal = "O(log n) o O(n)"
            espacial = "O(n) en pila de llamadas"
            analisis = "Algoritmo con llamadas recursivas detectadas."
        else:
            temporal = "O(1)"
            espacial = "O(1)"
            analisis = "Instrucciones de tiempo constante sin bucles detectados."

        propuestas = [
            "Garantizar liberación explícita de referencias al remover nodos en memoria.",
            "Utilizar pattern matching (match-case) para reducir la complejidad ciclomática.",
            "Considerar algoritmos Divide y Vencerás (MergeSort) si los datos crecen sustancialmente.",
        ]

        if nota:
            analisis = f"{analisis} [{nota}]"

        return {
            "complejidad_temporal": temporal,
            "complejidad_espacial": espacial,
            "analisis": analisis,
            "propuestas_refactorizacion": propuestas,
            "proveedor": "Motor Estático Local (Offline Fallback)",
        }
