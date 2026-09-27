# Plan de Estructuración y Desarrollo - Proyecto Komorebi
**Algoritmos y Estructuras II**  
**Enfoque de Desarrollo:** *Bottom-Up* (De lo Particular a lo General)  
**Paradigma:** Programación Orientada a Objetos en Python (Estricto: una clase por fichero)

---

## 🎯 Objetivo del Plan
Desglosar la construcción del Mini IDE en fases secuenciales que van desde las unidades más atómicas (nodos y algoritmos) hasta las capas más complejas (servicios, patrón comando, CLI y punto de entrada), garantizando el cumplimiento total de los requisitos de la cátedra sin dependencias circulares.

```
       [ Fase 6: main.py & Inicialización Global ]
                           ▲
       [ Fase 5: CLI / REPL & Parser de Comandos ]
                           ▲
       [ Fase 4: Patrón Command (Invoker & Comandos) ]
                           ▲
       [ Fase 3: Servicios de Negocio (Receptores) ]
                           ▲
       [ Fase 2: Modelos de Dominio & Estado (Núcleo) ]
                           ▲
       [ Fase 1: Estructuras de Datos & Algoritmos Base ]
```

---

## Fase 1: Componentes Atómicos (De lo Particular)
En esta fase se construyen los bloques fundamentales sobre los que reposará todo el sistema. **Prohibido el uso de estructuras y métodos nativos (`list.sort()`, `collections.deque`, etc.)**.

### 1.1. Nodos de Estructuras (Un fichero por cada nodo)
* **`src/estructuras/nodo_lista.py`**:
  * Clase `NodoLista`: almacena el dato (archivo/contenido) y punteros `siguiente` (y `anterior` si es doblemente enlazada).
* **`src/estructuras/nodo_pila.py`**:
  * Clase `NodoPila`: almacena el elemento (carácter/delimitador o estado de texto) y referencia `siguiente`.
* **`src/estructuras/nodo_cola.py`**:
  * Clase `NodoCola`: almacena la petición de IA y referencia `siguiente`.
* **`src/estructuras/nodo_arbol.py`**:
  * Clase `NodoArbol`: almacena `valor`, puntero `izquierda` y puntero `derecha`.

### 1.2. Estructuras de Datos Propias
* **`src/estructuras/lista_enlazada.py`**:
  * Clase `ListaEnlazada`: operaciones `insertar`, `eliminar`, `buscar`, `listar`, `obtener_por_indice`. Gestión de memoria y enlaces.
* **`src/estructuras/pila.py`**:
  * Clase `Pila`: operaciones LIFO `apilar` (*push*), `desapilar` (*pop*), `cima` (*peek*), `esta_vacia`, `tamano`.
* **`src/estructuras/cola_fifo.py`**:
  * Clase `ColaFIFO`: operaciones FIFO `encolar` (*enqueue*), `desencolar` (*dequeue*), `frente`, `esta_vacia`, `tamano`.
* **`src/estructuras/arbol_binario.py`**:
  * Clase `ArbolBinario`: operaciones requeridas en apuntes: `raiz`, `insertar`, `eliminar`, `modificar`, `consultar`.

### 1.3. Algoritmos de Ordenamiento Propios
* **`src/algoritmos/ordenador_base.py`**:
  * Clase abstracta `OrdenadorBase`: define el contrato `ordenar(coleccion, criterio, ascendente=True)`.
* **`src/algoritmos/mergesort.py`**:
  * Clase `MergeSort`: implementación divide y vencerás manual con complejidad $O(n \log n)$.
* **`src/algoritmos/shellsort.py`**:
  * Clase `ShellSort`: implementación con secuencias de intervalos (*gaps*) manual.

---

## Fase 2: Modelos de Dominio y Núcleo de Estado
Representación de la información de negocio que circula por el sistema.

* **`src/nucleo/archivo_codigo.py`**:
  * Clase `ArchivoCodigo`: representa un fichero en memoria (nombre, contenido en texto plano, fecha de creación/modificación).
* **`src/nucleo/diagnostico.py`**:
  * Clase `Diagnostico`: representa una advertencia o alerta de código (número de línea, gravedad/severidad: 'INFO', 'WARN', 'ERROR', mensaje).
* **`src/nucleo/peticion_ia.py`**:
  * Clase `PeticionIA`: modelo para encolar solicitudes (id, código a analizar, timestamp, estado).
* **`src/nucleo/configuracion_app.py`**:
  * Clase `ConfiguracionApp`: encapsula los valores leídos de `config.json` (rutas de respaldos, logs, URL base de IA, timeouts).
* **`src/nucleo/contexto_app.py`**:
  * Clase `ContextoApp`: almacena el estado global de la sesión en vivo (lista de archivos abiertos, referencia al archivo activo actual, configuración activa y diagnósticos generados).

---

## Fase 3: Capa de Servicios (Lógica de Negocio y Receptores)
Orquestan las operaciones complejas utilizando las estructuras de la Fase 1 y los modelos de la Fase 2.

* **`src/servicios/servicio_configuracion.py`**:
  * Clase `ServicioConfiguracion`: carga y valida el archivo `config.json`. Verifica existencia de carpetas `respaldos/` y `logs/`.
