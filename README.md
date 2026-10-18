# Komorebi Mini IDE

**Algoritmos y Estructuras II - Septiembre de 2026**  
**Universidad José Antonio Páez - Facultad de Ingeniería**  
**Escuela de Ingeniería en Computación**

Komorebi es un entorno de desarrollo minimalista (**Mini IDE**) interactivo para terminal, construido desde cero en **Python** bajo el paradigma de **Programación Orientada a Objetos (POO)**. Aplica el patrón de diseño **Command (Comandos)**, implementa estructuras de datos fundamentales **lineales** (`ListaEnlazada`, `Pila`, `ColaFIFO`) y **no lineales arbóreas** (`ArbolNario`, `ArbolExpresion`, `ArbolAVL`, `ArbolB` de orden $m=4$) junto con algoritmos de ordenamiento avanzados (`MergeSort`, `ShellSort`) sin el uso de estructuras ni métodos nativos prohibidos (`list.sort()`, `sorted()`, `collections.deque`, `eval()`, `ast`), e integra lectura de configuración externa y asistencia mediante Inteligencia Artificial (Google Gemini con fallback local seguro).

---

## 🏗️ Arquitectura del Sistema

El sistema sigue un diseño desacoplado en capas concebido bajo el enfoque *Bottom-Up* (De lo Particular a lo General), donde **cada clase reside en su propio fichero independiente**:

```
┌────────────────────────────────────────────────────────────────┐
│                 main.py / ConsolaApp (CLI REPL)                │
└───────────────────────────────┬────────────────────────────────┘
                                │ Despacha comandos (REPL)
                                ▼
┌────────────────────────────────────────────────────────────────┐
│               Capa de Comandos (Patrón Command)                │
│     InvocadorComandos ──► ComandoBase (27 comandos CLI)        │
└───────────────────────────────┬────────────────────────────────┘
                                │ Invoca servicios receptores
                                ▼
┌────────────────────────────────────────────────────────────────┐
│                 Capa de Servicios de Negocio                   │
│  Archivos • Workspace • Expresiones • Diccionario • Indexación │
│  Sintaxis • Historial • Diagnósticos • Cola IA • Cliente IA    │
└──────────────────┬──────────────────────────┬──────────────────┘
                   │ Modela datos             │ Opera sobre
                   ▼                          ▼
┌───────────────────────────────┐  ┌─────────────────────────────┐
│       Modelos de Núcleo       │  │     Estructuras Propias     │
│  ArchivoCodigo (id inmutable) │  │  ListaEnlazada (Doble)      │
│  ReferenciaToken (inmutable)  │  │  Pila (LIFO) / ColaFIFO     │
│  Diagnostico / PeticionIA     │  │  ArbolNario (Workspace)     │
│  ConfiguracionApp             │  │  ArbolExpresion (AST/RPN)   │
│  ContextoApp                  │  │  ArbolAVL (Diccionario)     │
│  Jerarquía ErrorSynthetix     │  │  ArbolB m=4 (Índice Global) │
└───────────────────────────────┘  └─────────────────────────────┘
```

---

## 📊 Análisis de Complejidad Temporal y Espacial ($Big\ O$)

### 1. Estructuras No Lineales (Árboles — Fase 2)

| Estructura | Búsqueda | Inserción | Eliminación | Recorridos / Consultas | Espacio | Justificación Técnica |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Árbol N-ario (`ArbolNario`)** | $\mathcal{O}(d \cdot b)$ por ruta / $\mathcal{O}(n)$ global | $\mathcal{O}(d \cdot b)$ | $\mathcal{O}(d \cdot b + s)$ | Preorden iterativo (`tree`): $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | $d$: profundidad de la ruta; $b$: hijos por directorio; $s$: tamaño del subárbol eliminado. Usa `ListaEnlazada` para hijos y `Pila` explícita en `tree`. |
| **Árbol de Expresiones (`ArbolExpresion`)** | $\mathcal{O}(n)$ | Construcción Shunting-Yard: $\mathcal{O}(n)$ | N/A (Inmutable tras construcción) | `evaluar()`, `preorden()`, `inorden()`, `postorden()`: $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Cada token se apila y desapila a lo sumo una vez en dos instancias de `Pila`. Evaluación postorden exacta con `fractions.Fraction`. |
| **Árbol AVL (`ArbolAVL`)** | $\mathcal{O}(\log n)$ peor caso | $\mathcal{O}(\log n)$ peor caso | $\mathcal{O}(\log n)$ peor caso | `inorden()`: $\mathcal{O}(n)$ <br> `sugerir(prefijo)` con poda: $\mathcal{O}(\log n + k)$ | $\mathcal{O}(n)$ | Invariante $\|\text{FB}\| \le 1$ mantenida con rotaciones simples (`LL`, `RR`) y dobles (`LR`, `RL`) en $\mathcal{O}(1)$. Altura acotada por $1.44 \log_2(n+2)$. |
| **Árbol B (`ArbolB`, orden $m=4$)** | $\mathcal{O}(\log_m n)$ peor caso | $\mathcal{O}(m \log_m n) = \mathcal{O}(\log n)$ | $\mathcal{O}(m \log_m n) = \mathcal{O}(\log n)$ | `inorden()` multicamino: $\mathcal{O}(n)$ | $\mathcal{O}(n + R)$ | Nodos con $[1, 3]$ claves y $[2, 4]$ hijos; hojas al mismo nivel. Inserción *bottom-up* con *split* por mediana y eliminación con préstamo/fusión. $R$: total de `ReferenciaToken`. |

