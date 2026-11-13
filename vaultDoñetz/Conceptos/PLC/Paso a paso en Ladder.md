---
tipo: concepto
area: plc
tags: [plc, ladder, paso-a-paso, métodos]
---

# Paso a paso en Ladder

Es el [[Método paso a paso]] programado: **una memoria por paso** (`M1…Mn`) y [[Set y Reset]]. Según el profe, es el método que más se usa para programar en Ladder.

## Las tres columnas imaginarias
| Habilitación | Condición | Acciones |
|---|---|---|
| Contacto de la **memoria del propio paso** (`Mn`) | Emisores del punto *n* del diagrama | 1) Generar el movimiento o acción · 2) **Habilitar el paso siguiente** (`S M(n+1)`) · 3) **Desconectar el paso anterior** (`R M(n−1)`) |

> Ojo: en el cableado, cada paso se habilitaba con el relé *anterior*. En Ladder, **cada memoria habilita su propio paso** y el paso anterior es el que la setea.

## El truco del paso 1 (lógica negativa)
- Al arrancar, todas las memorias valen 0, y entonces ningún paso estaría habilitado.
- Solución: el paso 1 se habilita con un **contacto NC de `M1`** (habilita cuando `M1 = 0`).
- Por eso `M1` funciona **al revés** que las demás:
  - el paso 2 **desconecta** el paso 1 con **`S M1`**;
  - el último paso **rehabilita** el paso 1 con **`R M1`**.
- Resultado: el último paso suele quedar con **todas bobinas reset**.

## Monoestables
Con `S Q1` el cabezal queda memorizado; no hace falta repetirlo en los pasos siguientes (lo que sí se hacía en cableado). Para que vuelva se usa `R Q1`.

## Ejemplo de los videos (5 pasos)
`1A−` (S Q1) · pausa `TT1` 4 s · `1A+` (R Q1) · `2A+` (S Q2) · `2A−` (R Q2).
- Paso 1: `/M1` · `MA`·`I3` → `S Q1`, `S M2`, `R M5`
- Paso 2: `M2` · `I1` → `TT1`, `S M3`, `S M1`
- Paso 3: `M3` · `T1` → `R Q1`, `S M4`, `R M2`
- Paso 4: `M4` · `I2` → `S Q2`, `S M5`, `R M3`
- Paso 5: `M5` · `I4` → `R Q2`, `R M1`, `R M4`

## Simulación
En [[Zelio Soft 2]] hay que ir accionando a mano los rodillos según dónde estaría cada vástago.

## Videos
[[2020-10-19 Paso a Paso en Ladder - pizarrón]] · [[2020-10-20 Paso a Paso en Ladder - simulación]]
