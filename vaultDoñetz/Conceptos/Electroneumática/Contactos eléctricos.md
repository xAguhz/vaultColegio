---
tipo: concepto
area: electroneumática
tags: [electroneumática, eléctrico, simbología]
---

# Contactos eléctricos y su numeración

## Tipos
| Contacto | Bornes | Uso |
|---|---|---|
| **Normal abierto (NA)** | 3 – 4 (13-14, 23-24…) | Deja pasar corriente al accionarse |
| **Normal cerrado (NC)** | 1 – 2 (11-12, 21-22…) | Corta la corriente al accionarse |
| **Conmutador** | 1 – 2 – 4 (11, 12, 14 / 21, 22, 24 / 31, 32, 34) | Entre 1 y 4 funciona como NA; entre 1 y 2, como NC |

- **El primer dígito** indica qué contacto del elemento es: 1x = primero, 2x = segundo, 3x = tercero.
- Los **rodillos** de los tableros didácticos traen contacto **conmutador**, igual que los relés que usan.
- **Relés temporizados:** el profe numera el NA temporizado como **17-18** y el NC como **35-36** (o 15-16 según el modelo) y los dibuja con un paréntesis. (`?` Revisá la numeración con la de tu tablero.)

## Accionamientos
Pulsador (corchete), interruptor (corchete con traba = enclavamiento mecánico), rodillo, bobina de relé.

## Cómo se marcan las condiciones iniciales
- **Rodillo pisado:** doble flechita hacia arriba. El conmutador se dibuja ya conmutado.
- **Contacto NA que arranca cerrado** (porque su rodillo o relé arranca accionado): se le hace un **arquito**.
- **Relé energizado desde el arranque** (por ejemplo `KB` de un sensor que ya detecta): un **puntito** en la bobina.

## Funciones lógicas con contactos
- **AND:** contactos NA en **serie**.
- **OR:** contactos NA en **paralelo**.
- **NOT:** contacto **NC**.

Ver [[Funciones lógicas]].
