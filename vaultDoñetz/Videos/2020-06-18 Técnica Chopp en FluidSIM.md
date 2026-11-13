---
tipo: video
fecha: 2020-06-18
url: https://www.youtube.com/watch?v=QnoNhFLIgFU
duracion: "9:10"
vistas: 691
area: electroneumática
lista: Repaso Electro-Neumática
---

# Técnica "Chopp" con un solo actuador, simulada en FluidSIM

## Parte 1: circuito con monoestable
- Doble efecto, 5/2 monoestable servopilotada (`1Y1`), estranguladoras para avance y retroceso, rodillos `1S1` y `1S2`. Dos fases, ciclo continuo.
- `0S1` (interruptor de marcha) AND `1S1` (doble clic para nombrarlo; el simulador lo muestra cerrado porque arranca accionado) → `K1`, con autorretención. NA de `K1` → `1Y1`.
- `1S2` (NC) rompe la autorretención y el actuador retrocede.
- Si se suelta el interruptor de marcha, **completa el ciclo** y para (no es parada de emergencia).

## Parte 2: reemplazo por biestable
- Se agrega `1Y2` alimentado por un **NC de `K1`**. Con una sola línea nueva, funciona.
- En reposo `1Y2` está energizado, lo que asegura el vástago retraído.
- Con NA y NC del mismo relé, nunca hay dos cabezales alimentados a la vez.

## Conceptos
[[Técnica Chopp]] · [[FluidSIM]] · [[Electroválvulas monoestables y biestables]] · [[Superposición de señales]]
