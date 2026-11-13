---
tipo: software
tags: [software, plc, simulador]
---

# Zelio Soft 2 (Schneider Electric)

- Software de programación y simulación de los relés programables **Zelio Logic**. Al principio el profe usa una versión vieja **portable**; después la **5.3**, que se descarga de la web de Schneider (se.com).
- **Nuevo programa:** se elige el modelo. El más chico: 24 Vcc, **6 entradas digitales, 4 salidas a relé**, sin entradas analógicas, con pantalla y teclado, con reloj (RTC), y solo Ladder. Los modelos más nuevos también aceptan **bloques de función (FBD)**.
- Se puede ver el programa con **símbolos Ladder** o **eléctricos**.
- **Grilla:** 5 columnas de contactos, 1 columna de bobinas y comentario. Las filas son las líneas del programa.
- **Primero se cargan los comentarios** de entradas (`I`), salidas (`Q`), memorias (`M`) y temporizadores (`T`) con el nombre del elemento externo.
- Se arrastran los contactos y las bobinas. Un clic en una línea punteada la convierte en conductor. Para pasar un contacto de NA a NC: **botón derecho**.
- Las bobinas solo se pueden soltar en la última columna. Variantes: "activo en estado" (bobina común), `S` (set), `R` (reset), `TT` (comando de temporizador).
- **Simulación:** botón *S*, tablas de entradas y salidas, **RUN**. Los elementos activos se ponen en **rojo**. Las entradas se fuerzan con un clic.
- ⚠️ No mueve actuadores: hay que **llevar en la cabeza** en qué estado está cada rodillo.

## Videos
[[2020-09-03 PLC Ladder parte II - Zelio Soft]] · [[2020-09-03 Automatismo electroneumático en Ladder]] · [[2020-10-01 Cascada en Ladder - simulación]] · [[2020-10-20 Paso a Paso en Ladder - simulación]]
