---
tipo: concepto
area: plc
tags: [plc, ladder]
aliases: [Ladder, Lenguaje escalera]
---

# Lenguaje Ladder (escalera)

## Historia (según el video)
Tiene **más de 60 años**. Al principio los programas se escribían con una **máquina de escribir**, que tenía pocos símbolos. De ahí sale la forma de los símbolos:
| Elemento | Escrito a máquina | Hoy |
|---|---|---|
| Contacto NA | `--] [--` | Parecido al símbolo de un capacitor no polarizado |
| Contacto NC | `--]/[--` | Con una barra diagonal |
| Bobina / salida | `--( )--` | Paréntesis |

## Estructura
- El circuito eléctrico se dibuja con rieles horizontales (+ arriba, 0 V abajo). En Ladder los rieles son **verticales**: a la izquierda el **valor lógico alto (HI)** y a la derecha el **bajo (LOW)**, que la mayoría de los softwares actuales ya no dibuja. Con muchas líneas horizontales entre los dos rieles, parece una **escalera**.
- Por los "cables" no circula corriente sino **el estado lógico (0/1)**.

## Contacto físico vs. contacto lógico
El contacto Ladder **no tiene por qué ser igual** al físico. Ejemplo: con un pulsador físico NA, si en Ladder se pone un **contacto NC**, se obtiene la función **NOT**.

## Funciones básicas
| Función | Ladder |
|---|---|
| **Identidad** | NA de `I1` → `( Q1 )` (copia la entrada en la salida) |
| **NOT (negador o inversor)** | NC de `I2` → `( Q2 )` |
| **AND** | NA `I1` en serie con NA `I2` → `( Q3 )` |
| **OR** | Contactos en paralelo |

## Estructura típica de un programa electroneumático
1. Marcha y parada (memoria `MA`).
2. Indicador de marcha (`MA` → `H1`).
3. Parte de mando (memorias de líneas o pasos).
4. Acciones sobre salidas (no hace falta una "parte de fuerza" aparte).

## Relacionado
[[Set y Reset]] · [[Temporizadores en PLC]] · [[Cascada en Ladder]] · [[Paso a paso en Ladder]] · [[Funciones lógicas]]

## Videos
[[2020-09-02 PLC Ladder parte I]] · [[2020-09-03 PLC Ladder parte II - Zelio Soft]]
