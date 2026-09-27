# Guía de Uso Rápido y Manual de Usuario - Komorebi Mini IDE

**Algoritmos y Estructuras II**  
**Universidad José Antonio Páez**

Esta guía proporciona instrucciones detalladas, tutoriales paso a paso y ejemplos prácticos para operar la consola interactiva de **Komorebi Mini IDE**, aprovechando al máximo sus estructuras de datos, su motor de ordenamiento y su conexión con inteligencia artificial.

---

## 1. Inicio Rápido (Quickstart)

### Iniciar la Consola
Abre tu terminal en el directorio raíz del proyecto y ejecuta:

```bash
python3 main.py
```

Inmediatamente verás la bienvenida y el prompt dinámico interactivo:

```text
====================================================================
  KOMOREBI MINI IDE - ALGORITMOS Y ESTRUCTURAS II
  Patrón Command • Estructuras desde Cero • Sin Menús Numéricos
  Escribe 'help' para ver la lista de comandos disponibles.
  Escribe 'exit' para cerrar la sesión.
====================================================================
Komorebi [sin-archivo]> 
```

> **Nota:** El texto entre corchetes `[...]` indica cuál es el **archivo activo actual**. Si no hay ninguno abierto, indicará `[sin-archivo]`.

---

## 2. Flujo de Trabajo Fundamental

```
[ new / switch ] ──► [ edit / show ] ──► [ check ] ──► [ sort ] ──► [ analyze ]
 (Cargar Código)      (Modificar/Ver)     (Sintaxis)   (Ordenar)    (IA Big O)
```

---

## 3. Guía Paso a Paso por Módulos

### Módulo A: Gestión de Archivos en Memoria y Respaldos

#### 1. Crear un archivo nuevo o cargar uno existente del disco
```text
Komorebi [sin-archivo]> new ordenamiento.py
```
* **Si el archivo ya existe en tu disco:** Komorebi lee su contenido automáticamente a memoria.
* **Si el archivo no existe:** Crea un fichero nuevo vacío en memoria y genera una copia de respaldo en la carpeta `respaldos/`.
* El prompt cambiará a: `Komorebi [ordenamiento.py]> `

También puedes crear un archivo pasando contenido inicial en la misma línea:
```text
Komorebi [sin-archivo]> new demo.cpp int main() { return 0; }
```

#### 2. Visualizar los archivos abiertos en la sesión
```text
Komorebi [demo.cpp]> list

--- Archivos Abiertos en la Sesión ---
  1. ordenamiento.py      ( 0 líneas, mod: 17:40:15)
  2. demo.cpp             ( 1 líneas, mod: 17:41:02) [ACTIVO] *
---------------------------------------
```

#### 3. Alternar de archivo activo
Puedes cambiar de archivo activo por su **nombre** o por su **índice numérico**:
```text
Komorebi [demo.cpp]> switch ordenamiento.py
[Éxito] Archivo activo cambiado a 'ordenamiento.py'.
Komorebi [ordenamiento.py]> switch 2
[Éxito] Archivo activo cambiado a 'demo.cpp'.
```

#### 4. Cerrar y eliminar un archivo de la memoria
```text
Komorebi [demo.cpp]> delete demo.cpp
[Éxito] Archivo 'demo.cpp' eliminado de la lista y memoria liberada.
[Información] Archivo activo actual: 'ordenamiento.py'.
```

---

### Módulo B: Edición, Visualización e Historial Undo/Redo

#### 1. Agregar líneas de código
Usa `edit` para agregar código al archivo activo:
```text
Komorebi [ordenamiento.py]> edit def burbuja(arr):
Komorebi [ordenamiento.py]> edit     for i in range(len(arr)):
Komorebi [ordenamiento.py]> edit         for j in range(len(arr)):
Komorebi [ordenamiento.py]> edit             print(i, j)
```

#### 2. Inspeccionar el código con números de línea
```text
Komorebi [ordenamiento.py]> show

--- Contenido de 'ordenamiento.py' (4 líneas) ---
    1 | def burbuja(arr):
    2 |     for i in range(len(arr)):
    3 |         for j in range(len(arr)):
    4 |             print(i, j)
---------------------------------------------------
```

#### 3. Deshacer y Rehacer cambios (Control LIFO)
Cada vez que usas `edit`, el estado anterior se apila en la pila de retroceso:
```text
Komorebi [ordenamiento.py]> undo
[Éxito] Cambio deshecho en 'ordenamiento.py'. (Líneas: 3)

Komorebi [ordenamiento.py]> redo
[Éxito] Cambio rehecho en 'ordenamiento.py'. (Líneas: 4)
```

---

### Módulo C: Validación Sintáctica y Motor de Ordenamiento

