# Guía Maestra de Defensa Académica — Fase 2: Estructuras Arbóreas

Esta guía prepara la defensa técnica de las **cuatro estructuras de datos no lineales (árboles)** implementadas desde cero en **Komorebi Mini IDE**:
1. **Árbol N-ario (`ArbolNario` y `NodoNario`)** — Sistema de archivos virtual del Workspace.
2. **Árbol Binario de Expresiones (`ArbolExpresion` y `NodoExpresion`)** — Evaluador aritmético exacto y generador de notaciones.
3. **Árbol Binario de Búsqueda Autobalanceado AVL (`ArbolAVL` y `NodoAVL`)** — Diccionario técnico y autocompletado por prefijo con poda.
4. **Árbol B Multicamino de Orden $m = 4$ (`ArbolB` y `NodoB`)** — Motor de indexación global de tokens en el proyecto.

---

## 1. Árbol N-ario (`ArbolNario`) — Jerarquía del Workspace

### 1.1 Explicación en Lenguaje Sencillo
Un árbol binario solo permite hasta 2 hijos por nodo, lo cual no sirve para modelar carpetas de un sistema operativo donde una carpeta puede contener $0, 1, 5$ o $100$ archivos y subcarpetas.
El **Árbol N-ario** resuelve esto haciendo que cada nodo de tipo `CARPETA` almacene sus hijos dentro de nuestra propia `ListaEnlazada` doblemente enlazada, mientras que cada nodo mantenga además un puntero `_padre` hacia su carpeta contenedora.
- El puntero `_padre` permite resolver `..` (subir un nivel) y reconstruir `pwd` en tiempo proporcional a la profundidad $d$.
- Los nodos de tipo `ARCHIVO` guardan una **referencia directa a la misma instancia de `ArchivoCodigo`** que está en `ContextoApp.archivos_abiertos`, evitando duplicar memoria o desincronizar ediciones.

### 1.2 Ejemplo Paso a Paso con Dibujos ASCII

Supongamos que ejecutamos en el REPL:
```text
mkdir src
cd src
new app.py
mkdir utils
cd /
tree
```

**Estado de punteros en el `ArbolNario`:**
```text
                  [NodoNario: "/" (CARPETA, padre=None)]
                                   │
                           _hijos (ListaEnlazada)
                                   ▼
                [NodoNario: "src" (CARPETA, padre="/")]
                                   │
                           _hijos (ListaEnlazada)
                          ┌────────┴────────┐
                          ▼                 ▼
     [NodoNario: "app.py" (ARCHIVO)]   [NodoNario: "utils" (CARPETA)]
             │ (misma ref en memoria)
             ▼
   ArchivoCodigo(id="file-8a91b2c3", nombre="app.py")
```

**Recorrido Preorden Iterativo con `Pila` para `tree`:**
Para evitar agotar la pila de llamadas de Python en jerarquías profundas, `generar_lineas_tree()` utiliza una instancia explícita de nuestra clase `Pila`:
1. Apila los hijos de la raíz en **orden inverso** para que el primer hijo quede en el tope de la `Pila` (LIFO).
2. Al desapilar cada nodo, imprime su conector (`├── ` o `└── `) y, si es carpeta, apila sus hijos en orden inverso.

```text
/
└── src/
    ├── app.py
    └── utils/
```

### 1.3 Complejidad Temporal y Espacial Justificada
- **Búsqueda / Resolución de ruta (`cd`, `ls`, `mkdir`):** $\mathcal{O}(d \cdot b)$, donde $d$ es la cantidad de segmentos de la ruta (`/a/b/c` $\rightarrow d=3$) y $b$ el número promedio de hijos por carpeta recorrida en la `ListaEnlazada`.
- **Movimiento (`mv`):** $\mathcal{O}(d \cdot b)$ para resolver origen y destino + $\mathcal{O}(d)$ para subir por los punteros `_padre` del destino y verificar que el origen no sea ancestro del destino (prevención de ciclos) + $\mathcal{O}(1)$ para reenganchar punteros.
- **Recorrido `tree`:** $\mathcal{O}(n)$ en tiempo y $\mathcal{O}(n)$ en espacio para visitar los $n$ nodos exactamente una vez.

---

