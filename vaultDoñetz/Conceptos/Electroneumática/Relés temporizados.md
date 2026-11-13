---
tipo: concepto
area: electroneumática
tags: [electroneumática, temporizador]
---

# Relés temporizados

Reemplazan al [[Temporizador neumático]] en electroneumática. Se usan para las fases de **pausa**.

## Retardo a la conexión (el más común)
- Cuenta el tiempo **mientras la bobina recibe señal** (señal positiva). Al terminar, conmuta sus contactos.
- Su NA (17-18) **alimenta** la fase siguiente; su NC **desconecta** una autorretención.
- La bobina tiene que **seguir alimentada** todo el tiempo de conteo.

## Retardo a la desconexión
- Al recibir señal **conmuta enseguida**. Empieza a contar cuando **se le corta** la señal y, al terminar, vuelve a reposo.
- Sirve para trabajar con **lógica negativa**: por ejemplo, con un rodillo conectado como NC, que *corta* la señal al pisarse. Ver [[Lógica positiva y negativa]].

## Contactos
Combinados (NA y NC). Se dibujan con un paréntesis en el accionamiento. Numeración en [[Contactos eléctricos]].

## En el diagrama
Se anota `T1` o directamente el relé (`K2`, `K6`). Si se usa `K1` en la fase 1, el temporizado de la fase 2 suele ser `K2`.

## Equivalente en PLC
[[Temporizadores en PLC]] (`TT1`, función A).
