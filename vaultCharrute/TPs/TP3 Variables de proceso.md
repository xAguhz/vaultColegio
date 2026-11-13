---
tipo: tp
materia: Sistemas Mecánicos
profesor: Charrute
numero: 3
tema: Variables de proceso e instrumentación básica
consigna: 2026-05-14
entrega: 2026-06-05
modalidad: grupal (Parte A 10 preguntas de análisis + Parte B sistema elegido + Parte C oral)
sistema_elegido: aire comprimido
tags: [tp, variables, instrumentación]
---

# TP3 · Variables de proceso e instrumentación básica

> [!abstract] En una línea
> Ya no alcanza con saber *qué equipo hay*: hay que saber **bajo qué condiciones el sistema funciona bien**. Que el fluido circule es necesario, pero **no suficiente**.

Anterior: [[TP2 Equipos de un proceso]] · Siguiente: [[TP4 Cañerías y válvulas]]

## Consigna (resumida)
- **Parte A – 10 preguntas de análisis.** Son casos, no definiciones:
  1. Las herramientas neumáticas tienen poca fuerza: ¿qué variable se mira primero?
  2. El agua llega, pero el resultado del calentamiento no es el esperado.
  3. La bomba no da el servicio: ¿por qué no alcanza con mirar solo la bomba?
  4. Dos procesos con una válvula y un recipiente: ¿qué falta saber para compararlos?
  5. Un equipo bien elegido y aun así un proceso que no funciona.
  6. La presión es crítica en un sistema y no en otro.
  7. Diferencia entre "trabaja con agua" e "importa el caudal".
  8. Un tanque que no impulsa ni calienta, pero es decisivo.
  9. "Si el fluido circula, el proceso funciona bien": ¿verdadero o falso?
  10. Por qué las variables cambian la manera de ver los sistemas.
- **Parte B:** elegir un sistema y fundamentar su variable principal, el instrumento asociado y qué problema se detecta si el valor no es el adecuado. Con un esquema simple, sin P&ID.
- **Parte C (oral):** "¿Qué cambió en la forma de analizar el sistema entre el trabajo de equipos y este trabajo de variables?"

## Ideas clave
- Las **[[Variables de proceso]]** (presión, temperatura, caudal, nivel) dicen si el proceso cumple su objetivo, no solo si está armado.
- **No hay una variable "más importante" en general:** depende del objetivo del sistema. En aire comprimido manda la presión; en calentamiento de agua, la temperatura; en un tanque de alimentación, el nivel.
- **Mirar el sistema completo:** una bomba sana puede fallar en el servicio por nivel bajo en el tanque (cavitación), una válvula cerrada aguas arriba o una cañería obstruida.
- **"Equipo bien elegido" no es lo mismo que "proceso que funciona":** el equipo no falla; falla el sistema porque las variables están fuera de rango.

## Nuestra resolución
### Parte A, en resumen
| # | Caso | Respuesta del grupo |
|---|---|---|
| 1 | Herramientas con poca fuerza | **Presión**, con un manómetro cerca de las herramientas. Causas posibles: fugas, compresor que no llega, tanque con poca carga o regulador mal ajustado |
| 2 | Calentamiento que no rinde | **Temperatura** a la salida del intercambiador o la caldera. Causas: poca fuente de calor, incrustaciones o caudal excesivo (falta tiempo de residencia) |
| 3 | La bomba no da servicio | Revisar el conjunto: nivel del tanque (cavitación), válvulas de aspiración e impulsión, cañerías y presiones |
| 4 | Válvula + recipiente en dos procesos | Hace falta la presión de trabajo, el caudal, el tipo de fluido, la función de la válvula y la temperatura |
| 5 | Equipo bien elegido que no anda | Las condiciones de operación (por ejemplo, la presión de aspiración) también tienen que ser correctas |
| 6 | Presión crítica o secundaria | Depende del objetivo: crítica en aire comprimido, secundaria en calentamiento de agua |
| 7 | "Trabaja con agua" e "importa el caudal" | Lo primero describe el **fluido**; lo segundo, la **variable** que define si el equipo cumple su función |
| 8 | Un tanque decisivo | Como reserva o *buffer*, como pulmón que estabiliza la presión y como lugar de decantación o separación |
| 9 | "Si circula, funciona" | **Falso**: circular es necesario, pero no suficiente |
| 10 | Qué cambian las variables | El análisis pasa de **descriptivo** a **funcional y cuantitativo** |

### Parte B · Aire comprimido
- **Variable principal:** la **presión**. Toda la capacidad de trabajo se transmite por la presión. El caudal varía con la demanda.
- **Instrumento:** el **manómetro**, a la salida del compresor, en el tanque pulmón y en las bajadas de consumo. En sistemas más avanzados se usan transmisores de presión conectados al control.
- **Problemas que se detectan:**
  - Presión **baja**: poca fuerza y actuadores que no completan la carrera.
  - Presión **alta**: fugas en las juntas, desgaste y disparo de válvulas de seguridad.
  - Presión **variable**: fugas o un compresor que no alcanza para la demanda.

```mermaid
flowchart LR
  C[Compresor<br/><small>genera presión</small>] --> T[("Tanque pulmón<br/><small>[M1] manómetro</small>")] --> R[Válvula reguladora<br/><small>ajusta la presión de trabajo</small>] --> U(["Punto de uso<br/><small>[M2] manómetro</small>"])
```

### Parte C · Idea para el oral
> Antes analizábamos **los equipos** (*¿qué hay y para qué está?*, un análisis estructural). Ahora analizamos **el comportamiento del proceso a través de sus variables** (*¿bajo qué condiciones funciona bien?*). Los mismos equipos se evalúan por lo que hacen con las variables, no por lo que son.

## Archivos en Drive
- Consigna: `TP3 _26.docx`
- Entrega: `TP3_Variables_de_Proceso` (Google Docs, 05/06/2026)

## Ver también
[[Variables de proceso]] · [[Sistema de aire comprimido]] · [[Bomba]] · [[Tanque]] · [[00 Inicio]]
