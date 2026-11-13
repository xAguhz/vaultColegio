---
tipo: concepto
area: métodos
tags: [métodos, electroneumática, válvulas]
---

# Técnica Chopp ("chopeado")

## Problema
Se rompe una electroválvula **monoestable** y hay que reemplazarla por una **biestable**, sin rehacer todo el análisis ni el circuito.

## Solución
1. Se agrega en el plano el **cabezal nuevo** (`1Y2`), en la parte de **fuerza**.
2. Ese cabezal se alimenta con un **contacto NC del mismo relé** que alimentaba al cabezal original (`1Y1`). Por ejemplo, con 31-32 de `K1`.

Eso es todo: una sola línea nueva.

## Por qué funciona
- Mientras `K1` está energizado: NA cerrado → `1Y1` (avance); NC abierto → `1Y2` sin energía.
- Cuando `K1` se desconecta: NA abierto, NC cerrado → `1Y2` (retroceso).
- Como dependen del **mismo relé** con contactos opuestos, **nunca** se alimentan los dos al mismo tiempo → no hay [[Superposición de señales]] en esa válvula.
- En reposo `1Y2` está energizado, lo que asegura que el vástago arranque retraído.

## Videos
[[2020-04-26 Circuito Chopp]] · [[2020-06-18 Técnica Chopp en FluidSIM]]