## 2. Árbol Binario de Expresiones (`ArbolExpresion`) — Evaluador Aritmético

### 2.1 Explicación en Lenguaje Sencillo
En un **Árbol Binario de Expresiones**:
- Todas las **hojas** son **operandos numéricos** (ej. `4`, `8`, `3`, `-2`).
- Todos los **nodos internos** son **operadores binarios** (`+`, `-`, `*`, `/`, `^`).
- Cuanto más profundo está un operador en el árbol, **antes se ejecuta**. De este modo, el propio árbol codifica la jerarquía de operaciones y los paréntesis sin necesidad de volver a analizarlos al evaluar.

### 2.2 Ejemplo Paso a Paso con Dibujos ASCII (Shunting-Yard y Evaluación)

Construyamos y evaluemos la expresión:
$$\text{Expresión: } (4 + 8) * 3 - 2 \wedge 3$$

**Paso 1: Tokenización Léxica Propia**
El escáner recorre la cadena carácter por carácter produciendo:
`["(", "4", "+", "8", ")", "*", "3", "-", "2", "^", "3"]`.

**Paso 2: Construcción con Dos Instancias de `Pila` (Shunting-Yard Modificado)**
Usamos `pila_operadores` y `pila_nodos`:
1. Se apila `"("` en `pila_operadores`.
2. Se crean nodos hoja `[4]` y `[8]` en `pila_nodos`, y `"+"` en `pila_operadores`.
3. Al llegar `")"`, se desapila `"+"` y se enlaza con `derecho = [8]` e `izquierdo = [4]`:
   ```text
         (+)
        /   \
      (4)   (8)
   ```
4. Llega `"*"` (precedencia 2) y luego `[3]`.
5. Llega `"-"` (precedencia 1 $\le$ precedencia de `"*"`): esto obliga a reducir `"*"` antes de apilar `"-"`:
   ```text
           (*)
          /   \
        (+)   (3)
       /   \
     (4)   (8)
   ```
6. Llegan `[2]`, `"^"` (precedencia 3, asociativo por la derecha) y `[3]`.
7. Al finalizar la entrada, se vacían los operadores restantes (`"^"` primero y `"-"` al final):

```text
               (-)          <-- Raíz (última operación en ejecutarse)
              /   \
            (*)    (^)
           /   \  /   \
         (+)  (3)(2)  (3)
        /   \
      (4)   (8)
```

**Paso 3: Evaluación Postorden (`Izquierda -> Derecha -> Raíz`) con `Fraction`**
1. Subárbol `(+)` $\rightarrow 4 + 8 = 12$.
2. Subárbol `(*)` $\rightarrow 12 \times 3 = 36$.
3. Subárbol `(^)` $\rightarrow 2^3 = 8$.
4. Raíz `(-)` $\rightarrow 36 - 8 = \mathbf{28}$.

**Recorridos Generados:**
- **Inorden (paréntesis mínimos):** `(4 + 8) * 3 - 2 ^ 3`
- **Preorden (Notación Polaca):** `- * + 4 8 3 ^ 2 3`
- **Postorden (RPN):** `4 8 + 3 * 2 3 ^ -`

### 2.3 Complejidad Temporal y Espacial Justificada
- **Construcción (Shunting-Yard):** $\mathcal{O}(n)$ temporal y espacial, porque cada uno de los $n$ tokens se apila y desapila como máximo una vez en `pila_operadores` y `pila_nodos`.
- **Evaluación y Recorridos (`preorden`, `inorden`, `postorden`):** $\mathcal{O}(n)$ temporal (visita cada nodo exactamente una vez) y $\mathcal{O}(h)$ en la pila de recursión.

---

## 3. Árbol AVL (`ArbolAVL`) — Diccionario y Autocompletado con Poda

### 3.1 Explicación en Lenguaje Sencillo
Un Árbol Binario de Búsqueda (BST) normal tiene un defecto crítico: si insertamos palabras en orden alfabético (`"and"`, `"as"`, `"assert"`, `"async"`, ...), degenera en una lista enlazada de altura $n$ y la búsqueda cae a $\mathcal{O}(n)$.
El **Árbol AVL** guarda la `altura` en cada nodo y exige que en **todo nodo** se cumpla:
$$\text{FB}(\text{nodo}) = \text{altura}(\text{derecho}) - \text{altura}(\text{izquierdo}) \in \{-1, 0, +1\}$$
Si tras insertar o eliminar un nodo algún ancestro llega a $\text{FB} = -2$ o $\text{FB} = +2$, el árbol aplica una **rotación local de punteros en $\mathcal{O}(1)$** que restaura el balance inmediatamente.

