---
tipo: video
fecha: 2020-05-23
url: https://www.youtube.com/watch?v=7vdjtyT1_Og
duracion: "16:08"
vistas: 4073
area: métodos
lista: Repaso Electro-Neumática
---

# Método de cascada eléctrica: 2 actuadores

Primer video de cascada (para alumnos que todavía no la habían visto).

## Ejercicio
- `1A1` doble efecto con válvula **biestable** (`1Y1` avance, `1Y2` retroceso).
- `2A1` con válvula **monoestable** (`2Y1`).
- Movimientos: `1A1+  2A1+  2A1−  1A1−`.
- Rodillos: `1S2` (fin de `1A1+`), `2S2` (fin de `2A1+`), `2S1` (fin de `2A1−`), `1S1` (fin del ciclo, nuevo arranque).

## Cuadro
| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Mov. | 1A1+ | 2A1+ | 2A1− | 1A1− |
| Línea | 1 | 1 | 2 | 2 |
| Relé | K1 | | K1 negado | |
| Bobina | 1Y1 | 2Y1 | 2Y1 negado | 1Y2 |

El cambio de línea va antes de la fase 3, porque ahí se repite `2A1`. Son 2 líneas, así que alcanza **un solo relé**.

## Circuito
- **Mando:** `K0` (NA, con arquito) + `1S1` → `K1`, autorretención con NA de `K1`, desconexión con **NC de `2S2`** (el emisor en el cambio de línea).
- **Línea 1** (NA de `K1`): `1Y1` directa; `2Y1` a través de un NA de `1S2`.
- **Línea 2** (NC de `K1`): `2Y1` negado → no se hace nada (se desconecta solo al caer la línea 1); `1Y2` a través de un NA de `2S1` (pisado).
- Las dos líneas **nunca** están alimentadas a la vez, y eso evita la superposición.

## Conceptos
[[Método cascada]] · [[Superposición de señales]]
