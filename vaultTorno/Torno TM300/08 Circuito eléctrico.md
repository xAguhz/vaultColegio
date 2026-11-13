---
tags: [torno-tm300, electricidad]
tipo: nota
fuentes: ["Manual AL340 (cap. 8, Electric Circuit Control)", "TP Torno TM300 (cap. 3)"]
---
# Circuito eléctrico

Volver a [[00 Torno TM300]] · Seguridad: [[04 Normas de seguridad]]

> [!danger] Bloqueo antes de abrir el tablero
> Cortar el seccionador general, colocar candado y tarjeta (**LOTO**), verificar ausencia de tensión. Los esquemas son de la serie de fábrica: **comparar siempre con el cableado real** y la placa del motor antes de reemplazar algo.

## Esquemas del manual

![[tm300_esquema_electrico_trifasico.png|520]]
*Esquema para alimentación trifásica (380 V), manual pág. 19.*

![[tm300_esquema_electrico_monofasico.png|520]]
*Esquema para alimentación monofásica (220 V), manual pág. 20.*

## Referencias de los esquemas

| Símbolo | Componente | Función |
|---|---|---|
| PE | Tierra de protección | Conductor de puesta a tierra de toda la máquina |
| L1, L2, L3 (o L, N) | Alimentación | Trifásica 380 V o monofásica 220 V |
| **QM1** | Interruptor / guardamotor general | Protege el circuito del motor principal |
| **KM1 / KM2** | Contactores | Giro adelante / atrás del husillo (enclavados entre sí) |
| **M1** | Motor principal 1,5 kW | U1-V1-W1 (trifásico) o U1-U2 + Z1-Z2 (monofásico con bobinado auxiliar) |
| **QM2** | Guardamotor de la bomba | Protección de M2 |
| **KA1** | Relé de la bomba | Arranca la bomba de refrigerante |
| **M2** | Bomba de refrigerante AB-12 (40 W) | U2-V2-W2 (trifásica) o 1L-1N (monofásica) |
| **TC** | Transformador de mando | Baja la tensión del circuito de mando (24 V CA según el TP) |
| **QM3** | Protección del mando | Fusible/termomagnética del secundario |
| EL | Lámpara de trabajo | Iluminación |
| HL | Piloto | Indica máquina energizada |
| **SB0** | Parada de emergencia | Seta "golpe de puño", contacto NC |
| SB1 | Pulsador / llave de refrigerante | Manda a KA1 |
| SB2 | Pulsador JOG (impulso) | Giro por impulsos para cambiar velocidades |
| SB3 | Pulsador de marcha / habilitación | Energiza KA0 |
| **KA0** | Relé de habilitación (mínima tensión) | Se autorretiene; si se corta la luz, la máquina **no rearranca sola** |
| SQ1, SQ2 | Interruptores de seguridad | Tapa de la lira / protección del plato / freno de pie (en serie con la emergencia) |
| SQ3 | Interruptor de neutro | Palanca de marcha en punto muerto |
| SQ4, SQ5 | Interruptores de la palanca de marcha | Seleccionan KM1 (adelante) o KM2 (atrás) |

> [!note] Interpretación
> El manual solo trae el dibujo, sin leyenda. La función de cada contacto se dedujo del esquema y de la tabla del TP; el **microinterruptor LXW5-11G2** de la caja Norton ([[Caja Norton y lira]], ítem 31) y el del freno de pie son de este tipo de contactos de seguridad. Verificar con multímetro en la máquina antes de rotular el tablero.

## Lógica de funcionamiento
1. Con QM1, QM3 y la emergencia SB0 cerradas, y las tapas en su lugar (SQ1, SQ2), se enciende el piloto HL.
2. Con la palanca de marcha en neutro (SQ3) se pulsa marcha (SB3): **KA0** se energiza y se autorretiene.
3. Al llevar la palanca (19) hacia adelante o atrás, SQ4 o SQ5 energizan **KM1** o **KM2**. Cada contactor tiene un contacto NC del otro en serie: **nunca pueden cerrar los dos a la vez** (enclavamiento eléctrico).
4. **SB2 (JOG)** permite girar el husillo por impulsos para que entren los engranajes.
5. **SB1** manda al relé KA1 y este a la bomba M2 (protegida por QM2).
6. Cualquier contacto de seguridad abierto (emergencia, tapa, freno) **cae KA0** y se detiene todo.

## Arquitectura según IEC 60204-1 (del TP)

**Circuito de potencia (380 V / 50 Hz trifásico)**
- **Q0** seccionador general tripolar con mando exterior, para aislar el tablero.
- **QF1** guardamotor magnetotérmico, ajustado a la corriente nominal de M1.
- **KM1 y KM2** contactores tripolares con enclavamiento eléctrico y mecánico (inversión de giro).
- **FR1** relé térmico bimetálico: corta ante sobrecargas sostenidas.
- **M1** motor principal (2 HP / 1,5 kW) y **M2** bomba AB-12 (40 W).

**Circuito de mando (24 V CA)**
- Transformador **TR1** 380/24 V para proteger al operador.
- **S0** seta de emergencia con enclavamiento mecánico, contacto NC al inicio de la cadena.
- **S1 / S2** microinterruptores de seguridad en la tapa de la lira y en la pantalla del plato.

> [!tip] Equivalencias de nombres
> El TP usa la nomenclatura IEC "Q0, QF1, KM, FR1, TR1, S0" y el manual chino usa "QM1, KM, TC, SB0". Son los mismos componentes: Q0/QF1 ≈ QM1, TR1 ≈ TC, S0 ≈ SB0, S1/S2 ≈ SQ1/SQ2.

## Mantenimiento eléctrico
| Tarea | Frecuencia |
|---|---|
| Probar la seta de emergencia (debe cortar KM1) | Diaria |
| Probar el freno de pie y los interruptores de tapas | Semanal |
| Reapretar bornes, limpiar contactos y polvo del tablero | Mensual |
| Termografía de bornes y medición de aislación del motor (megóhmetro) | Semestral |
| Verificar tierra (PE) y continuidad a la bancada | Semestral |

Repuestos eléctricos y dónde conseguirlos: [[13 Repuestos y compras]].