### 3.2 Ejemplo Paso a Paso con Dibujos ASCII: Las 4 Rotaciones AVL

#### Caso 1: Rotación Simple Derecha — Caso LL (`_rotar_ll`)
Ocurre cuando insertamos `"c"`, `"b"`, `"a"`. El nodo `z="c"` tiene $\text{FB}(c) = 0 - 2 = -2$ y su hijo izquierdo `y="b"` tiene $\text{FB}(b) = 0 - 1 = -1 \le 0$:

```text
    Antes (_rotar_ll en 'c')             Después (Altura reducida a 2)
          [c] (h=3, FB=-2)                        [b] (h=2, FB=0)
          /                                       /   \
        [b] (h=2, FB=-1)      =====>            [a]   [c] (h=1, FB=0)
        /                                      (h=1)
      [a] (h=1, FB=0)
```
*Reasignación:* `b.derecho = c`, `c.izquierdo = T3 (None)`. Se actualiza primero la altura de `c` (ahora abajo) y luego la de `b` (nueva raíz).

#### Caso 2: Rotación Simple Izquierda — Caso RR (`_rotar_rr`)
Ocurre cuando insertamos `"a"`, `"b"`, `"c"`. El nodo `z="a"` tiene $\text{FB}(a) = +2$ y su hijo derecho `y="b"` tiene $\text{FB}(b) = +1 \ge 0$:

```text
    Antes (_rotar_rr en 'a')             Después (Altura reducida a 2)
    [a] (h=3, FB=+2)                              [b] (h=2, FB=0)
      \                                           /   \
      [b] (h=2, FB=+1)        =====>            [a]   [c] (h=1, FB=0)
        \                                      (h=1)
        [c] (h=1, FB=0)
```

#### Caso 3: Rotación Doble Izquierda-Derecha — Caso LR (`_rotar_lr`)
Ocurre al insertar `"c"`, `"a"`, `"b"`. El nodo `z="c"` tiene $\text{FB}(c) = -2$ (izquierda pesada), pero su hijo izquierdo `y="a"` tiene $\text{FB}(a) = +1$ (derecha pesada en zigzag):

```text
      [c] (FB=-2)          Paso 1: _rotar_rr(a)         [c] (FB=-2)        Paso 2: _rotar_ll(c)        [b] (FB=0)
      /                                                 /                                             /   \
    [a] (FB=+1)            ===================>       [b] (FB=-1)          ===================>     [a]   [c]
      \                                               /
      [b]                                           [a]
```

#### Caso 4: Rotación Doble Derecha-Izquierda — Caso RL (`_rotar_rl`)
Ocurre al insertar `"a"`, `"c"`, `"b"`. El nodo `z="a"` tiene $\text{FB}(a) = +2$ y su hijo derecho `y="c"` tiene $\text{FB}(c) = -1$:

```text
    [a] (FB=+2)            Paso 1: _rotar_ll(c)       [a] (FB=+2)          Paso 2: _rotar_rr(a)        [b] (FB=0)
      \                                                 \                                             /   \
      [c] (FB=-1)          ===================>         [b] (FB=+1)        ===================>     [a]   [c]
      /                                                   \
    [b]                                                   [c]
```

### 3.3 Búsqueda de Prefijos con Poda (`sugerir(prefijo)`)
Cuando ejecutamos `suggest as`:
- Si `nodo.palabra < "as"` (ej. `"and"`), sabemos por la propiedad BST que **todo el subárbol izquierdo de `"and"` es menor que `"and"`**, por lo que **jamás** podrá empezar con `"as"`. **Podamos toda la rama izquierda** y solo bajamos a la derecha.
- Si `nodo.palabra > "as"` y no empieza con `"as"` (ej. `"break"`), **podamos toda la rama derecha** y solo bajamos a la izquierda.
- Si `nodo.palabra.startswith("as")` (ej. `"assert"`), exploramos `izquierdo`, agregamos `"assert"` y exploramos `derecho`, obteniendo `["as", "assert", "async"]` en orden alfabético estricto con costo $\mathcal{O}(\log n + k)$.

