---
tipo: experimento
tema: MHS
aliases: [sistema óptico, alineación óptica]
relacionado: ["[[Código determinista]]", "[[Capas de control]]", "[[QuEra - recuperación del clock del láser]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["12:53", "13:25"]
estado: segun-el-video
tags: [experimento]
---
# Alineación de un láser con cámara

## Qué hicieron [▶ 12:53](https://www.youtube.com/watch?v=3hxdHem70gw&t=773s)
Pusieron a [[Claude]] a trabajar con un **sistema óptico**:
1. El agente cambiaba la posición de un láser.
2. Miraba con una cámara qué pasaba con el haz.
3. Hacía otro ajuste.
4. Volvía a mirar, y así seguía.

## Analogía: enderezar un cuadro [▶ 13:25](https://www.youtube.com/watch?v=3hxdHem70gw&t=805s)
Lo movés un poco, te alejás, lo mirás y, si sigue torcido, lo corregís. No arrancás con una fórmula exacta: **probás, observás y corregís**.

## Lo interesante [▶ 13:25](https://www.youtube.com/watch?v=3hxdHem70gw&t=805s)
Cuando Claude encontró cómo hacer el procedimiento, **convirtió lo aprendido en código**: un **script determinista** que hace la alineación **sin que el modelo tenga que estar pensando en cada paso**.

## Por qué importa
Es el primer ejemplo del patrón "la IA desarrolla el procedimiento y después se retira". → [[Código determinista]], [[Capas de control]]
