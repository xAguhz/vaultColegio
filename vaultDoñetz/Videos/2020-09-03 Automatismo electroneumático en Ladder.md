---
tipo: video
fecha: 2020-09-03
url: https://www.youtube.com/watch?v=PgoD8ATRaNs
duracion: "24:05"
vistas: 35366
area: plc
---

# Ejemplo de automatismo electroneumático con programación Ladder

## Ejercicio
Un actuador de doble efecto con **biestable**, que **arranca extendido**. Ciclo continuo: retrocede → avanza.
**Entradas:** `I1` = `1S1`, `I2` = `1S2` (pisado), `I5` = `PM`, `I6` = `PP` (**NC**). **Salidas:** `Q1` = `1Y1`, `Q2` = `1Y2`.

## Puntos clave
- Primero hay que dibujar el circuito neumático y **ver cómo está conectada la válvula**: al principio el profe se confunde y se corrige (`1Y2` lo hace retroceder).
- **Memoria de marcha `MA`** (marca interna), que reemplaza a `K0`. Ver [[Enclavamiento eléctrico]].
- **Pulsador de parada NC** por seguridad → lógica negativa: en reposo `I6 = 1`. En este video usa **NA de `I6`** en serie dentro de la autorretención de `MA` (cuando se aprieta parada, `I6 = 0` y se corta).
- **Programa (método intuitivo):**
  1. `I5` ∥ `MA` (autorretención), en serie con `I6` → `( MA )`
  2. `MA` · `I2` → `( Q2 )` (1Y2, retrocede)
  3. `I1` → `( Q1 )` (1Y1, avanza)
- No hace falta circuito de fuerza: lo reemplaza la conexión de las salidas.
- Simulación: hay que poner `I2` e `I6` en 1 antes de RUN. La biestable memoriza la posición aunque se suelte el rodillo. Si se para, completa el ciclo y no vuelve a arrancar.

## Conceptos
[[PLC]] · [[Lenguaje Ladder]] · [[Lógica positiva y negativa]] · [[Método intuitivo]] · [[Zelio Soft 2]]
