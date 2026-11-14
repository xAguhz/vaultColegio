---
tipo: concepto
tema: MHS
aliases: [las máquinas no hablan el mismo idioma, problema de integración]
relacionado: ["[[API, SDK y protocolo]]", "[[Código pegamento]]", "[[Model Hardware Standard (MHS)]]", "[[Adopción del estándar]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["02:08", "02:55", "04:17", "21:55", "22:43"]
estado: segun-el-video
tags: [concepto, problema]
---
# Interoperabilidad

**El problema de fondo:** "las máquinas no hablan todas el mismo idioma", y eso existe desde mucho antes de la IA. [▶ 02:08](https://www.youtube.com/watch?v=3hxdHem70gw&t=128s)

## En un laboratorio [▶ 02:55](https://www.youtube.com/watch?v=3hxdHem70gw&t=175s)
Un brazo robótico de un fabricante, una cámara de otro, un manipulador de líquidos, un microscopio y sensores. Desde afuera son todos "aparatos electrónicos", pero cada uno se controla distinto: un programa propio, otro software, un protocolo particular, o un programa de hace 20 años que solo funciona apretando botones en pantalla.

## Para la IA es peor [▶ 04:17](https://www.youtube.com/watch?v=3hxdHem70gw&t=257s)
No le alcanza con *enviar* la orden. Tiene que entender:
- qué puede hacer cada máquina,
- qué puede leer y qué parámetros puede cambiar,
- qué límites tiene,
- qué acciones son peligrosas,
- **en qué orden** tienen que pasar las cosas.

## En IoT [▶ 22:43](https://www.youtube.com/watch?v=3hxdHem70gw&t=1363s)
Es la misma pregunta que el IoT se hace hace años: *¿cómo hacemos que miles de dispositivos distintos convivan en un mismo sistema?*
- **Casa inteligente:** lamparitas, termostatos, sensores y persianas, cada uno con su app y su nube. Mezclar marcas termina en caos.
- **Fábrica:** en vez de 10 dispositivos, cientos o miles: robots, bombas, motores, sensores, [[PLC|PLCs]].

## La respuesta de MHS
Una capa común que no reemplaza nada, pero hace que todo **se vea parecido desde arriba**. → [[Model Hardware Standard (MHS)]]
