---
tipo: video
fecha: 2020-10-01
url: https://www.youtube.com/watch?v=sojdPxmRAAU
duracion: "18:17"
vistas: 9415
area: plc
---

# Ejercicio electroneumático en Ladder, parte 2 (simulación)

Pasa a [[Zelio Soft 2]] **5.3** el programa de [[2020-10-01 Cascada en Ladder - pizarrón]].

## Contenido
- Cargar los comentarios: entradas, memorias (`MA` marcha, `M1` línea 1, `M2` línea 2), salidas y `T1`.
- `S MA` y `R MA`: por qué el contacto de parada tiene que ser **NC en Ladder** (si no, el reset queda siempre activo).
- Configurar `TT1`: **5 s, función A** (trabajo con comando mantenido = retardo a la conexión). Ver [[Temporizadores en PLC]].
- Simulación: forzar `I2` (1S2), `I3` (2S1) e `I6` antes de RUN; recorrer el ciclo a mano y ver cómo se prenden y apagan `M1`, `M2`, `Q1` y `Q2`.

## Conceptos
[[Cascada en Ladder]] · [[Zelio Soft 2]] · [[Set y Reset]]
