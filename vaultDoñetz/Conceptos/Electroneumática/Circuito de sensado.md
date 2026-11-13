---
tipo: concepto
area: electroneumática
tags: [electroneumática, sensores]
---

# Circuito de sensado

Es la primera parte del plano eléctrico.

## Sensores de proximidad
- Suelen ser de **3 hilos**: +24 V, 0 V y la salida de señal.
- Símbolo: rombo/cuadro con un contacto NA (si es de **lógica positiva**) y una bobina dibujada si es **inductivo** (detecta metales). También hay capacitivos y de color.
- La salida se conecta a la **bobina de un relé auxiliar** (`KA` para `1B1`, `KB` para `2B2`…). Después, en el circuito, en lugar del sensor se usan **contactos de ese relé**.
- Si el sensor detecta desde el arranque, su relé **arranca energizado** (se marca con un puntito y sus NA con un arquito).

## Rodillos con relé auxiliar
Un rodillo tiene **un solo contacto**. Si su señal hace falta en varias partes del circuito (por ejemplo, porque el actuador **repite movimiento** y lo pisa dos veces por ciclo), se lo conecta a un relé auxiliar para tener **varios contactos**. Ver [[2020-08-24 Paso a Paso con monoestables y repetición]].

## Ahorro de relés
Si la única función de un sensor es disparar un temporizador, el sensor puede alimentar **directamente** al relé temporizado (así lo hace en [[2020-04-20 Repaso EN 2 - Resolución del circuito eléctrico]]).
