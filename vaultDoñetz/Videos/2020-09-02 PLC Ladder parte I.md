---
tipo: video
fecha: 2020-09-02
url: https://www.youtube.com/watch?v=Ta-l0gqVJ08
duracion: "32:27"
vistas: 314444
area: plc
---

# Programación de PLC en lenguaje Ladder o escalera (parte I)

⭐ **El video más visto del canal**, con ~314 000 vistas (56 % del total).

## Contenido
- **PLC** = controlador lógico programable. [[Lógica cableada y programada]].
- **Historia del Ladder** (más de 60 años): símbolos que salen de la máquina de escribir (`] [`, `]/[`, `( )`). Ver [[Lenguaje Ladder]].
- Comparación **circuito eléctrico ↔ Ladder**: rieles verticales, valor lógico alto (HI) a la izquierda, LOW a la derecha (casi siempre se omite). La forma de escalera.
- **Conexión física del PLC:** alimentación de 24 Vcc; entradas `I1…I6` (pulsadores `0S1` en I1 y `0S2` en I2); salidas a relé `Q1…Q4` con dos bornes y un puente a +24 V (`H1`, `H2`, bobina `K1`). La letra **Q** se usa porque la O se confunde con el 0. Dirección vs. símbolo. Ver [[PLC]].
- **Tres programas:**
  1. **Identidad:** `I1` → `Q1` (H1).
  2. **NOT:** contacto **NC** de `I2` → `Q2` (H2). El pulsador físico sigue siendo NA: cambia el contacto *lógico*.
  3. **AND:** `I1` en serie con `I2` → `Q3` (K1).
- La simulación queda para la parte II: [[2020-09-03 PLC Ladder parte II - Zelio Soft]].

## Conceptos
[[PLC]] · [[Lenguaje Ladder]] · [[Funciones lógicas]] · [[Lógica cableada y programada]]
