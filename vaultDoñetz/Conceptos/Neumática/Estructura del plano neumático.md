---
tipo: concepto
area: neumática
tags: [neumática, norma, plano]
---

# Estructura del plano neumático

Según la norma ([[Nomenclatura ISO 1219]]), el plano respeta **niveles por función**, de abajo hacia arriba:

| Nivel | Contenido |
|---|---|
| 5 (arriba) | **Actuadores** |
| 4 | **Válvulas de mando / maniobra** (5/2, 3/2 que mueven actuadores) |
| 3 | **Procesamiento de señales** (válvula AND, temporizadores) |
| 2 | **Emisores de señal** (pulsadores, interruptores, rodillos) |
| 1 (abajo) | **Alimentación** (fuente de aire, `0Z1`) |

## Rodillos
En la máquina, el vástago pisa al rodillo. En el plano **no** se dibuja el rodillo junto al actuador (complicaría las mangueras): junto al actuador solo va una **marca con el nombre** (`1S1`, `1S2`) en la posición donde está, y la válvula del rodillo se dibuja en el nivel de emisores.

## Condiciones iniciales
Todo se dibuja **como arranca** la máquina: rodillos pisados conmutados, válvulas en su posición inicial.

## Plano eléctrico (electroneumática)
Líneas de +24 V arriba y 0 V abajo, con circuitos verticales. Orden típico de izquierda a derecha:
1. **Circuito de sensado** ([[Circuito de sensado]]).
2. **Enclavamiento eléctrico** ([[Enclavamiento eléctrico]]).
3. **Circuito de mando** (relés).
4. **Circuito de fuerza o potencia** (cabezales `Y`).
