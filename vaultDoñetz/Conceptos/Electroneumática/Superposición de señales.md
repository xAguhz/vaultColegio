---
tipo: concepto
area: electroneumática
tags: [electroneumática, problema, métodos]
---

# Superposición de señales

## Qué es
Se alimentan **al mismo tiempo los dos cabezales** de una electroválvula biestable (o los dos pilotajes de una válvula neumática), es decir, la orden de avance y la de retroceso a la vez.
La válvula **respeta la primera señal que llegó** y queda **trabada**: la máquina se detiene a mitad de ciclo.

## Por qué aparece
Un rodillo queda **pisado durante varias fases** (porque el actuador se queda quieto en esa posición) y sigue mandando señal cuando otro emisor quiere el movimiento contrario.

## Cómo detectarla en el diagrama (antes de armar nada)
1. Marcar en el [[Diagrama espacio-fase]] **desde qué punto hasta qué punto** está pisado cada rodillo (si el actuador queda horizontal arriba o abajo, sigue pisado).
2. Ver a quién alimenta ese rodillo (directa o indirectamente).
3. Si en ese intervalo otro emisor alimenta el cabezal **opuesto** de la misma válvula, hay superposición.

Ejemplo clásico (`1A+ 2A+ 2A− 1A−`): `1S2` queda pisado del punto 2 al 4 alimentando `2Y1`, y en el punto 3 `2S2` quiere `2Y2`. Además `2S1` queda pisado del 4 al 2 del ciclo siguiente.

## Cómo se evita
- **No** con el [[Método intuitivo]].
- Sí con: [[Método cascada]], [[Método paso a paso]] o [[Método de memorias]].
- La [[Técnica Chopp]] y las monoestables con un solo relé nunca alimentan los dos cabezales, porque usan NA y NC del mismo relé.

## Videos
[[2021-05-21 Cascada con lógica cableada y superposición]] · [[2025-05-04 Método de memorias - relé auxiliar]]
