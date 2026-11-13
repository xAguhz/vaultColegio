---
tipo: concepto
area: neumática
tags: [neumática, nomenclatura, norma]
---

# Nomenclatura ISO 1219

Así nombra el profe los elementos en los planos (según la norma ISO 1219, la que usan en la escuela).

## Regla de lectura
Se **escribe** de izquierda a derecha, pero el significado se **lee de atrás para adelante**.
- `1S2` → "segundo *switch* del cilindro 1".
- `0S1` → "primer switch **general** para toda la máquina" (el `0` significa *general*, no un actuador en particular).
- Los **actuadores** son la excepción: se leen de izquierda a derecha (`2A1`: actuador 2 del grupo 1).

## Letras
| Letra | Elemento | Ejemplos |
|---|---|---|
| **A** | Actuador | `1A1`, `2A1` (después abrevia `1A`, `2A`) |
| **V** | Válvula (se nombran de **arriba hacia abajo** y de **izquierda a derecha**) | `1V1` estranguladora, `1V3` válvula de mando, `1V4` válvula AND, `1V5` temporizador |
| **S** | Emisor de señal (*switch*): pulsador, interruptor, rodillo | `0S1` marcha, `0S2` parada, `0S3` parada de mantenimiento, `1S1` comienzo de carrera, `1S2` final de carrera |
| **Z** | Alimentación de aire comprimido | `0Z1` unidad de mantenimiento ([[Unidad de mantenimiento FRL]]) |
| **Y** | Solenoide o cabezal eléctrico de una electroválvula | `1Y1`, `1Y2`, `2Y1` |
| **B** | Sensor de proximidad (electroneumática) | `1B1`, `1B2`, `2B2` |
| **K** | Relé | `K0` enclavamiento, `K1…Kn` mando, `KA/KB` auxiliares de sensores, `K10` memoria |
| **H** | Indicador luminoso | `H1` |

- Los emisores de señal **no** llevan número de válvula: se identifican por el accionamiento (rodillo, pulsador).
- Alternativa que usa en algunos videos: `PM` (pulsador de marcha), `PP` (parada), `PS` (parada de servicio).

## Numeración de conexiones de válvulas
Está en [[Válvulas distribuidoras]] (1 presión, 2 y 4 salidas, 3 y 5 escapes, 12 y 14 pilotajes).

## Relacionado
[[Estructura del plano neumático]] · [[Contactos eléctricos]]
