---
tipo: concepto
area: electroneumática
tags: [electroneumática, plc, lógica]
---

# Lógica positiva y negativa

- **Lógica positiva:** la acción se activa con un **valor alto (1)**: pasa corriente cuando el elemento se acciona. Es lo habitual (contactos NA).
- **Lógica negativa:** la acción se activa con un **valor bajo (0)**: se **corta** la señal al accionar. Por ejemplo, un sensor que entrega 0 al detectar o un rodillo conectado como NC.

## Ejemplo del video (1 actuador: avanza, espera 3 s, retrocede)
| | Lógica positiva | Lógica negativa |
|---|---|---|
| Rodillo `1S2` | Conectado como NA → alimenta el temporizador al pisarse | Conectado como **NC** → corta al pisarse |
| Temporizador | Retardo a la **conexión** (`K2`) | Retardo a la **desconexión** (`K3`) |
| Corte de la autorretención de `K1` | **NC** de `K2` | **NA** de `K3` (que arranca cerrado porque el relé está energizado desde que se prende la fuente) |

El funcionamiento final es idéntico. Solo se cambiaron dos contactos.
La desconexión de una autorretención es en sí misma lógica negativa: para desconectar, hay que **abrir** el circuito.

## Pulsador de parada (seguridad eléctrica)
- Siempre **NC**: si se corta el cable, la máquina interpreta "parada" y se detiene por precaución. La parada tiene prioridad sobre la marcha.
- En PLC, la entrada del pulsador de parada **vale 1 en reposo**. Por eso en Ladder se usa un **contacto NC** para resetear la marcha (si se pusiera NA, el reset quedaría siempre activo y, como el reset tiene prioridad, la máquina nunca arrancaría).

## En el paso a paso con PLC
La memoria `M1` del primer paso se trabaja con lógica negativa para que el paso 1 esté habilitado al arrancar → [[Paso a paso en Ladder]].

## Videos
[[2021-04-10 Lógica positiva y negativa]] · [[2020-09-03 Automatismo electroneumático en Ladder]]
