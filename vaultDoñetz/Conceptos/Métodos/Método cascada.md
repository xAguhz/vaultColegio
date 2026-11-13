---
tipo: concepto
area: métodos
tags: [métodos, electroneumática, cascada]
aliases: [Paso a paso por líneas, Cascada eléctrica]
---

# Método cascada (paso a paso por líneas)

Es un método sistemático para resolver la [[Superposición de señales]]. La alimentación se divide en varias **líneas eléctricas** que se prenden **de a una y en orden**. Al cambiar de línea, se corta sola la energía de lo que causaba la superposición.

## 1. Cuadro de la cascada
Cuatro renglones, con tantas columnas como fases:
| Renglón | Contenido |
|---|---|
| **Movimientos** | Actuador + `+` (avanza) o `−` (retrocede). Ej.: `1A1+  2A1+  2A1−  1A1−` |
| **Líneas** | Dónde empieza y termina cada línea |
| **Relé** | Qué relé alimenta cada línea |
| **Bobina** | Qué cabezal se alimenta (o desconecta, con barra) en cada fase |

En el diagrama solo se anotan los **finales de carrera** al final de cada movimiento: el resto va en el cuadro.

## 2. Encontrar las líneas
- La **línea 1 siempre empieza en el punto 1**.
- Se recorre fase por fase. El cambio de línea va **justo antes de que se repita el movimiento de un actuador que ya se movió dentro de esa línea**.
- Al empezar una línea nueva, se "olvidan" los movimientos de las anteriores.
- **Nunca** pueden estar en la misma línea el avance y el retroceso del mismo actuador (si pasa, el corte está mal).
- **Mínimo 2 líneas** (con 1 sería el intuitivo); **máximo = cantidad de fases**.

## 3. Relés
- Se usa **un relé menos que la cantidad de líneas**.
- `K1` alimenta la línea 1, `K2` la línea 2, etc.
- La **última línea** se alimenta con **la negación de todos los relés anteriores** (NC de `K1` en serie con NC de `K2`…).

## 4. Circuito de mando
Para cada relé:
- **Emisores** que inician su línea (para la línea 1: `K0` AND la señal de nuevo arranque, en serie).
- [[Autorretención]] con un NA del propio relé (tiene que quedar energizado toda la línea).
- **Desconexión** con un NC del emisor que se acciona **al terminar la línea** (se sube verticalmente desde el cambio de línea hasta el diagrama).
- Con más de dos líneas, cada relé tiene **dos funciones**: alimentar su línea y desconectar la anterior.

## 5. Circuito de fuerza
- **Línea 1** = NA de `K1`. **Última línea** = NC de los relés. Se les pone un cartelito ("Línea 1", "Línea 2").
- Las bobinas se dibujan **en el orden del cuadro**.
- Bobina en la **primera fase de una línea** → va **directa con un cable** a la línea.
- Bobina en una fase posterior → va a la línea **a través de un NA del emisor** que inicia esa fase (se sube verticalmente del cuadro al diagrama).
- Las desconexiones de monoestables marcadas con barra **no requieren nada**: se cortan solas cuando se apaga su línea.

## Características
- ✅ Con pocas líneas, el circuito de mando es **mínimo** (un relé para 4 fases).
- ⚠️ La última línea, alimentada por NC, **queda siempre energizada** (consumo permanente mientras la máquina está parada).
- ❌ **No sirve si un actuador repite movimiento** dentro del ciclo: habría que alimentar la misma bobina en dos líneas y se mezclan → [[Método paso a paso]].

## En PLC
[[Cascada en Ladder]]: memorias `M1`, `M2` en lugar de relés, con [[Set y Reset]].

## Videos
[[2021-05-21 Cascada con lógica cableada y superposición]] (explicación más completa) · [[2020-05-23 Cascada eléctrica - 2 actuadores]] · [[2020-10-01 Cascada en Ladder - pizarrón]]
