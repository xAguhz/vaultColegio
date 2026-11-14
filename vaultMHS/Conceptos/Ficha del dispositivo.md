---
tipo: concepto
tema: MHS
aliases: [ficha de la máquina, descripción del dispositivo, mapa de capacidades]
relacionado: ["[[Model Hardware Standard (MHS)]]", "[[Interlock]]", "[[Razonamiento físico]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["07:24", "08:02", "08:49", "24:11"]
estado: segun-el-video
tags: [concepto]
---
# Ficha del dispositivo

Descripción que genera MHS de cada máquina, pensada para que un sistema entienda: [▶ 08:49](https://www.youtube.com/watch?v=3hxdHem70gw&t=529s)
- **qué** dispositivo es,
- **qué sabe hacer**,
- **qué puede medir**,
- **qué se puede cambiar**,
- **qué límites tiene**.

## Por qué no alcanza con los comandos [▶ 07:24](https://www.youtube.com/watch?v=3hxdHem70gw&t=444s)
> Conocer los comandos de una máquina no es suficiente.

Analogía de la **excavadora**: sabés qué botón levanta el brazo, pero no cuánto pesa la carga, hasta dónde llega el brazo, si hay alguien al lado ni qué movimientos están prohibidos. "Saber qué botón se puede pulsar es una parte del problema; entender qué significa pulsarlo es otra cosa."

## Información que no está en la API [▶ 08:02](https://www.youtube.com/watch?v=3hxdHem70gw&t=482s)
En un brazo robótico, la API da la posición y la velocidad de los motores y permite mandarlo a un punto. Pero **no** dice:
- cuánto peso puede levantar,
- qué recorrido físico tiene,
- qué zona no debería atravesar.

MHS permite agregar eso con **etiquetas**, que pueden estar escritas en **lenguaje natural**.

## Ejemplo de "mapa de capacidades" [▶ 23:31](https://www.youtube.com/watch?v=3hxdHem70gw&t=1411s)
> "Tengo una cámara: puede capturar imágenes. Tengo un sensor de temperatura: ahora mide 28 grados. Tengo un brazo robótico: puede recoger este objeto, pero no puede entrar en esta zona. Tengo una máquina que solo puede arrancar con esta puerta cerrada."

## Para investigar
- ¿Qué formato tiene la ficha (JSON, YAML, algún esquema)? → [[03 Preguntas abiertas]]
