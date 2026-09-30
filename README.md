# Komorebi Mini IDE

**Algoritmos y Estructuras II - Septiembre de 2026**  
**Universidad José Antonio Páez - Facultad de Ingeniería**  
**Escuela de Ingeniería en Computación**

Komorebi es un entorno de desarrollo minimalista (**Mini IDE**) interactivo para terminal, construido desde cero en **Python** bajo el paradigma de **Programación Orientada a Objetos (POO)**. Aplica el patrón de diseño **Command (Comandos)**, implementa estructuras de datos fundamentales (lineales y no lineales) y algoritmos de ordenamiento avanzados sin el uso de estructuras ni métodos nativos prohibidos (`list.sort()`, `collections.deque`, etc.), e integra lectura de configuración externa y asistencia mediante Inteligencia Artificial (Google Gemini con fallback local seguro).

---

## 🏗️ Arquitectura del Sistema

El sistema sigue un diseño desacoplado en capas concebido bajo el enfoque *Bottom-Up* (De lo Particular a lo General), donde cada clase reside en su propio fichero independiente:

```
┌────────────────────────────────────────────────────────┐
│             main.py / ConsolaApp (CLI)                 │
└───────────────────────────┬────────────────────────────┘
                            │ Despacha comandos (REPL)
                            ▼
┌────────────────────────────────────────────────────────┐
│           Capa de Comandos (Patrón Command)            │
│  InvocadorComandos ──► ComandoBase (15 comandos)       │
└───────────────────────────┬────────────────────────────┘
                            │ Invoca servicios receptores
                            ▼
┌────────────────────────────────────────────────────────┐
│             Capa de Servicios de Negocio               │
│  Archivos • Sintaxis • Historial • Diagnósticos • IA   │
└──────────────┬──────────────────────────┬──────────────┘
               │ Modela datos             │ Opera sobre
               ▼                          ▼
┌───────────────────────────┐  ┌─────────────────────────┐
│     Modelos de Núcleo     │  │  Estructuras Propias    │
│  ArchivoCodigo            │  │  ListaEnlazada (Doble)  │
│  Diagnostico              │  │  Pila (LIFO)            │
│  PeticionIA               │  │  ColaFIFO (FIFO)        │
│  ConfiguracionApp         │  │  ArbolBinario (BST)     │
│  ContextoApp              │  │  MergeSort / ShellSort  │
└───────────────────────────┘  └─────────────────────────┘
```

---

## 🧩 Diagrama de Clases (Patrón Command y Estructuras)

```
       ┌──────────────────┐
       │   ComandoBase    │◄─────────────────────────────┐
       │  (Abstract Class)│                              │
       ├──────────────────┤                              │
       │ + ejecutar()     │                              │
       └────────▲─────────┘                              │
                │ Realizaciones                          │
   ┌────────────┴───────────────┐                        │
   │ ComandoNew                 │                        │
   │ ComandoList                │                        │
   │ ComandoSwitch              │                        │
   │ ComandoDelete              │                        │
   │ ComandoConfig              │                        │ Registra y ejecuta
   │ ComandoCheck               │                        │
   │ ComandoUndo / Redo         │                        │
   │ ComandoSort                │               ┌────────┴──────────┐
   │ ComandoQueueStatus         │               │ InvocadorComandos │
   │ ComandoAnalyze             │               ├───────────────────┤
   │ ComandoEdit / Show / Help  │               │ - _comandos: dict │
   └────────────┬───────────────┘               └───────────────────┘
                │ Invoca Receptores
                ▼
┌────────────────────────────────────────────────────────────────┐
│                   Servicios de Negocio                         │
│  ServicioArchivos ────────► ListaEnlazada (NodoLista)          │
│  ServicioSintaxis ────────► Pila (NodoPila)                    │
│  ServicioHistorial ───────► Pila Undo / Pila Redo              │
│  ServicioDiagnosticos ────► MergeSort / ShellSort              │
│  ServicioColaIA ──────────► ColaFIFO (NodoCola)                │
│  ServicioClienteIA ───────► Google Gemini API REST / Offline   │
└────────────────────────────────────────────────────────────────┘
```

---

## 📊 Análisis de Complejidad Temporal y Espacial ($Big\ O$)

Todas las estructuras de datos y algoritmos de ordenamiento fueron programados desde cero:

| Componente / Estructura | Operación Clave | Complejidad Temporal | Complejidad Espacial | Justificación Técnica |
| :--- | :--- | :---: | :---: | :--- |
| **ListaEnlazada** (Doble) | Inserción Inicio / Final | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Acceso directo vía punteros `_cabeza` y `_cola`. |
| | Eliminación con referencia | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Desvinculación inmediata puenteando nodos vecinos. |
| | Búsqueda por Criterio | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Recorrido lineal secuencial desde la cabeza. |
| **Pila** (LIFO) | `apilar` (*push*) | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Mutación del puntero `_tope`. |
| | `desapilar` (*pop*) | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Extracción de la cima y avance al siguiente nodo. |
| **ColaFIFO** (FIFO) | `encolar` (*enqueue*) | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Inserción directa en `_final`. |
| | `desencolar` (*dequeue*) | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Extracción directa desde `_frente`. |
| **ArbolBinario** (BST) | Búsqueda / Inserción | $\mathcal{O}(\log n)$ prom. | $\mathcal{O}(\log n)$ prom. | Descarte de la mitad del subárbol en cada nivel. |
| | Eliminación de Nodo | $\mathcal{O}(\log n)$ prom. | $\mathcal{O}(\log n)$ prom. | Reemplazo por sucesor inorden (mínimo derecho). |
| | Recorrido Inorden | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Visita exhaustiva de todos los vértices. |
| **MergeSort** | `ordenar` | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | Divide y Vencerás con división en $\log n$ niveles y mezcla lineal. |
| **ShellSort** | `ordenar` | $\mathcal{O}(n^{3/2})$ prom. | $\mathcal{O}(1)$ *in-place* | Inserción con saltos según secuencia de Knuth ($h = 3h + 1$). |

---

## 💻 Comandos Disponibles de la Consola CLI

La aplicación interactúa mediante un prompt dinámico (`Komorebi [archivo_activo]> `), **sin menús numéricos**:

| Comando | Sintaxis de Ejemplo | Descripción |
| :--- | :--- | :--- |
| `new` | `new main.cpp int main() { return 0; }` | Crea un archivo en memoria y genera respaldo en disco. |
| `list` | `list` | Muestra todos los archivos abiertos y marca el activo. |
| `switch` | `switch main.cpp` o `switch 1` | Alterna el archivo activo por nombre o posición. |
| `delete` | `delete main.cpp` | Cierra el archivo y libera sus nodos en memoria. |
| `config` | `config config.json` | Carga parámetros externos o imprime la configuración activa. |
| `check` | `check` | Valida balanceo de delimitadores `()`, `{}`, `[]` usando Pila. |
| `undo` | `undo` | Deshace la última modificación usando la pila de retroceso. |
| `redo` | `redo` | Rehace el cambio revertido usando la pila de avance. |
| `sort` | `sort line mergesort` | Ordena alertas por línea o gravedad usando MergeSort o ShellSort. |
| `queue-status` | `queue-status` | Muestra el estado del buffer FIFO de peticiones de IA. |
| `analyze` | `analyze` | Encola en el buffer y solicita análisis $Big\ O$ a la IA. |
| `edit` | `edit x = 10` | Agrega código al archivo activo registrando historial. |
| `show` | `show` | Imprime el contenido del archivo actual numerando líneas. |
| `help` | `help` | Imprime la guía de todos los comandos disponibles. |
| `exit` | `exit` | Cierra ordenadamente la sesión. |

---

## 🚀 Requisitos e Instrucciones de Ejecución

### Requisitos
* Python 3.10 o superior (el proyecto hace uso de *Structural Pattern Matching* `match-case` y anotaciones de tipo modernas).
* Sin dependencias externas obligatorias (utiliza únicamente la biblioteca estándar de Python: `urllib`, `json`, `shlex`, `datetime`, `unittest`).

### Ejecución de la Consola
```bash
python3 main.py
```
O especificando un archivo de configuración personalizado:
```bash
python3 main.py --config config.json
```

### Ejecución de la Suite de Pruebas Unitarias
El proyecto cuenta con **89 pruebas unitarias automatizadas** que validan todas las capas:
```bash
python3 -m unittest discover -s test -p "test_*.py" -v
```

---

## ⚙️ Configuración (`config.json`)

```json
{
  "nombre_app": "Komorebi Mini IDE",
  "rutas": {
    "respaldos": "respaldos",
    "logs": "logs"
  },
  "ia": {
    "proveedor": "gemini",
    "modelo": "gemini-1.5-flash",
    "api_key": "",
    "url_base": "https://generativelanguage.googleapis.com/v1beta/models",
    "endpoint_analisis": "/analizar",
    "timeout_segundos": 15
  },
  "servidor": {
    "puerto": 8000
  }
}
```
