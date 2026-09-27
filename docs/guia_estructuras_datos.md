# Guía Conceptual y Técnica de Estructuras de Datos - Proyecto Komorebi

**Asignatura:** Algoritmos y Estructuras II  
**Objetivo:** Comprender en profundidad los fundamentos conceptuales, la representación en memoria, las operaciones clave y los casos de uso dentro del Mini IDE *Komorebi* para cada estructura implementada desde cero.

---

## 1. El Concepto Fundamental: ¿Qué es un Nodo y la Memoria Enlazada?

En un arreglo tradicional (`list` en Python o `vector` en C++), los elementos se almacenan en un bloque **contiguo** de memoria. Esto hace que acceder por índice sea instantáneo ($O(1)$), pero insertar o eliminar en el medio requiere desplazar todos los elementos posteriores ($O(n)$).

Una **estructura enlazada** renuncia a la memoria contigua. Cada elemento vive en una celda aislada llamada **Nodo**:
* **Dato / Carga útil (*payload*):** La información real que nos interesa (un archivo de código, un carácter delimitador, una petición de red, etc.).
* **Enlaces / Punteros (*pointers/references*):** Direcciones en memoria que apuntan a otros nodos (`siguiente`, `anterior`, `izquierda`, `derecha`).

---

## 2. Lista Doblemente Enlazada (`ListaEnlazada`)

### Concepto y Representación Mental
Una lista enlazada doble es una secuencia lineal de nodos donde cada nodo conoce a su predecesor y a su sucesor:

```
        ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
NULL ◄──┤ anterior     │◄────┤ anterior     │◄────┤ anterior     │
        │    DATO 1    │     │    DATO 2    │     │    DATO 3    │
        │ siguiente    ├────►│ siguiente    ├────►│ siguiente    ├──► NULL
        └──────────────┘     └──────────────┘     └──────────────┘
               ▲                                         ▲
          self._cabeza                              self._cola
```

### ¿Por qué doblemente enlazada y no simple?
1. **Navegación bidireccional:** Permite desplazarse hacia adelante y hacia atrás (por ejemplo, cambiar entre archivos de izquierda a derecha en un editor).
2. **Eliminación en $O(1)$ si ya tenemos el nodo:** En una lista simple, para eliminar un nodo necesitas recorrer desde el inicio para averiguar quién es su anterior. En una lista doble, el propio nodo ya conoce a su anterior (`nodo.anterior`), permitiendo desconectarlo de forma inmediata.

### Los 4 Casos Topológicos de Desvinculación (`_desvincular_nodo`)
Cuando eliminamos un nodo, alteramos los enlaces de sus vecinos según dónde esté ubicado:
1. `(None, None)`: **Nodo único.** La lista se queda vacía (`cabeza = None`, `cola = None`).
2. `(None, siguiente)`: **Cabeza.** El sucesor se convierte en la nueva cabeza (`cabeza = siguiente; siguiente.anterior = None`).
3. `(anterior, None)`: **Cola.** El predecesor se convierte en la nueva cola (`cola = anterior; anterior.siguiente = None`).
4. `(anterior, siguiente)`: **Intermedio.** Se puentean los vecinos (`anterior.siguiente = siguiente; siguiente.anterior = anterior`).

### Rol en Komorebi
Gestiona la lista de archivos abiertos en memoria (`NULL -> archivo1 -> archivo2 -> NULL`), permitiendo crear nuevos archivos (`new`), listarlos (`list`), cambiar de archivo activo (`switch`) y cerrarlos (`delete`).

---

## 3. Pila (`Pila` - LIFO)

### Concepto y Representación Mental
Una **Pila** (*Stack*) es una estructura de datos con disciplina **LIFO** (*Last In, First Out*: el último en entrar es el primero en salir).
* Analogía clásica: Una pila de platos o una caja estrecha. Solo puedes agregar un plato en la cima (*push*) o retirar el plato de la cima (*pop*).

```
         ┌───────────────┐
 Tope ──►│   Dato C      │  ◄── Entrada y Salida (apilar / desapilar)
         ├───────────────┤
         │   Dato B      │
         ├───────────────┤
         │   Dato A      │
         └───────────────┘
               Base
```

### Operaciones Principales
* **`apilar(elemento)` (*Push* - $O(1)$):** Se crea un nuevo nodo, se apunta su `siguiente` al tope actual y el tope pasa a ser el nuevo nodo.
* **`desapilar()` (*Pop* - $O(1)$):** Se extrae el dato del tope, el puntero del tope se mueve al siguiente nodo (`tope = tope.siguiente`) y se desconecta el nodo extraído.
* **`cima()` (*Peek* - $O(1)$):** Consulta el valor del tope sin extraerlo.

### Rol en Komorebi
Cumple dos funciones críticas:
1. **Verificación de Sintaxis (`check`):** Cada vez que se lee un delimitador de apertura (`(`, `{`, `[`), se **apila**. Cuando se encuentra uno de cierre (`)`, `}`, `]`), se **desapila** y se verifica que coincida en forma. Si al final la pila queda vacía, el código está perfectamente balanceado.
2. **Historial Deshacer/Rehacer (`undo` / `redo`):** Se mantienen dos pilas independientes. Cada modificación apila el estado en la pila `Undo`. Al presionar `undo`, el estado actual se mueve a la pila `Redo`.

---

