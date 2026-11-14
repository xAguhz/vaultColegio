---
tipo: experimento
tema: MHS
aliases: [burbujas, muestras viscosas, pipeteo]
relacionado: ["[[Razonamiento físico]]", "[[Automatización de laboratorio - curva de dilución]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["19:02", "19:48"]
estado: segun-el-video
tags: [experimento, limitacion]
---
# Líquidos viscosos y burbujas

El experimento que muestra el **límite**. [▶ 19:02](https://www.youtube.com/watch?v=3hxdHem70gw&t=1142s)

## Situación
Automatizar con [[Claude]] y MHS un procedimiento de laboratorio que manipula líquidos. Algunas muestras eran **viscosas**: no es lo mismo mover agua que mover miel.

## Qué puede salir mal
- Las muestras viscosas hacen **espuma y burbujas**.
- Una burbuja chiquita puede **arruinar una medición**.
- La pipeta "cree" que cargó cierto volumen, pero una parte era aire.
- Un sensor puede leer mal el nivel.

## Qué pasó [▶ 19:48](https://www.youtube.com/watch?v=3hxdHem70gw&t=1188s)
Claude arrancó con **parámetros genéricos**, y esos parámetros causaron burbujas en algunas muestras viscosas.

## Diagnóstico
El modelo **sabía manejar el software, interpretar datos y usar las herramientas**, pero le faltaba el conocimiento físico de alguien que hace ese procedimiento hace años.

[[Anthropic]] usa este caso para **reconocer** que los modelos todavía tienen limitaciones en razonamiento físico. → [[Razonamiento físico]]
