---
tipo: video
fecha: 2020-04-20
url: https://www.youtube.com/watch?v=xPYGSYCGWQ4
duracion: "3:35"
vistas: 4767
area: electroneumática
lista: Repaso Electro-Neumática
visibilidad: oculto
---

# Repaso EN 1 — Análisis del diagrama espacio-fase

Ejercicio de **repaso y diagnóstico** que había mandado a los alumnos. Este video solo hace el análisis; la resolución está en [[2020-04-20 Repaso EN 2 - Resolución del circuito eléctrico]].

## Enunciado (reconstruido)
- `1A1`: simple efecto, válvula 3/2 monoestable (la salida que no se usa lleva tapón), con **dos sensores** (inductivos o capacitivos).
- `2A1`: doble efecto, velocidad regulada con dos estranguladoras, 5/2 monoestable **con el cabezal y el resorte girados** (el aire entra por 1 y sale por 4: arranca **extendido**). Tiene dos rodillos.
- Hay una pausa de **5 s**.

## Análisis
1. El primer movimiento lo controla el primer relé de mando `K1` → alimenta `1Y1` (con autorretención).
2. Punto 2: `1B2` detecta → arranca el temporizador `K2`.
3. Punto 3: `K2` termina → desconecta `1Y1` (NC de `K2`) **y** alimenta `2Y1` a través de `K3`, que necesita autorretención porque la válvula es monoestable (no alcanza con `K2`).
4. Punto 4: se pisan `1S1` y `2S1` al mismo tiempo → función AND → `K4`, que desconecta `2Y1` (corta la autorretención de `K3`).
5. `2B2` es la señal de nuevo arranque, junto con `K0`.

## Conceptos
[[Diagrama espacio-fase]] · [[Relés temporizados]] · [[Autorretención]]