## 4. Cola FIFO (`ColaFIFO` - FIFO)

### Concepto y Representación Mental
Una **Cola** (*Queue*) sigue la disciplina **FIFO** (*First In, First Out*: el primero en llegar es el primero en ser atendido).
* Analogía: La fila de un banco o taquilla. El que llega primero es atendido primero. Los nuevos se forman al final.

```
                  ┌─────────┐     ┌─────────┐     ┌─────────┐
Desencolar ◄──────┤ Frente  ├────►│  Nodo   ├────►│  Final  │ ◄────── Encolar
  (Salida)        └─────────┘     └─────────┘     └─────────┘        (Llegada)
                       ▲                               ▲
                  self._frente                    self._final
```

### ¿Por qué se necesitan dos punteros (`_frente` y `_final`)?
Si solo tuviéramos un puntero al frente, para encolar un elemento tendríamos que recorrer toda la fila hasta el final, lo que degradaría la inserción a $O(n)$. Al mantener una referencia directa a `_final`, la operación `encolar` ocurre en **tiempo constante estricto ($O(1)$)**.

### Operaciones Principales
* **`encolar(elemento)` (*Enqueue* - $O(1)$):** Inserta al final de la cola y actualiza `_final`.
* **`desencolar()` (*Dequeue* - $O(1)$):** Extrae y retorna el elemento del `_frente`, moviendo el puntero al siguiente.
* **`frente()` (*Peek/Front* - $O(1)$):** Observa el elemento próximo a salir sin retirarlo.

### Rol en Komorebi
Actúa como el **Buffer de Peticiones hacia la API de IA**. Si el usuario invoca análisis repetitivos rápidamente, no saturamos el servidor HTTP con solicitudes simultáneas: las peticiones se encolan en orden cronológico y se despachan una a una.

---

## 5. Árbol Binario de Búsqueda (`ArbolBinario` / BST)

### Concepto y Representación Mental
Un **Árbol Binario** es una estructura no lineal y jerárquica. Un **Árbol Binario de Búsqueda** (*BST - Binary Search Tree*) impone la siguiente **invariante fundamental**:
> Para cualquier nodo con valor $V$:
> * Todo valor en su **subárbol izquierdo** es estrictamente **menor** que $V$ ($hijo.izq < V$).
> * Todo valor en su **subárbol derecho** es estrictamente **mayor** que $V$ ($hijo.der > V$).

```
                      [ 50 ]  (Raíz)
                     /      \
               [ 30 ]        [ 70 ]
              /      \      /      \
          [ 20 ]   [ 40 ] [ 60 ]  [ 80 ]
```

### Complejidad y Rendimiento
* **Búsqueda / Inserción / Eliminación promedio:** $O(\log n)$. Al comparar contra el nodo actual, descartamos la mitad del árbol en cada paso (similar a la búsqueda binaria).
* **Peor caso (árbol degenerado en lista):** $O(n)$ si los elementos se insertan ya ordenados.

### La Operación Más Compleja: Eliminación (`eliminar`)
Se divide en tres escenarios bien definidos:
1. **Caso 1: Nodo Hoja (sin hijos):** Se desconecta simplemente retornando `None` al padre.
2. **Caso 2: Nodo con 1 solo hijo:** El padre conecta directamente con el único hijo del nodo a eliminar (el hijo sube y toma su lugar).
3. **Caso 3: Nodo con 2 hijos:** No se puede borrar el nodo directamente sin romper la estructura.
   * **Solución matemática:** Se busca el **sucesor inorden** (el valor más pequeño del subárbol derecho, que se encuentra yendo todo a la izquierda a partir del hijo derecho).
   * Se copia el valor del sucesor al nodo actual.
   * Se llama recursivamente a eliminar el sucesor del subárbol derecho (el cual forzosamente tendrá 0 o 1 hijo, reduciendo la eliminación al Caso 1 o 2).

### Los Tres Recorridos Clásicos
1. **Inorden (Izquierda, Raíz, Derecha):** Visita los elementos en orden ascendente estricto. Ideal para reportes o volcados ordenados.
2. **Preorden (Raíz, Izquierda, Derecha):** Útil para clonar o serializar el árbol en disco.
3. **Postorden (Izquierda, Derecha, Raíz):** Útil para liberar memoria o evaluar expresiones matemáticas (bottom-up).

---

## 6. Cuadro Resumen de Complejidad Comparativa

| Estructura | Inserción | Eliminación | Búsqueda | Acceso por Posición | Caso de Uso Principal en Komorebi |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Lista Enlazada Doble** | $O(1)$ (inicio/final) | $O(1)$ (con nodo) / $O(n)$ | $O(n)$ | $O(n)$ | Archivos abiertos en sesión (`new`, `list`, `switch`, `delete`) |
| **Pila (LIFO)** | $O(1)$ (apilar) | $O(1)$ (desapilar) | $O(n)$ | No permitido | Verificador sintáctico (`check`) y Snapshot Undo/Redo |
| **Cola (FIFO)** | $O(1)$ (encolar) | $O(1)$ (desencolar) | $O(n)$ | No permitido | Buffer de peticiones a la API de IA (`queue-status`, `analyze`) |
| **Árbol Binario (BST)** | $O(\log n)$ prom. | $O(\log n)$ prom. | $O(\log n)$ prom. | N/A | Indexación jerárquica de símbolos y consultas de código |
