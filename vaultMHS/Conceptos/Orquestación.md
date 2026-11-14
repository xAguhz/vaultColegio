---
tipo: concepto
tema: MHS
aliases: [orquestar, capa de orquestación, coordinación]
relacionado: ["[[Capas de control]]", "[[Automatización de laboratorio - curva de dilución]]", "[[Ficha del dispositivo]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["11:31", "24:11"]
estado: segun-el-video
tags: [concepto]
---
# Orquestación

**Orquestar = coordinar las acciones.** [▶ 11:31](https://www.youtube.com/watch?v=3hxdHem70gw&t=691s)
> Primero hacé esto; cuando termine, mové aquello; después medí esto, y si el resultado está bien, seguí.

## En el experimento del laboratorio
Encima de los [[Driver MHS|drivers]] se puso una **capa de orquestación**, y así un agente pudo manejar todo el proceso sin tratar cada máquina como un mundo aparte. → [[Automatización de laboratorio - curva de dilución]]

## Ejemplo de una línea de producción (imaginado por el autor) [▶ 24:11](https://www.youtube.com/watch?v=3hxdHem70gw&t=1451s)
1. La cámara detecta que llegó una pieza.
2. El agente consulta el estado de la máquina.
3. Comprueba que está lista.
4. Coordina al robot que mueve la pieza.
5. La máquina hace su proceso.
6. Un sensor verifica el resultado.
7. El agente decide el paso siguiente.

> El autor aclara que es una forma de imaginarlo: no significa que MHS ya se pueda instalar así en cualquier línea.

> Para quien viene de neumática y PLC: es el diagrama espacio-fase y la secuencia (cascada, paso a paso), pero ahora entre máquinas distintas y armada por un agente.
