---
tipo: video
fecha: 2020-07-13
url: https://www.youtube.com/watch?v=bDfF7W6E0Mw
duracion: "19:13"
vistas: 4823
area: neumática
---

# Circuito neumático de ciclo continuo

Continúa [[2020-07-13 Circuito neumático de ciclo único]].

## Contenido
- Ejemplo de aplicación: **estampadora** sobre una cinta transportadora.
- **Ciclo continuo:** `3 ≡ 1`. Termina y vuelve a arrancar. Ver [[Ciclo único y ciclo continuo]].
- **Señal de nuevo arranque:** `1S1`, el último rodillo que se pisa. Va en AND con la marcha.
- El pulsador `0S1` pasa a ser un **interruptor** (pulsador con enclavamiento mecánico).
- Rodillo **pisado al inicio**: se dibuja conmutado, con un bloque que lo empuja.
- **[[Válvula lógica AND]]** en el nivel de procesamiento: entradas `0S1` y `1S1`, salida → `14 de 1V1`. Nombre `1V2`. Funcionamiento interno del núcleo en forma de "H".
- Se relaciona con la compuerta AND que ven en el taller de digitales los de Electrónica.

## Conceptos
[[Ciclo único y ciclo continuo]] · [[Válvula lógica AND]] · [[Estructura del plano neumático]]
