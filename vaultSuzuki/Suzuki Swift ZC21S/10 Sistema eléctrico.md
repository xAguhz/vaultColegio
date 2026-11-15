---
tags: [suzuki-swift, electrico, fusibles]
tipo: nota
actualizado: 2026-11-14
---
# 10 · Sistema eléctrico

Volver a [[00 Suzuki Swift ZC21S]]

## Carga y arranque
| Componente | Dato |
| ---------- | ---- |
| Batería | **46B24R** (norma japonesa: 46 = capacidad relativa, B = tamaño de la base, 24 = largo en cm, R = borne positivo a la derecha), **36 Ah**, 12 V |
| Alternador | 70 A · regula 14,2–14,8 V (alto) o 12,5–13,1 V (bajo); la computadora elige |
| Escobillas del alternador | 10,5 mm nuevas · límite 1,5 mm |
| Motor de arranque | 1,2 kW |

**Prueba rápida con un tester:**
- Motor apagado: la batería debe marcar **12,4–12,7 V**. Menos de 12,2 V = descargada.
- Motor en marcha: entre **13,5 y 14,8 V** en los bornes. Si sigue en 12 V, el alternador no carga (se prende el testigo de carga).

> [!warning] Al desconectar la batería
> Sacar **primero el negativo (−)** y conectarlo **último**. Si se trabaja cerca de los airbags, esperar al menos 90 segundos después de desconectarla (ver [[12 Seguridad, airbags y carrocería]]).

## Cajas de fusibles
Hay dos: la **del vano motor** (junto a la batería, con los fusibles grandes y los relés) y la **caja de empalmes** de la cabina (debajo del tablero, lado del conductor).

### Vano motor (algunos)
| Fusible | Amperaje | Qué protege |
| ------- | -------- | ----------- |
| FI | 15 A | Relé principal (inyección) |
| HTR FAN | 30 A | Ventilador de la calefacción |
| A/C CPRSR | 10 A | Compresor del aire acondicionado |
| AT ETM | 15 A | Relé de la caja automática (no se usa en este auto manual) |
| STOP LAMP | 15 A | Luces de freno |
| ABS MOT / ABS SOL | 30 A / 30 A | Módulo del ABS |
| ST MOT | 30 A | Relé del motor de arranque |
| EPS | 50 A | Dirección eléctrica |
| IG ACC | 30 A | Llave de contacto |
| RDTR FAN | 30 A | Electroventilador del radiador |
| FR FOG | 15 A | Faros antiniebla |
| H/L L · H/L R | 15 A cada uno | Faro izquierdo · faro derecho |

### Cabina (algunos)
| Fusible | Amperaje | Qué protege |
| ------- | -------- | ----------- |
| IG COIL | 15 A | Computadora, bomba de nafta, bobinas, alternador, sondas |
| DOME | — | Luz de techo y memoria de la computadora |

> [!tip] Regla de oro
> Un fusible se cambia **siempre por otro del mismo amperaje**. Si se vuelve a quemar enseguida, hay un cortocircuito: poner uno más grande puede quemar el cableado.

## Iluminación
- Faros delanteros con luz alta y baja, posición y giro; cada faro con su fusible.
- Calaveras traseras verticales con posición, freno, giro y marcha atrás.
- La regulación de los faros se hace con tornillos de altura y de lado, con el auto descargado, contra una pared.

Ver también [[11 Diagnóstico de fallas]] · [[04 Mandos e instrumentos]]
