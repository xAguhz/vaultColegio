---
tipo: tecnologia
tema: MHS
aliases: [PLCs, autómata programable, controlador lógico programable]
relacionado: ["[[Capas de control]]", "[[Código determinista]]", "[[Modbus]]", "[[OPC UA]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["17:40", "24:58"]
estado: segun-el-video
tags: [tecnologia, industrial]
---
# PLC

## Lo que dice el video
> "No hace falta sustituir un PLC por un modelo de lenguaje. Un PLC puede seguir encargándose de controlar una máquina." [▶ 17:40](https://www.youtube.com/watch?v=3hxdHem70gw&t=1060s)

> "Los PLC no desaparecen, OPC UA tampoco, Modbus tampoco, ni mucho menos los sistemas de control en tiempo real." [▶ 24:58](https://www.youtube.com/watch?v=3hxdHem70gw&t=1498s)

El PLC es la **capa de abajo**, la rápida y determinista, en el esquema de [[Capas de control]].

## Contexto general (no del video)
Controlador industrial que lee entradas (sensores, pulsadores), ejecuta un programa en ciclos (por ejemplo en Ladder) y maneja salidas (válvulas, contactores, motores). Es justamente el tipo de [[Código determinista]] al que el video quiere que llegue la IA.

> En `vaultDoñetz` están PLC, Ladder, Set/Reset, temporizadores y los métodos cascada y paso a paso. Todo eso sigue valiendo: MHS se monta encima.
