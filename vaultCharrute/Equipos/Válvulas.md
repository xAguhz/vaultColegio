---
tipo: equipo
funcion: abrir, cerrar, regular, desviar o impedir el retorno del fluido
fluido: cualquiera
aporta_energia: no
tps: [TP2, TP4, TP5, TP8]
tags: [equipo, válvulas]
---

# Válvulas

> [!summary] Función
> **Permiten, impiden, regulan o dirigen** el paso del fluido. **No almacenan, no impulsan y no aportan energía**: por eso **una válvula no reemplaza a una bomba**. Solo controla lo que otra máquina ya puso en movimiento.

## Clasificación por función (la que pide el profe)
| Función | Para qué | Ejemplos típicos |
|---|---|---|
| **Aislamiento** | Abrir o cerrar del todo: aislar sectores o hacer mantenimiento | **Esférica** (de ¼ de vuelta y paso total: casi no tiene pérdida), esclusa |
| **Regulación** | Ajustar el caudal o la presión | **Globo** (regula bien, pero pierde mucho aun abierta), reguladoras de presión, válvula de control con actuador |
| **Retención (check)** | Impedir que el fluido vuelva | Check a la salida del compresor, válvula de pie en la succión de una bomba |
| **Seguridad o alivio (PSV/PRV)** | Proteger contra una **sobrepresión** de forma **automática** | Resorte calibrado a la *set pressure* |
| **Distribuidoras** (neumática) | Dirigir el aire a las cámaras de un cilindro | **5/2 biestable** de la empaquetadora ([[TP4 Cañerías y válvulas|TP4]]) |

> [!warning] Lo que se confunde seguido
> - **Válvula manual ≠ válvula de seguridad.** La manual necesita a alguien y es de maniobra; la PSV dispara sola, en milisegundos ([[TP5 Tanques y recipientes a presión|TP5]]).
> - La válvula de seguridad **no** se usa para regular la presión de trabajo ([[TP8 Compresores de aire|TP8]]).
> - Una válvula elegida para aislar puede **no servir** para regular fino, y al revés.

## Válvulas y pérdidas de carga
Cada válvula agrega una **[[Pérdidas de carga|pérdida local]]** (coeficiente K):
- una **globo** abierta pierde mucho más que una **esférica** abierta;
- una válvula **entrecerrada** pierde muchísimo;
- **estrangular** la descarga de una bomba sobredimensionada mueve el punto de funcionamiento, pero **desperdicia energía** ([[TP7 Bombas industriales|TP7]]).

## Partes (según ISA)
- **cuerpo** a presión;
- **obturador**, que cambia de posición para ajustar el flujo;
- **actuador**, que da la fuerza para abrir o cerrar (manual, neumático o eléctrico).

## En los sistemas de la materia
- **[[Sistema de bombeo de agua|Bombeo]]:** válvula de pie con filtro en la succión, esférica de aislamiento, regulación en la descarga.
- **[[Sistema de aire comprimido|Aire comprimido]]:** check a la salida del compresor, PSV en el tanque, regulador (en la [[Unidad FRL|FRL]]) en el punto de uso, purgas.
- **Gas:** esférica de corte rápido de ¼ de vuelta antes del horno (Panadería Pilar).

## Vocabulario para el oral
Decir **"válvula de aislamiento o de regulación"**, nunca "llave de paso".

## Relacionado
[[Cañerías y accesorios]] · [[Pérdidas de carga]] · [[Bomba]] · [[Recipiente a presión]] · [[P&ID]]
