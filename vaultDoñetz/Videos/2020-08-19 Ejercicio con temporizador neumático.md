---
tipo: video
fecha: 2020-08-19
url: https://www.youtube.com/watch?v=WQohFv4CnQE
duracion: "21:50"
vistas: 7019
area: neumática
---

# Ejercicio resuelto: 1 actuador con temporizador neumático

## Ejercicio
Doble efecto, ciclo continuo, 3 fases: **avanza → espera 5 s (`T1`) → retrocede**.

## Resolución
- Estranguladoras `1V1` (avance, adelante) y `1V2` (retroceso, atrás); válvula de mando `1V3`.
- Fase 1: `0S1` (interruptor) AND `1S1` (pisado) → [[Válvula lógica AND]] `1V4` → `14 de 1V3`.
- Fase 2: `1S2` → entrada **12 del temporizador** `1V5`.
- Fase 3: salida del temporizador → `12 de 1V3` (retrocede).
- La AND y el temporizador van a la misma altura (procesamiento) y se nombran de izquierda a derecha.

## Funcionamiento del temporizador
Estrangulador con antirretorno + tanquecito + 3/2 NC pilotada. El aire primero llena el tanque, y cuando la presión vence al resorte conmuta. Al soltarse `1S2`, el tanque se vacía por el antirretorno. Ver [[Temporizador neumático]].

## Conceptos
[[Temporizador neumático]] · [[Válvula estranguladora]] · [[Válvula lógica AND]] · [[Nomenclatura ISO 1219]]
