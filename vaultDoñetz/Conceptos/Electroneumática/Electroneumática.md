---
tipo: concepto
area: electroneumática
tags: [electroneumática]
---

# Electroneumática

## Por qué pasar de neumática a electroneumática
- La neumática pura **no puede detectar** propiedades como el color o el material (metal vs. plástico o madera) ni el magnetismo. Los sensores que lo hacen son **electrónicos** y necesitan señal eléctrica.
- Permite automatizar máquinas con movimientos más complejos.

## Dos energías
1. **Neumática**: aire comprimido (compresor → [[Unidad de mantenimiento FRL]]). Mueve los actuadores.
2. **Eléctrica**: una **fuente de 24 V de continua**, alimentada desde 220 V de alterna. Alimenta el mando: emisores, relés y solenoides.

## La electroválvula
Es el **conversor de señales**: transforma una señal eléctrica (energiza el solenoide `1Y1`) en una señal neumática (la válvula conmuta). Es obligatoria: un contacto eléctrico nunca se conecta directo a un actuador. Ver [[Electroválvulas monoestables y biestables]].

## Símbolo del solenoide en el plano eléctrico
Rectángulo con una diagonal, dos conexiones y dos flechitas (una hacia arriba y otra hacia abajo). Lleva el **mismo nombre** que en el plano neumático (`1Y1`): es "como si hubiera un cable" entre los dos planos.

## Reglas eléctricas que repite
- **Bobinas siempre en paralelo**, nunca en serie: en serie se repartirían los 24 V (12 V cada una) y no funcionarían.
- Nunca alimentar al mismo tiempo los dos cabezales de una biestable → [[Superposición de señales]].

## Temas
[[Contactos eléctricos]] · [[Enclavamiento eléctrico]] · [[Autorretención]] · [[Circuito de sensado]] · [[Relés temporizados]] · [[Mando directo e indirecto]] · [[Método intuitivo]]
