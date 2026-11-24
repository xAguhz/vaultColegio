---
tipo: tp
pieza: Peón
tags: [tp, peon, torno]
---

# TP Peón

Primer trabajo práctico de torno CNC: una pieza de ajedrez (el peón) torneada de una barra. Curso 6° 1° Electromecánica, EEST N°3.

## Datos

| Dato | Valor |
|---|---|
| Material | SAE 4140 (rótulo) |
| Bruto | Ø42 x 130 mm |
| Agarre | 30 mm |
| Largo de la pieza | 74 mm |
| Control | Fanuc 16iTA |
| Cero pieza | G54 con Z = 129 (en la punta de la pieza) |
| Catálogo | Kennametal Universal |
| Fecha del plano | 4/12/25 |
| Fecha de presentación | 16/12/2025 |

> [!warning] Contradicción de material
> El rótulo dice SAE 4140, pero la hoja de proceso dice "Acero Inoxidable (M)" y las velocidades salen del grupo M. Ver [[Bitácora]].

## Dimensiones del perfil (de la punta a la base)

| Tramo | Z | Diámetro |
|---|---|---|
| Bola de la punta, R10 (G03) | 0 a -17 | Ø0 a Ø14 |
| Cono | -17 a -22 | Ø14 a Ø22 |
| Cuello | -27 a -32 | Ø14 |
| Cono | -32 a -34,5 | Ø14 a Ø22 |
| Cilindro | -34,5 a -42 | Ø22 |
| Cono y arco R2 | -42 a -47 | Ø14, Ø20, Ø24 |
| Cilindro | -47 a -50 | Ø24 |
| Cono | -50 a -54 | Ø22 a Ø30 |
| Collar, arco R5 | -54 a -59 | Ø30 a Ø40 |
| Cilindro (collar) | -59 a -64 | Ø40 |
| Espiga (base) | -64 a -74 | Ø30 |

Diámetros del plano: Ø40, Ø30, Ø22, Ø20, Ø14. Radios: R10, R5, R2. El plano no tiene tolerancias ni chaflanes cotados.

## Hoja de proceso

Todas las operaciones usan G96 y M3. No figuran tiempos.

| Op | Operación | Ciclo | Herramienta | Portaherramienta | Inserto | Vc | Avance |
|---|---|---|---|---|---|---|---|
| 1 | Desbaste exterior | G90-G01 | T0101 | DCLN R/L 2020K12KC04 | CNMG120408RP | 180 | 0,3 |
| 2 | Terminación | G01-G03 | T0303 | DVJN R/L 2020K16KC04 | VNMG160404FP | 180 | 0,2 |
| 3 | Ranurado | G94 | T0505 | A4SM R/L 2016K0317 | A4G0305M03U02GMP | 105 | 0,1 |
| 4 | Terminación ultrafina derecha | G01-G03 | T0909 | SVJB R/L 1212N11 (3) | VBMT110304LF | 180 | 0,2 |
| 5 | Terminación ultrafina izquierda | G01-G02 | T1010 | SVJB R/L 1212N11 (4) | VBMT110304LF | 180 | 0,2 |
| 6 | Tronzado | G01 | T1111 | A4SM R/L 3225P0626 | A4G0605M06U08GMP | 105 | 0,19 |

Vc en m/min y avance en mm/vuelta. Detalle de cada herramienta en [[Herramientas y plaquitas]].

## Regla de la posición de tronzado
El tronzado corta en **Z = -(largo + 6)**. Con largo 74: Z = -80. Interpretación: los 6 mm de más serían el ancho del inserto de tronzar (T1111, 6 mm), para que el corte deje la pieza completa de 74 mm.

## Programa

```
%
O2222
G54
T0101
G96 S180 M3
G00 X50 Z5
G90 X41 Z-80 F.3
G00 X45
G90 X39 Z-54
X37
X35
X33
X31
G00 X35
G90 X29 Z-51
X27
X25
G00 X23
G01 Z-45
G01 X40
G00 Z5
G00 X0
G01 Z0.5
G01 X9
G01 Z0
G01 X20 Z-5
G01 Z-17
G01 X19
G01 X22 Z-22
G01 X25
G00 Z-48
G01 Z-50.5
G01 X31 Z-54
G03 X41 Z-59 R5
G01 Z-64
G01 X45
G00 X100 Z100
T0303
G96 S180 M3
G00 X25 Z-10
G01 X16 Z-17 F.2
G01 X22 Z-22
G01 Z-23
G01 X17 Z-27
G01 X25
G00 Z-32
G01 X17
G01 X22 Z-34.5
G01 Z-37
G01 X17
G01 X25
G00 Z-42
G01 X16
G01 X21 Z-45
G01 X45
G00 Z5
G00 X1
G01 Z0
G03 X15 Z-17 R10
G01 X22 Z-21
G01 X30
G00 X100 Z100
T0505
G96 S105 M3
G00 X30 Z-30
G01 X14 F.1
G01 X30
G00 Z-32
G01 X14
G01 X30
G00 Z-40
G01 X14
G01 X30
G00 Z-42
G01 X14
G01 X45
G00 Z-67
G94 X30 Z-69
Z-71
Z-73
Z-75
Z-77
Z-79
Z-80
G01 X34
G01 X40 Z-65
G01 X50
G00 X100 Z100
T0909
G96 S180 M3
G00 X0 Z5
G01 Z0 F.2
G03 X14 Z-17 R10
G01 X22 Z-22
G01 X14 Z-27
G01 Z-32
G01 X22 Z-34.5
G01 Z-42
G01 X14
G01 X20 Z-45
G03 X24 Z-47 R2
G01 Z-50
G01 X22
G01 X30 Z-54
G03 X40 Z-59 R5
G01 Z-64
G01 X45
G00 X100 Z100
T1010
G96 S180 M3
G00 X45 Z-64
G01 X30 F.2
G02 X40 Z-59 R5
G01 Z-50
G01 X22
G01 X20 Z-49
G02 X24 Z-47 R2
G01 Z-37
G01 X14
G01 X22 Z-34.5
G01 X30
G00 X100 Z100
T1111
G96 S105 M3
G00 X50 Z-80
G01 X-1 F.19
G01 X50
G00 X100 Z100
M30
%
```

Notas del programa:
- Desbaste con G90 de X41 a X25 por pasadas, y después el perfil en G01.
- T0505 ranura en Z-30, -32, -40 y -42 hasta X14, y frentea con G94 de Z-69 a Z-80.
- T1111 tronza en `Z-80` hasta `X-1`.

Ver también: [[TP Alfil]], [[Ciclos G90 G94 G71 G72 G70 G74]], [[Estructura de un programa]], [[Rótulo EEST3]], [[Formato de archivos WinUnisoft]].
