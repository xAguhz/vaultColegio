---
tipo: concepto
area: electroneumática
tags: [electroneumática, marcha-parada]
---

# Enclavamiento eléctrico (circuito de marcha y parada)

Es el circuito que **memoriza que la máquina está en marcha**. El relé `K0` cumple esa función.

## Armado típico (tres pulsadores)
- NA del **pulsador de marcha `0S1`** en serie con NC del **interruptor de parada de mantenimiento `0S3`** → bobina de **`K0`**.
- [[Autorretención]]: NA de `K0` (11-14) en serie con NC del **pulsador de parada `0S2`**, en paralelo con `0S1`.
- `0S3` (parada de servicio o mantenimiento): si está accionado, aunque se toque marcha **no arranca**. Sirve para trabajar seguro sobre la máquina.

## Uso
Un contacto NA de `K0` va en la primera línea de mando, en **AND** con la señal de nuevo arranque.

## En PLC
`K0` se reemplaza por la **memoria de marcha `MA`** (ver [[PLC]] y [[Set y Reset]]).
- Opción 1: autorretención con un contacto de `MA`.
- Opción 2: `SET MA` con el pulsador de marcha y `RESET MA` con el de parada.

El pulsador de parada es **NC** por seguridad → [[Lógica positiva y negativa]].

## Videos
[[2020-04-20 Repaso EN 2 - Resolución del circuito eléctrico]] · [[2020-09-03 Automatismo electroneumático en Ladder]]
