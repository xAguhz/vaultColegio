---
tipo: concepto
area: neumática
tags: [neumática, electroneumática, análisis]
---

# Diagrama espacio-fase

Es la herramienta central de **todo** el canal: antes de armar cualquier circuito (neumático, eléctrico o Ladder), el profe analiza este diagrama.

## Qué representa
- **Espacio:** el desplazamiento de cada actuador. Abajo (0) = **retraído**; arriba (1) = **extendido**.
- **Fase:** el movimiento completo, desde que empieza hasta que termina. No mide tiempo. Cada cuadradito es una fase, y la fase es **toda la columna** (todos los actuadores alineados).
- **Puntos numerados (1, 2, 3…)**: el punto *n* es el comienzo de la fase *n* y el fin de la anterior. El último punto marca el fin del ciclo.
- **Ciclo:** el conjunto de todas las fases.

## Cómo se dibuja
| Trazo | Significado |
|---|---|
| Diagonal que sube (pendiente +) | Avance |
| Diagonal que baja (pendiente −) | Retroceso |
| Línea horizontal | El actuador está quieto (arriba = extendido, abajo = retraído) |
| Flecha entre dos puntos con `T1` | Pausa temporizada (ver [[Temporizador neumático]] y [[Relés temporizados]]) |
| `3 ≡ 1` (tres rayitas) | **Ciclo continuo**: termina y vuelve a arrancar (ver [[Ciclo único y ciclo continuo]]) |

Si en una fase hay **dos movimientos**, la fase termina recién cuando terminan los dos.

## Cómo se analiza (el procedimiento del profe)
1. Marcar con una **flecha** dónde aparece el **primer movimiento**. Ahí se anota quién da la señal de arranque: `0S1` en neumática, `K0` (relé de [[Enclavamiento eléctrico]]) en electroneumática, `MA` (memoria de marcha) en PLC.
2. En serie con el arranque se anota la **señal de nuevo arranque**: el último final de carrera que se pisa en el ciclo (por ejemplo `1S1`). Juntos forman una función **AND**.
3. En cada punto donde **termina un movimiento**, anotar el final de carrera que detecta esa posición (los rodillos van siempre donde *termina* el movimiento, nunca donde empieza).
4. Anotar **qué se alimenta** para lograr cada movimiento:
   - neumática: la entrada de la válvula de mando (`14 de 1V1` para avanzar, `12 de 1V1` para retroceder);
   - electroneumática: el cabezal (`1Y1`), o el relé de mando (`K1`) en mando indirecto;
   - monoestable: retroceder = **desconectar** el cabezal (`1Y1` negado).
5. **Flechita cerrada sobre sí misma:** el emisor que se pisa hace volver al **mismo** actuador que lo pisó.
6. Señal **negada** (por ejemplo `0S1` negado) = soltar el pulsador.
7. En métodos avanzados se marca además **desde qué punto hasta qué punto** queda pisado cada rodillo. Así se descubre la [[Superposición de señales]].

> [!tip]
> "Una vez que tengo analizado el diagrama, ya tengo resuelto el circuito": todo lo demás es trasladar la información del diagrama al plano.

## Videos
[[2020-07-14 Mando directo neumático parte 1]] · [[2020-07-14 Mando directo neumático parte 2]] · [[2020-07-13 Circuito neumático de ciclo único]] · [[2020-07-13 Circuito neumático de ciclo continuo]] · [[2020-04-20 Repaso EN 1 - Análisis del diagrama espacio-fase]] · [[2021-05-21 Cascada con lógica cableada y superposición]]
