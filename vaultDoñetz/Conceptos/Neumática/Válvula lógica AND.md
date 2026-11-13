---
tipo: concepto
area: neumática
tags: [neumática, válvulas, lógica]
---

# Válvula lógica AND (de simultaneidad)

- **Dos entradas (1, 1) y una salida (2)**. En nomenclatura vieja, las entradas son X e Y.
- Sale aire **solo si entra aire por las dos entradas al mismo tiempo**. Es lo mismo que la compuerta AND de electrónica digital (ver [[Funciones lógicas]]).
- **Funcionamiento:** el núcleo interno es como una "H" ancha que se desplaza. Si entra aire por un solo lado, el núcleo se corre y sella ese paso. Si entra por los dos, el aire pasa a la salida.
- Es un elemento de **procesamiento de señales**: va un nivel arriba de los emisores en el plano ([[Estructura del plano neumático]]).
- Uso típico: marcha (`0S1`) AND señal de nuevo arranque (`1S1`) → entrada 14 de la válvula de mando.
- Nombre en el plano: una válvula más del actuador, por ejemplo `1V2` o `1V4`.

## Videos
[[2020-07-13 Circuito neumático de ciclo continuo]] · [[2020-08-19 Ejercicio con temporizador neumático]]
