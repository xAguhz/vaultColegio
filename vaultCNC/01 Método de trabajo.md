---
tipo: método
tags: [metodo, cnc]
---

# Método de trabajo del curso

Así se arma una pieza en la materia. Lo sacamos de la carpeta digital y de los dos TP.

## Paso a paso

1. **Dibujo de la pieza.** Plano A4 vertical, escala 1:1, normativa IRAM-ISO, con vistas y cotas de diámetros, radios y longitudes. Lleva el [[Rótulo EEST3]].
2. **Tabla de coordenadas del contorno.** Se pasa el perfil a puntos (X, Z) recorriendo de la punta hacia la base. Recordá que **X es diámetro** y Z es negativo hacia la base. Los arcos llevan radio y sentido (G02 o G03).
3. **Hoja de proceso.** Tabla con: Operación N°, Parámetros (Vc, avance), Herramientas y Esquema de proceso (un dibujo de la pieza por operación). Tiene su propio rótulo (ver [[Rótulo EEST3]]).
4. **Elección de herramientas.** Se elige según la operación, el material y las dimensiones, con el catálogo **Kennametal Universal**: portaherramienta, inserto, página del catálogo, Vc y avance. Ver [[Herramientas y plaquitas]].
5. **Programa.** Cero pieza (G54), herramienta (T), G96 con S, aproximación, ciclos ([[Ciclos G90 G94 G71 G72 G70 G74]]), retiro y M30. Ver [[Estructura de un programa]].
6. **Simulación.** Se corre el programa en el simulador y se saca una captura por herramienta (T0101, T0303, T0505...). Ver [[Torno y control]].
7. **Informe.** Se junta todo en el documento final (ver abajo).

> [!tip] Antes de elegir un valor de tabla
> Cuando el catálogo da un rango (Vc, avance), mirá el rango entero y elegí con criterio; no tomes el primer número que ves.

## Orden de operaciones que se repite

| Op | Operación | Ciclo o G | Herramienta típica |
|---|---|---|---|
| 1 | Desbaste exterior | G90 (como en los TP) | T0101 |
| 2 | Terminación / diagonales y radios | G01-G03 | T0303 |
| 3 | Ranurado | G94 | T0505 o T1111 |
| 4 | Terminación lado derecho | G01-G03 | T0909 |
| 5 | Terminación lado izquierdo | G01-G02 | T1010 |
| 6 | Tronzado | G01 | T1111 |

> [!note] Desbaste con G90
> En los TP el desbaste se hace con G90 (pasadas a mano) y no con G71. Se decidió seguir así en los TP nuevos.

## Estructura del informe (TP Alfil)

1. **Carátula**: trabajo práctico, taller, profesor, alumno, curso, escuela y fecha.
2. **Rótulo de la hoja de proceso** (escuela, materia, material; estudiante, tema, fecha de presentación).
3. **Hoja de proceso**: tabla de operaciones con parámetros, herramientas y esquema de proceso.
4. **Programación CNC**: el programa completo.
5. **Aclaraciones**: significado del código de forma (3 o 4).
6. **Características de la pieza**: nombre, material, bruto, punto cero, torno, manual y velocidades de torneado y ranurado.
7. **Una hoja por herramienta** con la captura del catálogo y sus características (T0101, T0303, T1111, T0909/T1010).
8. **Herramientas usadas**: portaherramientas e insertos con página del catálogo.
9. **Capturas de catálogo** de cada herramienta.

> [!info] Decisión
> Cada TP nuevo lleva informe completo con esta estructura. El informe del Alfil no incluye teoría de códigos G/M ni descripción del torno: eso queda en las notas de este vault.

Ver también: [[TP Peón]], [[TP Alfil]], [[Fórmulas de corte]].
