---
tipo: concepto
area: plc
tags: [plc, ladder, cascada, métodos]
---

# Cascada en Ladder

Es el mismo [[Método cascada]], con **memorias** en lugar de relés y con [[Set y Reset]].

## Ejemplo de los videos
2 actuadores de doble efecto, válvulas **monoestables**, 4 rodillos y un temporizador. Movimientos: `1A−`, `1A+`, *pausa T1*, `2A+`, `2A−` → **3 líneas** → memorias `M1`, `M2` (la línea 3 es `M1` negado AND `M2` negado).

## Programa
1. `I5 (PM) → S MA` · `I6 (PP) NC → R MA` · `MA → Q3 (H1)`.
2. **Mando:**
   - `MA` + `I3 (2S1)` → **S M1** · `M2` → **R M1** (al arrancar la línea 2 se corta la 1, en forma instantánea y prolija).
   - `I1 (1S1)` → **S M2** · `I4 (2S2)` → **R M2**.
3. **Fuerza:**
   - `M1` → `Q1 (1Y1)`: bobina en la 1.ª fase de la línea → directa. **Sin set**: ya está memorizado `M1`.
   - `M2` + `I2 (1S2)` → `TT1`.
   - `M2` + `T1` → `Q2 (2Y1)`.
   - Línea 3: **no se programa nada**. Con monoestables, al apagarse `M2` se corta `2Y1` y el resorte hace volver.

## Videos
[[2020-10-01 Cascada en Ladder - pizarrón]] · [[2020-10-01 Cascada en Ladder - simulación]]
