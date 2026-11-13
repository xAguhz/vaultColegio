---
tipo: concepto
area: neumática
tags: [neumática, ciclo]
---

# Ciclo único y ciclo continuo

- **Ciclo único:** se pulsa, la máquina hace un ciclo y se detiene. Para otro ciclo hay que volver a pulsar. Se arranca con un **pulsador**.
- **Ciclo continuo:** termina y vuelve a arrancar solo. En el diagrama se escribe **`3 ≡ 1`** (el último punto equivale al primero), como si se copiara y pegara el ciclo a continuación. Se arranca con un **interruptor** (pulsador con enclavamiento mecánico) o con un relé o memoria de marcha.

## Señal de nuevo arranque
El **último final de carrera que se pisa** al terminar el ciclo (casi siempre `1S1` o `2S1`). Hasta que no se pisa, no arranca un nuevo ciclo. Va en **AND** con la marcha:
- neumática: [[Válvula lógica AND]];
- eléctrico: dos contactos NA en serie;
- Ladder: dos contactos en serie.

## Parada
Al soltar el interruptor de marcha (o tocar la parada), la máquina **completa el ciclo** y se detiene en la posición inicial. *No* es una parada de emergencia.

## Ejemplo
Estampadora sobre una cinta transportadora: baja el actuador (estampa), sube, y la pieza sigue su camino.

## Videos
[[2020-07-13 Circuito neumático de ciclo único]] · [[2020-07-13 Circuito neumático de ciclo continuo]]
