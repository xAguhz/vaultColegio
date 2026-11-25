---
tags: [cnc, tp, ajedrez]
fecha: 2026-11-25
---
# TP 7°1 (2): Peón, Alfil y Torre con herramientas en par

Segundo TP de piezas de ajedrez. El alumno pasó dos croquis sin medidas: un peón y un alfil. La torre la inventó la IA, con el mismo estilo de líneas rectas. El flujo es el mismo de [[00 Inicio]]: **JSON → plano en FreeCAD → proyecto WinUnisoft → simulación → informe**. La diferencia está en que las herramientas se usan en los dos sentidos.

## Medidas (corregidas y simétricas)
El croquis no es simétrico respecto del eje. Para cada diámetro se promediaron la mitad de arriba y la de abajo. Se tomó **Ø26** para la base y se escaló el resto con esa proporción, redondeando a 0,5 mm.

| Pieza | Largo | Perfil (de la punta a la base) |
|---|---|---|
| Peón | 36 | bola R4,5 → cono a collarín Ø14 (Z−14,5) → pared de atrás a cuello Ø8,5 (Z−16) → cuello hasta Z−21,5 → cono a Ø26 (Z−29,5) → base |
| Alfil | 47 | punta cónica hasta Ø9 (Z−5,5) → vástago Ø9 → collarín Ø16 en Z−22 → baja a Ø9 (Z−28,5) → cono a Ø26 (Z−41) → base |
| Torre | 38 | cara plana Ø18, chaflán a Ø20 → ranura de 4 mm a Ø16 (Z−2,5 a −6,5) → corona hasta Z−9 → pared de abajo a Ø12 (Z−10,5) → cuerpo Ø12 → cono a Ø26 (Z−32) → base |

> [!warning] Cambio respecto del croquis del alfil
> En el croquis, la punta del collarín del alfil se adelanta hacia la cabeza y queda colgando sobre el vástago: es una **pared socavada** (30° pasada la vertical). Ninguna herramienta exterior del catálogo llega ahí. Para tornearla haría falta un ángulo de posición de unos 120° más el despeje, y el portaherramientas más abierto (DVON) llega a 117,5°. Por eso la cara de adelante del collarín se hizo **radial** (vertical).

## Herramientas (catálogo Kennametal, grupo P)
| T | Portaherramienta | Inserto | Vc | Uso |
|---|---|---|---|---|
| T0101 | DCLN R 2020K12KC04 (A22) | CNMG120408RP KU30T (A10) | 150 | Refrentado, G90 y pasada de contorno |
| T0505 | **A4SM R 2020K0317** (A75), mango 20×20 | A4G0305M03U02GMN KU30T (A73) | 120 | Ranura a medida, valles con G90 en los dos sentidos y tronzado |
| T0303 | DVJN R 2020K16KC04 (A27) | VNMG160404FP KU10T (A14) | 200 | Acabado del perfil cortando hacia −Z |
| T0404 | **DVJN L** 2020K16KC04: la misma herramienta, invertida | VNMG160404FP | 200 | Acabado de las paredes que bajan de diámetro hacia la base, cortando hacia +Z |

- **Herramienta invertida en WinUnisoft:** igual que T0909/T1010 en los TP originales, la línea de la T4 es una copia de la T3 con `Quadrant=2` y código de forma 4.
- **Por qué no hay T0202 (DCLN L):** los valles quedan entre dos paredes, y desde la base no se puede entrar a desbastar.
- **Por qué no hay T0606:** el inserto A4 ranura y tornea en los dos sentidos, así que la misma T0505 hace el G90 hacia −Z y hacia +Z.

## Programa optimizado
Solo con los códigos de los TP originales: G00, G01, G02, G03, G90, G96 y M3/M30. No se usan G71 ni G72.
- **T0101:**
  - **Primera pasada de G90:** Ø27,2. Deja 0,6 mm por lado sobre la base.
  - **Pasadas siguientes:** bajan **6 mm en diámetro** (3 mm por lado), con F0,4. El rompevirutas RP admite de 1,1 a 6,4 mm de profundidad y avances de 0,2 a 0,6.
  - **Contorno:** después la T0101 copia el perfil y deja 0,3 mm por lado. Se omiten los tramos donde su filo secundario (5°) tocaría material.
- **T0505:**
  - Las ranuras rectas se hacen a medida: entra una vez y corre por el fondo.
  - En cada valle, entra en el punto **más hondo** y desde ahí hace G90 de 3,2 mm en diámetro **hacia −Z y hacia +Z**.
- **T0303 y T0404:** sacan los 0,3 mm finales. La T0404 también termina el tramo de cuello pegado a la pared, adonde el porta de la T0303 no entra.
- **Control de profundidad:** el generador mide el espesor que corta cada herramienta, perpendicular a la pasada.

| Pieza | Profundidad máxima medida | Tiempo en WinUnisoft |
|---|---|---|
| Peón | T0101 3,0 · T0303 1,8 · T0404 1,0 mm | **10:53** (el TP anterior: 25:35) |
| Alfil | T0101 5,8 (rincón del collarín) · T0303 1,7 mm | **10:18** (antes: 29:32) |
| Torre | T0101 2,8 · T0303 1,5 · T0404 1,0 mm | **10:50** (antes: 18:23) |

Los tres se simularon en WinUnisoft, en la pantalla oculta: **sin colisiones ni errores**, y la forma final coincide con el plano.

## Archivos
- **Piezas:** `Piezas/tp2_*.json`, con `"estrategia": "par"`. Quedan solo locales porque llevan el rótulo.
- **Proyectos WinUnisoft:** `WinUnisoft/TP2 PEON/`, `TP2 ALFIL/` y `TP2 TORRE/`.
- **Generador:** `generar_winunisoft.py`, función `generar_par`. Planos e informes: los mismos scripts; el informe detecta el modo par.
- **Captura del catálogo:** `T0505_2020_GMN.png` es la misma página A75, con la fila 2020K0317 resaltada.
- **Imágenes de WinUnisoft para el informe**, como en el TP original:
  - `esquemas_wus.py` tilda "Cambio Hta.", simula y captura la pieza en cada pausa (`op1.png`…). Esas imágenes van en la columna "Esquema de proceso".
  - Las fichas de cada herramienta se capturan desde Gestor → Herramientas. Van en una página por herramienta (`--fichas`).
