---
tags: [cnc, tp, ajedrez]
fecha: 2026-11-28
---
# TP Completacarrera: Rey, Alfil y Reina (herramientas en par)

TP de otro alumno del curso Completacarrera, hecho con el mismo flujo y las mismas herramientas que [[TP Completacarrera - herramientas en par]]: T0101 desbaste y contorno, T0505 ranuras, valles y tronzado, T0303 y T0404 (DVJN derecha e izquierda) para el acabado. El alumno pasó un croquis a mano con las tres piezas.

## Medidas
Base Ø26 y el resto del croquis escalado en proporción. Estas piezas son más altas que las del otro TP. Las tres entran en la barra Ø30 × 130 con 30 mm de agarre.

| Pieza | Largo | Perfil (de la punta a la base) |
|---|---|---|
| Rey | 88 | botón Ø5 × 4 → cilindro Ø13 → cara a Ø26 (Z−8,5) → cono de la corona hasta Ø14 (Z−22) → anillo Ø19 (Z−22 a −25,5) → vástago Ø13 → cono a Ø26 (Z−65,5) → base con dos ranuras de 3,5 mm a Ø20 |
| Alfil | 73 | bola R2,5 → cuello Ø3 → mitra de arco R16,25 hasta Ø19 (Z−18,5) → collarín Ø26 (Z−18,5 a −22) → bajada a Ø20 y empalme R3 → vástago Ø14 → curva R15 a Ø26 (Z−64,5) → base |
| Reina | 77,5 | bola R2,5 → cúpula R6 hasta Ø12 (Z−9,5) → cara a Ø26 → cono de la corona hasta Ø18 (Z−17,5) → empalme R3 a vástago Ø13 → cono a Ø26 (Z−60) → base con garganta semicircular R2,5 (Z−66 a −71) |

Decisiones para que se pueda tornear:
- **Ranuras del rey:** en el croquis miden unos 2 mm y la cuchilla mide 3,05. Se hicieron de 3,5 mm.
- **Bolas del alfil y la reina:** se hicieron de R2,5, porque con R2 el cuello quedaba de Ø1,9 y la unión con la cúpula daba cotas con decimales raros.

## Resultados
| Pieza | Profundidad máxima medida | Tiempo en WinUnisoft |
|---|---|---|
| Rey | T0101 1,8 · T0303 2,0 · T0404 0,3 mm | 23:03 |
| Alfil | T0101 2,1 · T0303 1,9 · T0404 1,8 mm | 20:24 |
| Reina | T0101 2,1 · T0303 1,8 · T0404 1,8 mm | 21:44 |

Las tres se simularon en la pantalla oculta **sin colisiones**. Los planos salen a escala 1:1 (FreeCAD en modo offscreen, sin ventana).

## Compensación del radio de punta
En la simulación aparecían tres defectos: una marca en la garganta de la reina, otra en la bolita, y material de más en la diagonal de la copa. Venían de que el programa seguía el perfil con la punta teórica, mientras que el inserto tiene radio (r 0,4). En las diagonales quedaba material, y en los arcos que terminan entre dos herramientas (T0303 de un lado y T0404 del otro) el error caía hacia lados opuestos y dejaba un escalón.

Se evaluaron cuatro opciones: G41/G42, compensar en el programa, inserto de radio completo para la garganta, y radio 0 en el simulador. **El alumno eligió compensar en el programa**, sin códigos nuevos:
- `compensar()` corre el perfil la distancia del radio de punta (más el sobremetal), rodea las esquinas convexas con un arco y recorta las cóncavas en la intersección. Después pasa del centro del radio a la punta teórica según el código de forma: 3 = (−r, −r) y 4 = (+r, −r).
- Se aplica al contorno de la T0101 (r 0,8) y a las pasadas de la T0303 y la T0404 (r 0,4).
- `sin_gubias()` recorta el principio y el final de cada pasada donde el radio tocaría por debajo del perfil terminado. Hace falta cuando la pasada empieza o termina al lado de un tramo que hace otra herramienta.
- El mapa de material del generador y el verificador ahora simulan el radio de punta. La salida de cada pasada sube siempre, nunca baja.
- Resultado: garganta, bolita y copa salen lisas en WinUnisoft. En los rincones con ángulo vivo queda el radio del inserto (0,24 a 0,4 mm), como en la pieza real.
- En el programa, algunas coordenadas de esas pasadas no coinciden con las cotas del plano. El informe lo explica en las aclaraciones.

## Cambios en el generador (para piezas más altas)
- **Fin del G90 en modo par:** termina contra las paredes verticales (antes frenaba 0,5 mm antes). La franja que quedaba obligaba a la pasada de contorno de la T0101 a sacar 6,8 mm de una vez, por encima del máximo del rompevirutas RP.
- **Valles:** la T0505 frena a 0,05 mm de la pared.
- **Pasada previa del acabado:** si a la T0303 o a la T0404 les queda más de 2,4 mm (por ejemplo, en el rincón de la corona del rey), primero hacen una pasada paralela.
- **Control de choque del contorno:** se recalcula con los tramos que el contorno recorre de verdad.
- **Corte de arcos en su ápice:** ya no falla cuando el ápice cae en un extremo (la cúpula de la reina).

## Archivos
- `Piezas/tp3_*.json` (solo locales).
- `WinUnisoft/TP3 REY/`, `TP3 ALFIL/` y `TP3 REINA/`.
