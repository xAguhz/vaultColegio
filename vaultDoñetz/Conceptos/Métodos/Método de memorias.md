---
tipo: concepto
area: métodos
tags: [métodos, electroneumática, memorias]
---

# Método de memorias (relé auxiliar de memoria)

Es el método más reciente del canal (2025). Se parte del **[[Método intuitivo]]** y se corrigen solo los puntos donde hay [[Superposición de señales]] con **un relé auxiliar autorretenido** (en el ejemplo, `K10`) que funciona como memoria eléctrica.

## Procedimiento
1. Resolver por el método intuitivo y **detectar los rodillos problemáticos**: los que quedan pisados durante varias fases (se marcan en el diagrama).
   En el ejemplo, `2S1` (pisado del punto 1 al 4, alimenta `1Y2` a través de `K1`) y `1S2` (pisado del 4 al 6, alimenta `2Y1` a través de `K3`).
2. Armar el relé auxiliar con autorretención: un **NA que lo activa** y un **NC que lo desconecta** (todavía sin nombre).
3. Poner contactos del auxiliar **en serie con cada rodillo problemático**:
   - **NC de K10** para el rodillo que tiene que **actuar desde el arranque** del ciclo (`2S1`). Así deja pasar la señal hasta que K10 se active.
   - **NA de K10** para el rodillo que **no** tiene que actuar al arranque (`1S2`). Si no se bloquea, el actuador 2 **sale solo** al prender.
4. Buscar **quién activa** y **quién desconecta** a K10:
   - **Activar** K10 en el punto donde aparece la primera superposición (fin del temporizador, punto 3) → NA de `K2`.
   - **Desconectar** K10 en el punto de la segunda superposición (punto 5) → NC de `K4`.

## Reglas para encontrarlos
- Un rodillo hay que **habilitarlo una fase antes** de que se use, y **bloquearlo donde provoca la superposición**.
- Usar como emisores **relés** (que tienen varios contactos), no rodillos sueltos.
- Como el punto final equivale al punto 1 (ciclo continuo), "una fase antes del punto 1" = el punto 5.

## Videos
[[2025-05-04 Método de memorias - relé auxiliar]]
