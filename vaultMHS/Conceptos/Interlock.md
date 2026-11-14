---
tipo: concepto
tema: MHS
aliases: [interlocks, enclavamiento, límites de seguridad]
relacionado: ["[[Ficha del dispositivo]]", "[[Razonamiento físico]]", "[[Capas de control]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["17:40", "18:27"]
estado: segun-el-video
tags: [concepto, seguridad]
---
# Interlock

**Definición del video:** básicamente una protección: una regla que, físicamente o desde el sistema, **impide ciertas operaciones**. [▶ 18:27](https://www.youtube.com/watch?v=3hxdHem70gw&t=1107s)

## Analogía: la lavadora
Mientras lava, la puerta queda trabada. No se confía en que el usuario se acuerde de no abrirla: **la máquina lo impide**.

## Por qué en MHS
- En software, un error tira abajo una aplicación. En una máquina de toneladas, **puede haber vidas en juego**. [▶ 17:40](https://www.youtube.com/watch?v=3hxdHem70gw&t=1060s)
- MHS permite **declarar límites e interlocks** en la descripción del dispositivo.
- Objetivo: que la seguridad **no dependa solo de que la IA recuerde una instrucción escrita en algún lado**. Que haya límites que directamente no la dejen ejecutar ciertas acciones.

## Ejemplos que aparecen en el video
- Un robot que **no puede entrar en cierta zona**.
- Una máquina que **solo arranca con la puerta cerrada**. [▶ 24:11](https://www.youtube.com/watch?v=3hxdHem70gw&t=1451s)
- Riesgos citados: mover un robot contra una persona, calentar algo de más, abrir una válvula que debería estar cerrada, hacer girar un motor con alguien trabajando encima. [▶ 04:17](https://www.youtube.com/watch?v=3hxdHem70gw&t=257s)

> Si estudiaste electroneumática, es la misma idea que el *enclavamiento eléctrico*: que el circuito haga imposible la combinación peligrosa.

## Para investigar
- ¿El interlock se hace cumplir en el driver, en el hardware o solo se declara? → [[03 Preguntas abiertas]]
