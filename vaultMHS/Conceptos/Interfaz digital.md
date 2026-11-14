---
tipo: concepto
tema: MHS
aliases: [puerta digital, máquinas sin interfaz, equipos legacy]
relacionado: ["[[API, SDK y protocolo]]", "[[Adopción del estándar]]", "[[ActiveX y COM]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["21:23", "21:55"]
estado: segun-el-video
tags: [concepto, limitacion]
---
# Interfaz digital

> "MHS necesita alguna puerta digital por la que entrar." [▶ 21:23](https://www.youtube.com/watch?v=3hxdHem70gw&t=1283s)

## El caso de la máquina de hace 40 años
Tiene botones, palancas, motores y relés, pero no tiene computadora, ni red, ni software, ni ninguna interfaz digital. **MHS no puede aparecer mágicamente y controlarla.** [▶ 21:55](https://www.youtube.com/watch?v=3hxdHem70gw&t=1315s)

Antes hay que digitalizarla de alguna manera:
- agregando sensores,
- instalando un controlador (por ejemplo, un [[PLC]]),
- conectándola a otro sistema.

## Puertas posibles en equipos modernos
Una API, un SDK, un protocolo industrial ([[Modbus]], [[OPC UA]]), un programa, **incluso una interfaz gráfica**.

## Línea de trabajo abierta
[[Anthropic]] reconoce que uno de los frentes es trabajar con más equipos **que no tienen buenas interfaces programables**.

> Lo mismo vale para un torno como el Femar TM300 de `vaultTorno`: sin sensores ni controlador, no hay nada que MHS pueda describir.
