---
tipo: concepto
area: plc
tags: [plc, ladder, temporizador]
---

# Temporizadores en PLC (Zelio)

- Ya no es un relé físico: es un **bloque de programación** dentro del PLC (`T1`).
- **Comando (bobina):** `TT1`. Se coloca en la columna de bobinas.
- **Contacto:** `T1`. Se cierra cuando terminó de contar.
- **Configuración** (doble clic en la bobina): tiempo (por ejemplo `4.0` o `5` s), unidad y **tipo de función**.
- **Función A — "trabajo con comando mantenido"** = **retardo a la conexión**, la más común. Hay que **mantener la señal en el comando** durante todo el conteo; si se corta antes, no se activa.

## Uso típico (cascada)
`M2` (línea 2) y `I2` (rodillo `1S2`) → `TT1`; después `M2` y `T1` → `Q2` (`2Y1`).

## Relacionado
[[Relés temporizados]] · [[Temporizador neumático]] · [[Zelio Soft 2]]
