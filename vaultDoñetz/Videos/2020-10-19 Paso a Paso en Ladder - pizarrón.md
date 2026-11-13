---
tipo: video
fecha: 2020-10-19
url: https://www.youtube.com/watch?v=Ly56JfIn3xM
duracion: "31:50"
vistas: 23537
area: plc
capitulos: [Inicio, Memorias PLC, Paso a Paso, Columnas imaginarias, Habilitación, Acciones, Memorias, Continuidad de los pasos]
---

# Ejercicio electroneumático con método Paso a Paso en Ladder (pizarrón)

Ejemplo para la última actividad del año. Es el único video con **capítulos**.

## Ejercicio
2 actuadores con **monoestables**, 4 rodillos, `PM`/`PP`. `H1` es una lámpara de **220 Vca** en otra salida: demuestra que las salidas a relé admiten otra tensión.
Fases: `1A−` · T1 · `1A+` · `2A+` · `2A−` → 5 pasos, memorias `M1…M5`.

## Método
- Tres **columnas imaginarias**: habilitación · condición · acciones.
- Acciones: movimiento (`S`/`R` de salidas, `TT1`) + `S` del paso siguiente + `R` del paso anterior.
- **`M1` con lógica negativa** (contacto NC) para que el paso 1 esté habilitado al arrancar; el paso 2 hace `S M1` y el último hace `R M1`.
- Con `S Q1` el cabezal monoestable queda memorizado; para que vuelva, `R Q1`.
- "El último paso queda con todas bobinas reset."
- Es seguro y repetitivo: no es el programa más corto, pero **sale funcionando**.

## Conceptos
[[Paso a paso en Ladder]] · [[Método paso a paso]] · [[Set y Reset]] · [[PLC]]

Simulación: [[2020-10-20 Paso a Paso en Ladder - simulación]]
