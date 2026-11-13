---
tipo: video
fecha: 2020-04-20
url: https://www.youtube.com/watch?v=7K-tgNjpm_M
duracion: "11:10"
vistas: 1743
area: electroneumática
lista: Repaso Electro-Neumática
---

# Repaso EN 2 — Resolución del circuito eléctrico

Continúa [[2020-04-20 Repaso EN 1 - Análisis del diagrama espacio-fase]].

## Orden de armado
1. **Sensado:** `1B2` → relé `KA`; `2B2` → relé `KB`. `2B2` arranca detectando, así que `KB` arranca energizado (puntito) y sus NA se dibujan con arquito. Ver [[Circuito de sensado]].
2. **Enclavamiento:** `0S1` NA + `0S3` NC → `K0`, autorretención con NA de `K0` + NC de `0S2`. Ver [[Enclavamiento eléctrico]].
3. **Línea de mando 1:** NA de `K0` (21-24) + NA de `KB` → `K1`, autorretenido, con hueco para el NC que lo corte.
4. **Línea 2:** el sensor alimenta **directamente** al temporizado `K2` (5 s) para ahorrar un relé.
5. **Fuerza:** NA de `K1` → `1Y1`, con un **NC de `K2`** en serie para desconectarlo.
6. **Línea 3:** NA de `K2` → `K3` autorretenido; NA de `K3` → `2Y1`.
7. **Línea 4:** NA de `1S1` (pisado) **en serie** con NA de `2S1` → `K4` (AND); el NC de `K4` (11-12) corta la autorretención de `K3`.

## Detalles
- Numeración de los contactos de relés temporizados del tablero: ver [[Contactos eléctricos]].
- Por qué no alcanza con `K2` para `2Y1`: la válvula es monoestable y `K2` se suelta, así que se necesita un relé que se autorretenga.

## Conceptos
[[Método intuitivo]] · [[Autorretención]] · [[Relés temporizados]]
