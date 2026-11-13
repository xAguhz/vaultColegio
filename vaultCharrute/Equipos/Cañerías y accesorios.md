---
tipo: equipo
funcion: conducir el fluido entre equipos
tps: [TP4, TP8]
tags: [equipo, cañerías, accesorios, piping]
---

# Cañerías y accesorios

> [!summary] Idea central
> **"El recorrido del fluido nunca es neutro."** La cañería no es "un tubo por donde pasa algo": condiciona la **pérdida de energía**, el **mantenimiento**, la **seguridad** y la conexión entre equipos. Una planta con buenos equipos puede andar mal por culpa de la red.

## Qué se estudia de una cañería (diseño curricular de 7°)
- material y proceso de fabricación;
- diámetro nominal y espesor;
- **uniones**: roscada, soldada, bridada, termofusión;
- **pruebas** de hermeticidad y de presión;
- **soportes**, y cómo se transmiten los esfuerzos y las vibraciones;
- la representación de todo esto en el **[[P&ID]]**.

## Accesorios
Codos, tees, reducciones, uniones y derivaciones: cada uno **agrega una [[Pérdidas de carga|pérdida local]]**.
- **Codo de radio largo (R = 1,5 D)** en lugar de una esquina viva: menos K y menos turbulencia.
- **Reducción excéntrica** en la aspiración de una bomba, con la cara plana arriba.

## Criterios de trazado
- Con más recorrido, más accesorios y más restricciones, el fluido **no se comporta igual** que en una línea simple.
- **Pendiente en el sentido del flujo** y **drenajes o piernas de purga** en los puntos bajos (aire comprimido y vapor).
- **Apertura lenta** de las válvulas de vapor para evitar el **golpe de ariete**.
- **Diámetro pleno** hasta el consumo crítico (simultaneidad, como en la amasadora de Panadería Pilar).
- **Red anular** en el aire comprimido, para alimentar desde dos lados.
- Las cañerías **mal soportadas** cargan las bridas de la bomba: desalineación y fallas del sello.

## Materiales vistos en el TP4
| Red | Material | Unión |
|---|---|---|
| Agua potable | PPR | Termofusión |
| Gas | Acero con revestimiento epoxi | Soldadura (resiste las vibraciones) |
| Desagüe cloacal | PVC reforzado de 110 mm | Por gravedad, con pendiente del 2–3 % |

## Código de colores (IRAM 2507, Decreto 351/79)
| Color | Fluido |
|---|---|
| **Verde** | Agua |
| **Azul** | Aire comprimido |
| **Amarillo** | Gas |
| Marrón o negro | Desagües |

## Relacionado
[[Válvulas]] · [[Pérdidas de carga]] · [[P&ID]] · [[TP4 Cañerías y válvulas]]
