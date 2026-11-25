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

> [!note] Tabla de herramientas del `.prj`
> El generador la escribe directo en el `.prj`; en la pantalla de WinUnisoft no se edita nada.
> - T1: radio de punta 0,8 (CNMG120408). T3: radio 0,4 (VNMG160404). La plantilla traía 0,2 en las dos.
> - T5: cuchilla de 3 mm (GMN). T9: neutra DVVNN, `Orient.` y `_Orient.` 72,5, `_CodForma` 8, radio 0,4.
> - Los programas no usan compensación de radio (G41/G42): el radio solo cambia cómo se dibuja la plaquita y cuánto material deja en los rincones.
> - T2, T4, T6, T7, T8, T10 y T11 vienen de la plantilla y no se usan.

## Archivos
- Proyectos WinUnisoft: `WinUnisoft/TP71 PEON/`, `TP71 ALFIL/` y `TP71 TORRE/`.
- Planos (PDF y FCStd) e informes (.docx): quedan solo en la compu porque llevan los nombres del rótulo.