* **`src/servicios/servicio_archivos.py`**:
  * Clase `ServicioArchivos`: gestiona la `ListaEnlazada` de archivos abiertos en memoria, realiza backups automáticos al disco y controla el archivo activo.
* **`src/servicios/servicio_sintaxis.py`**:
  * Clase `ServicioSintaxis`: utiliza una `Pila` propia para verificar el balanceo de delimitadores (`()`, `{}`, `[]`), reportando línea y carácter exacto ante discrepancias.
* **`src/servicios/servicio_historial.py`**:
  * Clase `ServicioHistorial`: administra dos instancias de `Pila` (pila Deshacer y pila Rehacer) por cada archivo o sesión para registrar snapshots de texto.
* **`src/servicios/servicio_diagnosticos.py`**:
  * Clase `ServicioDiagnosticos`: recopila alertas y aplica los algoritmos de ordenamiento (`MergeSort` o `ShellSort`) según criterio (`line` o `severity`).
* **`src/servicios/servicio_cola_ia.py`**:
  * Clase `ServicioColaIA`: administra la `ColaFIFO` de peticiones a la IA, garantizando despacho estrictamente secuencial y reporte de `queue-status`.
* **`src/servicios/servicio_cliente_ia.py`**:
  * Clase `ServicioClienteIA`: efectúa la petición HTTP al endpoint de IA configurado, extrayendo métricas de complejidad ($Big\ O$) y propuestas de refactorización.

---

## Fase 4: Implementación del Patrón Command
Desacopla la invocación de comandos de su ejecución real, encapsulando cada acción en un objeto independiente.

### 4.1. Base e Invocador
* **`src/comandos/comando_base.py`**:
  * Clase abstracta `ComandoBase`: define `ejecutar(self, argumentos: list[str]) -> bool`.
* **`src/comandos/invocador_comandos.py`**:
  * Clase `InvocadorComandos`: mantiene un registro `dict[str, ComandoBase]`, valida sintaxis de entrada y dispara la ejecución.

### 4.2. Comandos Concretos (Un fichero por cada comando del enunciado)
* **`src/comandos/comando_new.py`**: `new <nombre_archivo>`
* **`src/comandos/comando_list.py`**: `list`
* **`src/comandos/comando_switch.py`**: `switch <id/nombre>`
* **`src/comandos/comando_delete.py`**: `delete <id/nombre>`
* **`src/comandos/comando_config.py`**: `config <ruta_archivo>`
* **`src/comandos/comando_check.py`**: `check`
* **`src/comandos/comando_undo.py`**: `undo`
* **`src/comandos/comando_redo.py`**: `redo`
* **`src/comandos/comando_sort.py`**: `sort <criterio> <algoritmo>`
* **`src/comandos/comando_queue_status.py`**: `queue-status`
* **`src/comandos/comando_analyze.py`**: `analyze`
* **Comandos auxiliares indispensables:**
  * **`src/comandos/comando_edit.py`**: `edit <linea/texto>` (permite mutar el archivo activo para generar historial).
  * **`src/comandos/comando_show.py`**: `show` (imprime el contenido del archivo actual).
  * **`src/comandos/comando_help.py`**: `help` (muestra la lista de comandos disponibles).
  * **`src/comandos/comando_exit.py`**: `exit` (cierre ordenado de la sesión).

---

## Fase 5: Capa de Interfaz CLI (A lo General)
Interacción por terminal mediante prompt continuo (sin menús numéricos para evitar penalización).

* **`src/cli/analizador_comandos.py`**:
  * Clase `AnalizadorComandos`: tokeniza la cadena de entrada del usuario en `(nombre_comando, lista_argumentos)`.
* **`src/cli/consola_app.py`**:
  * Clase `ConsolaApp`: ciclo interactivo REPL (`while True`), muestra el prompt `Komorebi [archivo_activo]> `, captura comandos, invoca al despachador y maneja excepciones amigablemente.

---

## Fase 6: Punto de Entrada y Bootstrap Global
Unión de todas las capas en el arranque del sistema.

* **`config.json`**:
  * Archivo base con rutas relativas a `respaldos/`, `logs/`, timeout y endpoint de IA.
* **`main.py`**:
  * Inicializa el `ContextoApp`.
  * Carga `config.json` mediante `ServicioConfiguracion`.
  * Instancia los servicios de negocio.
  * Registra todos los comandos en el `InvocadorComandos`.
  * Inicia `ConsolaApp.ejecutar()`.

---

## Fase 7: Estrategia de Versionado Git y Defensa (Buenas Prácticas)
1. **Ramas por Integrante / Módulo:**
   * `feature/estructuras-datos`: Implementación de nodos, lista, pila, cola y árbol.
   * `feature/algoritmos-ordenamiento`: Implementación de Mergesort y Shellsort.
   * `feature/patron-comandos`: Implementación de comandos e invocador.
   * `feature/integracion-ia`: Buffer FIFO y cliente HTTP.
2. **Políticas de Commit:**
   * Mensajes descriptivos en presente imperativo (`feat: implementa pila propia para verificador sintactico`).
3. **Merge a Main:**
   * Integración continua y pruebas previas antes de fusionar en la rama principal.
4. **Documentación Técnica en `README.md`:**
   * Diagrama de clases de estructuras y patrón Command.
   * Tabla de análisis de complejidad temporal y espacial ($Big\ O$).
   * Instrucciones claras de ejecución.
