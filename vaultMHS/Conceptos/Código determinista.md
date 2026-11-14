---
tipo: concepto
tema: MHS
aliases: [script determinista, código tradicional]
relacionado: ["[[Capas de control]]", "[[Alineación de un láser con cámara]]", "[[QuEra - recuperación del clock del láser]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["13:25", "14:14", "14:48", "16:11"]
estado: segun-el-video
tags: [concepto]
---
# Código determinista

Código que **siempre sigue las mismas reglas**: [▶ 14:14](https://www.youtube.com/watch?v=3hxdHem70gw&t=854s)
> Si pasa A, hacés B. Si el sensor pasa de cierto valor, hacés C. No hay un modelo improvisando una respuesta nueva cada vez.

## El patrón que muestran los experimentos
1. La IA **explora**: prueba un cambio, observa el resultado y corrige (como cuando enderezás un cuadro).
2. Cuando encuentra el procedimiento, lo **convierte en un script**.
3. El script **corre solo**, sin que el modelo "piense" en cada paso.
4. Se lo prueba por separado.

## Por qué importa
- Es **predecible y verificable**: se puede probar 700 veces y medir. → [[QuEra - recuperación del clock del láser]]
- Es **rápido**: no espera la respuesta de un modelo.
- Deja a la IA en el lugar de **ingeniera que desarrolla el controlador**, no de controlador. → [[Capas de control]]

## Ejemplos
- [[Alineación de un láser con cámara]] [▶ 13:25](https://www.youtube.com/watch?v=3hxdHem70gw&t=805s)
- [[QuEra - recuperación del clock del láser]] [▶ 16:11](https://www.youtube.com/watch?v=3hxdHem70gw&t=971s)

> Para quien viene de PLC: es como si la IA hiciera la puesta a punto y dejara escrito el programa Ladder final, y después la máquina corriera ese programa y nada más.
