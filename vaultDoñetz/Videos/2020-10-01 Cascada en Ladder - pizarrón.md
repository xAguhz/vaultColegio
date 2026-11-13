---
tipo: video
fecha: 2020-10-01
url: https://www.youtube.com/watch?v=tLEJLLvQuWM
duracion: "22:41"
vistas: 14250
area: plc
---

# Ejercicio electroneumático con método de cascada en Ladder (pizarrón)

## Ejercicio
2 actuadores de doble efecto con **monoestables**, 4 rodillos (`1S1` I1, `1S2` I2, `2S1` I3, `2S2` I4), `PM` I5, `PP` I6, `H1` en Q3.
Movimientos: `1A−` · `1A+` · **T1** · `2A+` · `2A−`.

## Análisis
- **Flechita cerrada sobre sí misma** en el punto 2 (`1S1` hace volver al mismo actuador) y en el 5 (`2S2`).
- **Líneas:** cambio antes de la fase 2 (se repite `1A`) y antes de la fase 5 (se repite `2A`) → **3 líneas** → memorias `M1`, `M2`; línea 3 = `M1` negado AND `M2` negado.
- Bobinas: `1Y1` (retroceso, depende de la conexión) en la línea 1; las negaciones no requieren nada.

## Programa
- `I5` → `S MA`; `I6` (NC en Ladder) → `R MA`; `MA` → `Q3`.
- `MA` · `I3` → `S M1`; `M2` → `R M1`; `I1` → `S M2`; `I4` → `R M2`.
- `M1` → `Q1`; `M2` · `I2` → `TT1`; `M2` · `T1` → `Q2`.
- Línea 3: nada (las monoestables vuelven solas).

## Conceptos
[[Cascada en Ladder]] · [[Set y Reset]] · [[Temporizadores en PLC]] · [[Método cascada]]

Simulación: [[2020-10-01 Cascada en Ladder - simulación]]
