---
tipo: referencia
tags: [planos, rotulo, freecad]
---

# Rótulo EEST3

Cajetín de los planos de los TP. Medidas tomadas sobre el plano del [[TP Peón]] (error de unos 0,3 mm); el rótulo del [[TP Alfil]] es igual.

## Hoja y marco
- Hoja **A4 vertical**, 210 x 297 mm. Origen de las medidas: esquina superior izquierda, con Y hacia abajo.
- Borde fino de la hoja (210 x 297).
- Marco interior grueso: X de 25 a 200 e Y de 10 a 287 (margen izquierdo de 25 mm para encuadernar, los otros tres de 10 mm).
- El rótulo ocupa el pie del marco: X de 25 a 200 (175 mm), Y de 227 a 287 (60 mm). Las líneas son gruesas.

## Líneas
- Verticales (X, mm): **25, 51, 66, 79, 99, 145, 200**.
- Horizontales (Y, mm): **227, 232, 237, 242, 247, 267, 277, 287**.

## Celdas

| Celda | X (mm) | Y (mm) | Contenido |
|---|---|---|---|
| Observación | 25 a 51 | 227 a 287 | Texto "Observacion" arriba a la izquierda; el resto vacío |
| Etiquetas | 51 a 66 | 227 a 232 | Vacía |
| | | 232 a 237 | "Dibujo" |
| | | 237 a 242 | "Reviso" |
| | | 242 a 247 | "Aprobo" |
| | | 247 a 267 | "Escala" con "1:1" abajo, centrado |
| | | 267 a 277 | "Normativa IRAM-ISO" en dos líneas, texto chico |
| | | 277 a 287 | Vacía |
| Fecha | 66 a 79 | 227 a 247 | Encabezado "Fecha"; la fecha del dibujo en la fila Dibujo, texto más chico; Reviso y Aprobo vacías |
| Nombre | 79 a 99 | 227 a 247 | Encabezado "Nombre"; en cada fila el nombre abreviado (alumno en Dibujo, profe en Reviso y Aprobo) |
| Colegio | 99 a 200 | 227 a 247 | "E.E.S.TECNICA n°3" en una sola línea, muy grande |
| Título | 66 a 145 | 247 a 287 | Nombre de la pieza, centrado y grande |
| Curso | 145 a 200 | 247 a 267 | "CURSO: 6°1" |
| Lámina | 145 a 200 | 267 a 277 | "LAMINA: 1" |
| Nota | 145 a 200 | 277 a 287 | "NOTA:" (vacío después de los dos puntos) |

Debajo de la fila Aprobo (Y de 247 a 287) las columnas Fecha y Nombre se unen con la del título. Los textos de la columna derecha van alineados a la izquierda con una sangría de 1 mm.

## Fuentes
Sans-serif tipo Arial o Liberation Sans, normal y sin cursiva. Alturas aproximadas:

| Texto | Altura (mm) |
|---|---|
| "E.E.S.TECNICA n°3" | 12 |
| Título de la pieza | 14 |
| CURSO, LAMINA, NOTA | 4 |
| Etiquetas (Dibujo, Reviso, Aprobo, Escala, Fecha, Nombre, Observacion) | 3,5 |
| Nombres | 3,5 |
| Fecha del dibujo | 2,8 |
| "Normativa IRAM-ISO" | 2,5 |
| "1:1" | 3,5 |

No hay logo de la escuela. "n°3" va en minúscula. Los datos de cada pieza salen de la clave `rotulo` del JSON (ver `Piezas/FORMATO.md`).

## Segundo rótulo: hojas de proceso
Las hojas de proceso del informe llevan **otro formato** (no está medido en mm). Es una tabla con estos campos:

- ESCUELA DE EDUCACION SECUNDARIA TECNICA N°3
- DISEÑO Y PROCESAMIENTO MECANICO
- MATERIAL (SAE 4140)
- ESTUDIANTE y REVISADO POR
- TRABAJO PRACTICO (nombre de la pieza) y TEMA
- FECHA PRESENTACION

Debajo va la tabla OPERACIÓN N° | PARAMETROS | HERRAMIENTAS | ESQUEMA DE PROCESO. Cada hoja lleva el encabezado "TP: <pieza>" y un pie con el número de página, el nombre del alumno y "EEST3". La carpeta digital usa además "CARPETA DIGITAL CNC" arriba y el curso "6°1 ELECTROMECANICA" abajo.

> [!note] Cómo se usa
> El plano de proceso (el dibujo reducido para la hoja) lleva el mismo rótulo con otra escala, por ejemplo 1:1,5 en el Alfil.

Ver también: [[01 Método de trabajo]].
