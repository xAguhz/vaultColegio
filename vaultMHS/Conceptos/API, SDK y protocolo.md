---
tipo: concepto
tema: MHS
aliases: [API, SDK, protocolo, APIs]
relacionado: ["[[Driver MHS]]", "[[Interoperabilidad]]", "[[Modbus]]", "[[ActiveX y COM]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["02:55", "03:43"]
estado: segun-el-video
tags: [concepto, basico]
---
# API, SDK y protocolo

Las formas que existen hoy para controlar un equipo desde otro programa. Las definiciones son las del video: [▶ 03:43](https://www.youtube.com/watch?v=3hxdHem70gw&t=223s)

| Término | Qué es | Ejemplo del video |
|---|---|---|
| **API** | Lo que ofrece un programa para que otro le pueda pedir cosas | En vez de hacer clic en el botón de la cámara, otro programa manda la orden "sacá una foto" |
| **SDK** | Herramientas que el fabricante da a los desarrolladores para hacer software que trabaje con su equipo | El kit del fabricante del robot |
| **Protocolo** | Las reglas que siguen dos equipos para intercambiar información | [[Modbus]], [[OPC UA]] |

## El problema
Ninguna de las tres está mal. El problema aparece cuando hay **muchos dispositivos y cada uno tiene sus propias reglas**: hay que armar "pequeños traductores" entre cada par. → [[Código pegamento]]

## Y además…
Hay equipos que **no tienen ninguna de las tres**: solo una interfaz gráfica (el lector de placas del experimento) o directamente nada digital. → [[Interfaz digital]]
