# Guía Arquitectónica y Mapa del Proyecto — Komorebi Mini IDE

**Algoritmos y Estructuras II**  
**Universidad José Antonio Páez - Facultad de Ingeniería**  
**Escuela de Ingeniería en Computación**

---

## 1. Resumen del Proyecto (Overview)

**Komorebi Mini IDE** es un entorno de desarrollo minimalista interactivo para terminal (CLI/REPL), concebido para gestionar archivos de código fuente en memoria con respaldos automáticos en disco, validación sintáctica de delimitadores, control de cambios temporal (*Undo/Redo*), ordenamiento de diagnósticos estáticos y evaluación de complejidad algorítmica ($\mathcal{O}$) asistida por Inteligencia Artificial.

* **Propósito Principal:** Proveer un IDE ligero operado por comandos de consola (sin menús numéricos) donde todas las colecciones críticas y motores de ordenamiento operan sobre estructuras de datos y algoritmos construidos desde cero, sin depender de colecciones o métodos de ordenamiento nativos del lenguaje (`list.sort()`, `sorted()`, `collections.deque`).
* **Tecnología y Stack Principal:**
  * **Lenguaje:** Python 3.10+ (aprovecha *Structural Pattern Matching* `match-case` para manipulación topológica de enlaces y *Type Hints* estrictos con `typing`).
  * **Dependencias:** **Zero-Dependency** (100% Biblioteca Estándar de Python: `abc`, `shlex`, `json`, `urllib.request`, `uuid`, `datetime`, `os`, `re`, `unittest`).
  * **Integración Externa:** API REST de Google Gemini (`generateContent`) mediante peticiones HTTP nativas, con degradación elegante (*Graceful Fallback*) hacia un motor de análisis estático local offline.
* **Paradigma y Principios de Ingeniería:**
  * **Programación Orientada a Objetos (POO) Estricta:** Regla arquitectónica de **una sola clase por archivo**, encapsulamiento mediante atributos privados (`_atributo`) expuestos con `@property`, polimorfismo mediante clases base abstractas (`ABC`) y separación estricta de responsabilidades (*Single Responsibility Principle*).
  * **Arquitectura en Capas (*Bottom-Up*):** Construcción jerárquica unidireccional desde los componentes atómicos (nodos y estructuras) hasta la interfaz de usuario (`ConsolaApp`) y el *bootstrap* (`main.py`).

---

## 2. Árbol de Directorios y Archivos

