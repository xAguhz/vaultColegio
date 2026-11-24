---
tags: [cnc, tp, ajedrez]
fecha: 2026-11-24
---
# TP 7°1: Peón, Alfil y Torre

Tres TP separados (láminas 1, 2 y 3) hechos con el flujo de [[00 Inicio]]: **JSON de la pieza → plano en FreeCAD → proyecto WinUnisoft → validación → informe**.

## Datos de partida
El alumno pasó un dibujo con medidas aproximadas:

| Pieza | Alto | Ø base | Radio cotado |
|---|---|---|---|
| Peón | 32 mm | Ø22 (máx.) | R6 (cabeza) |
| Alfil | 36 mm hasta la base del botón (39 con el botón) | Ø26 | R6 (mitra) |
| Torre | 38 mm | Ø26 | R4 (esquina de la corona) |

El resto de las medidas (cuello, collarín, corona, curva del cuerpo) se **midió sobre la imagen**, con una escala por eje porque el dibujo no está en proporción, y se redondeó a 0,5 mm.

## Supuestos (a confirmar)
- **Bruto SAE 4140 Ø30 × 130.** Las piezas miden Ø26 como máximo, así que con Ø30 hay menos pasadas de desbaste que con el Ø42 de los TP anteriores.
- **R4 de la torre** = redondeo de la esquina superior de la corona (Ø20). Las almenas no se pueden hacer en el torno.
- **Botón del alfil**: bola R2 arriba de la mitra.
- Las curvas cóncavas del cuerpo se hicieron con un solo arco: R20 (peón), R25 (alfil) y R40 (torre).

## Programas
Los tres siguen el estilo de los TP aprobados (ver [[TP Peón]] y [[TP Alfil]]):

| Herramienta | Uso |
|---|---|
| T0101 | Desbaste con G90, pasadas de 2 mm en diámetro |
| T0303 | Semiterminación del contorno |
| T0505 | Ranurado de las gargantas |
| T0909 | Terminación de los tramos que crecen hacia la base |
| T1010 | Terminación de los tramos que bajan hacia la base |
| T1111 | Tronzado en Z = −(largo + 6) |

Validación con `simular_nc.py`: **0 errores** en los tres.
- Peón: 5 avisos.
- Alfil: 6 avisos.
- Torre: 3 avisos.

Todos los avisos son del tipo "G00 baja X con Z<0", el mismo aviso que dan los programas originales.

> [!warning] Revisar en WinUnisoft
> En el alfil, el generador marca un posible choque del portaherramientas T1010 cerca de Z−19, debajo del collarín. Mirá esa pasada en la simulación.

## Archivos
- Proyectos WinUnisoft: `WinUnisoft/TP71 PEON/`, `TP71 ALFIL/` y `TP71 TORRE/`.
- Planos (PDF y FCStd) e informes (.docx): quedan solo en la compu porque llevan los nombres del rótulo.
