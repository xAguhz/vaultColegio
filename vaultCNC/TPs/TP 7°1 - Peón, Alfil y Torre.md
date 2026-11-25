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
Herramientas elegidas para estas piezas (SAE 4140, grupo P), con datos del catálogo Kennametal Universal:

| Herramienta | Portaherramienta + inserto | Uso | Vc |
|---|---|---|---|
| T0101 | DCLN 2020K12KC04 + CNMG120408RP (KU30T) | Desbaste G90, pasadas de 2 mm en diámetro | 150 m/min |
| T0303 | DVJN 2020K16KC04 + VNMG160404FP (KU10T) | Semiterminación del contorno | 200 m/min |
| T0909 | **DVVNN 2020K16KC04** (neutra, 72,5°, código de forma 8) + VNMG160404FP | Acabado de todo el perfil, en los dos sentidos | 200 m/min |
| T0505 | A4SM 2016K0317 + **A4G0305M03U02GMN** (KU30T, 3 mm) | Ranurado de gargantas y tronzado en Z = −(largo + 3) | 120 m/min |

Por qué se cambió respecto de los TP anteriores:
- La herramienta neutra reemplaza a la pareja T0909/T1010 (mano derecha e izquierda) y tiene más despeje en cuellos y gargantas.
- GMN es la geometría para acero; GMP es para inoxidable (página A70).
- La cuchilla de 3 mm alcanza para piezas de Ø26 y desperdicia menos material que la de 6 mm.

Validación con `simular_nc.py`: **0 errores** en los tres programas. Los rápidos diagonales que pasaban cerca de la pieza ahora salen primero a Z5 y después bajan en X.

> [!warning] Verificar en WinUnisoft
> La línea de la T9 en el `.prj` (portaherramienta neutro) se escribió por analogía con las otras herramientas: `Orient.` 72,5, `_Orient.` 107,5, `Quadrant` 1 y `_CodForma` 8. Al abrir el proyecto, mirá que la plaquita se dibuje apuntando hacia −X y que no choque en las gargantas.

## Archivos
- Proyectos WinUnisoft: `WinUnisoft/TP71 PEON/`, `TP71 ALFIL/` y `TP71 TORRE/`.
- Planos (PDF y FCStd) e informes (.docx): quedan solo en la compu porque llevan los nombres del rótulo.
