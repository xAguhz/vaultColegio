---
tipo: video
fecha: 2020-10-20
url: https://www.youtube.com/watch?v=q5DCUokGTFg
duracion: "22:31"
vistas: 12521
area: plc
---

# Ejercicio de método Paso a Paso con Ladder, parte 2 (simulación)

Carga en [[Zelio Soft 2]] 5.3 el programa de [[2020-10-19 Paso a Paso en Ladder - pizarrón]].

## Contenido
- Comentarios: `I1…I4` rodillos, `I5` PM, `I6` PP, `MA` y `M1…M5` (pasos), `Q1` 1Y1, `Q2` 2Y1, `Q4` H1, `T1`.
- `TT1` configurado en **4 s**, función A.
- Paso por paso, igual que en el pizarrón (ver la tabla en [[Paso a paso en Ladder]]).
- **Simulación:** forzar `I6`, `I2` e `I3` en 1. Al tocar PM, se activan `MA` y `H1`, el paso 1 dura un instante (pone `S Q1` y `S M2`), y después se recorre el ciclo accionando los rodillos a mano. Al final del ciclo, `R M1` rehabilita el paso 1.
- Comenta que es difícil de simular porque no hay actuadores en movimiento, y promete un simulador de PLC vinculado a actuadores (no se publicó).

## Conceptos
[[Paso a paso en Ladder]] · [[Zelio Soft 2]] · [[Temporizadores en PLC]]
