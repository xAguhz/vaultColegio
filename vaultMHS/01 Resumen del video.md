---
tipo: resumen
tema: MHS
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
relacionado: ["[[Model Hardware Standard (MHS)]]", "[[Capas de control]]"]
tags: [resumen]
---
# Resumen del video

**Tesis:** antes de pensar en robots autónomos, hay que resolver algo menos llamativo: *¿cómo le explicamos a una IA qué es una máquina, qué puede hacer y qué límites tiene?* Eso es lo que busca [[Model Hardware Standard (MHS)]]. [▶ 27:52](https://www.youtube.com/watch?v=3hxdHem70gw&t=1672s)

## 1. Qué es MHS [▶ 00:00](https://www.youtube.com/watch?v=3hxdHem70gw&t=0s)
Es un **estándar**, no un modelo de IA. Funciona como un lenguaje común entre IAs y máquinas: "esto es una cámara, podés pedirle una imagen"; "esto es un sensor, podés preguntarle la temperatura"; "esta acción no se puede ejecutar porque es peligrosa". → [[Ficha del dispositivo]]

## 2. Estado actual [▶ 01:21](https://www.youtube.com/watch?v=3hxdHem70gw&t=81s)
- Lo presentó [[Anthropic]] el **27 de agosto de 2026** (según el video), en colaboración con [[HHMI Janelia]].
- Es una *research preview* limitada, con laboratorios, empresas de robótica y fabricantes ([[Raspberry Pi]], [[Universal Robots]]).
- La idea es liberarlo como open source más adelante.
- El autor aclara que **no** significa que Claude pueda entrar a una fábrica y controlar todo: "estamos bastante lejos de eso".

## 3. El problema [▶ 02:08](https://www.youtube.com/watch?v=3hxdHem70gw&t=128s)
Las máquinas no hablan el mismo idioma. Cada fabricante tiene su [[API, SDK y protocolo|API, SDK o protocolo]], y conectar equipos exige [[Código pegamento]]. A una IA, además, no le alcanza con *enviar* la orden: tiene que *entender* qué significa, qué límites hay y qué puede ser peligroso. En el mundo físico, un error puede lastimar a alguien. → [[Interoperabilidad]]

## 4. Cómo funciona [▶ 05:02](https://www.youtube.com/watch?v=3hxdHem70gw&t=302s)
- La máquina sigue igual. Entre ella y la IA se pone un [[Driver MHS]] que traduce órdenes genéricas ([[Operaciones read y write|read / write]]) a lo que entiende cada equipo, sea [[Modbus]], una API o lo que tenga.
- Además de comandos, describe **características y restricciones** con etiquetas que pueden estar en lenguaje natural. → [[Ficha del dispositivo]]
- Puede usarse a través de [[Model Context Protocol (MCP)|MCP]], de la línea de comandos o desde código, y es [[Model agnostic]].

## 5. Experimentos [▶ 10:10](https://www.youtube.com/watch?v=3hxdHem70gw&t=610s)
- [[Automatización de laboratorio - curva de dilución]]: 4 equipos en 3 computadoras, automatizados en 8 horas en lugar de semanas.
- [[Alineación de un láser con cámara]]: Claude prueba, mira y corrige, y al final deja un **script determinista**.
- [[QuEra - recuperación del clock del láser]]: el script que generó Claude recupera el clock en el 99,3 % de los casos (695 de 700), contra el 58 % del script humano.
- [[Líquidos viscosos y burbujas]]: la limitación, porque le falta intuición física.

## 6. Dónde queda la IA [▶ 13:25](https://www.youtube.com/watch?v=3hxdHem70gw&t=805s)
La IA **no controla cada milisegundo**. Trabaja en una capa superior: prueba, ajusta y genera [[Código determinista]]. El [[PLC]], el variador y el control en tiempo real siguen abajo. → [[Capas de control]]

## 7. Seguridad [▶ 17:40](https://www.youtube.com/watch?v=3hxdHem70gw&t=1060s)
Se pueden declarar límites e [[Interlock|interlocks]] para que la seguridad no dependa de que la IA recuerde una instrucción. Aun así, los modelos "saben mucho del mundo físico sin comprenderlo". → [[Razonamiento físico]]

## 8. Limitaciones [▶ 21:23](https://www.youtube.com/watch?v=3hxdHem70gw&t=1283s)
- Hace falta una [[Interfaz digital]]: una máquina de hace 40 años sin electrónica no se puede controlar sin antes modificarla.
- No se sabe si la industria lo va a adoptar. Le pasa lo mismo que al [[USB]]: solo sirve si todos lo implementan. → [[Adopción del estándar]]

## 9. Conexión con IoT [▶ 22:43](https://www.youtube.com/watch?v=3hxdHem70gw&t=1363s)
Es el problema de siempre del IoT: miles de dispositivos distintos que tienen que convivir. Un agente podría tener un "mapa de capacidades" y [[Orquestación|orquestar]] cámara, robot, sensor y máquina. Ya hay movimientos en esa dirección: [[Hugging Face]] con LeRobot y [[Raspberry Pi]] con un driver para sus cámaras.

## 10. Conclusión del autor [▶ 27:21](https://www.youtube.com/watch?v=3hxdHem70gw&t=1641s)
La evolución fue de modelos que **hablan**, a modelos que **usan herramientas**, a **agentes que hacen cosas**, y el paso siguiente es el **mundo físico**. Para el autor, la IA en lo físico va a pasar "no tanto por quitar toda la tecnología que tenemos, sino por que la IA entienda mucho mejor las capas que ya tenemos".
