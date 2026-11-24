---
tipo: tp
pieza: Alfil
tags: [tp, alfil, torno]
---

# TP Alfil

Segundo trabajo práctico: un alfil de ajedrez. Es más fino que el [[TP Peón]]: la cabeza llega a Ø4.

## Datos

| Dato | Valor |
|---|---|
| Material | SAE 4140 (rótulo) |
| Bruto | Ø42 x 130 mm |
| Largo de la pieza | 93 mm |
| Control | Fanuc 16iTA |
| Cero pieza | G54 con Z = 129 (en la punta) |
| Catálogo | Kennametal Universal |
| Fecha del plano | 12/12/25 |
| Fecha de presentación | 16/12/2025 |

> [!warning] Texto heredado
> La ficha "Características pieza" del informe dice nombre PEON y material "Acero Inoxidable (M)". Parece texto heredado del TP Peón. Ver [[Bitácora]].

## Dimensiones

- Diámetros: Ø4, Ø5, Ø7, Ø10 (cabeza), Ø14, Ø20 y Ø30 (base). El programa usa además Ø25 y Ø40 (toro).
- Radios: R3 (bola de la cabeza), R1 (collarín), R2,5 (dos anillos) y R5 (toro grande de la base).
- Cotas longitudinales desde la punta: 5, 6, 8, 13, 18, 29, 39, 49, 54, 58, 63, 73, 83, 93.
- Largo total 93 mm. No hay ranuras ni chaflanes cotados.

Perfil por tramos, de la punta a la base: bola R3; collarín R1 (Ø6 en Z-7); cuello Ø4,5 a Ø5; anillo R2,5 (Ø10, de Z-15,5 a Z-29); cono Ø10 a Ø7 (Z-29 a Z-39); cono Ø7 a Ø14 (Z-39 a Z-49); cilindro Ø14 (Z-49 a Z-54); cono Ø14 a Ø20 (Z-54 a Z-58); anillo R2,5 con Ø25 (Z-58 a Z-68); cono Ø25 a Ø30 (Z-68 a Z-73); toro R5 hasta Ø40 (Z-73 a Z-78); base Ø30 hasta Z-93.

## Hoja de proceso

| Op | Operación | Ciclo | Herramienta | Vc | Avance | Inserto | Portaherramienta |
|---|---|---|---|---|---|---|---|
| 1 | Desbaste exterior | G90 | T0101 | 180 | 0,3 | CNMG120408RP | DCLN R/L 2020K12KC04 |
| 2 | Diagonales y radios brutos | G01-G03 | T0303 | 180 | 0,2 | VNMG160404FP | DVJN R/L 2020K16KC04 |
| 3 | Ranurado | G94 | T1111 | 105 | 0,19 | A4G0605M06U08GMP | A4SM R/L 3225P0626 |
| 4 | Radios y diagonales, lado derecho | G01-G03 | T0909 | 180 | 0,2 | VBMT110304LF | SVJB R/L 1212N11 (3) |
| 5 | Radios y diagonales, lado izquierdo | G01-G02 | T1010 | 180 | 0,2 | VBMT110304LF | SVJB R/L 1212N11 (4) |
| 6 | Tronzado | G01 | T1111 | 105 | 0,19 | A4G0605M06U08GMP | A4SM R/L 3225P0626 |

Vc en m/min y avance en mm/vuelta. Todas las operaciones usan G96 (S180 o S105).

## Regla de la posición de tronzado
**Z = -(largo + 6)**. Con largo 93: Z = -99. El programa tronza en `X50 Z-99`.

## Programa

```
%
O2222
G54
T0101
G96 S180 M3
G00 X50 Z5
G90 X41 Z-99 F.3
G00 X45
G90 X39 Z-72
X37
X35
X33
X31
G00 X35
G90 X29 Z-66
X27
X26
G00 X30
G90 X24 Z-57.5
X22
G00 X27
G90 X20 Z-55.5
X18
G00 X25
G90 X16 Z-53
X15
G00 X20
G90 X13 Z-43
X11
G00 X15
G90 X7 Z-13
G00 X15
G00 Z-42
G01 Z-52
G01 X22 Z-58
G01 X27 Z-60
G01 Z-65
G01 X30 Z-73
G01 X35.5
G01 X42 Z-78
G01 Z-93
G01 X45
G00 X100 Z100
T0303
G96 S180 M3
G00 X3 Z5
G01 Z0 F.2
G01 X7 Z-3
G01 X5 Z-5
G01 Z-6
G01 X7 Z-7
G01 Z-12
G01 X6
G01 X11 Z-12
G01 Z-20
G01 X7
G01 X12 Z-29
G01 X9 Z-39
G01 X16 Z-49
G01 X30
G00 Z-65
G01 Z-67
G01 X26
G01 X31 Z-73
G01 X45
G00 X100 Z100
T1111
G96 S105 M3
G00 X45 Z-89
G94 X30 Z-95 F.19
Z-99
G01 X35.5
G01 X42 Z-84
G01 X45
G00 X100 Z100
T0909
G96 S180 M3
G00 X0 Z5
G01 Z0 F.2
G03 X4 Z-5 R3
G01 Z-6
G03 X6 Z-7 R1
G01 Z-10.5
G01 X4.5
G01 X5 Z-13
G03 X10 Z-15.5 R2.5
G01 Z-29
G01 X7 Z-39
G01 X14 Z-49
G01 Z-54
G01 X20 Z-58
G03 X25 Z-60.5 R2.5
G01 Z-68
G01 X30 Z-73
G03 X40 Z-78 R5
G01 X45
G00 X100 Z100
T1010
G96 S180 M3
G00 X45 Z-83
G01 X30 F.2
G02 X40 Z-78 R5
G01 Z-68
G01 X25
G01 X20 Z-63
G02 X25 Z-60.5 R2.5
G01 Z-60
G00 Z-29
G01 X10
G01 X5 Z-18
G02 X10 Z-15.5 R2.5
G01 Z-10.5
G01 X4.5
G01 X4 Z-8
G02 X6 Z-7 R1
G01 X10
G00 X100 Z100
T1111
G00 X50 Z-99
G01 X0 F.19
G01 X50
G00 X100 Z100
M30
%
```

Notas del programa:
- El desbaste con G90 cambia el Z final en cada tramo (Z-99, -72, -66, -57.5, -55.5, -53, -43, -13) para ir bajando de a escalones.
- T1111 se usa dos veces: primero para el ranurado de desahogo (G94 hasta Z-99) y al final para tronzar.
- El perfil bruto llega a Z-93 y el tronzado corta en Z-99: serían los 6 mm del inserto (interpretación, la fuente no lo aclara).

## Informe
Se armó con la estructura de [[01 Método de trabajo]] (carátula, rótulo, hoja de proceso, programa, aclaraciones sobre el código de forma, características de la pieza y una hoja por herramienta).

Ver también: [[Ciclos G90 G94 G71 G72 G70 G74]], [[Herramientas y plaquitas]], [[Rótulo EEST3]], [[Formato de archivos WinUnisoft]].