### 3.4 Complejidad Temporal y Espacial Justificada
- **Búsqueda, Inserción y Eliminación:** $\mathcal{O}(\log n)$ garantizado en el peor caso, porque la altura de un AVL con $n$ nodos nunca supera $1.44 \log_2(n + 2)$, y cada rotación toma $\mathcal{O}(1)$.
- **Autocompletado `sugerir(prefijo)`:** $\mathcal{O}(\log n + k)$, donde $\log n$ acota los dos caminos de frontera del rango lexicográfico y $k$ es el número de palabras devueltas.

---

## 4. Árbol B de Orden $m = 4$ (`ArbolB`) — Índice Global de Tokens

### 4.1 Explicación en Lenguaje Sencillo
Un **Árbol B de orden $m = 4$** (también conocido como árbol 2-3-4 en la convención de Knuth) agrupa **múltiples claves ordenadas dentro de un mismo nodo (página)**:
- **Máximo por nodo:** $m - 1 = 3$ claves y $m = 4$ hijos.
- **Mínimo en nodos no raíz:** $\lceil m/2 \rceil - 1 = 1$ clave y $\lceil m/2 \rceil = 2$ hijos.
- **Todas las hojas están siempre al mismo nivel.**
- Cada clave es un identificador del código (ej. `"monto_final"`) y su valor asociado es una lista ordenada de `ReferenciaToken(id_archivo, linea)`.

### 4.2 Ejemplo Paso a Paso con Dibujos ASCII: Split (Inserción) y Préstamo/Fusión (Eliminación)

#### A. División por Desbordamiento (*Split Bottom-Up*) en Orden $m = 4$
Insertamos los tokens `"a"`, `"b"`, `"c"` en un nodo hoja inicialmente vacío:
```text
   [ "a" | "b" | "c" ]   (3 claves = máximo permitido m - 1)
```
Ahora insertamos `"d"`. La hoja alcanza temporalmente $m = 4$ claves (`["a", "b", "c", "d"]`), superando el máximo de $3$:
1. Se calcula el índice de la mediana: `mediana = (4 - 1) // 2 = 1` $\rightarrow$ clave `"b"`.
2. `"b"` **sube al padre**; `"a"` queda en el hijo izquierdo y `["c", "d"]` pasan al nuevo hermano derecho:

```text
            [ "b" ]                 <-- Nueva raíz (el árbol crece hacia arriba)
           /       \
       [ "a" ]   [ "c" | "d" ]      <-- Ambas hojas quedan exactamente en el nivel 1
```

#### B. Eliminación con Préstamo desde Hermano (`_prestar_de_derecho`)
Si eliminamos `"a"` del árbol anterior, el hijo izquierdo queda temporalmente con $0$ claves ($< \text{min\_claves}=1$). Como su hermano derecho `["c", "d"]` tiene $2 > 1$ claves, le **presta una clave rotando a través del separador del padre**:
1. El separador `"b"` baja desde el padre al hijo izquierdo.
2. La primera clave del hermano derecho (`"c"`) sube al padre como nuevo separador:

```text
            [ "c" ]                 <-- 'c' subió desde el hermano derecho
           /       \
       [ "b" ]   [ "d" ]            <-- 'b' bajó al hijo izquierdo; equilibrio restaurado
```

#### C. Eliminación con Fusión de Hermanos (`_fusionar_hijos`) y Decrecimiento de Raíz
Si ahora eliminamos `"b"` del árbol anterior:
- El hijo izquierdo queda con $0$ claves, y su hermano derecho `["d"]` tiene solo $1$ clave ($\text{min\_claves}=1$), por lo que no puede prestar.
- **Fusión:** El separador `"c"` del padre baja y se une con el hermano derecho en un solo nodo `["c", "d"]`.
- Como la raíz se quedó con $0$ claves, el nodo fusionado `["c", "d"]` se convierte en la nueva raíz, disminuyendo la altura del árbol en $1$:

