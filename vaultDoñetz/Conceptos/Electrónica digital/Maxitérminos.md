---
tipo: concepto
area: digital
tags: [digital, álgebra-de-boole]
---

# Maxitérminos

## Definición
Un **maxitérmino** es una **suma lógica** (OR) que contiene **todas las variables** de la función, negadas o sin negar.

## Cómo se arma (al revés que el minitérmino)
- Variable que vale **1** en el renglón → va **negada**.
- Variable que vale **0** → va **directa**.
- Comprobación: al reemplazar, el maxitérmino da **0** (una OR solo da 0 si todas sus entradas son 0).

## Producto de maxitérminos
Z = **producto (AND) de los maxitérminos de los renglones donde Z = 0**. Cada maxitérmino va entre **paréntesis**.

## Ejemplo: XOR
| A | B | Z | Maxitérmino |
|---|---|---|---|
| 0 | 0 | **0** | **(A + B)** |
| 0 | 1 | 1 | (A + B') |
| 1 | 0 | 1 | (A' + B) |
| 1 | 1 | **0** | **(A' + B')** |

**Z = (A + B)·(A' + B')** → dos OR de 2 entradas (la segunda con las entradas negadas) que van a una AND.

## Minitérminos vs. maxitérminos
| | Minitérmino | Maxitérmino |
|---|---|---|
| Operación | Producto | Suma |
| Se niega la variable que vale | 0 | 1 |
| Se usan los renglones con | Z = 1 | Z = 0 |
| Función resultante | Suma de productos | Producto de sumas |

## Video
[[2025-05-12 Maxitérminos]]
