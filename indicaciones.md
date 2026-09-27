# Universidad José Antonio Páez
**Facultad de Ingeniería**  
**Escuela de Ingeniería en Computación**  
**Algoritmos y Estructuras II - Septiembre de 2026**  

## Primer Proyecto: Komorebi

El objetivo de este proyecto es diseñar y desarrollar una aplicación que funcione como un entorno de desarrollo minimalista (**Mini IDE**), aplicando el patrón de diseño **Comandos (Command Pattern)** para estructurar las operaciones sobre el código. El sistema integrará estructuras de datos lineales, algoritmos avanzados de ordenamiento, lectura de configuraciones externas, control de versiones mediante GitHub y comunicación con una API de inteligencia artificial para asistir en la revisión de código.

---

## 1. Notas Adicionales del Proyecto (Apuntes de Clase)

* **Organización:** Individual o en equipo de máximo 3 personas.
* **Lenguaje y Paradigma:** Programación Orientada a Objetos en **Python**.
* **Integración con IA:** Utilizar una API de IA para analizar código:
  * Errores
  * Advertencias
  * Almacenar código
* **Estructura Interna de Archivos:** Representación mediante Lista Enlazada:
  $$\text{NULL} \rightarrow \text{archivo} \rightarrow \text{archivo} \rightarrow \text{archivo} \rightarrow \text{archivo} \rightarrow \text{NULL}$$
* **Archivo de Configuración:**
  * Rutas
  * Tiempo máximo de ejecución
  * Nombres
  * Puertas / Endpoints
* **Consola de Línea de Comandos:**
  * Debe usar el **Patrón de Diseño Comando**.
  * **No programar menú de opciones** (conlleva penalización de puntos menos en todos los módulos).
* **Organización del Código Fuente:**
  * Todas las clases deben estar en **ficheros separados**.
* **Repositorio GitHub y Flujo de Trabajo:**
  * Uso continuo de `commit` y `push`.
  * Una **rama principal** (*main/master*).
  * Cada integrante tendrá su propia rama individual.
  * Hacer `merge` con la rama principal; esa versión final será la que se va a presentar.
* **Estructura de Árbol Binario:**
  * **Nodo:** `valor`, `izquierda`, `derecha`.
  * **Árbol Binario:** `raíz`, `métodos` (`insertar`, `eliminar`, `modificar`, `consultar`).

---

## 2. Requerimientos Técnicos y Distribución de Puntuación

El desarrollo debe realizarse estrictamente desde cero, implementando las estructuras de datos y algoritmos por cuenta propia (está prohibido el uso de estructuras predefinidas como `std::list`, `std::stack`, `std::queue` o métodos nativos de ordenamiento como `.sort()`).

### 1. Archivos y Configuración (3 pts)
* **Lista Enlazada de Archivos:** Implementar una estructura de lista enlazada (simple o doble) donde cada nodo represente un archivo o fragmento de código abierto en la sesión. Debe soportar operaciones para:
  1. Crear un nuevo archivo en memoria asignándole un nombre y contenido inicial.
  2. Listar todos los archivos actualmente abiertos indicando su posición o estado.
  3. Cambiar de archivo activo para visualizar o editar su contenido.
  4. Eliminar un archivo de la lista liberando correctamente los nodos en memoria.
* **Archivo de Configuración Externo:** Al iniciar la ejecución, el programa debe leer obligatoriamente un archivo de configuración (ej. `config.json` o un archivo de texto estructurado). Este archivo debe especificar:
  * Las rutas de los directorios locales donde se guardarán automáticamente los respaldos de los códigos y los archivos de logs de errores.
  * Los parámetros de conexión y endpoints del sistema (como la URL base para conectar con la API de IA).

### 2. Validación e Historial (3 pts)
* **Pila de Verificación de Sintaxis:** Desarrollar una estructura de pila propia para validar el correcto anidamiento y balanceo de símbolos de agrupación (`()`, `{}`, `[]`) en el fragmento de código activo. El programa debe indicar si los delimitadores están correctos o reportar en qué línea/carácter ocurre el desbalance.
* **Historial Undo/Redo con Pilas:** Implementar un sistema de control de cambios basado en dos pilas independientes (Deshacer y Rehacer). Cada vez que el usuario modifique el texto del código activo, el estado anterior debe apilarse para permitir retroceder (Undo) o avanzar (Redo) en las modificaciones realizadas durante la sesión.

