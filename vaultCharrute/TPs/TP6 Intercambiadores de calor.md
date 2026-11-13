---
tipo: tp
materia: Sistemas Mecánicos
profesor: Charrute
numero: 6
tema: Intercambiadores de calor
consigna: 2026-09-04
entrega: 2026-09-18
modalidad: grupal (investigación de 2 semanas + caso obligatorio + exposición)
tags: [tp, intercambiadores, transferencia-de-calor, fouling]
---

# TP6 · Intercambiadores de calor

> [!abstract] En una línea
> El intercambiador **no crea calor ni frío**: facilita que la energía térmica pase de una corriente caliente a una fría, **sin mezclarlas**. Para saber si anda bien hacen falta **cuatro temperaturas**, el caudal y la **caída de presión**.

Anterior: [[TP5 Tanques y recipientes a presión]] · Siguiente: [[TP7 Bombas industriales]]

## Consigna (resumida)
Investigación grupal del tema completo, sin repartir tipos entre grupos, con dos semanas de plazo.
1. Principio físico. Intercambio **directo** e **indirecto**.
2. Comparar **carcasa y tubos** con **placas**: tamaño, mantenimiento, limpieza, presión y temperatura, fluidos, ensuciamiento y aplicaciones. Ventajas y límites de cada uno respecto del otro, no solo una descripción.
3. Flujo **paralelo**, **contracorriente** y **cruzado**: por qué cambia el resultado térmico.
4. Variables para evaluar el funcionamiento: temperaturas de entrada y salida, caudal y caída de presión.
5. Sección específica de **ensuciamiento (fouling)**: qué es, por qué baja la transferencia, cómo sube la caída de presión e importancia de la limpieza.
6. **Corrosión, fugas y contaminación cruzada**: por qué una falla interna puede ser peor que una pérdida visible.
7. **Caso obligatorio:** *un intercambiador calentaba bien el agua; después de meses baja la temperatura de salida y **sube** la diferencia de presión entre la entrada y la salida.* Dar al menos 3 causas, qué información pedir antes de intervenir y un orden lógico de revisión.
8. Al menos **4 fuentes**: una de un fabricante y otra de bibliografía, norma o institución técnica.

## Teoría clave del apunte
- **Mecanismos:** **convección** del fluido caliente a la pared → **conducción** a través de la pared → **convección** de la pared al fluido frío.
- **Indirecto** (placas, carcasa y tubos): los fluidos no se mezclan. **Directo** (torre de enfriamiento): hay contacto.
- **Cuatro temperaturas:** entrada y salida del fluido caliente, entrada y salida del frío.
- **Q = m · cp · ΔT:** el calor depende de *cuánto* fluido pasa y de *cuánto* cambia su temperatura. Con las mismas temperaturas y distinto caudal se transfiere otra cantidad de calor.
- **Superficie:** más área transfiere más, pero también suma pérdida de presión, tamaño, costo y dificultad de limpieza.
- **Disposición del flujo:**
  - **contracorriente** > paralelo: mantiene una diferencia de temperatura útil a lo largo de todo el equipo;
  - **cruzado** en radiadores y equipos aire–líquido.
- **Carcasa y tubos:**
  - haz de tubos, placas tubulares, cabezales y **deflectores** (dirigen el flujo y sostienen los tubos);
  - **pasos** (más velocidad: mejor transferencia, pero más ΔP);
  - qué fluido va por los tubos se decide por presión, corrosión, suciedad y limpieza.
- **Placas:**
  - placas corrugadas con canales alternados y **juntas**;
  - muy compacto, se puede abrir para limpiar y se pueden agregar o quitar placas.
- **No hay un tipo "mejor":** "transfiere más" no sirve si después no se puede limpiar, si el material no es compatible o si la ΔP es excesiva.
- **Caudal y velocidad:**
  - poca velocidad: se ensucia y transfiere poco;
  - mucha velocidad: más ΔP y erosión.
- **Fouling:** depósitos (sarro, sedimentos, óxido, materia orgánica) que **agregan resistencia térmica** y **achican el paso**. Resultado: menos calor transferido **y** más esfuerzo de bombeo.
- **Corrosión interna:**
  - una perforación comunica los dos circuitos;
  - el fluido de **mayor presión entra en el de menor presión** y lo contamina.
- **Expansión térmica:** partes a distinta temperatura generan esfuerzos.
- **Cambios de fase:** condensadores y evaporadores intercambian mucha energía sin cambiar la temperatura del mismo modo.
- **Instrumentación:** temperatura en las 4 bocas, presión de entrada y salida (para la ΔP), caudal y una **válvula de control** que regula la temperatura de salida.
- **Diagnóstico:** antes de decir "está roto", revisar:
  - la temperatura y el caudal del fluido caliente;
  - las válvulas;
  - la suciedad;
  - el caudal del fluido frío;
  - los instrumentos.
- **Recuperación de calor:** una corriente caliente de descarte puede precalentar otra, y así se ahorra energía.
- **Normas:** **TEMA** para el diseño mecánico de los tubulares; código de recipientes a presión si corresponde.

## Resolución del caso obligatorio (guía de estudio)
> [!note] Resuelto a partir de la teoría del profe
> Las entregas del grupo están en PDF **escaneados (sin texto)** y no se pudieron leer automáticamente. Esta resolución sale del apunte. Ver [[#Archivos en Drive]].

**Síntomas:** baja la temperatura de salida del agua **y** sube la ΔP. Que aparezcan **los dos juntos** apunta a algo que **achica el paso y aísla térmicamente**.

| # | Causa posible | Por qué encaja |
|---|---|---|
| 1 | **Ensuciamiento o incrustaciones (fouling)** del lado del agua: sarro por dureza del agua | Agrega resistencia térmica (menos calor) y reduce la sección (más ΔP). Es la causa más probable |
| 2 | **Filtro, válvula o canal parcialmente obstruido** (sedimentos, juntas desplazadas en placas) | Más restricción, más ΔP y distribución desigual del flujo |
| 3 | **Aumento del caudal de agua** (cambió la demanda o una válvula de regulación) | Más caudal da más ΔP y menos tiempo de contacto, así que sale más fría |
| 4 | **Menos aporte del fluido caliente** (baja temperatura de entrada o poco caudal) | Explica la caída térmica, aunque **no** la suba de ΔP del lado del agua |

**Información que pediría antes de abrir el equipo:**
- las 4 temperaturas actuales comparadas con las de diseño o las del arranque;
- los caudales de ambas corrientes;
- la ΔP de cada lado y su evolución en el tiempo;
- la calidad del agua (dureza);
- el historial de limpieza;
- cambios recientes en la planta;
- la calibración de los instrumentos.

**Orden lógico de revisión:**
1. Instrumentos (que la lectura sea real).
2. Válvulas y filtros.
3. Caudales.
4. Condiciones del fluido caliente.
5. Tendencia de la ΔP.
6. Recién entonces, **abrir y limpiar** (química o mecánica) e inspeccionar si hay corrosión o fugas internas, con una prueba de estanqueidad entre circuitos.

## Archivos en Drive
- Teoría: `Intercambiadores de calor_26.docx`
- Consigna: `TI GrupalINTERC DE CALOR_26.docx`
- Entregas del grupo (carpeta *Charrute*, PDF escaneados): `tp6 charrute.pdf`, `tp6 charrute estudio.pdf`, `tp6 charrute investigación.pdf`
- Fuente usada: `Heat_Exchanger_Engineering.pdf`

## Ver también
[[Intercambiador de calor]] · [[Caldera]] · [[Variables de proceso]] · [[Pérdidas de carga]] · [[00 Inicio]]
