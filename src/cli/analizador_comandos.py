"""Módulo del analizador sintáctico de comandos de la consola."""

import shlex
from typing import List, Tuple


class AnalizadorComandos:
    """Tokeniza y extrae el comando y los argumentos de una línea de texto de la terminal.
    
    Admite argumentos con espacios delimitados por comillas simples o dobles
    y maneja de forma robusta entradas vacías o comillas sin cerrar.
    """

    def parsear(self, linea_entrada: str) -> Tuple[str, List[str]]:
        """Convierte una cadena de entrada en una tupla (nombre_comando, lista_argumentos).
        
        Args:
            linea_entrada: Cadena sin procesar capturada desde el prompt de la terminal.
            
        Returns:
            Tupla (comando_normalizado, lista_de_argumentos).
        """
        texto_limpio = linea_entrada.strip()
        if not texto_limpio:
            return "", []

        try:
            tokens = shlex.split(texto_limpio)
        except ValueError:
            # Fallback si quedaron comillas abiertas sin cerrar
            tokens = texto_limpio.split()

        if not tokens:
            return "", []

        nombre_comando = tokens[0].lower()
        argumentos = tokens[1:]

        return nombre_comando, argumentos
