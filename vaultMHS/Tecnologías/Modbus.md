---
tipo: tecnologia
tema: MHS
aliases: [Modbus RTU, Modbus TCP]
relacionado: ["[[Driver MHS]]", "[[Operaciones read y write]]", "[[API, SDK y protocolo]]", "[[OPC UA]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["05:50", "06:37", "24:58"]
estado: segun-el-video
tags: [tecnologia, protocolo, industrial]
---
# Modbus

## Lo que dice el video
- Es el ejemplo de protocolo que hay **debajo** del [[Driver MHS]]: el sensor de temperatura habla Modbus, hay que leer un registro concreto y el número que devuelve hay que convertirlo a °C. [▶ 05:50](https://www.youtube.com/watch?v=3hxdHem70gw&t=350s)
- "Una máquina Modbus seguirá funcionando con Modbus." MHS no la cambia. [▶ 06:37](https://www.youtube.com/watch?v=3hxdHem70gw&t=397s)

## Contexto general (no del video)
Protocolo industrial abierto y muy viejo (de fines de los 70), basado en leer y escribir **registros** numerados. Corre por serie (RTU) o por red (TCP). Un registro no dice qué significa: por eso alguien tiene que saber que el 40001 es "temperatura × 10". Eso es justo lo que MHS quiere hacer explícito para la IA. → [[Ficha del dispositivo]]
