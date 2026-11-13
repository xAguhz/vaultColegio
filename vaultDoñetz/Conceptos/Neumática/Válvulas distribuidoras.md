---
tipo: concepto
area: neumática
tags: [neumática, válvulas]
---

# Válvulas distribuidoras

## Denominación "vías / posiciones"
- **3/2**: 3 conexiones (vías) y 2 posiciones. *Normal cerrada* (NC): en reposo la entrada de presión (1) está tapada.
- **5/2**: 5 vías y 2 posiciones. Es la que controla un actuador de **doble efecto**.
- La posición **de la derecha** del símbolo es la posición normal (de reposo).

## Numeración de conexiones
| N.º | Función | Letra vieja |
|---|---|---|
| 1 | Entrada de presión | P |
| 2, 4 | Salidas de trabajo (normalmente **2 adelante** del émbolo y **4 atrás**) | A, B |
| 3, 5 | Escapes (los impares) | R, S |
| 12 | Pilotaje que conecta 1 con 2 → **retroceso** | Z/Y |
| 14 | Pilotaje que conecta 1 con 4 → **avance** | Z/Y |
| 10 | Pilotaje que cierra la 1 (en 3/2) | — |

> El número del pilotaje dice **qué conexión establece**: "14" = une 1 con 4.

## Accionamientos
Pulsador manual, interruptor (pulsador con **enclavamiento mecánico**: queda trabado), rodillo, neumático (piloto de aire) y eléctrico (solenoide → [[Electroválvulas monoestables y biestables]]). El retorno suele ser por **resorte**.

## Rodillo pisado al inicio
Se dibuja la válvula **conmutada** (las conexiones del lado contrario) y, en neumática, un bloque sólido que la empuja. En eléctrico se usa la doble flechita (ver [[Contactos eléctricos]]).

## El uso más común
Como emisor de señal: **3/2 NC con retorno a resorte**, que cambia solo el accionamiento (pulsador, rodillo…). Si una salida no se usa, va un **tapón**.

## Relacionado
[[Válvula lógica AND]] · [[Temporizador neumático]] · [[Válvula estranguladora]] · [[Nomenclatura ISO 1219]]
