---
tipo: concepto
area: métodos
tags: [métodos, electroneumática, paso-a-paso]
---

# Método paso a paso

## Idea
- **Una fase = un paso = un relé.** No se buscan líneas: con 4 fases hay 4 pasos y 4 relés.
- Cada paso solo puede arrancar si **el paso anterior se cumplió**. Así el ciclo se respeta siempre y se resuelve tanto la superposición como la **repetición de movimientos** (lo que la cascada no puede).
- Si se para la máquina, siempre completa el ciclo entero (por ejemplo, las 4 fases "sale-entra-sale-entra").

## Cuadro
Solo los renglones **Relé** (`K1`…`Kn`) y **Bobina**. Los movimientos ya están en el diagrama.

## Estructura de cada paso (circuito de mando)
```
+24V ─┬─[emisores NA]──[NA K(n−1) habilita]─┬─[NC K(n+1) desconecta]──( Kn )── 0V
      └───────────────[NA Kn autorretención]─┘
```
1. **Emisores de señal:** los que marca el diagrama en el punto *n*.
2. **Habilitación:** NA del **relé anterior**. Sin él, el paso no arranca aunque llegue la señal (por ejemplo, si un rodillo arranca pisado, sin habilitación arrancaría por el paso 3).
3. **Autorretención:** NA del propio `Kn`, **entre el que habilita y el que desconecta** (puentea emisores y habilitación, porque al arrancar el paso *n* se desconecta el anterior).
4. **Desconexión:** NC del **relé siguiente**.
- Se piensa como un ciclo continuo: el anterior de `K1` es el **último** (`K4`), y el siguiente del último es `K1`.

## Arranque la primera vez
Al poner en marcha por primera vez, el último relé nunca se energizó, y entonces el paso 1 no está habilitado. **Solución del profe:** un NA del **pulsador de marcha** en paralelo con la autorretención del **último paso**. Le da un pulso, el último paso se autorretiene y habilita el paso 1.

## Circuito de fuerza
- Cada bobina se alimenta con NA de **todos los pasos en que aparece**, en **paralelo** (OR). Ej.: `1Y1` con `K1 ∥ K3`; `1Y2` con `K2 ∥ K4`.
- Usar **un contacto distinto para cada bobina** para no mezclar señales.
- **Monoestables:** como el relé se suelta al terminar su paso, la bobina se repite en el cuadro en los pasos siguientes mientras el actuador tenga que seguir extendido (ej.: `2Y1` en `K1`, `K2` y `K4`).
- El relé **temporizado** también se pone en fuerza (es una "acción", una pausa): ej.: `K6` alimentado por `K2`.

## Rodillos que actúan dos veces por ciclo
Se conectan a relés auxiliares (`KA`, `KB`) en un [[Circuito de sensado]] para tener varios contactos.

## Comparado con cascada
Más relés y más líneas, pero **repetitivo y seguro**: "aplicando el método sale funcionando". Es el más usado en Ladder.

## En PLC
[[Paso a paso en Ladder]]

## Videos
[[2020-07-06 Método Paso a Paso - 1 actuador 4 fases]] · [[2020-08-24 Paso a Paso con monoestables y repetición]] · [[2020-10-19 Paso a Paso en Ladder - pizarrón]]
