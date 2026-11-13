---
tipo: video
fecha: 2021-05-21
url: https://www.youtube.com/watch?v=yaZsF8jzw7A
duracion: "35:45"
vistas: 7929
area: métodos
lista: Electro-Neumática Avanzada
---

# Método sistemático de "Cascada" (paso a paso por líneas) con lógica cableada

⭐ **La explicación más completa de cascada del canal.** Lo grabó cuando el canal llegó a los **1000 suscriptores**.

## Ejercicio
2 actuadores de doble efecto con **biestables**. `1A1+  2A1+  2A1−  1A1−`.

## Detección de la superposición
- `1S2` queda pisado del punto 2 al 4 alimentando `2Y1`. En el punto 3, `2S2` quiere `2Y2` → **superposición 1**.
- `2S1` queda pisado del punto 4 al 2 del ciclo siguiente alimentando `1Y2`. En el punto 1 se quiere `1Y1` → **superposición 2**.
- Conclusión: no se puede resolver con el método intuitivo.

## Cuadro
| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Mov. | 1A1+ | 2A1+ | 2A1− | 1A1− |
| Línea | 1 | 1 | 2 | 2 |
| Relé | K1 | | K1 negado | |
| Bobina | 1Y1 | 2Y1 | 2Y2 | 1Y2 |

Reglas: cambio de línea antes de que se repita un actuador; mínimo 2 y máximo tantas líneas como fases; relés = líneas − 1; la última línea = negación de todos los relés.

## Circuito (en FluidSIM)
- **Mando:** `K0` (21-24) · `1S1` → `K1`, autorretención, NC de `2S2` (el emisor en el cambio de línea) para desconectar. **Un solo relé para 4 fases.**
- **Línea 1** (NA de `K1`): `1Y1` directa; `2Y1` por NA de `1S2`.
- **Línea 2** (NC de `K1`, 31-32): `2Y2` directa; `1Y2` por NA de `2S1`.
- Característica: la última línea **siempre tiene energía** (consumo permanente).
- Se verifica con el diagrama de estados del simulador.

## Conceptos
[[Método cascada]] · [[Superposición de señales]] · [[FluidSIM]]
