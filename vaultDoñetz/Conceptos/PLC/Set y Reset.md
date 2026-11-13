---
tipo: concepto
area: plc
tags: [plc, ladder, memoria]
---

# Set y Reset

- **SET** (`S`): cuando le llega un 1, **memoriza un 1** en la bobina, salida o memoria, aunque después la señal desaparezca.
- **RESET** (`R`): cuando le llega un 1, pone la bobina en **0**.
- En [[Zelio Soft 2]] la letra va **adelante** de la bobina (`S MA`, `R MA`). En otros PLC la S o la R va **dentro de los paréntesis**.
- Reemplaza el circuito de [[Autorretención]] (que igual también se puede programar).
- En la mayoría de los PLC el **reset tiene prioridad** sobre el set.

## Usos en el canal
- **Marcha y parada:** `I5 (PM) → S MA` y `I6 (PP, contacto NC en Ladder) → R MA`. Ver [[Lógica positiva y negativa]].
- **Válvulas monoestables:** `S Q1` mantiene el cabezal sin repetirlo en cada paso; `R Q1` lo suelta.
- **Cascada:** `S M1` para iniciar la línea 1 y `R M1` con un contacto de `M2` para cortarla. Ver [[Cascada en Ladder]].
- **Paso a paso:** cada paso hace `S` del siguiente y `R` del anterior. Ver [[Paso a paso en Ladder]].
