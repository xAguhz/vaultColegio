---
tipo: concepto
tps: [TP1, TP2, TP3, TP5, TP6, TP7, TP8, TP9]
tags: [concepto, variables, instrumentación]
---

# Variables de proceso

> [!summary] Definición
> Son las magnitudes que **cambian durante el funcionamiento** y que conviene **observar, medir o controlar** para saber si el proceso **cumple su objetivo**, no solo si está armado. "Que el fluido circule es necesario, pero no suficiente."

## Las cuatro principales
| Variable | Qué indica | Dónde importa más | Instrumento típico |
|---|---|---|---|
| **Presión** | La fuerza del fluido sobre la superficie | [[Compresor]], [[Recipiente a presión]], líneas de aire, descarga de la [[Bomba]] | Manómetro (tubo Bourdon), transmisor de presión, presostato |
| **Temperatura** | La condición térmica | [[Intercambiador de calor]], [[Caldera]], salida del compresor | Termómetro, RTD (PT-100), termocupla |
| **Caudal** | Cuánto fluido pasa por unidad de tiempo | Bombas, consumos, intercambiadores | Caudalímetro |
| **Nivel** | Cuánto hay almacenado | [[Tanque]], caldera | Visor, flotante, radar |

## Ideas que pide el profe
- **No hay una variable "más importante" en general:** depende del **objetivo** del sistema.
  - Aire comprimido: **presión**.
  - Calentamiento: **temperatura**.
  - Tanque de alimentación: **nivel**.
- **"Trabaja con agua" ≠ "importa el caudal":** lo primero describe el **fluido**; lo segundo, la **variable** que define si el equipo cumple su función.
- **Un equipo bien elegido** puede no funcionar si las variables están fuera de rango (por ejemplo, poca presión de aspiración).
- **Diagnóstico:** se relacionan variables antes de cambiar equipos. En un intercambiador: 4 temperaturas + caudal + ΔP. En una bomba: nivel, presión de succión y descarga, caudal y amperes.
- **De medir a controlar:** la presión no es solo un número en un manómetro; puede ser una **señal** que arranca o para un compresor (presostato) o mueve una válvula de control.
- **Control ≠ seguridad:** el manómetro y el control de nivel *operan*; la PSV, el corte por bajo nivel y la detección de llama *protegen*.

## Cómo cambia el análisis
| Trabajo | Pregunta | Tipo de análisis |
|---|---|---|
| TP2 (equipos) | ¿Qué hay y para qué está? | Estructural, descriptivo |
| TP3 (variables) | ¿Bajo qué condiciones funciona bien? | **Funcional y cuantitativo** |

## Relacionado
[[TP3 Variables de proceso]] · [[P&ID]] · [[Diagrama de proceso]]
