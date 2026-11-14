---
tipo: tecnologia
tema: MHS
aliases: [MCP, Model Context Protocol]
relacionado: ["[[Model Hardware Standard (MHS)]]", "[[Model agnostic]]", "[[Anthropic]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["08:49", "09:23"]
estado: segun-el-video
tags: [tecnologia, software]
---
# Model Context Protocol (MCP)

## Lo que dice el video [▶ 09:23](https://www.youtube.com/watch?v=3hxdHem70gw&t=563s)
- Es de [[Anthropic]] y apareció para que los modelos de IA **se conecten con herramientas externas**: un calendario, una base de datos, una aplicación o un buscador.
- MHS comparte parte de esa filosofía, pero para el **mundo físico**.
- MHS **puede apoyarse en MCP** como una de las vías para que un agente llegue al hardware, pero no es la única. También puede ir por **línea de comandos** o **directamente desde código**.

## Comparación
| | MCP | MHS |
|---|---|---|
| Conecta la IA con… | Software (apps, datos, servicios) | Hardware (sensores, robots, instrumentos) |
| Riesgo de un error | Una app que se cae, datos mal | Consecuencias físicas, personas |
| Relación | — | Puede usar MCP como transporte |

## Contexto general (no del video)
MCP es un protocolo abierto: un *servidor MCP* expone herramientas y recursos, y un cliente (la app de la IA) los descubre y los usa. Mirar cómo está definido ayuda a imaginar cómo podría verse un [[Driver MHS]].