### 3. Motor de Ordenamiento (3 pts)
* **Algoritmos de Ordenamiento desde Cero:** Al realizar un análisis estático del código, el sistema generará un conjunto de alertas, advertencias o diagnósticos (ej. conteo de líneas por función, nivel de severidad de errores o número de línea). Los estudiantes deben diseñar e implementar manualmente al menos dos algoritmos de ordenamiento avanzados vistos en clase (por ejemplo, **Mergesort** o **Shellsort**). El usuario debe poder elegir cómo ordenar la salida: de forma ascendente por número de línea o por nivel de gravedad del diagnóstico.

### 4. Buffer de Peticiones (3 pts)
* **Cola FIFO para Peticiones:** Implementar una estructura de cola (*First-In, First-Out*) propia para administrar las solicitudes de análisis enviadas hacia la API de IA. Si el usuario solicita múltiples análisis de manera consecutiva o rápida, las peticiones deben encolarse de forma segura y el sistema deberá procesarlas y despacharlas de manera estrictamente secuencial, evitando la saturación del cliente HTTP.

### 5. Integración con la API de IA (2 pts)
* Conectar la aplicación con un modelo de IA mediante solicitudes HTTP (apoyándose en el endpoint definido en el archivo de configuración) para enviar el código fuente y recibir métricas de complejidad ($Big\ O$) y propuestas de refactorización.

### 6. Control de Versiones con GitHub (2 pts)
* Todo el desarrollo debe gestionarse obligatoriamente en un repositorio de GitHub público o privado (compartido con el docente).
* Se evaluará la frecuencia y claridad de los commits, el uso de ramas (*branches*) para el desarrollo de módulos y un archivo `README.md` completo que detalle la compilación, ejecución y arquitectura del programa.

---

## 3. Comandos de la Consola CLI

Programar una consola de línea de comandos. A continuación se muestra la tabla con todos los comandos (**hacer menú de opciones tendrá penalización de puntos menos**):

| Módulo | Comando CLI / Acción | Descripción | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **1. Archivos y Configuración** | `new <nombre_archivo>` | Crea un nuevo archivo en memoria con el nombre indicado y contenido inicial. | `new main.cpp` |
| | `list` | Muestra la lista de todos los archivos abiertos en la sesión indicando su posición o estado. | `list` |
| | `switch <id/nombre>` | Cambia el archivo activo actual para visualizar o editar su contenido. | `switch main.cpp` |
| | `delete <id/nombre>` | Elimina un archivo de la lista y libera correctamente sus nodos en memoria. | `delete main.cpp` |
| | `config <ruta_archivo>` | Carga el archivo de configuración externo (ej. `config.json`) para leer rutas de directorios y endpoints de la API. | `config config.json` |
| **2. Validación e Historial** | `check` | Valida el correcto anidamiento y balanceo de símbolos (`()`, `{}`, `[]`) en el código activo e indica la línea de error si aplica. | `check` |
| | `undo` | Deshace el último cambio realizado sobre el código utilizando la pila de retroceso. | `undo` |
| | `redo` | Rehace el cambio previamente deshecho utilizando la pila de avance. | `redo` |
| **3. Motor de Ordenamiento** | `sort <criterio> <algoritmo>` | Ordena los diagnósticos y alertas del código activo usando algoritmos implementados desde cero (Mergesort o Shellsort) por línea o gravedad. | `sort line mergesort` |
| **4. Buffer de Peticiones** | `queue-status` | Muestra el estado actual de la cola FIFO que administra las solicitudes pendientes hacia la API de IA. | `queue-status` |
| **5. Integración con IA** | `analyze` | Envía el fragmento de código activo mediante una petición HTTP al endpoint configurado para recibir métricas de complejidad ($Big\ O$) y refactorización. | `analyze` |

---

## 4. Pautas Generales

1. Modalidad: **Individual o en equipos de máximo 3 integrantes**.
2. **Defensa:** 4 pts.
3. Enlace al repositorio de **GitHub** con el código fuente estructurado.
4. **Completamente en Programación Orientada a Objetos (POO)** en **Python**; no hacerlo conlleva penalización de puntos.
5. Códigos iguales o copiados conllevan penalización de puntos.
6. Archivo de configuración de ejemplo (`config.json`/`txt`) funcional.
7. Informe técnico breve o documentación dentro del repositorio que detalle el diseño de clases y la justificación de la complejidad algorítmica.