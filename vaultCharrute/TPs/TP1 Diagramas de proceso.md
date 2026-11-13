---
tipo: tp
materia: Sistemas Mecánicos
profesor: Charrute
numero: 1
tema: Desarrollo de la ingeniería básica – Diagrama de proceso
consigna: 2026-03-20
entrega: 2026-03-27
modalidad: grupal (cuestionario + aplicación + exposición oral)
sistema_elegido: aire comprimido
tags: [tp, diagrama-de-proceso, ingeniería-básica]
---

# TP1 · Diagramas de proceso

> [!abstract] En una línea
> Aprender a **leer un proceso**: qué entra, qué sale, qué equipos participan, en qué orden y qué fluido circula. Es la base de todo lo que viene en la materia.

Anterior: — · Siguiente: [[TP2 Equipos de un proceso]]

## Consigna (resumida)
Trabajo grupal, una semana de plazo. Leer el apunte teórico de Classroom, resolver el cuestionario, hacer la aplicación y preparar una exposición oral corta.

- **Parte A – Cuestionario (12 preguntas, de menor a mayor dificultad):** qué es un proceso industrial, qué es la ingeniería básica, qué es y para qué sirve un diagrama de proceso, cuatro elementos que aparecen en él, diferencia con un plano constructivo o un layout, por qué muestra lo general y no los detalles, importancia de entradas, salidas y sentido de circulación, función de un equipo a elección, cómo funcionan los sistemas de aire comprimido y de bombeo o calentamiento de agua, y por qué el diagrama es base para el resto de la materia.
- **Parte B – Aplicación:** elegir un sistema (aire comprimido, bombeo de agua o calentamiento de agua), dibujar el diagrama, marcar fluido, equipos, entrada, salida, sentido y una variable importante, y explicar el funcionamiento en 8 a 12 líneas.
- **Parte C – Exposición:** presentar el sistema, mostrar el diagrama, recorrer el fluido y nombrar la función de cada equipo.

## Teoría clave del apunte
- **Proceso industrial:** conjunto ordenado de operaciones para transformar materias primas, transportar fluidos, transferir energía o producir un resultado útil.
- **Ingeniería básica:** la etapa inicial de un proyecto en la que se define *qué* se quiere hacer, con qué equipos, qué fluido circula, en qué secuencia y qué variables hay que controlar, antes de entrar en los detalles constructivos.
- **[[Diagrama de proceso]]:** representación gráfica **simplificada** de los equipos principales y del recorrido de materiales, fluidos o energía. Muestra el funcionamiento general, no las medidas ni el montaje.
- **Elementos:** equipos principales, líneas o corrientes, sentido de circulación (flechas), entradas y salidas, [[Variables de proceso|variables]] (presión, temperatura, caudal, nivel, velocidad).
- **Cómo leerlo, en 6 pasos:** tipo de proceso → fluido principal → equipos → recorrido → secuencia → variable importante.
- **No hay que confundirlo con:** el layout (dónde está cada cosa en la planta), el [[P&ID]] (cañerías e instrumentos con detalle) ni el plano constructivo (medidas, materiales, montaje).
- **Errores comunes:** tomarlo como un plano real, pensar los equipos aislados, no mirar el sentido del flujo, no distinguir entradas de salidas y no preguntarse qué aporta cada equipo.

Los tres sistemas de ejemplo del apunte se volvieron a usar en los TP1, TP2 y TP3:

| Sistema | Esquema |
|---|---|
| [[Sistema de aire comprimido]] | Aire ambiente → compresor → tanque pulmón → línea de distribución → herramienta neumática |
| [[Sistema de bombeo de agua]] | Tanque → bomba → cañería → válvula → punto de consumo |
| [[Sistema de calentamiento de agua]] | Tanque → bomba → intercambiador o calentador → línea de agua caliente → consumo |

## Nuestra resolución
**Sistema elegido: aire comprimido.**

```mermaid
flowchart LR
  A([Aire del ambiente]) --> C[Compresor] --> T[(Tanque pulmón)] --> L[Línea de distribución] --> H([Herramienta neumática])
```

| Elemento | Respuesta del grupo |
|---|---|
| Fluido de trabajo | Aire / aire comprimido |
| Equipos principales | [[Compresor]] y tanque pulmón |
| Entrada | Aire ambiente |
| Salida | Aire comprimido (energía neumática) |
| Sentido | De izquierda a derecha |
| Variable importante | 1) presión, 2) temperatura |

- **Equipo elegido para la pregunta 9:** [[Compresor]] **de tornillo**. Dos rotores giran en una carcasa, atrapan el aire y achican el espacio hasta comprimirlo. Trabaja de forma **continua**, y por eso es el más usado en la industria.
- **Diferencia entre diagrama, layout y plano constructivo:** el diagrama explica cómo funciona, el layout muestra dónde está cada máquina y el plano constructivo da medidas, materiales y detalles.
- **Entradas, salidas y sentido:** las entradas dicen de dónde viene el fluido (dónde empieza el proceso) y las salidas dónde termina. Sin el sentido de circulación no se sabe en qué orden van los equipos.
- **Por qué es la base de la materia:** dice qué fluido circula y por dónde, qué equipos hay y cómo trabajan, y desde ahí se arman estudios más detallados de cada componente.

> [!tip] Exposición
> Se armó una presentación en Google Slides para exponer (preguntas del cuestionario resumidas, una diapositiva por pregunta, y la Parte B con el diagrama).

## Archivos en Drive
- Consigna: `Trabajo Práctico Grupal N1.docx` (del profe)
- Teoría: `Introduccion a diagramas de proceso.docx` (del profe)
- Entrega: `TP N°1 CHARRUTE, DIAGRAMAS DE PROCESO` (Google Docs) y su `BORRADOR`
- Exposición: `Sis.Mecanicos Ola Gente Bonitya-1` (Google Slides)
- Organización: `Minigrupos Charrute`

## Ver también
[[Diagrama de proceso]] · [[Variables de proceso]] · [[Compresor]] · [[Tanque]] · [[00 Inicio]]
