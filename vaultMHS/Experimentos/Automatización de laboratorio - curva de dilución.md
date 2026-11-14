---
tipo: experimento
tema: MHS
aliases: [curva de dilución, experimento del laboratorio, 8 horas]
relacionado: ["[[Driver MHS]]", "[[Orquestación]]", "[[ActiveX y COM]]", "[[Código pegamento]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["10:10", "10:43", "11:31", "12:06"]
estado: segun-el-video
datos_clave: {equipos: 4, computadoras: 3, horas: 8, alternativa_tradicional: "varias semanas", velocidad_vs_manual: "3x"}
tags: [experimento]
---
# Automatización de laboratorio: curva de dilución

## Objetivo [▶ 10:10](https://www.youtube.com/watch?v=3hxdHem70gw&t=610s)
Automatizar un experimento de laboratorio coordinando:
| Equipo | Cómo se controlaba |
|---|---|
| Brazo robótico | Un sistema que **recibía archivos** |
| Manipulador de líquidos | Interfaz antigua de [[ActiveX y COM]] |
| Lector de placas | **Sin API moderna**: había que manejar una interfaz gráfica |
| Varias cámaras | — |

Todo repartido en **3 computadoras distintas**.

> Analogía del video: es como automatizar tu casa si para prender cada lamparita necesitás una app distinta: una marca funciona mandando archivos, otra solo con botones en pantalla y otra con comandos completamente distintos. [▶ 10:43](https://www.youtube.com/watch?v=3hxdHem70gw&t=643s)

## Solución [▶ 11:31](https://www.youtube.com/watch?v=3hxdHem70gw&t=691s)
1. Un [[Driver MHS]] por equipo, como traductor hacia la capa común.
2. Una capa de [[Orquestación]] encima.
3. Un agente que trabaja con todo el proceso sin tratar cada máquina como un mundo aparte.

## Resultado [▶ 11:31](https://www.youtube.com/watch?v=3hxdHem70gw&t=691s)
- De "equipos listos pero sin automatizar" a una **curva de dilución completa en 8 horas**.
- Dentro de esas 8 horas hubo una **repetición autónoma** del experimento.
- Según el equipo, con el enfoque tradicional (un proveedor que integra) habría llevado **varias semanas**.
- Las pruebas indican que el proceso podría ser **3 veces más rápido que hacerlo a mano**.

## Advertencia del autor [▶ 12:06](https://www.youtube.com/watch?v=3hxdHem70gw&t=726s)
> "Esto no significa que cualquiera vaya a pasar de tres meses de integración a horas." Es un experimento concreto, con máquinas concretas, y los datos salen de la presentación del propio proyecto.
