---
tipo: concepto
tema: MHS
aliases: [MHS, Model Hardware Standard]
relacionado: ["[[Driver MHS]]", "[[Ficha del dispositivo]]", "[[Model Context Protocol (MCP)]]", "[[Capas de control]]", "[[Interlock]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["00:00", "01:21", "05:02", "27:52"]
estado: segun-el-video
tags: [concepto, central]
---
# Model Hardware Standard (MHS)

**Definición:** estándar de [[Anthropic]] para que una IA pueda **descubrir qué es una máquina, qué puede hacer con ella y cómo interactuar**, sin aprender un sistema distinto con cada equipo. [▶ 00:34](https://www.youtube.com/watch?v=3hxdHem70gw&t=34s)

> "No estamos hablando de un nuevo modelo de inteligencia artificial, estamos hablando de un estándar."

## Qué le tiene que decir a la IA
- **Qué** dispositivo es (cámara, robot, sensor…).
- **Qué información** puede obtener de él (leer).
- **Qué órdenes** puede darle (escribir o actuar).
- **Qué no** debería hacer (límites, [[Interlock|interlocks]]).

## Piezas
- [[Driver MHS]]: traduce entre la máquina real y la capa común.
- [[Ficha del dispositivo]]: descripción de capacidades y restricciones.
- [[Operaciones read y write]]: las operaciones básicas.
- Acceso por [[Model Context Protocol (MCP)|MCP]], línea de comandos o código.

## Lo que NO es
- No reemplaza [[Modbus]], [[OPC UA]], los [[PLC]] ni las APIs de los fabricantes. Se monta **encima**. [▶ 06:37](https://www.youtube.com/watch?v=3hxdHem70gw&t=397s)
- No es una IA que controla la máquina en tiempo real. → [[Capas de control]]
- No es (todavía) un producto terminado: es una *research preview*. [▶ 01:21](https://www.youtube.com/watch?v=3hxdHem70gw&t=81s)
- No es exclusivo de [[Claude]]. → [[Model agnostic]]

## Datos (según el video)
| | |
|---|---|
| Presentado | 27/08/2026 |
| Origen | [[Anthropic]] + [[HHMI Janelia]] |
| Estado | Research preview limitada |
| Primeros participantes | [[Raspberry Pi]], [[Universal Robots]], laboratorios |
| Futuro | Open source |

## Analogía clave
Un **ratón USB**: lo enchufás y la computadora sabe que es un ratón, sea de la marca que sea. MHS apunta a eso, *conceptualmente*, para máquinas industriales. → [[Analogías]]
