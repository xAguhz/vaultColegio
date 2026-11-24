---
tipo: referencia
tags: [programacion, codigos-g]
---

# Códigos G

Los G definen **cómo se mueve** la máquina o en qué **modo** trabaja. Los de esta tabla son los que aparecen en la carpeta digital y en los TP.

| Código | Significado | Formato / ejemplo |
|---|---|---|
| **G00** | Movimiento rápido (posicionamiento, no corta) | `G00 X50 Z5` |
| **G01** | Interpolación lineal (corta) | `G01 Z-10 F.2` · `G01 X25 F.2` · `G01 X25 Z-10 F.2` |
| **G02** | Arco horario | `G02 X40 Z-6 R6` |
| **G03** | Arco antihorario | `G03 X28 Z-6 R6` |
| **G10** | Cero pieza | `G10 P0 Z-149` |
| **G50** | Límite de velocidad (RPM máximas) | `G50 S4500` |
| **G54** | Sistema de coordenadas de trabajo | `G54` |
| **G70** | Ciclo de terminación | `G70 P10 Q20` |
| **G71** | Desbaste longitudinal | ver [[Ciclos G90 G94 G71 G72 G70 G74]] |
| **G72** | Desbaste frontal | ver [[Ciclos G90 G94 G71 G72 G70 G74]] |
| **G74** | Ciclo de perforado | ver [[Ciclos G90 G94 G71 G72 G70 G74]] |
| **G90** | Ciclo fijo de cilindrado (horizontal, o cónico con R) | `G90 X57 Z-84 F.2` |
| **G94** | Ciclo fijo de frenteado (vertical, o cónico con R) | `G94 X30 Z8 F.2` |
| **G96** | Velocidad de corte constante, en m/min | `G96 S180` |
| **G97** | RPM constantes | `G97 S4246` |
| **G98** | Avance en mm/min | `G98` |
| **G99** | Avance en mm/vuelta | `G99 F.16` |

## Coordenadas
- **Absolutas:** X y Z.
- **Incrementales:** X se escribe **U** y Z se escribe **W**.
- **X va en diámetro.** Una pieza de Ø40 se programa `X40`.
- Z es 0 en la punta y negativo hacia la base.

## Arcos G02 y G03
El sentido depende de desde dónde recorrés el perfil. La carpeta aclara que en G03 "el camino se empieza del lado contrario a G02". En los TP, recorriendo de la punta hacia la base con el radio hacia arriba y +Z a la derecha, el arco de la punta es **G03** (antihorario). Con la herramienta de terminación izquierda (T1010) se recorre al revés y se usa **G02**.

## Cero pieza
- `G10 P0 Z-149`: con bruto Ø60 x 150, deja el cero de pieza en la cara, a 149 mm del fondo. Otros ejemplos de la carpeta: `Z-199` (bruto de 200) y `Z-164`.
- En los programas completos se usa **G54** como sistema de trabajo. El valor de G54 vive en el `.prj` (ver [[Formato de archivos WinUnisoft]]): en los TP es `G54 = 0,0,129`.

## No aparecen en las fuentes
G75, G76, G81, G40/G41/G42 y G20/G21.

Ver también: [[Códigos M]], [[Estructura de un programa]].