```text
         [ "c" | "d" ]              <-- Nueva raíz única de altura 1
```

### 4.3 Complejidad Temporal y Espacial Justificada
- **Búsqueda (`buscar`):** $\mathcal{O}(\log_m n) = \mathcal{O}(\log n)$ porque en cada nivel se inspeccionan como máximo $m - 1 = 3$ claves y se desciende un nivel entre $\le \log_{\lceil m/2 \rceil} n$ niveles.
- **Inserción y Eliminación:** $\mathcal{O}(m \log_m n) = \mathcal{O}(\log n)$, ya que a lo sumo se realiza un *split*, préstamo o fusión por cada nivel de la altura del árbol.
- **Espacio:** $\mathcal{O}(n + R)$, donde $n$ es la cantidad de tokens únicos y $R$ el número total de ocurrencias (`ReferenciaToken`) en el Workspace.

---

## 5. Las 10 Preguntas Difíciles de Defensa (Con Respuestas de Nivel Senior)

### Pregunta 1: ¿Por qué `ReferenciaToken` guarda `id_archivo` (`file-xxxxxxxx`) en lugar de guardar directamente la ruta `/src/app.py`?
**Respuesta:** Si guardáramos la ruta textual `/src/app.py` dentro de miles de nodos del Árbol B, cada vez que el usuario ejecutara `mv /src /core` tendríamos que recorrer y reconstruir todo el Árbol B en $\mathcal{O}(n + R)$ para actualizar las rutas. Al almacenar el `id_archivo` inmutable de `ArchivoCodigo`, el comando `mv` solo mueve un puntero en el `ArbolNario` en $\mathcal{O}(1)$ y el Árbol B permanece 100% válido sin tocar una sola clave; cuando el usuario ejecuta `find-global`, resolvemos el `id_archivo` contra el `ArbolNario` para mostrar su ubicación actual.

### Pregunta 2: ¿Por qué `ArbolAVL` no hereda de `ArbolExpresion` si ambos son árboles binarios?
**Respuesta:** Por el **Principio de Sustitución de Liskov (LSP)**. `ArbolExpresion` modela un árbol sintáctico donde la posición de cada nodo depende de la precedencia de operadores (`+`, `*`, `^`) y no de un orden lexicográfico de claves. En cambio, `ArbolAVL` es un Árbol Binario de Búsqueda (BST) con invariante de orden total (`izq < raíz < der`) e invariante de balance (`|FB| <= 1`). Heredar uno del otro acoplaría contratos incompatibles.

### Pregunta 3: En las rotaciones del AVL (`_rotar_ll` y `_rotar_rr`), ¿qué ocurre si actualizamos primero la altura de la nueva raíz `y` y después la del nodo descendido `z`?
**Respuesta:** La altura de `y` quedaría **incorrecta**. Tras la rotación, `z` pasa a ser hijo directo de `y`, por lo que `altura(y) = 1 + max(altura(y.izq), altura(z))`. Si calculamos primero `altura(y)`, estaríamos usando la altura vieja de `z` (antes de bajar), corrompiendo los factores de balance de todos los ancestros superiores y rompiendo el árbol AVL.

### Pregunta 4: ¿Por qué una inserción en un Árbol AVL requiere a lo sumo 1 rotación (simple o doble), mientras que una eliminación puede requerir $\mathcal{O}(\log n)$ rotaciones?
**Respuesta:** Al insertar un nodo, la altura del subárbol desbalanceado crece en $+1$, y al aplicar una rotación (`LL`, `RR`, `LR` o `RL`) ese subárbol recupera exactamente la misma altura que tenía **antes** de la inserción, por lo que ningún ancestro superior ve alterado su factor de balance. En cambio, al eliminar un nodo y rotar, la altura del subárbol resultante puede disminuir en $-1$, propagando el desbalance hacia el padre, el abuelo y potencialmente hasta la raíz.

