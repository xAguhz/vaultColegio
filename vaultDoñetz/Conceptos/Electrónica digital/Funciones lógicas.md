---
tipo: concepto
area: digital
tags: [digital, lógica]
---

# Funciones lógicas

Las variables **binarias** solo valen 0 o 1.

| Función | Comportamiento | Con contactos | Neumática |
|---|---|---|---|
| **Identidad** | Z = A | NA | — |
| **NOT** (negador o inversor) | Z = A' | NC | — |
| **AND** (producto lógico) | 1 solo si **todas** las entradas valen 1 | NA en serie | [[Válvula lógica AND]] |
| **OR** (suma lógica) | 0 solo si **todas** las entradas valen 0 | NA en paralelo | (válvula OR) |
| **XOR** (suma exclusiva) | 1 cuando las entradas son **distintas** | — | — |

AND, OR y NOT son las **funciones básicas**: con ellas se arma cualquier otra.

## Tabla de verdad
- Cantidad de combinaciones = **2ⁿ** (n = número de variables).
- Para completarla sin memorizar: en la columna de más a la derecha se alterna `0,1,0,1…`; en cada columna hacia la izquierda se duplica el bloque (`00 11`, `0000 1111`…).

## Función mínima
Para una tabla hay **infinitos circuitos** posibles. El **mínimo** es el que tiene menos compuertas y menos variables de entrada. Se obtiene con álgebra de Boole o con el **diagrama de Karnaugh** (que el profe promete para un video futuro).

## Relacionado
[[Minitérminos]] · [[Maxitérminos]] · [[Lenguaje Ladder]] · [[Contactos eléctricos]]