```text
Komorebi/
├── main.py                              # Punto de entrada y ensamblador (Composition Root / Bootstrap)
├── config.json                          # Configuración externa (rutas, timeouts, proveedor y modelo IA)
├── README.md                            # Documentación general, tabla Big O e instrucciones de uso
├── indicaciones.md                      # Especificaciones y requisitos académicos del proyecto
├── docs/                                # Documentación técnica, planes y guías de defensa
│   ├── ESTRUCTURA.md                    # Guía arquitectónica y mapa completo del proyecto
│   ├── auditoria_aprendizaje_ia.md      # Lineamientos de integración ética y auditoría de IA
│   ├── commits.md                       # Convención de mensajes de commit del repositorio
│   ├── guia_de_uso.md                   # Manual práctico interactivo de comandos CLI
│   ├── guia_defensa.md                  # Guion técnico y defensa arquitectónica del proyecto
│   ├── guia_estructuras_datos.md        # Justificación teórica y matemática de las estructuras propias
│   └── plan_estructuracion.md           # Hoja de ruta de diseño Bottom-Up por fases
├── logs/                                # Directorio de trazas operativas y errores persistentes
│   └── errores.log                      # Archivo cronológico de eventos INFO, WARNING y ERROR
├── respaldos/                           # Directorio de copias de seguridad físicas de archivos abiertos
│   └── demo.py                          # Ejemplo de archivo respaldado desde la sesión en memoria
├── src/                                 # Código fuente principal dividido en 6 paquetes modulares
│   ├── estructuras/                     # Capa 1A: Estructuras de datos lineales y no lineales desde cero
│   │   ├── nodo_lista.py                # Nodo doblemente enlazado (dato, siguiente, anterior)
│   │   ├── nodo_pila.py                 # Nodo enlazado simple para estructura LIFO
│   │   ├── nodo_cola.py                 # Nodo enlazado simple para estructura FIFO
│   │   ├── nodo_arbol.py                # Nodo binario (valor, izquierda, derecha)
│   │   ├── lista_enlazada.py            # Lista Doblemente Enlazada (gestión de archivos en memoria)
│   │   ├── pila.py                      # Pila LIFO (balanceo sintáctico e historial Undo/Redo)
│   │   ├── cola_fifo.py                 # Cola FIFO (buffer secuencial de peticiones a la IA)
│   │   └── arbol_binario.py             # Árbol Binario de Búsqueda (BST con recorridos y eliminación)
│   ├── algoritmos/                      # Capa 1B: Motores de ordenamiento manuales
│   │   ├── ordenador_base.py            # Clase abstracta que define el contrato de ordenación
│   │   ├── mergesort.py                 # Algoritmo Divide y Vencerás O(n log n) estable
│   │   └── shellsort.py                 # Algoritmo por intervalos decrecientes (secuencia de Knuth)
│   ├── nucleo/                          # Capa 2: Modelos de dominio y contenedor de estado global
│   │   ├── archivo_codigo.py            # Entidad que representa un archivo abierto en memoria
│   │   ├── diagnostico.py               # Entidad para alertas sintácticas con nivel de prioridad
│   │   ├── peticion_ia.py               # Entidad con ciclo de vida para solicitudes de análisis IA
│   │   ├── configuracion_app.py         # Modelo tipado y validador de parámetros de config.json / .env
│   │   └── contexto_app.py              # Estado central de la sesión (archivos, activo, cola, alertas)
│   ├── servicios/                       # Capa 3: Lógica de negocio (Receptores del patrón Command)
│   │   ├── servicio_configuracion.py    # Carga de config.json, variables .env y creación de carpetas
│   │   ├── servicio_archivos.py         # CRUD de archivos en ListaEnlazada y sincronización a disco
│   │   ├── servicio_sintaxis.py         # Verificador de delimitadores (), {}, [] mediante Pila
│   │   ├── servicio_historial.py        # Motor Undo/Redo basado en doble Pila LIFO de snapshots
│   │   ├── servicio_diagnosticos.py     # Selector y ejecutor de algoritmos MergeSort / ShellSort
│   │   ├── servicio_cola_ia.py          # Gestor del buffer ColaFIFO para despacho secuencial IA
│   │   ├── servicio_cliente_ia.py       # Cliente HTTP REST para Gemini con fallback estático local
│   │   └── servicio_logs.py             # Registrador de eventos y errores en disco
│   ├── comandos/                        # Capa 4: Patrón Command (Invocador y 15 comandos concretos)
│   │   ├── comando_base.py              # Interfaz abstracta ComandoBase (método ejecutar)
│   │   ├── invocador_comandos.py        # Despachador central y registro de comandos (Invoker)
│   │   ├── comando_new.py               # Comando 'new': crea archivo en memoria y respaldo
│   │   ├── comando_list.py              # Comando 'list': enumera archivos de la ListaEnlazada
│   │   ├── comando_switch.py            # Comando 'switch': cambia el archivo activo por nombre/índice
│   │   ├── comando_delete.py            # Comando 'delete': cierra archivo y desvincula su nodo
│   │   ├── comando_config.py            # Comando 'config': recarga o muestra la configuración activa
│   │   ├── comando_check.py             # Comando 'check': ejecuta análisis de balanceo sintáctico
│   │   ├── comando_undo.py              # Comando 'undo': revierte última edición desde pila Deshacer
│   │   ├── comando_redo.py              # Comando 'redo': reaplica edición desde pila Rehacer
│   │   ├── comando_sort.py              # Comando 'sort': ordena diagnósticos por línea o severidad
│   │   ├── comando_queue_status.py      # Comando 'queue-status': inspecciona el buffer ColaFIFO
│   │   ├── comando_analyze.py           # Comando 'analyze': encola y despacha análisis Big O a la IA
│   │   ├── comando_edit.py              # Comando 'edit': anexa líneas registrando snapshot previo
│   │   ├── comando_show.py              # Comando 'show': imprime el código activo numerado
│   │   ├── comando_help.py              # Comando 'help': lista la sintaxis de todos los comandos
│   │   └── comando_exit.py              # Comando 'exit': finaliza ordenadamente el ciclo REPL
│   └── cli/                             # Capa 5: Interfaz de línea de comandos e intérprete REPL
│       ├── analizador_comandos.py       # Parser léxico (shlex) que separa comando y argumentos
│       └── consola_app.py               # Bucle interactivo REPL y generador de prompt dinámico
└── test/                                # Suite de 21 módulos de pruebas unitarias automatizadas
    ├── test_nodos.py                    # Pruebas de NodoLista, NodoPila, NodoCola y NodoArbol
    ├── test_lista_enlazada.py           # Pruebas de inserción, búsqueda, eliminación y memoria
    ├── test_pila.py                     # Pruebas LIFO (apilar, desapilar, cima, vaciado)
    ├── test_cola_fifo.py                # Pruebas FIFO (encolar, desencolar, frente, vaciado)
    ├── test_arbol_binario.py            # Pruebas BST (insertar, consultar, modificar, eliminar, recorridos)
    ├── test_algoritmos_ordenamiento.py  # Pruebas de MergeSort y ShellSort con criterios custom
    ├── test_archivo_codigo.py           # Pruebas del modelo ArchivoCodigo
    ├── test_diagnostico.py              # Pruebas del modelo Diagnostico y prioridades
    ├── test_peticion_ia.py              # Pruebas de transiciones de estado de PeticionIA
    ├── test_configuracion_app.py        # Pruebas de serialización, validación y variables de entorno
    ├── test_contexto_app.py             # Pruebas del contenedor de estado global ContextoApp
    ├── test_servicio_configuracion.py   # Pruebas de lectura de JSON y creación de directorios
    ├── test_servicio_archivos.py        # Pruebas de gestión de archivos y respaldos en disco
    ├── test_servicio_sintaxis.py        # Pruebas de balanceo de delimitadores (), {}, []
    ├── test_servicio_historial.py       # Pruebas de pilas Undo y Redo
    ├── test_servicio_diagnosticos.py    # Pruebas del servicio de ordenamiento de alertas
    ├── test_servicio_cola_ia.py         # Pruebas del buffer FIFO de IA
    ├── test_servicio_cliente_ia.py      # Pruebas del cliente HTTP Gemini y fallback local
    ├── test_servicio_logs.py            # Pruebas de persistencia y lectura de logs
    ├── test_patron_comandos.py          # Pruebas de InvocadorComandos y los 15 comandos concretos
    ├── test_cli.py                      # Pruebas de AnalizadorComandos y ConsolaApp
    └── test_bootstrap.py                # Pruebas de integración del arranque completo en main.py
```

