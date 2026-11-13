---
tipo: video
fecha: 2020-08-24
url: https://www.youtube.com/watch?v=OTHHkpURGSg
duracion: "24:29"
vistas: 5511
area: métodos
lista: Electro-Neumática Avanzada
---

# Método Paso a Paso con lógica cableada, monoestables y repetición de movimiento

## Ejercicio
2 actuadores, **2 monoestables**, **5 fases**. `2A` **repite movimiento** dentro del ciclo (sale, espera con temporizador, vuelve, sale otra vez, vuelve) y hay un temporizador `K6`. En la última fase retroceden los dos.

## Claves
- 5 fases → 5 pasos → relés `K1…K5`; temporizado `K6`.
- Nuevo arranque: `1S1` **y** `2S1` (retroceden los dos a la vez).
- **Rodillos que actúan dos veces** (`2S1`, `2S2`) → relés auxiliares `KA` y `KB` en un [[Circuito de sensado]], para tener varios contactos.
- **Monoestables en el cuadro:** la bobina se repite en los pasos siguientes mientras el actuador tenga que seguir extendido:
  - `2Y1` en K1, K2 y K4;
  - `1Y1` en K3 y K4;
  - `K6` en K2.
- **Fuerza:** `2Y1` ← `K1 ∥ K2 ∥ K4`; `1Y1` ← `K3 ∥ K4`; `K6` ← `K2`.
- **Mando:** paso 1 = `K0` · `KA` · `1S1`, habilita `K5`, desconecta `K2`, …; paso 3 = NA de `K6`; paso 4 = `1S2` · `KA`; paso 5 = `KB`. Primer arranque con `0S1` en paralelo con la autorretención de `K5`.
- Con cascada sería complicado: se mezclarían las líneas por la repetición y por las monoestables.

## Conceptos
[[Método paso a paso]] · [[Circuito de sensado]] · [[Electroválvulas monoestables y biestables]] · [[Relés temporizados]]
