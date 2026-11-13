---
tipo: concepto
area: métodos
tags: [métodos, electroneumática]
---

# Método intuitivo

Es la forma básica de resolver (la de "electroneumática básica"): se **lee el diagrama** y se traduce cada flecha en una línea del circuito.

## Procedimiento (mando indirecto)
1. Analizar el [[Diagrama espacio-fase]]: emisores de señal en cada punto y qué cabezal se alimenta.
2. **Sensado** → **enclavamiento** (`K0`) → **mando** → **fuerza**.
3. **Mando:** por cada movimiento, los emisores (en serie si son AND) alimentan la bobina de un relé `Kn`.
4. **Fuerza:** un contacto NA de `Kn` alimenta al cabezal correspondiente.
5. Si la válvula es **monoestable**, hacer la [[Autorretención]] de `Kn` y buscar en el diagrama quién la desconecta (NC del emisor de la fase de retorno).
6. Para desconectar un cabezal: ver **quién lo alimenta** y cortar a ese.

## Límite
**No resuelve la [[Superposición de señales]]**: si un rodillo sigue pisado cuando otro pide el movimiento contrario, la máquina se traba o hasta arranca sola. En [[2025-05-04 Método de memorias - relé auxiliar]] se muestra cómo falla en el simulador.

## Videos
[[2020-04-26 Electroneumática 1 actuador monoestable]] · [[2020-04-20 Repaso EN 2 - Resolución del circuito eléctrico]] · [[2020-06-26 Clase en vivo - Mando directo electroneumático]]
