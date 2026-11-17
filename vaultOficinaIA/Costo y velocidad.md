---
tipo: análisis
actualizado: 2026-11-17
tags: [oficina-ia, costos]
---

# Costo y velocidad: cuándo conviene

## Precios por millón de tokens (API, noviembre 2026)
| Modelo | Entrada | Salida |
|---|---|---|
| Claude Opus 5.5 | US$ 4 | US$ 20 |
| Claude Sonnet 5.5 | US$ 2 | US$ 10 |
| Claude Haiku 5.5 | US$ 0,10 | US$ 0,50 |

Sonnet sale **la mitad** que Opus por token. Si usás un plan de suscripción en vez de la API, la lógica es la misma pero en "uso del límite" en vez de dólares.

## El detalle que cambia la cuenta
Cada agente **arranca de cero**: tiene que leer sus instrucciones, el `CLAUDE.md` y volver a buscar lo que necesita. Ese arranque cuesta tokens, y además el orquestador escribe el encargo y lee la respuesta. Entonces:

- **Conviene** cuando el agente hace mucho trabajo pesado (leer archivos grandes, correr pruebas, generar notas largas) que si no haría Opus.
- **No conviene** para tareas chicas: arrancar un agente puede costar más que hacer el cambio directamente.

## Ejemplo ilustrativo (números redondos, no medidos)
Tarea: revisar tres módulos grandes (~200.000 tokens de lectura) y escribir un resumen (~10.000 tokens).

| | Solo Opus | Oficina |
|---|---|---|
| Lectura pesada | Opus: 200k × 4 = US$ 0,80 | 3 exploradores Sonnet: (200k + 45k de arranque) × 2 = US$ 0,49 |
| Escritura | Opus: 10k × 20 = US$ 0,20 | Sonnet: 12k × 10 = US$ 0,12 |
| Coordinación | — | Opus: 30k entrada + 3k salida = US$ 0,18 |
| **Total** | **~US$ 1,00** | **~US$ 0,79** |
| Tiempo | lectura en serie | 3 lecturas **en paralelo** |

Ahorro de ~20 %, no de 50 %, y bastante más rápido por el paralelismo. En una tarea chica (un archivo, un cambio), la oficina sale **más cara**.

## Velocidad
- Se acelera lo que se puede hacer **a la vez**: varias búsquedas, probar y revisar juntos, documentar mientras se prueba.
- No se acelera lo que va en **cadena**: no se puede probar algo antes de programarlo.
- Cada agente suma una pequeña demora de arranque y de coordinación.

## Cómo medirlo de verdad
1. Elegí dos tareas parecidas.
2. Hacé una sin agentes ("no uses agentes") y otra con la oficina.
3. Compará `/usage` (o `/cost`) y el tiempo total.

Recién con eso se sabe cuánto ahorra en **tu** forma de trabajar.
