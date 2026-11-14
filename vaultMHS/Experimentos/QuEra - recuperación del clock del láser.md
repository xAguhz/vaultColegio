---
tipo: experimento
tema: MHS
aliases: [QuEra, clock del láser, "99,3 %"]
relacionado: ["[[QuEra Computing]]", "[[Código determinista]]", "[[Capas de control]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["14:48", "15:24", "16:11", "16:52"]
estado: segun-el-video
datos_clave: {humano_experto: "5-10 min", script_previo_exito: "58%", script_previo_tiempo: "~150 s", script_claude_exito: "99,3% (695/700)", script_claude_tiempo: "10-14 s en los casos difíciles"}
tags: [experimento, central]
---
# QuEra: recuperación del clock del láser

## Contexto [▶ 14:48](https://www.youtube.com/watch?v=3hxdHem70gw&t=888s)
[[QuEra Computing]] hace computadoras cuánticas con **átomos neutros**. Usa láseres cuya **frecuencia tiene que mantenerse extremadamente estable**.
> Analogía: tener una radio siempre sintonizada justo en la misma frecuencia. Si te corrés, perdés la señal.

Cuando el sistema se desvía, puede **perder el "clock"**, y recuperarlo exige reajustar varias partes.

## Antes [▶ 15:24](https://www.youtube.com/watch?v=3hxdHem70gw&t=924s)
| Método | Éxito | Tiempo |
|---|---|---|
| Persona experta | — | 5 a 10 min |
| Script hecho por ingenieros (meses de trabajo) | ~58 % | ~150 s por intento |

## Qué le pidieron a Claude
**No** que se quedara a cargo del láser, sino que **desarrollara un programa** que resolviera el problema. Nada más.

Proceso: provocaban perturbaciones → el agente hacía cambios → corría el script → veía qué pasaba → modificaba el código. **Cientos de veces durante una noche.**

## Resultado [▶ 16:11](https://www.youtube.com/watch?v=3hxdHem70gw&t=971s)
Un **programa normal y determinista**, probado aparte con **700 perturbaciones**:
| | |
|---|---|
| Recuperaciones correctas | **695 de 700 (99,3 %)** |
| Tiempo en los casos difíciles | **10 a 14 s** (contra minutos de un humano) |

## La lección [▶ 16:11](https://www.youtube.com/watch?v=3hxdHem70gw&t=971s)
> "El dato más interesante no es solo el 99,3 %; es dónde queda la IA."

[[Claude]] **no controla cada microsegundo** del láser: participó en el **desarrollo del controlador**. Lo que queda funcionando sobre la máquina es un programa convencional, y el control ultrarrápido del láser sigue por debajo. [▶ 16:52](https://www.youtube.com/watch?v=3hxdHem70gw&t=1012s) → [[Capas de control]], [[Código determinista]]
