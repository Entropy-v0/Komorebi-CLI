"""Script de demostración comparativa: Altura de Árbol AVL vs. BST sin balanceo.

Ejecución directa:
    python3 -m scripts.demo_avl_vs_bst
"""

import math
from src.estructuras.arbol_avl import ArbolAVL
from src.estructuras.nodo_avl import NodoAVL


class DemostradorAVLvsBST:
    """Compara empíricamente la altura tras N inserciones ordenadas en un AVL frente a un BST."""

    @staticmethod
    def insertar_bst_iterativo(raiz: NodoAVL | None, palabra: str) -> tuple[NodoAVL, int]:
        """Inserta en un BST estándar (sin rotaciones) y retorna (raíz, altura_resultante)."""
        nuevo = NodoAVL(palabra, "")
        if raiz is None:
            return nuevo, 1

        actual = raiz
        profundidad = 1
        while True:
            profundidad += 1
            if palabra < actual.palabra:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    break
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = nuevo
                    break
                actual = actual.derecho
        return raiz, profundidad

    @classmethod
    def generar_tabla_comparativa(
        cls, tamanios: tuple[int, ...] = (10, 50, 100, 250, 500, 1000)
    ) -> str:
        """Ejecuta N inserciones estrictamente ascendentes y compara alturas BST vs AVL."""
        lineas = [
            "==========================================================================",
            "  COMPARACIÓN DE ALTURA TRAS N INSERCIONES ORDENADAS (BST vs. ÁRBOL AVL)  ",
            "==========================================================================",
            f"  {'N (nodos)':>10} | {'Altura BST Normal':>18} | {'Altura Árbol AVL':>17} | {'Cota 1.44*log2(N+2)':>19}",
            "--------------------------------------------------------------------------",
        ]

        for n in tamanios:
            avl = ArbolAVL()
            raiz_bst: NodoAVL | None = None
            altura_bst = 0

            for i in range(1, n + 1):
                clave = f"palabra_{i:05d}"
                avl.insertar(clave, f"Entrada ordenada #{i}")
                raiz_bst, prof = cls.insertar_bst_iterativo(raiz_bst, clave)
                if prof > altura_bst:
                    altura_bst = prof

            cota_avl = math.ceil(1.44 * math.log2(n + 2))
            lineas.append(
                f"  {n:>10} | {altura_bst:>18} | {avl.altura:>17} | {cota_avl:>19}"
            )

        lineas.append("==========================================================================")
        return "\n".join(lineas)


if __name__ == "__main__":
    print(DemostradorAVLvsBST.generar_tabla_comparativa())