### 2. Estructuras Lineales y Algoritmos de Ordenamiento (Fase 1)

| Componente / Estructura | Operación Clave | Complejidad Temporal | Complejidad Espacial | Justificación Técnica |
| :--- | :--- | :---: | :---: | :--- |
| **ListaEnlazada** (Doble) | Inserción Inicio / Final | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Acceso directo vía punteros `_cabeza` y `_cola`. |
| | Eliminación con referencia | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Desvinculación inmediata puenteando nodos vecinos. |
| | Búsqueda por Criterio | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Recorrido lineal secuencial desde la cabeza. |
| **Pila** (LIFO) | `apilar` (*push*) / `desapilar` (*pop*) | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Mutación directa del puntero `_tope`. |
| **ColaFIFO** (FIFO) | `encolar` / `desencolar` | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Inserción en `_final` y extracción desde `_frente`. |
| **MergeSort** | `ordenar` | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | Divide y Vencerás con división en $\log_2 n$ niveles y mezcla lineal. |
| **ShellSort** | `ordenar` | $\mathcal{O}(n^{3/2})$ prom. | $\mathcal{O}(1)$ *in-place* | Inserción con saltos decrecientes de Knuth ($h = 3h + 1$). |

---

## 💻 Comandos Disponibles de la Consola CLI

La aplicación interactúa mediante un prompt dinámico (`Komorebi [/ruta]> `), **sin menús numéricos**:

### Gestión del Workspace Jerárquico (Árbol N-ario y Lista Enlazada)
| Comando | Sintaxis | Descripción |
| :--- | :--- | :--- |
| `mkdir` | `mkdir <ruta>` | Crea un nuevo directorio en el árbol N-ario del Workspace. |
| `cd` | `cd [ruta \| ws:ruta \| -]` | Navega libremente por el **sistema de archivos real** (absolutas, relativas, `~`, `..`, `-`; sin argumento va a `~`). Con el prefijo `ws:` (o `@ws`) entra al Workspace virtual: `cd ws:/src`. |
| `pwd` | `pwd` | Muestra la ruta actual: real, o `ws:/ruta` cuando se está en el Workspace virtual. |
| `ls` | `ls [-a] [ruta \| ws:ruta]` | Lista el contenido del directorio actual o indicado (orden alfabético; `-a` incluye ocultos). Usa `ws:` para listar el Workspace virtual. |
| `tree` | `tree [ruta]` | Dibuja la jerarquía del Workspace mediante recorrido preorden iterativo con `Pila`. |
| `mv` | `mv <origen> <destino>` | Mueve o renombra un archivo o carpeta previniendo ciclos jerárquicos. |
| `new` | `new <nombre> [contenido]` | Crea un archivo en el directorio actual, lo abre en la sesión y guarda respaldo físico. |
| `list` | `list [nombre_o_ruta]` | Muestra los archivos abiertos en sesión indicando su ruta en el Workspace. |
| `switch` | `switch <id/nombre/ruta>` | Cambia el archivo activo detectando ambigüedades si existen homónimos. |
| `delete` | `delete <nombre_o_ruta>` | Elimina un archivo o carpeta del árbol N-ario, la lista enlazada, el índice B-Tree y el disco. |
| `edit` | `edit <linea_de_codigo>` | Agrega una línea de código al archivo activo registrando historial Undo/Redo. |
| `show` | `show` | Imprime el contenido numerado del archivo activo. |

