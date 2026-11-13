---
tipo: concepto
area: plc
tags: [plc]
---

# PLC (Controlador Lógico Programable)

## Partes y conexión (modelo didáctico que usa el profe)
- Se alimenta con **24 V de continua** (borne + y −/común). Hay modelos con otras tensiones.
- **Entradas digitales `I1…I6`** (*input*): ahí van los **emisores de señal** (pulsadores, interruptores, rodillos, sensores). Con 24 V en el borne la entrada vale **1**; sin tensión, **0**.
- **Salidas `Q1…Q4`**: se usa la **Q** porque la **O** (*output*) se confunde con el cero. Ahí van las cargas: cabezales de electroválvulas, lámparas, bobinas de relés o contactores, motores, resistencias.
- **Salidas a relé:** cada salida tiene **dos bornes** y adentro un contacto NA de un relé interno. Por eso cada salida puede manejar **otra tensión**. Ejemplo: `Q1` y `Q2` con 24 Vcc para los cabezales y `H1` (lámpara de 220 Vca) en otra salida, aislada por el relé.
- Configuración típica de los modelos chicos: 6 entradas y 4 salidas (hoy suelen ser 8 entradas).
- **Memorias o marcas `M`** (por ejemplo `MA`, `M1`): son como bobinas **sin conexión física**, internas al programa. Se usan igual que una salida.

## Dirección y símbolo
- **Dirección:** el nombre interno (`I1`, `Q2`, `M1`).
- **Símbolo / comentario:** el nombre del elemento externo conectado (`0S1`, `1Y1`). En [[Zelio Soft 2]] se carga como comentario (aparece en un sobrecito).

## Sin programa no hace nada
Con todo conectado pero sin programa cargado y "en marcha" (RUN), el PLC no actúa.

## Ventaja en electroneumática
La conexión de las salidas **reemplaza al circuito de fuerza**: al activar `Q1` en el programa ya se alimenta el cabezal.

## Relacionado
[[Lenguaje Ladder]] · [[Set y Reset]] · [[Temporizadores en PLC]] · [[Lógica positiva y negativa]]
