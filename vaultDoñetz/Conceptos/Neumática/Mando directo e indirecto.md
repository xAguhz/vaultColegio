---
tipo: concepto
area: neumática
tags: [neumática, electroneumática]
---

# Mando directo e indirecto

## En neumática
- **Mando directo:** el emisor de señal (pulsador, rodillo) se conecta **directamente** al actuador. No hay nada en el medio.
  Ejemplo: pulsador 3/2 → cilindro de simple efecto (avanza mientras se mantiene apretado).
- **Mando indirecto:** el emisor de señal pilotea una **válvula de mando** (o de maniobra), y esa válvula controla al actuador.

## En electroneumática
- Un contacto eléctrico nunca puede ir "directo" al actuador neumático: **siempre hay una electroválvula**, que convierte la señal eléctrica en neumática.
- **Mando directo:** los emisores (pulsadores, interruptores, rodillos eléctricos) alimentan **directamente al cabezal** (solenoide) de la electroválvula.
- **Mando indirecto:** los emisores alimentan la **bobina de un relé** (circuito de mando) y un contacto de ese relé alimenta al cabezal (circuito de **fuerza** o potencia).

## Ejemplo de aplicación (mando directo, dos actuadores)
Morsa + agujereadora de banco: con el pulsador apretado, `1A1` sujeta la pieza. Al llegar pisa `1S2`, que hace bajar el mandril (`2A1`). Al soltar el pulsador vuelven los dos.
Problema: mientras el operario sostiene el pulsador, la pieza puede quedar suelta. Eso se resuelve con métodos más avanzados.

## Videos
[[2020-07-14 Mando directo neumático parte 1]] · [[2020-07-14 Mando directo neumático parte 2]] · [[2020-06-26 Clase en vivo - Mando directo electroneumático]]
