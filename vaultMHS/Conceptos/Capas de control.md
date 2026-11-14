---
tipo: concepto
tema: MHS
aliases: [capa superior, arquitectura en capas, dónde va la IA]
relacionado: ["[[Código determinista]]", "[[PLC]]", "[[Orquestación]]", "[[QuEra - recuperación del clock del láser]]"]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
minutos: ["14:14", "16:52", "17:40", "24:58"]
estado: segun-el-video
tags: [concepto, central]
---
# Capas de control

La idea más importante del video para entender **dónde se ubica la IA**. [▶ 14:14](https://www.youtube.com/watch?v=3hxdHem70gw&t=854s)

```
┌───────────────────────────────────────────────┐
│ CAPA DE AGENTES (IA)                          │  analiza, supervisa, planifica,
│ lenta, flexible, no determinista              │  busca parámetros, escribe código
├───────────────────────────────────────────────┤
│ MHS (drivers + fichas)                        │  describe qué hay y qué se puede hacer
├───────────────────────────────────────────────┤
│ CONTROL (PLC, variadores, controladores RT)   │  rápido, predecible, determinista
├───────────────────────────────────────────────┤
│ MÁQUINA FÍSICA                                │
└───────────────────────────────────────────────┘
```

## Lo que NO es
> "Probablemente se nos viene a la cabeza ChatGPT decidiendo cada milisegundo hacia dónde tirar, moviendo el motor. Pero no tiene por qué funcionar así."

## Lo que sí es
- La IA **prueba, analiza resultados, busca buenos parámetros y desarrolla un procedimiento**.
- Esa solución se convierte en [[Código determinista]] (código tradicional) que corre sin la IA.
- El control rápido **sigue funcionando abajo**. [▶ 16:52](https://www.youtube.com/watch?v=3hxdHem70gw&t=1012s)

## Ejemplo: los frenos de un auto [▶ 16:52](https://www.youtube.com/watch?v=3hxdHem70gw&t=1012s)
No se le puede preguntar a un modelo de lenguaje cada vez que hay que aumentar un poco la presión de frenado. Hay funciones que tienen que ser **rápidas, predecibles y muy controladas**, y se quedan donde están.

## "No hace falta reemplazar un PLC por un modelo de lenguaje" [▶ 17:40](https://www.youtube.com/watch?v=3hxdHem70gw&t=1060s)
Un [[PLC]] sigue controlando la máquina y un variador sigue controlando el motor. MHS trabaja en otra capa.

## Analogía: el jefe de cocina [▶ 24:58](https://www.youtube.com/watch?v=3hxdHem70gw&t=1498s)
Coordina, decide qué plato preparar, se fija si falta algo y organiza tareas, pero no reemplaza al horno, a la heladera, al cuchillo ni al cocinero. → [[Analogías]]

## Ver también
[[QuEra - recuperación del clock del láser]] es el ejemplo más claro: Claude escribió el controlador, pero no es el controlador.
