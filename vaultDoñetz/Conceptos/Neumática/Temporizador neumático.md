---
tipo: concepto
area: neumática
tags: [neumática, temporizador]
---

# Temporizador neumático

Es un **grupo de válvulas** que se comporta como un solo elemento. Se usa cuando en una fase **no hay movimiento** (una pausa), así que ningún rodillo puede dar la señal siguiente.

## Composición
1. **Válvula estranguladora con antirretorno** ([[Válvula estranguladora]]): regula el caudal de entrada.
2. **Pequeño acumulador** (tanquecito).
3. **Válvula 3/2 NC** con accionamiento **neumático** y retorno a resorte.

Todo va encerrado en una línea de **raya y punto** (así lo pide la norma).

## Conexiones
`1` (presión), `2` (salida) y `12` (señal de comando). A diferencia de una 3/2 común, cuando llega señal a 12 **cuenta un tiempo** y recién después conecta 1 con 2.

## Funcionamiento
1. Entra señal por 12 → pasa por el estrangulador (pasa poco aire).
2. El aire tiene dos caminos: conmutar la 3/2 (tiene que vencer el resorte) o llenar el tanque (que al principio está vacío y opone menos resistencia). Elige **el tanque**.
3. A medida que el tanque se llena, sube la presión. Cuando cuesta más entrar al tanque que vencer el resorte, **conmuta la 3/2** y sale la señal.
4. Al cortarse la señal, el antirretorno deja escapar el aire y el tanque se vacía.

El tiempo se ajusta con el tornillo del estrangulador.

## En el plano
Va a la misma altura que la [[Válvula lógica AND]] (procesamiento de señales) y se nombra como una válvula más (por ejemplo `1V5`). En el diagrama se marca `T1`.

## Equivalentes
Eléctrico: [[Relés temporizados]]. PLC: [[Temporizadores en PLC]].

## Videos
[[2020-08-19 Ejercicio con temporizador neumático]]
