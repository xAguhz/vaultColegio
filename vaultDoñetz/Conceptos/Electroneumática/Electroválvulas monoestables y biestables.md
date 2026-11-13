---
tipo: concepto
area: electroneumática
tags: [electroneumática, válvulas]
---

# Electroválvulas monoestables y biestables

## Monoestable
- **Un solo cabezal** eléctrico (`1Y1`, en general servopilotado) y **retorno por resorte**.
- Es estable en una sola posición: si se corta la corriente, **vuelve sola**.
- Hay que **mantenerla alimentada** todo el tiempo que el actuador tenga que quedar en la otra posición → [[Autorretención]] del relé que la alimenta.
- "Retroceder" = **desconectar** el cabezal. En el diagrama se anota `1Y1` negado (la barrita de negación significa desconexión).
- Detalle de un ejercicio: si se gira el cabezal y el resorte de lugar, la misma válvula hace que el actuador arranque extendido.

## Biestable
- **Dos cabezales** (`1Y1` avance y `1Y2` retroceso, según cómo esté conectada) y **sin resorte**.
- Es estable en las dos posiciones: **memoriza mecánicamente** la última orden. Basta un **pulso**.
- Peligro: si los dos cabezales están alimentados a la vez → [[Superposición de señales]]. La válvula respeta la **primera** señal que llegó y queda trabada.

## Cambiar una por otra
Para pasar de monoestable a biestable sin rehacer el circuito está la [[Técnica Chopp]].

## Importante
Antes de completar el diagrama hay que **mirar cómo está conectada** la válvula al actuador: en algunos ejercicios alimentar `1Y1` hace **retroceder** el actuador.
