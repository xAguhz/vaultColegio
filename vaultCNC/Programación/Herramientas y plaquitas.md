---
tipo: referencia
tags: [herramientas, plaquitas, kennametal]
---

# Herramientas y plaquitas

Catálogo usado: **Kennametal Universal** (catálogo general 5090, sistema métrico y pulgadas). Las herramientas están cargadas en la torreta de los proyectos de [[Formato de archivos WinUnisoft|WinUnisoft]].

## Herramientas de los TP

| T | Operación | Portaherramienta (pág.) | Inserto (pág.) | Vc (m/min) | Avance (mm/vuelta) | Prof. máx. (mm) |
|---|---|---|---|---|---|---|
| T0101 | Desbaste exterior | DCLN R/L 2020K12KC04 (A22) | CNMG432RP o CNMG120408RP (A10) | 180 | 0,3 (rango 0,2-0,6) | 6,4 |
| T0303 | Terminación | DVJN R/L 2020K16KC04 (A27) | VNMG160404FP (A14) | 180 | 0,2 (rango 0,1-0,3) | 2,5 |
| T0505 | Ranurado 3 mm | A4SM R/L 2016K0317 (A75), forma 3 | A4G0305M03U02GMP (A73) | 105 | 0,1 | 17 |
| T0909 | Terminación ultrafina derecha | SVJB R/L 1212N11 (3) (A36) | VBMT110304LF (A19) | 180 | 0,2 (rango 0,2-0,4) | 2,3 a 2,5 |
| T1010 | Terminación ultrafina izquierda | SVJB R/L 1212N11 (4) | VBMT110304LF | 180 | 0,2 | sin dato |
| T1111 | Ranurado y tronzado 6 mm | A4SM R/L 3225P0626 (A75) | A4G0605M06U08GMP (A73) | 105 | 0,19 | 26 |

Notas:
- CNMG432RP (nombre ANSI) y CNMG120408RP (nombre ISO) son el mismo inserto con dos nombres. Las hojas usan los dos.
- Los avances de T0505 y T1111 salen de la pág. A70 (tamaño 3 da 0,1; tamaño 6 da 0,19).
- Radio de punta (según el simulador): T0101 0,2; T0303 0,2; T0505 0; T0909 0; T1111 0.
- La hoja de proceso del Peón y del Alfil no tiene tiempos por operación.

## Torreta completa de los proyectos WinUnisoft

| T | Descripción en el `.prj` | Uso |
|---|---|---|
| T0 | Sin correctores | vacía |
| T1 | DCLN R/L 2020K12KC04 | desbaste exterior |
| T2 | SCLCL desbastar interiores | no se usa en los TP |
| T3 | DVJN R/L 2020K16KC04 | terminación |
| T4 | SDUCL acabar interiores | no se usa en los TP |
| T5 | A4SM R/L 2016K0317 (3) | ranurado 3 mm |
| T6 | STIL ranurado interiores | no se usa en los TP |
| T7 | NLL roscar exteriores | no se usa en los TP |
| T8 | NVRL roscado interiores | no se usa en los TP |
| T9 | SVJB R/L 1212N11 (3) | terminación derecha |
| T10 | SVJB R/L 1212N11 (4) | terminación izquierda |
| T11 | A4SM R/L 3225P0626 | tronzado |

En el programa, `T0505` significa torreta 05 con corrector 05. La posición de la torreta coincide con el número T de esta tabla.

> [!note] T11 en el Peón y en el Alfil
> En el `.prj` del Peón, T11 tiene cuadrante 2 y código de forma 4. En el del Alfil, T11 tiene cuadrante 1 y código de forma 3. Es la única diferencia entre las herramientas de los dos proyectos (el T5 del Alfil además lleva "(3)" en el nombre).

## Código de forma (3 o 4)
Es un número del portaherramienta que dice **cómo está orientada la herramienta** respecto de la pieza. Si no se indica, vale **3**. Ejemplos: T0909 (3) y T1010 (4). La carpeta da estos códigos: exterior 4, 8 y 3; interior 5, 1, 6 y 2; broca 7. En los proyectos, los interiores usan 2.

## Formas de inserto (primera letra)
C = rómbica 80°, D = rómbica 55°, R = redonda, S = cuadrada, T = triangular, V = rómbica 35°, W = trigonal.

## Nomenclatura de portaherramientas
- SCLC (insertos CC..) y SDJC (insertos DC..) aparecen en la carpeta digital como desbaste y terminación.
- La carpeta cita al catálogo Mitsubishi (pág. C006, A002-A003) y Corokey 2007 para la nomenclatura. Los datos están en imágenes.

## Calidades y geometrías
- KU10T: medio a fino; KU25T: roscado y tronzado; KU30T: desbaste y medio.
- Geometrías: -RN, -MN (desbaste); -MP, -RP (medio); -MF, -UF, -LF (acabado fino).

Ver también: [[Fórmulas de corte]], [[01 Método de trabajo]], [[TP Peón]], [[TP Alfil]].
