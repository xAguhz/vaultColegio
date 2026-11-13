---
tipo: video
fecha: 2025-05-04
url: https://www.youtube.com/watch?v=x3tHWYUn9UU
duracion: "19:23"
vistas: 700
area: métodos
lista: Electro-Neumática Avanzada
---

# Automatismo con superposición de señales, resuelto con relé auxiliar de memoria

**La vuelta al canal** después de más de 4 años, "a pedido de mis alumnos".

## Ejercicio
2 actuadores de doble efecto con **biestables**. `1A` arranca **extendido**. 5 fases: `1A−` · pausa 4 s (`K2`) · `1A+` · `2A+` · `2A−`. Señal de nuevo arranque: `2S1`.

## Primero, el método intuitivo (y por qué falla)
- `K0`·`2S1` → `K1` → `1Y2`; `1S1` → `K2` (4 s) → `1Y1`; `1S2` → `K3` → `2Y1`; `2S2` → `K4` → `2Y2`.
- En el simulador, **`2A` sale solo** al prender (porque `1S2` está pisado) y después se traba.
- En el diagrama: `2S1` está pisado de 1 a 4 (alimenta `1Y2`) y choca con `1Y1` en el punto 3; `1S2` está pisado de 4 a 6 (alimenta `2Y1`) y choca con `2Y2` en el punto 5.

## Solución con el relé `K10`
- **NC de K10** en serie con `2S1` (tiene que dejar pasar al arranque).
- **NA de K10** en serie con `1S2` (lo bloquea al arranque).
- **Activa** K10: NA de `K2` (punto 3) + autorretención.
- **Desactiva** K10: NC de `K4` (punto 5).
- Regla: habilitar una fase antes de usar la señal y cortar donde provoca la superposición.
- Resultado: "funcionando de mil maravillas".

Al final consulta si los alumnos prefieren una serie de neumática, de electroneumática o seguir con PLC.

## Conceptos
[[Método de memorias]] · [[Superposición de señales]] · [[Método intuitivo]] · [[FluidSIM]]
