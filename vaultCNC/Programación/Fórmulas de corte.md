---
tipo: referencia
tags: [programacion, formulas, corte]
---

# Fórmulas de corte

## Fórmulas

| Qué calculás | Fórmula |
|---|---|
| Velocidad de corte | Vc (m/min) = π · Ø · n / 1000 |
| RPM | n = Vc · 1000 / (π · Ø) |
| Avance por minuto | F (mm/min) = n · F (mm/vuelta) |
| Tiempo de mecanizado | T (min) = Lm / (F · n) |

Ejemplos de la carpeta:
- 250 RPM x 0,25 mm/vuelta = 62,5 mm/min.
- T = 80 / (0,25 · 250) = 1,28 min.
- Con Vc = 120: Ø40 da unas 955 RPM, Ø30 unas 1273, Ø20 unas 1910 y Ø10 unas 3820. En Ø0 las RPM serían infinitas: por eso se usa el límite `G50 S4500`.

Ejemplo propio con Vc = 180 y bruto Ø42: n = 180 · 1000 / (π · 42) = unas 1364 RPM. A Ø14 sube a unas 4090 RPM, cerca del máximo de 4000 del simulador (ver [[Torno y control]]).

## Por qué G96
Con [[Códigos G|G96]] la máquina calcula las RPM sola para mantener la Vc cuando cambia el diámetro. Cerca del centro las RPM tienden a subir sin límite, y entonces se pone G50.

## Valores usados en los TP (grupo ISO M, catálogo Kennametal)

| Operación | Herramienta | Vc (m/min) | Avance (mm/vuelta) |
|---|---|---|---|
| Desbaste exterior | T0101 | 180 | 0,3 |
| Terminación | T0303 | 180 | 0,2 |
| Ranurado (3 mm) | T0505 | 105 | 0,1 |
| Terminación ultrafina | T0909 y T1010 | 180 | 0,2 |
| Tronzado (6 mm) | T1111 | 105 | 0,19 |

- Velocidad de torneado (pág. A5, grupo M): promedio 180 m/min, rango 100-250 m/min (KU10T 600 sfm; KU30T 450 sfm = 140 m/min).
- Velocidad de ranurado (pág. A71, grupo M): promedio 105 m/min, rango 70-150 m/min.

## Valores de ejercicios (SAE 4140)
- Desbaste exterior: Vc 180, avance 0,22 (G71 con F.24, G72 con F.25).
- Terminación: Vc 250, avance 0,16.
- Ranurado y tronzado: Vc 120 a 150, avance 0,12 a 0,15.
- Desbaste y ranurado interior: Vc 140, avance 0,2.
- Taladrado: `G97 S4246` y avance 0,2.
- Profundidades: `G71 U2 R2`, `G72 W2 R2`, pasadas de 2 a 3 mm por lado en G90/G94, sobrematerial `U1 W1`.

## Catálogo Kennametal: velocidades iniciales (pág. A5)

| Grupo ISO | Material | Vc aprox. (m/min) |
|---|---|---|
| P | Acero al carbono y aleado | 200 (KU10T) y 150 (KU30T) |
| M | Inoxidable austenítico | 180 y 140 |
| K | Fundición | 240 y 200 |
| N | Aluminio bajo silicio | 460 |
| S | Alta temperatura | 65 y 45 |
| H | Endurecidos (más de 48 HRC) | 60 |

> [!warning] Material de las piezas
> Los rótulos dicen **SAE 4140** (acero aleado, grupo **P**), pero las velocidades de los TP se tomaron del grupo **M** (inoxidable). La tabla del catálogo salió con el texto desordenado, así que la asignación de grado y valor es dudosa. Ver [[Bitácora]].

El catálogo da condiciones **iniciales** que hay que ajustar. Recomienda usar el 60 % central del rango de avance.

Ver también: [[Herramientas y plaquitas]], [[01 Método de trabajo]].