> **Nota:** `mkdir`, `tree`, `mv`, `new`, `delete`, `index-all` y `find-global` operan siempre sobre el Workspace virtual (rutas como `/src/app.py`), sin importar si el prompt muestra una ruta real o `ws:`. El prompt indica la ubicación activa: `Komorebi [/home/usuario]>` (SO real) o `Komorebi [ws:/src]>` (Workspace).

### Evaluación Aritmética Exacta (Árbol Binario de Expresiones)
| Comando | Sintaxis | Descripción |
| :--- | :--- | :--- |
| `eval` | `eval ["<expresion>"] [--tree]` | Evalúa una expresión aritmética exacta (o las líneas aritméticas del archivo activo) mostrando recorridos inorden, preorden, postorden (RPN) y árbol ASCII opcional. |

### Diccionario Técnico y Autocompletado (Árbol AVL)
| Comando | Sintaxis | Descripción |
| :--- | :--- | :--- |
| `add-keyword` | `add-keyword <palabra> [descripcion]` | Inserta una nueva palabra clave en el diccionario AVL autobalanceado. |
| `suggest` | `suggest <prefijo>` | Autocompleta palabras clave por prefijo usando búsqueda con poda en $\mathcal{O}(\log n + k)$. |
| `remove-keyword` | `remove-keyword <palabra>` | Elimina una palabra clave del diccionario AVL rebalanceando los ancestros. |

### Indexación Global de Tokens (Árbol B de Orden $m=4$)
| Comando | Sintaxis | Descripción |
| :--- | :--- | :--- |
| `index-all` | `index-all` | Escanea todos los archivos del Workspace e indexa sus identificadores en el Árbol B ignorando keywords del AVL. |
| `find-global` | `find-global <token>` | Busca un identificador en el Árbol B y muestra los archivos (con ruta) y números de línea donde aparece. |

### Verificación Sintáctica, Historial, Diagnósticos, IA y Sistema
| Comando | Sintaxis | Descripción |
| :--- | :--- | :--- |
| `check` | `check` | Verifica el balanceo de delimitadores `()`, `{}`, `[]` usando `Pila`. |
| `undo` | `undo` | Deshace el último cambio en el archivo activo usando la pila Undo. |
| `redo` | `redo` | Rehace el último cambio revertido usando la pila Redo. |
| `sort` | `sort <line\|severity> [mergesort\|shellsort] [asc\|desc]` | Ordena los diagnósticos estáticos con MergeSort o ShellSort. |
| `queue-status` | `queue-status` | Muestra el estado de la cola FIFO de peticiones de IA. |
| `analyze` | `analyze` | Encola y despacha el análisis de complejidad algorítmica asistido por IA. |
| `config` | `config [ruta_json]` | Muestra o recarga la configuración externa del sistema. |
| `clear` | `clear` (o `cls`) | Limpia la pantalla de la terminal interactiva. |
| `help` | `help` | Muestra el listado completo de comandos disponibles y su sintaxis. |
| `exit` | `exit` | Finaliza de forma segura la sesión del Mini IDE. |

---

## 🚀 Requisitos e Instrucciones de Ejecución

### Requisitos
* Python 3.10 o superior.
* Sin dependencias externas obligatorias (únicamente biblioteca estándar de Python: `fractions`, `math`, `shlex`, `json`, `urllib`, `datetime`, `uuid`, `unittest`).

### Ejecución de la Consola
```bash
python3 main.py
```

### Ejecución de la Suite de Pruebas Unitarias e Integración
El proyecto cuenta con **140 pruebas automatizadas** (unitarias + integración E2E + auditoría arquitectónica):
```bash
python3 -m unittest discover -s test -p "test_*.py" -v
```

### Demostración Empírica de Altura: Árbol AVL vs. BST sin Balanceo
```bash
python3 -m scripts.demo_avl_vs_bst
```

---

## 📚 Documentación Arquitectónica y de Defensa

* **[Mapa Arquitectónico del Proyecto (`docs/ESTRUCTURA.md`)](docs/ESTRUCTURA.md):** Árbol de directorios completo, patrones de diseño, desglose de módulos y flujos de ejecución.
* **[Guía de Defensa — Fase 2: Estructuras Arbóreas (`docs/guia_defensa_fase2.md`)](docs/guia_defensa_fase2.md):** Explicación didáctica de las 4 estructuras arbóreas, trazas paso a paso con diagramas ASCII (rotaciones AVL, split/fusión en Árbol B, Shunting-Yard), justificación formal de complejidades y 10 preguntas avanzadas de defensa con sus respuestas.
* **[Estándar de Commits (`docs/commits.md`)](docs/commits.md):** Convención de mensajes de commit utilizada en todas las ramas del proyecto.
