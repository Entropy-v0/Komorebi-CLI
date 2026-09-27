# Guía Maestra para la Defensa Académica - Komorebi Mini IDE

**Universidad José Antonio Páez - Facultad de Ingeniería**  
**Escuela de Ingeniería en Computación**  
**Cátedra:** Algoritmos y Estructuras II (Septiembre de 2026)  
**Puntuación de la Defensa:** 4 puntos  

Esta guía ha sido diseñada para prepararte ante las preguntas conceptuales, técnicas y de arquitectura más exigentes que el jurado o profesor evaluador realizará durante la defensa del proyecto.

---

## 🧭 Índice de Preparación
1. [Estructura de la Presentación (Guion de 5 a 7 Minutos)](#1-estructura-de-la-presentación-guion-de-5-a-7-minutos)
2. [Demostración en Vivo Paso a Paso (Live Demo Script)](#2-demostración-en-vivo-paso-a-paso-live-demo-script)
3. [Tabla Definitiva de Complejidad Algorítmica ($Big\ O$)](#3-tabla-definitiva-de-complejidad-algorítmica-big-o)
4. [Justificación Técnica de Estructuras de Datos Propias](#4-justificación-técnica-de-estructuras-de-datos-propias)
5. [Algoritmos de Ordenamiento: MergeSort vs. ShellSort](#5-algoritmos-de-ordenamiento-mergesort-vs-shellsort)
6. [Arquitectura de Software y Patrones de Diseño](#6-arquitectura-de-software-y-patrones-de-diseño)
7. [Batería de Preguntas Difíciles y Preguntas Trampa del Evaluador](#7-batería-de-preguntas-difíciles-y-preguntas-trampa-del-evaluador)
8. [Detalles de Implementación Destacados (Para Ganar Puntos Extra)](#8-detalles-de-implementación-destacados-para-ganar-puntos-extra)

---

## 1. Estructura de la Presentación (Guion de 5 a 7 Minutos)

Para asegurar la máxima nota en el tiempo disponible, mantén una presentación fluida dividida en 4 actos:

* **Minuto 1: Introducción y Propósito:**
  * Presentar el nombre del proyecto (*Komorebi Mini IDE*).
  * Explicar que el objetivo es modelar un entorno de desarrollo minimalista desacoplado mediante el **Patrón Command**, prescindiendo completamente de menús numéricos prohibidos y de funciones o colecciones nativas (`list.sort()`, `collections.deque`).
* **Minutos 2-3: Estructuras de Datos y Algoritmos desde Cero:**
  * Mencionar que cada estructura (`ListaEnlazada`, `Pila`, `ColaFIFO`, `ArbolBinario`) y algoritmo (`MergeSort`, `ShellSort`) fue programado nodo a nodo con gestión manual de punteros.
  * Resaltar el ciclo de vida de la memoria y la desvinculación explícita para evitar fugas (*memory leaks*).
* **Minutos 4-5: Demostración Funcional en Vivo:**
  * Arrancar `python3 main.py`.
  * Ejecutar el flujo clave: `new` ➔ `edit` ➔ `check` ➔ `sort` ➔ `analyze`.
* **Minuto 6-7: Respaldos, Logs, Seguridad y Conclusión:**
  * Mostrar cómo los cambios se respaldan en disco (`respaldos/`), cómo los incidentes se trazan en `logs/errores.log`, y la resiliencia del sistema ante fallos de internet (Modo Offline Fallback).

---

## 2. Demostración en Vivo Paso a Paso (Live Demo Script)

Abre la terminal en la raíz del proyecto y sigue exactamente esta secuencia:

### Paso 1: Arranque y Revisión de Configuración
```bash
python3 main.py
```
En el prompt:
```text
config
```
> **Qué decir:** *"El comando `config` lee `config.json` y el entorno `.env`. Noten que la API Key está protegida y enmascarada para evitar fugas de credenciales en pantalla."*

### Paso 2: Apertura y Carga de Archivo Real
```text
new src/algoritmos/mergesort.py
show
```
> **Qué decir:** *"Komorebi detecta que el archivo ya existe en disco y carga su contenido a memoria dentro de un nodo de nuestra `ListaEnlazada` doble, asignándolo como archivo activo y creando un respaldo preventivo."*

### Paso 3: Validación Sintáctica con Pila (LIFO)
```text
check
```
Luego introduce un desbalance intencional para demostrar la captura de errores:
```text
edit def error_demo(arr): print(arr[0)
check
```
> **Qué decir:** *"El verificador sintáctico recorre el archivo ignorando literales de texto y utiliza una estructura `Pila` (LIFO) para apilar los delimitadores de apertura `(`, `[`, `{`. Al encontrar `)` verifica la cima; como se esperaba `]` detecta el desajuste indicando fila y columna exactas."*

### Paso 4: Deshacer Cambios (Historial LIFO)
```text
undo
show
```
> **Qué decir:** *"Mediante la pila de historial revertimos el cambio erróneo en tiempo $O(1)$, restaurando el estado previo del código."*

### Paso 5: Ordenamiento Manual (MergeSort y ShellSort)
Genera diagnósticos y ordénalos con ambos motores:
```text
sort line mergesort
sort severity shellsort desc
```
> **Qué decir:** *"Para cumplir la restricción de no usar `sort()` nativo, implementamos MergeSort ($O(n \log n)$ estable) y ShellSort ($O(n \log n)$ in-place) para jerarquizar las alertas por línea o nivel de severidad."*

### Paso 6: Buffer FIFO y Asistencia de Inteligencia Artificial
```text
analyze
```
> **Qué decir:** *"La solicitud se encola en una `ColaFIFO`. El servicio de IA la despacha hacia Google Gemini usando la API REST con `urllib` sin librerías externas. La IA analiza el código y devuelve la complejidad teórica ($O(n \log n)$) y sugerencias de refactorización. Si desconectamos internet, el sistema activa automáticamente un motor estático local sin colgarse."*

### Paso 7: Cierre y Liberación
```text
exit
```

---

## 3. Tabla Definitiva de Complejidad Algorítmica ($Big\ O$)

Ten estos valores memorizados para responder instantáneamente:

| Estructura / Algoritmo | Inserción | Búsqueda | Eliminación | Espacio Auxiliar | Justificación en Komorebi |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Lista Enlazada Doble** | $O(1)$ cab/cola | $O(n)$ | $O(1)$ c/nodo | $O(n)$ | Mantiene los archivos abiertos sin requerir memoria contigua. |
| **Pila (LIFO)** | $O(1)$ push | $O(n)$ | $O(1)$ pop | $O(n)$ | Balanceo de sintaxis e historial `undo`/`redo`. |
| **Cola (FIFO)** | $O(1)$ enqueue| $O(n)$ | $O(1)$ dequeue| $O(n)$ | Buffer secuencial de peticiones hacia la API de IA. |
| **Árbol Binario (BST)** | $O(\log n)$ prom.<br>$O(n)$ peor | $O(\log n)$ prom.<br>$O(n)$ peor | $O(\log n)$ prom.<br>$O(n)$ peor | $O(n)$ | Indexación jerárquica de símbolos y consultas de código. |
| **MergeSort** | N/A | N/A | N/A | $O(n)$ aux. | Ordenamiento estable garantizado $O(n \log n)$ en todos los casos. |
| **ShellSort** | N/A | N/A | N/A | $O(1)$ in-place | Ordenamiento rápido in-place con salto de decremento Knuth. |

---

## 4. Justificación Técnica de Estructuras de Datos Propias

Si el jurado pregunta: *¿Por qué usaron estas estructuras y no listas normales de Python?*

### 1. Lista Doblemente Enlazada (`ListaEnlazada`)
* **Por qué no un array/lista nativa:** En una lista nativa de Python, eliminar el primer elemento o un elemento intermedio obliga a reubicar todos los elementos siguientes en memoria ($O(n)$ por *shifting*).
* **Nuestra solución:** Al mantener punteros `siguiente` y `anterior`, una vez localizado el nodo su extracción es $O(1)$ reconectando los punteros vecinos.

### 2. Pila LIFO (`Pila`)
* **Por qué no `list.pop()`:** Porque queríamos control total del puntero `_tope` y asegurar una liberación inmediata del nodo en memoria al desapilar (`nodo.siguiente = None`).
* **Uso dual:** Validador sintáctico (empareja el cierre con el delimitador más reciente) y sistema Undo/Redo (deshace la última acción efectuada).

### 3. Cola FIFO (`ColaFIFO`)
* **Por qué no `queue.Queue`:** Prohibido por la cátedra.
* **Nuestra solución:** Mantiene punteros dedicados a `_frente` y `_final`. Encolar en el final y desencolar en el frente se ejecutan ambas en tiempo constante estricto $O(1)$.

### 4. Árbol Binario de Búsqueda (`ArbolBinario`)
* **Propósito:** Búsqueda rápida de símbolos, variables o líneas de diagnóstico en tiempo logarítmico promedio $O(\log n)$.
* **Recorridos implementados:** *In-Order* (recorre los elementos en orden ascendente), *Pre-Order* (útil para clonación o serialización), y *Post-Order* (útil para destrucción ordenada de nodos de abajo hacia arriba).

---

## 5. Algoritmos de Ordenamiento: MergeSort vs. ShellSort

Si el profesor pregunta: *¿Cuál es la diferencia entre los dos algoritmos implementados y cuándo usarías uno u otro?*

### Comparativa Teórica

1. **MergeSort (Divide y Vencerás):**
   * **Complejidad:** $O(n \log n)$ en el mejor, promedio y peor caso. Es determinista y predecible.
   * **Estabilidad:** Es **estable** (dos alertas en la misma línea conservan su orden relativo original).
   * **Costo Espacial:** Requiere memoria adicional $O(n)$ para los sub-arreglos temporales durante la mezcla (*merge*).
   * **Cuándo elegirlo:** Cuando la estabilidad es crítica y la memoria no es una limitación severa.

2. **ShellSort (Inserción con Incrementos Decrecientes):**
   * **Complejidad:** Varía entre $O(n^{1.25})$ y $O(n^{1.5})$ según la secuencia de saltos (Gaps).
   * **Estabilidad:** **No es estable** (un intercambio a larga distancia puede alterar el orden relativo de elementos iguales).
   * **Costo Espacial:** $O(1)$ estricto (in-place), no reserva memoria auxiliar.
   * **Cuándo elegirlo:** En sistemas embebidos o situaciones con restricciones estrictas de memoria RAM.

---

## 6. Arquitectura de Software y Patrones de Diseño

### El Patrón Command (Patrón de Comandos)

Si el profesor pregunta: *¿Dónde está el patrón Command y cómo interactúan sus partes?*

* **Command Interface (`ComandoBase`):** Clase abstracta con el contrato `ejecutar(argumentos: List[str]) -> bool`.
* **Concrete Commands (15 Comandos):** `ComandoNew`, `ComandoCheck`, `ComandoSort`, `ComandoAnalyze`, `ComandoUndo`, etc. Cada uno encapsula una petición del usuario.
* **Invoker (`InvocadorComandos`):** Diccionario hash que registra los comandos y los despacha dinámicamente cuando el usuario ingresa texto en la consola.
* **Receivers (Servicios de Negocio):** `ServicioArchivos`, `ServicioSintaxis`, `ServicioHistorial`, `ServicioColaIA`, `ServicioLogs`. Los comandos no hacen la lógica pesada; delegan el trabajo a los receptores.
* **Beneficios de esta arquitectura:**
  1. **Principio Abierto/Cerrado (OCP):** Podemos añadir 50 comandos nuevos creando nuevos archivos sin tocar una sola línea de la consola ni del bucle REPL.
  2. **Auditabilidad y Logs:** Cada invocación pasa por un punto centralizado que permite registrar incidentes en `logs/errores.log`.

---

## 7. Batería de Preguntas Difíciles y Preguntas Trampa del Evaluador

### Pregunta 1: *"Python tiene Garbage Collector automático. ¿Para qué se molestaron en desvincular punteros manualmente?"*
> **Respuesta del estudiante:**  
> *"Aunque Python cuenta con un recolector de basura basado en conteo de referencias y un recolector cíclico generacional, en estructuras enlazadas como las listas dobles existen referencias circulares (`nodo_A.siguiente = nodo_B` y `nodo_B.anterior = nodo_A`).  
> Si simplemente dejamos de apuntar a la cabeza, el conteo de referencias nunca llega a cero de inmediato y los nodos quedan atrapados en la Generación 1 o 2 del GC hasta que ocurra un ciclo de recolección forzada.  
> Al desvincular explícitamente `nodo.siguiente = None` y `nodo.anterior = None`, rompemos el ciclo, el conteo cae inmediatamente a 0 y la memoria se libera en tiempo $O(1)$ sin sobrecargar el recolector."*

---

### Pregunta 2: *"En el Árbol Binario de Búsqueda, ¿cómo manejaron el caso más difícil de la eliminación: un nodo con dos hijos?"*
> **Respuesta del estudiante:**  
> *"Cuando un nodo tiene dos hijos, no se puede eliminar directamente sin romper la propiedad de orden del BST.  
> Aplicamos el algoritmo clásico: localizamos el **sucesor in-order** (el nodo con el menor valor dentro del subárbol derecho, hallado bajando por todas las ramas izquierdas).  
> Copiamos el valor de ese sucesor en el nodo actual y luego invocamos recursivamente la eliminación sobre el sucesor en el subárbol derecho, reduciendo el problema a eliminar un nodo con un solo hijo o una hoja."*

---

### Pregunta 3: *"¿Por qué usaron `match-case` en la eliminación del árbol y de la lista en lugar de múltiples `if-elif-else`?"*
> **Respuesta del estudiante:**  
> *"Por reducción de la complejidad ciclomática y limpieza de código. En un árbol binario existen exactamente 4 estados topológicos para los hijos de un nodo: `(None, None)`, `(izq, None)`, `(None, der)` y `(izq, der)`.  
> Con `match (nodo.izquierda, nodo.derecha):` evaluamos la topología en una sola estructura declarativa de nivel 1, eliminando ramas anidadas propensas a errores lógicos."*

---

### Pregunta 4: *"¿Qué sucede si se cae el internet durante la llamada a la IA o si no hay API Key en el aula?"*
> **Respuesta del estudiante:**  
> *"El sistema implementa un patrón de **Fallback Seguro**. Si `ServicioClienteIA` detecta un error HTTP, timeout o ausencia de credenciales, captura la excepción, la registra en `logs/errores.log` y conmuta automáticamente a un motor estático local basado en inspección de bucles y recursión.  
> Esto garantiza que la consola nunca se congele ni lance un traceback no controlado durante la defensa."*

---

### Pregunta 5: *"¿Por qué la verificación de sintaxis ignora caracteres dentro de comillas?"*
> **Respuesta del estudiante:**  
> *"Porque en lenguajes reales como Python o C++, un string como `texto = 'este parentesis ( no cierra'` no es un error de sintaxis. Si contáramos ese paréntesis dentro de comillas, generaríamos un falso positivo. Nuestro analizador mantiene una máquina de estados que detecta cuándo está dentro de una cadena literal (`'` o `"`) y omite el apilamiento de delimitadores."*

---

### Pregunta 6: *"¿Cómo aseguran que el sistema no rompa el principio de Responsabilidad Única?"*
> **Respuesta del estudiante:**  
> *"Aplicando la regla estricta de **una sola clase por fichero**:  
> - Los nodos (`NodoLista`, `NodoPila`, etc.) solo contienen datos y punteros.  
> - Las estructuras solo gestionan la topología y punteros de datos.  
> - Los modelos de dominio (`ArchivoCodigo`, `Diagnostico`) almacenan el estado del negocio.  
> - Los servicios orquestan las operaciones.  
> - Los comandos solo traducen la entrada del usuario a llamadas de servicios."*

---

## 8. Detalles de Implementación Destacados (Para Ganar Puntos Extra)

Menciona estos tres puntos clave durante las conclusiones:

1. **Suite de Pruebas Automatizadas:** Contamos con **94 pruebas unitarias** que cubren el 100% de los componentes (nodos, árboles, pilas, colas, algoritmos, servicios y comandos), ejecutándose en tan solo `0.010` segundos.
2. **Seguridad de Credenciales con `.env` Dinámico:** No exponemos claves en el código ni en `config.json`. El cargador interpola variables de entorno de forma nativa.
3. **Persistencia Dual (Respaldos + Logs):** La persistencia en disco está completamente desacoplada: el código se respalda en `respaldos/` con soporte para subcarpetas y las trazas de auditoría se registran en `logs/errores.log`.

---

> 🎯 **Consejo de Oro para la Presentación:** Habla con calma, utiliza la terminología formal de la materia (*LIFO, FIFO, punteros, complejidad ciclomática, in-place, divide y vencerás*) y deja que el código limpio y los 94 tests hablen por la calidad de tu trabajo.