#### 1. Validar anidamiento de `()`, `{}`, `[]` con Pila
```text
Komorebi [ordenamiento.py]> check
[Análisis] Verificando sintaxis del archivo activo 'ordenamiento.py'...
  [INFO ] Línea   1, Col  1: Sintaxis balanceada: todos los delimitadores () {} [] están en equilibrio.
[Éxito] Verificación sintáctica completada sin errores de balanceo.
```

Si el código contiene errores (ej. `arr = [1, 2, 3)`):
```text
[Análisis] Verificando sintaxis del archivo activo 'test.py'...
  [ERROR] Línea   1, Col 15: Desbalance de delimitadores: se cerró con ')' pero se esperaba '['.
[Fallo] Se detectaron 1 discrepancia(s) de delimitadores.
```

#### 2. Ordenar alertas con algoritmos propios (MergeSort o ShellSort)
Puedes ordenar la lista de diagnósticos generados según tu preferencia:

* **Por número de línea con MergeSort (Ascendente):**
  ```text
  Komorebi [test.py]> sort line mergesort
  ```

* **Por nivel de gravedad con ShellSort (Descendente):**
  ```text
  Komorebi [test.py]> sort severity shellsort desc
  ```

---

### Módulo D: Buffer FIFO y Análisis Algorítmico con IA

#### 1. Solicitar análisis $Big\ O$ del código activo
```text
Komorebi [ordenamiento.py]> analyze
[Buffer FIFO] Encolando solicitud de análisis para 'ordenamiento.py'...
[Buffer FIFO] Petición encolada con ID: req-8f3a1c02. Despachando secuencialmente...

================= REPORTE DE ANÁLISIS DE IA =================
  Archivo:               ordenamiento.py
  Proveedor:             Motor Estático Local (Offline Fallback)
  Complejidad Temporal:  O(n^2)
  Complejidad Espacial:  O(1)
  Diagnóstico Técnico:   Se detectaron múltiples estructuras de iteración anidadas.
  Propuestas de Refactorización:
    1. Garantizar liberación explícita de referencias al remover nodos en memoria.
    2. Utilizar pattern matching (match-case) para reducir la complejidad ciclomática.
    3. Considerar algoritmos Divide y Vencerás (MergeSort) si los datos crecen sustancialmente.
============================================================
```

#### 2. Consultar el estado de la cola FIFO
Si encolas múltiples peticiones antes de despacharlas, puedes monitorear el buffer:
```text
Komorebi [ordenamiento.py]> queue-status
```

---

## 4. Tabla Resumen de Comandos

| Comando | Sintaxis de Ejemplo | Descripción |
| :--- | :--- | :--- |
| **`new`** | `new app.py [codigo]` | Crea o carga un archivo en memoria y genera respaldo en disco. |
| **`list`** | `list` | Lista los archivos abiertos, sus líneas y marca cuál es el activo. |
| **`switch`** | `switch app.py` o `switch 1` | Cambia de archivo activo por nombre o posición. |
| **`delete`** | `delete app.py` o `delete 1` | Cierra el archivo y libera su nodo en memoria. |
| **`show`** | `show` | Muestra el código fuente del archivo activo numerando las líneas. |
| **`edit`** | `edit <linea_de_codigo>` | Agrega una línea al archivo activo registrando snapshot Undo. |
| **`undo`** | `undo` | Deshace la última edición usando la pila de retroceso. |
| **`redo`** | `redo` | Rehace el cambio revertido usando la pila de avance. |
| **`check`** | `check` | Valida con una Pila el balanceo de delimitadores `()`, `{}`, `[]`. |
| **`sort`** | `sort line mergesort` | Ordena los diagnósticos por línea o gravedad con MergeSort o ShellSort. |
| **`queue-status`**| `queue-status` | Muestra el estado del buffer FIFO de peticiones de IA. |
| **`analyze`** | `analyze` | Encola y analiza el código activo extrayendo métricas Big O. |
| **`config`** | `config [ruta.json]` | Carga una nueva configuración o muestra la activa. |
| **`help`** | `help` | Imprime la lista de comandos disponibles. |
| **`exit`** | `exit` | Finaliza de forma ordenada la sesión de trabajo. |

---

## 5. Configuración de Gemini y Modo Offline

En [config.json](file:///home/entropy/Olimpo/Proyectos/Komorebi/config.json):
* **Para usar Google Gemini Real:** Agrega tu clave en el campo `"api_key": "TU_API_KEY"` o define la variable de entorno `export GEMINI_API_KEY="TU_API_KEY"`.
* **Para la Defensa en el Aula (Sin Internet):** No necesitas hacer nada; si no hay conexión o no hay API Key, el sistema activa automáticamente su **Modo Offline Fallback**, realizando un análisis de complejidad local preciso sin lanzar errores ni colgarse.
