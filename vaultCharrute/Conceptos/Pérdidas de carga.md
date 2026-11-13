---
tipo: concepto
tps: [TP4, TP6, TP7, TP8]
tags: [concepto, pérdidas-de-carga, hidráulica]
---

# Pérdidas de carga

> [!summary] Definición
> Es la energía (presión) que el fluido **pierde** al circular por la instalación. Por eso **"el recorrido nunca es neutro"**: cada metro de cañería y cada accesorio cobran su parte.

## Tipos
- **Continuas (distribuidas):** por rozamiento a lo largo del tramo recto. Crecen con la longitud y la velocidad y bajan con el diámetro (ecuación de Darcy-Weisbach).
- **Locales (menores):** en codos, tees, reducciones, uniones, filtros y **válvulas**. Cada elemento tiene su coeficiente **K**.
- Para un sistema completo: **h_f ≈ k · Q²**. Si se duplica el caudal, las pérdidas se cuadruplican.

## Consecuencias en cada equipo
| Contexto | Qué pasa |
|---|---|
| **[[Bomba]]** | Las pérdidas forman la **curva del sistema**. Más longitud o accesorios bajan el caudal sin tocar la bomba. Es el motivo para no elegir solo por los "metros a elevar" |
| **Aspiración de la bomba** | Las pérdidas en la succión **bajan el NPSHA** y producen **cavitación** |
| **[[Intercambiador de calor]]** | Si la ΔP sube con el tiempo, hay **fouling** |
| **[[Sistema de aire comprimido\|Aire comprimido]]** | Filtros sucios, secadores, diámetro chico o red larga hacen que **no llegue presión al extremo**. **No** se arregla subiendo la presión del compresor |
| **Válvula entrecerrada** | La pérdida local aumenta muchísimo. Estrangular regula, pero desperdicia energía |

## Cómo se reducen
- **Codos de radio largo** (R = 1,5 D) en lugar de esquinas vivas.
- **Válvulas esféricas de paso total** para aislar.
- Diámetro adecuado, recorrido corto y con pocos accesorios, **red anular** en el aire comprimido.
- Mantener limpios los filtros y los intercambiadores.

## Relacionado
[[Cañerías y accesorios]] · [[Válvulas]] · [[TP4 Cañerías y válvulas]] · [[TP7 Bombas industriales]]