---

## 3. Arquitectura y Patrones de Diseño

### 3.1. Arquitectura en Capas (Layered Architecture)

El sistema implementa una arquitectura estrictamente estratificada en **5 capas funcionales + 1 capa de ensamblaje (Bootstrap)**. Las dependencias fluyen exclusivamente hacia abajo, evitando acoplamiento circular:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CAPA 6: BOOTSTRAP (main.py)                          │
│         Inyección manual de dependencias e inicio del sistema           │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ instancia y enlaza
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    CAPA 5: INTERFAZ CLI (src/cli/)                      │
│          ConsolaApp (Bucle REPL) ──► AnalizadorComandos (Parser)        │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (nombre_cmd, args)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 CAPA 4: PATRÓN COMMAND (src/comandos/)                  │
│          InvocadorComandos ──► ComandoBase ◄── 15 Comandos Concretos    │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ delega acción de negocio
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               CAPA 3: SERVICIOS DE NEGOCIO (src/servicios/)             │
│  Archivos • Sintaxis • Historial • Diagnósticos • ColaIA • ClienteIA    │
└──────────────────┬───────────────────────────────────┬──────────────────┘
                   │ muta / consulta                   │ opera con
                   ▼                                   ▼
┌─────────────────────────────────────┐ ┌─────────────────────────────────┐
│   CAPA 2: NÚCLEO (src/nucleo/)      │ │ CAPA 1: ESTRUCTURAS Y ALGORITMOS│
│ ContextoApp • ArchivoCodigo         │ │ ListaEnlazada • Pila • ColaFIFO │
│ Diagnostico • PeticionIA • Config   │ │ ArbolBinario • Merge/ShellSort  │
└─────────────────────────────────────┘ └─────────────────────────────────┘
```

### 3.2. Patrones de Diseño Identificados

1. **Command Pattern (Patrón Comando):**
   * **Estructura:** Compuesto por `InvocadorComandos` (*Invoker*), la clase abstracta `ComandoBase` (*Command*), las 15 subclases en `src/comandos/` (*Concrete Commands*) y las clases de `src/servicios/` junto a `ContextoApp` (*Receivers*).
   * **Propósito:** Desacoplar por completo el bucle de lectura de terminal (`ConsolaApp`) de las operaciones de negocio. Agregar un comando nuevo no requiere modificar el parser ni la consola; basta con crear una clase hija de `ComandoBase` y registrarla en `bootstrap()`.

2. **Strategy & Template Method Pattern (Estrategia y Método Plantilla en Ordenamiento):**
   * **Estructura:** `OrdenadorBase` define el contrato abstracto `ordenar()` y el método auxiliar común `_es_menor_o_igual()`. `MergeSort` y `ShellSort` implementan las estrategias concretas.
   * **Propósito:** `ServicioDiagnosticos` selecciona dinámicamente en tiempo de ejecución qué algoritmo aplicar (`mergesort` o `shellsort`) y qué función extractora de clave usar (`linea` o `prioridad`) sin acoplarse a los detalles internos del algoritmo.

3. **Dependency Injection & Composition Root (Inyección de Dependencias):**
   * **Estructura:** La función `bootstrap()` en `main.py` instancia el estado compartido (`ContextoApp`), los servicios y los comandos, inyectando por constructor únicamente las dependencias que cada componente necesita.
   * **Propósito:** Evita variables globales o Singletons ocultos, facilitando las pruebas unitarias aisladas en `test/`.

4. **State Object / Shared Context (Contenedor de Estado de Sesión):**
   * **Estructura:** `ContextoApp` centraliza el estado mutable de la sesión en memoria (la `ListaEnlazada` de archivos, el puntero al `ArchivoCodigo` activo, la `ColaFIFO` de peticiones IA, la lista de `Diagnostico` y la `ConfiguracionApp`).

5. **Circuit Breaker / Graceful Fallback (Degradación Elegante Offline):**
   * **Estructura:** En `ServicioClienteIA.procesar_peticion()`, cualquier ausencia de API Key, fallo de red o timeout HTTP activa transparentemente `_analisis_estatico_local()`, garantizando continuidad operativa.

---

## 4. Desglose de Clases, Módulos y Funciones Clave

### 4.1. Punto de Entrada e Interfaz CLI (`main.py` y `src/cli/`)

| Componente | Archivo | Rol y Responsabilidad Principal |
| :--- | :--- | :--- |
| `bootstrap()` / `main()` | `main.py` | Ensambla las capas del proyecto, procesa flags CLI (`-c`/`--config`) e inicia el REPL. |
| `ConsolaApp` | `src/cli/consola_app.py` | Gestiona el bucle `while` interactivo, construye el prompt dinámico (`Komorebi [archivo]> `) y captura interrupciones (`KeyboardInterrupt`, `EOFError`, `SystemExit`). |
| `AnalizadorComandos` | `src/cli/analizador_comandos.py` | Tokeniza la línea ingresada por el usuario usando `shlex.split` (con fallback a `.split()` si hay comillas sin cerrar), retornando `(nombre_comando, argumentos)`. |

### 4.2. Capa de Comandos (`src/comandos/`)

| Componente | Archivo | Sintaxis CLI | Rol y Receptores Invocados |
| :--- | :--- | :--- | :--- |
| `ComandoBase` | `comando_base.py` | *(Abstracta)* | Define propiedades `nombre`, `descripcion`, `sintaxis` y el método abstracto `ejecutar(argumentos)`. |
| `InvocadorComandos` | `invocador_comandos.py` | *(Invoker)* | Almacena el registro `dict[str, ComandoBase]`, busca comandos por nombre y despacha `ejecutar_comando()`. |
| `ComandoNew` | `comando_new.py` | `new <archivo> [contenido]` | Invoca `ServicioArchivos.crear_archivo()` para insertar en la `ListaEnlazada` y respaldar en disco. |
| `ComandoList` | `comando_list.py` | `list` | Recorre los archivos abiertos mediante `ServicioArchivos.listar_archivos()` indicando cuál está activo. |
| `ComandoSwitch` | `comando_switch.py` | `switch <id/nombre>` | Alterna el archivo activo por nombre o índice 1-based vía `ServicioArchivos.cambiar_archivo_activo()`. |
| `ComandoDelete` | `comando_delete.py` | `delete <id/nombre>` | Elimina un archivo de la `ListaEnlazada` y reasigna el archivo activo si era el seleccionado. |
| `ComandoEdit` | `comando_edit.py` | `edit <linea_codigo>` | Guarda snapshot en `ServicioHistorial`, anexa la línea al archivo activo y actualiza el respaldo físico. |
| `ComandoShow` | `comando_show.py` | `show` | Muestra en consola el contenido del `ArchivoCodigo` activo con líneas numeradas. |
| `ComandoUndo` | `comando_undo.py` | `undo` | Desapila el estado previo en `ServicioHistorial.deshacer()`, apila el actual en *Redo* y guarda respaldo. |
| `ComandoRedo` | `comando_redo.py` | `redo` | Desapila de la pila *Redo* en `ServicioHistorial.rehacer()`, restaura el texto y actualiza respaldo. |
| `ComandoCheck` | `comando_check.py` | `check` | Ejecuta `ServicioSintaxis.validar_codigo()` y almacena la lista de `Diagnostico` en `ContextoApp`. |
| `ComandoSort` | `comando_sort.py` | `sort <line\|severity> <mergesort\|shellsort> [asc\|desc]` | Ordena los diagnósticos activos mediante `ServicioDiagnosticos.ordenar()`. |
| `ComandoQueueStatus` | `comando_queue_status.py` | `queue-status` | Consulta `ServicioColaIA.obtener_estado()` e imprime las peticiones pendientes en la `ColaFIFO`. |
| `ComandoAnalyze` | `comando_analyze.py` | `analyze` | Encola el código en `ServicioColaIA`, desencola en orden FIFO y procesa con `ServicioClienteIA`. |
| `ComandoConfig` | `comando_config.py` | `config [ruta_archivo]` | Recarga un archivo JSON externo con `ServicioConfiguracion` o muestra la configuración activa. |
| `ComandoHelp` | `comando_help.py` | `help` | Consulta `InvocadorComandos.listar_comandos()` y formatea la tabla de ayuda. |
| `ComandoExit` | `comando_exit.py` | `exit` | Emite mensaje de cierre y ejecuta `sys.exit(0)`, capturado por `ConsolaApp.iniciar_repl()`. |

### 4.3. Capa de Servicios de Negocio (`src/servicios/`)

| Servicio | Archivo | Estructuras / Modelos que Orquesta | Responsabilidad Principal |
| :--- | :--- | :--- | :--- |
| `ServicioConfiguracion` | `servicio_configuracion.py` | `ConfiguracionApp` | Lee `config.json`, inyecta variables de `.env` y asegura la existencia física de `respaldos/` y `logs/`. |
| `ServicioArchivos` | `servicio_archivos.py` | `ContextoApp`, `ArchivoCodigo`, `ListaEnlazada` | Gestiona el alta, baja, cambio y listado de archivos en memoria, sincronizando copias físicas en `respaldos/`. |
| `ServicioSintaxis` | `servicio_sintaxis.py` | `Pila`, `Diagnostico` | Verifica línea por línea y columna por columna el balanceo de `()`, `{}` y `[]` apilando aperturas y comparando cierres. |
| `ServicioHistorial` | `servicio_historial.py` | Dos instancias de `Pila` (`_pila_deshacer`, `_pila_rehacer`) | Administra snapshots de texto para revertir (`undo`) o rehacer (`redo`) cambios, limpiando `redo` ante nuevas ediciones. |
| `ServicioDiagnosticos` | `servicio_diagnosticos.py` | `MergeSort`, `ShellSort`, `Diagnostico` | Traduce criterios textuales (`line`/`severity`) a funciones `lambda` y delega el ordenamiento al algoritmo elegido. |
| `ServicioColaIA` | `servicio_cola_ia.py` | `ColaFIFO`, `PeticionIA` | Encola y desencola solicitudes hacia la IA en estricto orden de llegada (FIFO) y construye reportes de estado. |
| `ServicioClienteIA` | `servicio_cliente_ia.py` | `ConfiguracionApp`, `PeticionIA` | Ejecuta peticiones HTTP POST a Google Gemini REST o activa el analizador estático local offline si no hay red/API Key. |
| `ServicioLogs` | `servicio_logs.py` | Archivo `logs/errores.log` | Escribe trazas con marca de tiempo (`INFO`, `WARNING`, `ERROR`) para auditoría y diagnóstico de fallos. |

### 4.4. Capa de Núcleo, Estructuras de Datos y Algoritmos (`src/nucleo/`, `src/estructuras/`, `src/algoritmos/`)

| Categoría | Clase | Archivo | Detalles Técnicos y Complejidad |
| :--- | :--- | :--- | :--- |
| **Núcleo** | `ContextoApp` | `contexto_app.py` | Mantiene `_archivos_abiertos` (`ListaEnlazada`), `_archivo_activo`, `_cola_ia` (`ColaFIFO`), `_diagnosticos` y `_configuracion`. |
| **Núcleo** | `ArchivoCodigo` | `archivo_codigo.py` | Encapsula nombre, contenido textual, timestamps de creación/modificación, conteo de líneas y tamaño en bytes. |
| **Núcleo** | `Diagnostico` | `diagnostico.py` | Alerta con `linea`, `columna`, `severidad` (`INFO`=1, `WARN`=2, `ERROR`=3) y propiedad numérica `prioridad`. |
| **Núcleo** | `PeticionIA` | `peticion_ia.py` | Máquina de estados (`PENDIENTE` $\rightarrow$ `EN_PROCESO` $\rightarrow$ `COMPLETADO` \| `FALLIDO`) con ID único `req-<uuid>`. |
| **Núcleo** | `ConfiguracionApp` | `configuracion_app.py` | Resuelve interpolación `${GEMINI_API_KEY}`, enmascara claves sensibles y construye URLs completas del endpoint IA. |
| **Estructura** | `ListaEnlazada` + `NodoLista` | `lista_enlazada.py` | Doblemente enlazada (`_cabeza`, `_cola`). Inserción en extremos $\mathcal{O}(1)$, búsqueda $\mathcal{O}(n)$, desvinculación con `match-case` $\mathcal{O}(1)$. |
| **Estructura** | `Pila` + `NodoPila` | `pila.py` | Estructura LIFO con puntero `_tope`. Operaciones `apilar`, `desapilar` y `cima` en tiempo constante $\mathcal{O}(1)$. |
| **Estructura** | `ColaFIFO` + `NodoCola` | `cola_fifo.py` | Estructura FIFO con punteros `_frente` y `_final`. Operaciones `encolar`, `desencolar` y `frente` en $\mathcal{O}(1)$. |
| **Estructura** | `ArbolBinario` + `NodoArbol` | `arbol_binario.py` | Árbol Binario de Búsqueda (BST). Soporta `insertar`, `consultar`, `modificar`, `eliminar` (3 casos vía `match-case`) en $\mathcal{O}(\log n)$ promedio, y recorridos `inorden`, `preorden`, `postorden` en $\mathcal{O}(n)$. |
| **Algoritmo** | `MergeSort` | `mergesort.py` | Ordenamiento recursivo Divide y Vencerás estable. Complejidad temporal $\mathcal{O}(n \log n)$ garantizada y espacial $\mathcal{O}(n)$. |
| **Algoritmo** | `ShellSort` | `shellsort.py` | Ordenamiento por inserción con intervalos de Knuth ($h = 3h + 1$). Complejidad temporal $\mathcal{O}(n^{3/2})$ prom. y espacial auxiliar $\mathcal{O}(1)$. |

---

## 5. Flujo de Ejecución (Data Flow)

### 5.1. Fase de Arranque e Inicialización (Bootstrap)

1. **Entrada por SO:** El usuario ejecuta `python3 main.py` (opcionalmente con `--config <ruta>`). La función `main()` extrae la ruta de configuración y llama a `bootstrap(ruta_config)`.
2. **Carga de Configuración y Entorno:** `ServicioConfiguracion.cargar_configuracion()` lee variables desde `.env` (si existe), parsea `config.json` construyendo una instancia de `ConfiguracionApp` y crea los directorios físicos `respaldos/` y `logs/`.
3. **Creación del Estado Global:** Se instancia `ContextoApp(configuracion)`, que inicializa una `ListaEnlazada` vacía para los archivos y una `ColaFIFO` vacía para las peticiones de IA.
4. **Instanciación de Servicios y Registro de Comandos:** Se crean los 7 servicios adicionales y se registran las 15 instancias de comandos concretos dentro de `InvocadorComandos`.
5. **Inicio del Bucle REPL:** Se retorna `ConsolaApp` y se invoca `consola.iniciar_repl()`.

### 5.2. Ciclo de Vida de una Petición Interactiva (Paso a Paso)

En cada iteración del bucle REPL dentro de `ConsolaApp`, el flujo de datos atraviesa las capas de la siguiente forma:

```
[Usuario en Terminal]
       │ 1. Ingresa línea de texto (ej. "check", "sort severity mergesort desc", "analyze")
       ▼
