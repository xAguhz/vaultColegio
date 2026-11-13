---
tipo: equipo
funcion: entregar energía mecánica a un líquido
fluido: líquidos
variable_principal: caudal y altura (presión)
tps: [TP1, TP2, TP3, TP7]
tags: [equipo, bomba]
---

# Bomba

> [!summary] Función
> Máquina hidráulica que **transfiere energía mecánica a un líquido** para que circule: puede subir su presión, su velocidad o la altura que alcanza. Decir que "crea presión" es incorrecto: la presión aparece por la **resistencia del sistema**.

![[bomba.png|420]]

## Familias
| | Centrífuga (rotodinámica) | Desplazamiento positivo |
|---|---|---|
| Principio | Un impulsor acelera el líquido y la voluta convierte la velocidad en presión | Encierra un volumen y lo empuja (pistón, diafragma, engranajes, tornillo, lóbulos) |
| Caudal | Depende del sistema (curva H–Q) | Casi fijo por vuelta o embolada |
| Servicio típico | Caudales medios y altos, líquidos poco viscosos | Poco caudal y alta presión, **viscosos**, dosificación |
| Con la salida bloqueada | Llega a la presión de *shut-off* (finita) y **calienta** el líquido | **La presión sube hasta romper** → **válvula de alivio obligatoria** |

## Bomba centrífuga
- **Impulsor:**
  - **cerrado** para líquidos limpios (mejor rendimiento);
  - **semiabierto, abierto o vórtex** para sólidos.
- **Carcasa (voluta), eje, rodamientos, sello** (mecánico o empaquetadura) y bocas de aspiración y descarga.
- **No "chupa":** el líquido tiene que **llegar** al ojo del impulsor.

## Curvas y punto de funcionamiento
- **Curva H–Q** de la bomba (H baja al subir Q) y **curva del sistema** (H_estática + k·Q²): su cruce es el **punto de funcionamiento**.
- Si se cambia una válvula o una cañería, **el punto se mueve** aunque la bomba sea la misma. Por eso dos bombas idénticas pueden dar caudales distintos.
- **H total** = desnivel + diferencia de presión + **[[Pérdidas de carga|pérdidas]]**. No se elige por los "metros a elevar": con 15 m de desnivel puede necesitarse una H de 16 m o de 40 m.
- **Potencia:** P_hid = ρ·g·Q·H; rendimiento η = P_hid / P_eje.
- **BEP:** el punto de mejor rendimiento. Lejos de él aparecen empuje radial, recirculación, vibración y desgaste.
- **Sobredimensionar "por las dudas"** obliga a estrangular: se pierde energía y la bomba sale del BEP.
- **Regulación:** con una **válvula** (funciona, pero disipa energía) o con un **variador de frecuencia**. Leyes de afinidad: Q ∝ n, H ∝ n², P ∝ n³.

## Aspiración: el punto crítico
- **Cebado:** muchas centrífugas **no son autocebantes**; con aire no bombean (el aire es unas 800 veces menos denso que el agua).
- **Marcha en seco:** el líquido refrigera y lubrica el sello; sin él, el sello se rompe en segundos.
- **Cavitación:**
  1. la presión local cae por debajo de la **presión de vapor** y se forman burbujas;
  2. las burbujas **implotan** en la zona de alta presión;
  3. se produce **ruido de grava**, vibración, pérdida de rendimiento y **erosión** del impulsor.
- **Causas de cavitación:** nivel bajo, mucha altura de succión, filtro sucio, válvula de aspiración entrecerrada, **líquido caliente**, caudal excesivo.
- **NPSH:** el **disponible** (NPSHA) lo da la instalación; el **requerido** (NPSHR) lo da el fabricante. Hay que cumplir NPSHA ≥ NPSHR + margen (0,6 a 1 m).
- **Reducción excéntrica** en la aspiración, **con la cara plana arriba**, para que no se junte aire.

## Serie y paralelo
- **En serie** suma **altura**.
- **En paralelo** suma **caudal**.
- En ninguno de los dos casos es una suma directa: el punto se mueve sobre la curva del sistema.

## Diagnóstico: "es diagnóstico del sistema de bombeo"
Ante un **caudal insuficiente**, revisar en este orden:
1. **Instalación:** válvulas (la compuerta puede estar caída), filtros, nivel y vórtices, entradas de aire.
2. **Grupo motor:** sentido de giro, RPM, amperes, alineación, presiones reales comparadas con la curva.
3. **Interior:** impulsor tapado o erosionado, anillos de desgaste.

Un **sello que falla siempre** es la *víctima*, no la causa: buscar desalineación, eje flexionado, cavitación, marcha en seco o esfuerzos de las cañerías.

## Relacionado
[[Sistema de bombeo de agua]] · [[Tanque]] · [[Válvulas]] · [[Pérdidas de carga]] · [[TP7 Bombas industriales]] · [[Compresor]] (bomba ≠ compresor)
