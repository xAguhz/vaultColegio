---
tipo: concepto
area: digital
tags: [digital, álgebra-de-boole]
---

# Minitérminos

## Definición
Un **minitérmino** es un **producto lógico** (AND) que contiene **todas las variables** de la función, cada una **negada o sin negar**. Hay uno por cada renglón de la tabla.

## Cómo se arma
- Variable que vale **0** en el renglón → va **negada**.
- Variable que vale **1** → va **directa**.
- Comprobación: al reemplazar los valores de ese renglón, el minitérmino da **1**.

## Suma de minitérminos
Z = **suma (OR) de los minitérminos de los renglones donde Z = 1**.

## Ejemplo: XOR de dos variables
| A | B | Z | Minitérmino |
|---|---|---|---|
| 0 | 0 | 0 | A'·B' |
| 0 | 1 | **1** | **A'·B** |
| 1 | 0 | **1** | **A·B'** |
| 1 | 1 | 0 | A·B |

**Z = A'·B + A·B'** → circuito: dos AND de 2 entradas (con negadores) que van a una OR. Se comprueba renglón por renglón en [[Multisim]].

## Relacionado
[[Maxitérminos]] (su dual) · [[Funciones lógicas]]

## Video
[[2025-05-12 Minitérminos]]