[ConsolaApp.ejecutar_linea()] (src/cli/consola_app.py)
       │ 2. Solicita tokenización de la cadena
       ▼
[AnalizadorComandos.parsear()] (src/cli/analizador_comandos.py)
       │ 3. Retorna tupla normalizada: (nombre_cmd, lista_argumentos)
       ▼
[InvocadorComandos.ejecutar_comando()] (src/comandos/invocador_comandos.py)
       │ 4. Busca en diccionario O(1) la instancia ComandoBase y llama a comando.ejecutar(args)
       ▼
[Comando Concreto] (src/comandos/comando_*.py)
       │ 5. Valida argumentos y delega la operación al Servicio de Negocio inyectado
       ▼
[Servicio de Negocio] (src/servicios/servicio_*.py)
       │ 6. Manipula Modelos de Dominio (src/nucleo/) apoyándose en Estructuras/Algoritmos (src/estructuras/, src/algoritmos/)
       ▼
[ContextoApp / Disco / Consola]
       │ 7. Actualiza el estado en memoria, persiste respaldos/logs y muestra respuesta en CLI
```

#### Casos de Flujo Representativos hasta las Capas Profundas:

* **Flujo A — Creación, Edición y Retroceso (`new` $\rightarrow$ `edit` $\rightarrow$ `undo`):**
  1. `new app.py "def suma(a, b):"` $\rightarrow$ `ComandoNew` llama a `ServicioArchivos.crear_archivo()` $\rightarrow$ crea `ArchivoCodigo` $\rightarrow$ `ContextoApp.abrir_archivo()` invoca `ListaEnlazada.insertar_al_final()` envolviendo el archivo en un `NodoLista` en $\mathcal{O}(1)$ y escribe `respaldos/app.py`.
  2. `edit "    return a + b"` $\rightarrow$ `ComandoEdit` invoca `ServicioHistorial.registrar_modificacion()`, el cual apila el texto anterior en `_pila_deshacer` (`Pila.apilar()` creando un `NodoPila`) y limpia `_pila_rehacer`. Luego actualiza `ArchivoCodigo.modificar_contenido()` y sobreescribe el respaldo en disco.
  3. `undo` $\rightarrow$ `ComandoUndo` llama a `ServicioHistorial.deshacer()`, que extrae el snapshot de `_pila_deshacer` (`Pila.desapilar()` desvinculando el `NodoPila`), apila el estado actual en `_pila_rehacer` y restaura el contenido previo del archivo.

* **Flujo B — Validación Sintáctica y Ordenamiento (`check` $\rightarrow$ `sort`):**
  1. `check` $\rightarrow$ `ComandoCheck` invoca `ServicioSintaxis.validar_codigo()` $\rightarrow$ recorre cada carácter del archivo activo; apila `(simbolo, linea, col)` en su `Pila` ante `(` `{` `[` y desapila al encontrar `)` `}` `]`. Las discrepancias generan instancias de `Diagnostico` que se guardan en `ContextoApp.diagnosticos`.
  2. `sort severity mergesort desc` $\rightarrow$ `ComandoSort` llama a `ServicioDiagnosticos.ordenar()` $\rightarrow$ resuelve `severity` a `lambda d: d.prioridad` y ejecuta `MergeSort.ordenar()` con `ascendente=False` $\rightarrow$ divide recursivamente la lista de diagnósticos y los intercala en `_mezclar()` usando `OrdenadorBase._es_menor_o_igual()`.

* **Flujo C — Buffer FIFO y Análisis de Complejidad con IA (`analyze`):**
  1. `analyze` $\rightarrow$ `ComandoAnalyze` invoca `ServicioColaIA.encolar()`, que instancia una `PeticionIA` en estado `PENDIENTE` y la inserta al final de la `ColaFIFO` (`NodoCola`).
  2. Acto seguido, `ServicioColaIA.desencolar_siguiente()` extrae la petición del frente de la `ColaFIFO` en $\mathcal{O}(1)$ y la entrega a `ServicioClienteIA.procesar_peticion()`.
  3. `ServicioClienteIA` cambia el estado a `EN_PROCESO`. Si hay API Key configurada, envía un `POST` JSON a Google Gemini (`urllib.request`); si no hay clave o ocurre un error de red, registra el incidente en `ServicioLogs` y ejecuta `_analisis_estatico_local()`. Finalmente, marca la petición como `COMPLETADO` e imprime el reporte de complejidad temporal, espacial y propuestas de refactorización.

