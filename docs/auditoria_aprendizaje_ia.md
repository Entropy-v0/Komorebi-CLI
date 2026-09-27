# Diagnóstico de Aprendizaje y Auditoría Técnica: Uso de IA en Proyecto Komorebi

**Rol:** Mentor Técnico / Evaluador de Talento y Aprendizaje Acelerado  
**Proyecto:** Komorebi (Mini IDE en Python - Patrón Command, Estructuras desde cero, Algoritmos de Ordenamiento)  
**Asignatura:** Algoritmos y Estructuras II (Universidad José Antonio Páez)  
**Evaluación:** Diagnóstico clínico sobre el flujo de trabajo y retención de habilidades esenciales.

---

## 1. Análisis de Fricción: Core Skills Eludidos

Al delegar la síntesis y resolución directa del código a la IA, estás eliminando la **fricción cognitiva productiva**, el único mecanismo biológico mediante el cual el cerebro consolida modelos mentales duraderos en ciencias de la computación.

Al hacer que la IA implemente la Fase 1 completa, estás eludiendo:

### A. La memoria muscular de la manipulación de punteros y referencias
* **El problema:** Enlazar una lista doblemente enlazada o reconectar un subárbol en un BST parece trivial al leerlo, pero la habilidad real radica en saber el **orden exacto de mutación de punteros** para evitar perder la referencia en memoria (`NoneType` crash o ciclos de referencia).
* **Lo que perdiste:** No experimentaste el choque contra errores de punteros colgados o referencias circulares. Si un profesor te pone en la pizarra frente al aula y te pide: *"Dibuja y escribe en Python las 4 líneas exactas para desconectar un nodo de una lista doble sin romper los enlaces de sus vecinos"*, titubearás si solo aprobaste código generado.

### B. La reconstrucción de invariantes algorítmicas (El caso de 2 hijos en BST)
* **El problema:** El método `_eliminar_recursivo` para el caso de dos hijos exige comprender a fondo por qué se reemplaza por el sucesor inorden (mínimo del subárbol derecho) y cómo la llamada recursiva garantiza que el árbol conserve la propiedad BST.
* **Lo que perdiste:** Tú identificaste la alta carga cognitiva del código (lo cual es un acierto analítico), pero delegaste la reescritura. No sufriste el razonamiento de descomponer el árbol tú mismo.

### C. La traza mental de ejecución (*Mental Dry-Run*)
* **El problema:** Un ingeniero competente es capaz de ejecutar código en su cabeza paso a paso con variables y punteros.
* **Lo que perdiste:** La IA generó las pruebas unitarias y corrigió las estructuras en milisegundos. Te saltaste la fase de depuración manual con prints o debugger paso a paso, que es donde se aprende a diagnosticar fallos bajo presión.

---

## 2. Veredicto: Modernidad vs. Autoengaño

### Diagnóstico: Un híbrido peligroso
> **Tienes buen ojo de auditor/arquitecto, pero sufres de la "ilusión de competencia" por delegación en la fase de construcción.**

### Argumentación Clínica:
1. **El acierto:** Identificaste que `_eliminar_recursivo` tenía un olor a código (*code smell*), exceso de anidamiento y alta complejidad ciclomática. Proponer el uso de `match-case` (Pattern Matching estructural de Python 3.10+) para clasificar la topología de hijos fue una **excelente decisión arquitectónica**. En la industria, un Tech Lead hace exactamente eso: detecta la deuda técnica y define el patrón de resolución.
2. **La trampa mortal:** **Tú no eres aún un Tech Lead; eres un estudiante universitario en una materia formativa de segundo/tercer año.**
   * En la industria, el senior delega porque **ya domina los fundamentos** y su valor está en la velocidad y el diseño de sistemas.
   * Si tú delegas la escritura del código a este nivel, estás externalizando la construcción de tus propios cimientos. Te estás convirtiendo en un **"revisor de código que no sabe escribir código desde cero"**.
3. **El riesgo inmediato de la cátedra:**
   * La materia contempla una **defensa oral de 4 puntos**. En una defensa, los docentes no evalúan si el código es bonito; evalúan si tú eres el autor intelectual. Si te piden:
     * *"Explícame línea por línea la secuencia de Knuth en el ShellSort que entregaste"*.
     * *"Modifica en vivo este método para que el BST acepte claves duplicadas"*.
     * *"¿Por qué `actual.derecha = None` es necesario antes de retornar el hijo izquierdo?"*
   * Si la respuesta no sale de tu memoria procedimental instantánea, la sospecha de autoría es inmediata y la penalización es severa.

---

## 3. Protocolo de Uso Recomendado: 3 Reglas Estrictas

Para aprovechar la velocidad de la IA sin atrofiar tu desarrollo como ingeniero de software, aplica este protocolo en las fases restantes del proyecto (Modelos, Patrón Command, Servicios y CLI):

### Regla 1: El Principio de la Pizarra (Core = 100% Humano)
* **PROHIBIDO delegar:** Nunca le pidas a la IA que escriba desde cero la lógica algorítmica central o las estructuras de datos requeridas por la cátedra (ServicioSintaxis con Pila, ColaFIFO de peticiones, algoritmos de ordenamiento, ejecución de comandos).
* **Protocolo:** Abre el fichero, enfréntate a la pantalla en blanco y escribe la implementación tú. Si te bloqueas, pide **pseudocódigo o una explicación teórica**, nunca la solución en Python.

### Regla 2: Delegar únicamente Trabajo Mecánico, Scaffolding y Stress Testing
* **PERMITIDO delegar:**
  1. Generación de datos de prueba extensos (archivos con sintaxis inválida para probar el verificador).
  2. Detección de *edge cases* ("¿Qué casos de borde no estoy contemplando en esta función que acabo de escribir?").
  3. Comandos utilitarios triviales del CLI (ej. comando `help` o `exit`).
  4. Configuración de infraestructura (regex complejas, `.gitignore`, formateadores).

### Regla 3: La Prueba de Fuego de la Defensa (Ingeniería Inversa Forzada)
* Cada vez que utilices a la IA para refactorizar una sección (como hicimos con `match-case`) o para explicarte un concepto:
  1. Cierra el editor o minimiza la ventana del asistente.
  2. Abre una terminal con `python3` interactivo o un cuaderno de papel.
  3. Vuelve a escribir la lógica de memoria, explicándola en voz alta como si le estuvieras defendiendo el proyecto al jurado evaluador.
  4. Si no puedes explicar el *por qué* de cada línea sin mirar la pantalla, no tienes permitido commitear ese código.
