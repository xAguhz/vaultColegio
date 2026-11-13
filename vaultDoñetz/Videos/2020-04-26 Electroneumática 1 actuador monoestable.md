---
tipo: video
fecha: 2020-04-26
url: https://www.youtube.com/watch?v=7ARQojNrfUE
duracion: "6:59"
vistas: 936
area: electroneumática
lista: Repaso Electro-Neumática
visibilidad: oculto
---

# Electroneumática: 1 actuador monoestable

"Nuestro primer ejemplo monoestable": un actuador de doble efecto con una 5/2 monoestable (servopilotada, retorno a resorte), estranguladoras y rodillos `1S1` y `1S2`. Dos fases.

## Resolución
- Primer movimiento: `K0` (enclavamiento) AND `1S1` (pisado, NA conectado en 1-4, arranca cerrado) → `K1`.
- Como la válvula es monoestable, `K1` se **autorretiene** (NA de `K1` en paralelo con los emisores) y se deja el lugar para la desconexión.
- **Fuerza:** NA de `K1` (21-24) → `1Y1`.
- Punto 2: `1S2` tiene que **desconectar** `1Y1` (se anota `1Y1` negado). Se hace con un **NC de `1S2`** que rompe la autorretención; no hace falta otro relé.
- `1S1` es la señal de nuevo arranque.

## Conceptos
[[Electroválvulas monoestables y biestables]] · [[Autorretención]] · [[Método intuitivo]] · [[Enclavamiento eléctrico]]
