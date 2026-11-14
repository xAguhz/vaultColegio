---
tipo: concepto
tema: MHS
aliases: [driver, drivers MHS]
relacionado: ["[[Model Hardware Standard (MHS)]]", "[[API, SDK y protocolo]]", "[[Operaciones read y write]]", "[[Código pegamento]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["05:02", "05:50", "06:37", "11:31"]
estado: segun-el-video
tags: [concepto]
---
# Driver MHS

Pieza de software que se pone **entre la máquina y la IA** y hace de **traductor**. [▶ 05:02](https://www.youtube.com/watch?v=3hxdHem70gw&t=302s)

```
IA / agente
   │  orden genérica: "leé la temperatura"
   ▼
Driver MHS          ← traduce
   │  orden específica: leer el registro 40001 por Modbus y pasar a °C
   ▼
Máquina real (no cambia)
```

## Ideas clave
- La máquina **sigue funcionando con la tecnología que ya tenía**. MHS no obliga a cambiarla.
- El agente no necesita conocer los detalles internos de cada fabricante.
- Alguien **tiene que escribir el driver** (hacer la integración). La ventaja es que, una vez hecho, todo lo que está arriba ve a los equipos de manera parecida. [▶ 06:37](https://www.youtube.com/watch?v=3hxdHem70gw&t=397s)
- En el experimento del laboratorio se escribió un driver por equipo, más una capa de [[Orquestación]] encima. → [[Automatización de laboratorio - curva de dilución]]

## Ejemplo del video: sensor de temperatura [▶ 05:50](https://www.youtube.com/watch?v=3hxdHem70gw&t=350s)
Para la IA, la acción es "quiero saber la temperatura". Por debajo, el sensor puede usar [[Modbus]], hay que leer un registro concreto y el número que devuelve hay que convertirlo a grados Celsius. De todo eso se encarga el driver.

## Analogía
El **driver de una impresora**: tocás "imprimir" y no sabés qué señales manda Windows a cada motor. → [[Analogías]]
