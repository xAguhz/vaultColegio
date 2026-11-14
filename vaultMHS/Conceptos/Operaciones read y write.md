---
tipo: concepto
tema: MHS
aliases: [read, write, leer y escribir]
relacionado: ["[[Driver MHS]]", "[[Modbus]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["05:50"]
estado: segun-el-video
tags: [concepto]
---
# Operaciones read y write

Según el video, Anthropic habla de operaciones muy básicas: [▶ 05:50](https://www.youtube.com/watch?v=3hxdHem70gw&t=350s)
- **read**: leer algo (la temperatura de un sensor, la posición de un motor).
- **write**: cambiar algo (mover un robot, cambiar un parámetro).

La IA pide la operación genérica y el [[Driver MHS]] la traduce al mecanismo real de cada equipo (por ejemplo, leer un registro [[Modbus]] y convertir la unidad).

> Es la misma lógica de los registros de entrada y salida de un [[PLC]] o de Modbus, pero expuesta de una forma que un agente puede descubrir y entender.

## Para investigar
- ¿Hay operaciones más allá de read y write (acciones, eventos, suscripciones)? → [[03 Preguntas abiertas]]
