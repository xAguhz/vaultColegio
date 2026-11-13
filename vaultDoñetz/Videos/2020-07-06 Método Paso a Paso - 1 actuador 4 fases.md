---
tipo: video
fecha: 2020-07-06
url: https://www.youtube.com/watch?v=1nsBV1uBXpo
duracion: "21:59"
vistas: 3971
area: métodos
lista: Electro-Neumática Avanzada
---

# Método sistemático "Paso a Paso" (electroneumática avanzada)

## Ejercicio
Un actuador de doble efecto con biestable y **4 fases**: sale, entra, sale, entra. Recién ahí termina el ciclo. Sensores `1B1` (→ `KA`, arranca detectando) y `1B2` (→ `KB`). Marcha `PM`, parada `PP` y parada de servicio `PS`.

## Por qué no sirve la cascada
La misma bobina habría que alimentarla en **dos líneas distintas** (`1Y1` en la 1 y en la 3), y eso mezcla las líneas. "Inténtenlo por cascada y van a ver que se traba."

## Cuadro
| Paso | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Relé | K1 | K2 | K3 | K4 |
| Bobina | 1Y1 | 1Y2 | 1Y1 | 1Y2 |
| Emisor | K0 · KA | KB | KA | KB |

## Mando (estructura repetida)
`emisores` + `NA del relé anterior (habilita)` + `NC del relé siguiente (desconecta)` → `Kn`, con autorretención de `Kn` **entre el que habilita y el que desconecta**.
- Paso 1: `K0` · `KA` · habilita `K4` · desconecta `K2`.
- Paso 2: `KB` · habilita `K1` · desconecta `K3`.
- Paso 3: `KA` (otro contacto) · habilita `K2` · desconecta `K4`. Sin la habilitación, como `KA` arranca energizado, ¡arrancaría por el paso 3!
- Paso 4: `KB` · habilita `K3` · desconecta `K1`.
- **Primer arranque:** NA de `PM` en paralelo con la autorretención de `K4`.

## Fuerza
`1Y1` ← `K1 ∥ K3` (OR) · `1Y2` ← `K2 ∥ K4`. Un contacto distinto por bobina.

## Conceptos
[[Método paso a paso]] · [[Método cascada]] · [[Circuito de sensado]]
