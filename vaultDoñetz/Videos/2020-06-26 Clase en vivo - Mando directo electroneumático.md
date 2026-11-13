---
tipo: video
fecha: 2020-06-26
url: https://www.youtube.com/watch?v=_LD3peJLNRM
duracion: "54:36"
vistas: 4161
area: electroneumática
lista: [Electro-Neumática, Repaso Electro-Neumática]
---

# Clase en vivo: electroneumática, ejemplos de mando directo

Grabación de una **clase sincrónica** (pandemia), con alumnos conectados por celular. El profe les pide poner el teléfono horizontal para ver el pizarrón.

## Teoría
- Por qué electroneumática: los sensores de color, de material o magnéticos son electrónicos. Ver [[Electroneumática]].
- **Dos energías**: aire comprimido + fuente de **24 Vcc** (desde 220 Vca).
- Repaso de 3/2 NC con simple efecto y de 5/2 con doble efecto; numeración 1/2/3, 10/12 y 14. Ver [[Válvulas distribuidoras]].
- **Cabezal eléctrico:** símbolo, nombres `1Y1` y `1Y2`; cómo funciona como electroimán.
- [[Superposición de señales]]: la válvula respeta la primera señal que llega.
- **Contactos:** NA (3-4), NC (1-2), conmutador (1-2-4), y los accionamientos. Ver [[Contactos eléctricos]].
- **Mando directo en electroneumática:** emisores conectados directamente al cabezal. La electroválvula es un **conversor de señal eléctrica a neumática**. Ver [[Mando directo e indirecto]].
- Las bobinas van **en paralelo** (en serie recibirían 12 V cada una).

## Ejercicio 1: un actuador, 2 fases, ciclo continuo
`0S1` (interruptor 13-14) en serie con `1S1` (conmutador conectado en 1-4, pisado) → `1Y1`. `1S2` (1-4) → `1Y2`.

## Ejercicio 2: dos actuadores, 3 fases
`2A1+` → `2A1−` + `1A1+` (a la vez) → `1A1−`.
- Fase 1: `0S1` + `1S1` → `2Y1`.
- Fase 2: `2S2` alimenta **en paralelo** `2Y2` y `1Y1`.
- Fase 3: `1S2` en serie con `2S1` (pisado) → `1Y2`.

## Notas
Recomienda [[FluidSIM]] **4.2** para todos, para que los archivos sean compatibles.

## Conceptos
[[Mando directo e indirecto]] · [[Electroneumática]] · [[Diagrama espacio-fase]]
