---
tipo: equipo
funcion: almacenar
fluido: líquidos (a veces gases a baja presión)
variable_principal: nivel
tps: [TP2, TP3, TP5]
tags: [equipo, tanque]
---

# Tanque de almacenamiento

> [!summary] Función
> **Almacena** un fluido como reserva, alimentación, pulmón o etapa intermedia. **No impulsa, no comprime ni transfiere calor**, pero puede ser decisivo para el sistema.

## Para qué está en un proceso
- **Reserva o buffer:** cubre una demanda variable o una fuente intermitente, para que la [[Bomba]] no trabaje en vacío ([[TP3 Variables de proceso|TP3]]).
- **Pulmón:** estabiliza la presión y absorbe pulsaciones (el pulmón del aire comprimido ya es un [[Recipiente a presión]]).
- **Decantación o separación** de sólidos o fases.
- La capacidad se elige **según el servicio**:
  - alimentación continua → caudal y tiempo de retención;
  - reserva → autonomía y logística ([[TP5 Tanques y recipientes a presión|TP5]]).

## Tipos
| Criterio | Opciones |
|---|---|
| Geometría | Cilíndrico vertical (el más común en grandes volúmenes), horizontal sobre cunas, rectangular |
| Techo | **Fijo** (productos poco volátiles) o **flotante** externo o interno (IFR), que reduce la evaporación |
| Ubicación | Apoyado (fundación), **elevado** (estructura; da presión aguas abajo sin bomba), **enterrado** (suelo, napa, corrosión exterior) |

## Física: presión hidrostática
**P = ρ · g · h**: crece con la profundidad y con la **densidad**. Con la misma altura y un líquido más denso, el fondo soporta más presión. El fondo y la fundación cargan todo el peso del líquido.

## Variables e instrumentos
- **Nivel** (la principal): evita el vaciado (cavitación de la bomba) y el sobrellenado (derrame). Se mide con radar, flotante o servo, y lleva alarmas de alto y bajo (*Hi-Hi* en un SIS).
- **Temperatura:** dilatación y propiedades del fluido.
- A veces, **presión**.

## Conexiones y accesorios
Entrada y salida (con **placa antivórtice** en la succión), drenaje o sumidero, **venteo o válvula de presión y vacío (PVV)**, conexiones para instrumentos y **boca de inspección** (*manhole*).

## Fallas típicas
- **Corrosión** uniforme o por **picado**, y corrosión microbiológica: adelgaza la pared **sin pérdida visible**. Se compensa con **sobreespesor de corrosión**.
- **Sobrellenado:** derrame e incendio. Se contiene con un **cubeto de retención** (110 % del tanque mayor).
- **Colapso por vacío** (implosión) si se vacía rápido con el venteo tapado.
- Fallas en las conexiones o válvulas: el tanque puede estar perfecto y aun así cortarse el servicio.

## Norma
**API 650**: tanques soldados, verticales, de fondo plano, para petróleo, hasta unos 2,5 psig. **No es la norma de todos los tanques**: API 620 cubre presiones de hasta 15 psig; para enterrados se usan UL 58 o IRAM; para tanques de incendio, NFPA 22. Ver [[Normas y códigos]].

## Relacionado
[[Recipiente a presión]] · [[Bomba]] · [[Variables de proceso]] · [[Sistema de bombeo de agua]]