### Pregunta 5: ¿Cómo garantiza `sugerir(prefijo)` en el Árbol AVL una complejidad $\mathcal{O}(\log n + k)$ en vez de $\mathcal{O}(n)$?
**Respuesta:** Mediante **poda guiada por las cotas lexicográficas del BST**. Cuando visitamos un nodo cuya clave es menor que `prefijo`, sabemos que todas las claves de su subárbol izquierdo son aún menores y jamás empezarán con `prefijo`, por lo que descartamos ese subárbol completo sin visitarlo. Análogamente, si la clave es mayor que `prefijo` y no comienza con `prefijo`, descartamos todo su subárbol derecho. Solo visitamos los nodos en los dos caminos de borde ($\le 2 \cdot \text{altura} = \mathcal{O}(\log n)$) más los $k$ nodos que sí coinciden.

### Pregunta 6: En el algoritmo Shunting-Yard de `ArbolExpresion`, ¿cómo se diferencia la asociatividad de `-` (izquierda) frente a la de `^` (derecha) en `2 ^ 3 ^ 2`?
**Respuesta:** Al comparar el operador entrante `op_actual` con el operador en la cima de `pila_operadores`:
- Si `op_actual` es asociativo por la **izquierda** (`+`, `-`, `*`, `/`), desapilamos mientras `precedencia(cima) >= precedencia(op_actual)`. Así `10 - 3 - 2` agrupa `(10 - 3) - 2 = 5`.
- Si `op_actual` es asociativo por la **derecha** (`^`), desapilamos solo mientras `precedencia(cima) > precedencia(op_actual)` (desigualdad estricta). Así en `2 ^ 3 ^ 2`, el segundo `^` no desapila al primero, agrupando `2 ^ (3 ^ 2) = 2 ^ 9 = 512`.

### Pregunta 7: ¿Cómo distingue el tokenizador de `ArbolExpresion` entre un signo menos binario (`5 - 3`) y un signo menos unario (`-3 + 5` o `4 * -2`)?
**Respuesta:** Llevando el contexto del token inmediatamente anterior (`esperando_operando`). Si aparece `-` al inicio de la expresión, después de un paréntesis de apertura `(` o después de otro operador (`+`, `-`, `*`, `/`, `^`), es un **operador unario**: si precede a un literal numérico se absorbe en el número (`-2`), y si precede a un paréntesis `-(a + b)` se transforma algebraicamente en `0 - (a + b)` con precedencia de signo para respetar `-2 ^ 2 = -(2 ^ 2) = -4`.

### Pregunta 8: ¿Por qué todas las hojas de un Árbol B están siempre al mismo nivel, a diferencia de un BST o un AVL?
**Respuesta:** Porque los árboles BST y AVL crecen **hacia abajo** (creando nuevas hojas en el fondo), mientras que el Árbol B crece y decrece **por la raíz (hacia arriba)**. En un Árbol B, las inserciones siempre ocurren en hojas existentes; cuando una hoja se llena ($m$ claves), se divide en dos hojas a la **misma profundidad** y promueve su mediana al padre. La altura del árbol solo aumenta cuando la **raíz misma se divide**, agregando un nivel por encima de todos los subárboles simultáneamente.

### Pregunta 9: ¿Qué pasaría en `ServicioWorkspace.mover(origen, destino)` si el usuario intenta ejecutar `mv /src /src/utils/sub`?
**Respuesta:** Antes de desvincular `/src`, `ArbolNario.mover()` invoca `nodo_origen.es_ancestro_de(padre_destino)`, que sube por la cadena de punteros `_padre` desde `/src/utils` hasta la raíz `/`. Al detectar que `/src` aparece en el camino de ancestros del destino, lanza inmediatamente `MovimientoInvalidoError`, evitando desconectar el subárbol de la raíz y formar un ciclo infinito en memoria.

### Pregunta 10:Durante `index-all`, ¿por qué `ServicioIndexacion` consulta el `ArbolAVL` para filtrar palabras reservadas en lugar de usar una lista lineal?
**Respuesta:** Al escanear $T$ identificadores a lo largo de todos los archivos del Workspace, verificar si cada identificador es una palabra reservada en una lista lineal de $K$ keywords costaría $\mathcal{O}(T \cdot K)$. Al consultar el `ArbolAVL` de `ServicioDiccionario`, cada verificación cuesta $\mathcal{O}(\log K)$ en el peor caso (con $K=35$, a lo sumo 6 comparaciones), y además cualquier palabra clave agregada dinámicamente por el usuario con `add-keyword` queda automáticamente excluida de la indexación de variables en el Árbol B.

