---
tags: [autolid, informe]
tipo: resumen
fuente: "AutoLID INFORME FINAL (Google Docs, 10/11/2026)"
actualizado: 2026-11-12
---
# Informe final - resumen

> [!summary] Qué dice el documento principal
> Resumen del [AutoLID INFORME FINAL](https://docs.google.com/document/d/1OecoL8DSYKZxiSlKSvtnaXOIvBBHetvMpxqblyg_-EE/edit) (10/11/2026). Ante cualquier duda, manda el Doc, no esta nota.

## En una frase
**AutoLID** es un dispositivo *retrofit* que se instala sobre las bisagras de cualquier inodoro y abre y cierra la tapa solo, sin contacto, con un sensor de peso que impide que se cierre con alguien sentado.

## Datos
| | |
|---|---|
| Escuela | E.E.S.T. N° 3 de San Antonio de Padua, Electromecánica / Electrónica |
| Equipo | Agustín Calderón, Thiago Iglesias y Luciano Romero (7° 1°) |
| Contacto | contacto.autolid@gmail.com |
| Estado | Hardware definido, firmware validado en Tinkercad, plan industrial PYME |

## Público y problema
| Público | Problema | Solución |
|---|---|---|
| **Perfil A**: adultos mayores y movilidad reducida | Agacharse y levantar la tapa (0,5-1 kg); riesgo de caídas | Servo de 20 kg·cm, apertura por cercanía, bloqueo por peso |
| **Hogares** | Contaminación por contacto y por el *toilet plume* | 100 % sin contacto; cierre automático 5 s después de irse |
| **Perfil B**: industria, laboratorios, clínicas | Romper protocolos de higiene con guantes/EPP | Gabinete IP65, carcasa inoxidable, sin obra ni 220 V |

## Cómo funciona
1. La persona está a **menos de 60 cm durante 3 s** (HC-SR04) → la tapa sube a **3 RPM** (90° en 5 s).
2. Si el **FSR 402** marca más de **200** (alguien sentado), el cierre queda bloqueado.
3. Cuando la persona se levanta y se aleja **5 s**, la tapa baja.
4. Firmware **no bloqueante** (`millis()`), servo de a 1° cada 55 ms.

## Hardware
Diagrama: [[Arquitectura AutoLID.excalidraw|Arquitectura del hardware]] (Excalidraw).

- Arduino Nano · HC-SR04 (D9/D10) · FSR 402 en A0 con 10 kΩ · servo DS3218 en D6.
- 2 × 18650 en paralelo (6000 mAh) → TP4056 (carga) → MT3608 (5 V). El servo **no** se alimenta desde el pin 5 V del Arduino (picos de 900 mA).
- Gabinete IP65 150×150×100 mm, carcasa AISI 304, adaptador PETG para bisagras de 38-43 mm.
- PCB en EasyEDA: pistas de potencia de 1 mm, señal de 0,254 mm, plano de masa en las dos caras.
- **Autonomía:** ~100 mAh/día con modo sleep → **~60 días** por carga (4 días sin optimizar).

## Costos (lista de materiales)
| | Prototipo | Serie (lote de 100) |
|---|---|---|
| Total por unidad | **$185.800 ARS** | **$138.000 ARS** (−25,7 %) |
| Partes más caras | Servo DS3218 ($55.000), carcasa inox ($32.000), FSR 402 ($28.000) | |
| Ya comprados | Arduino Nano, HC-SR04, gabinete IP65 | |

## Planta y mercado
- Planta alquilada de **60 m²** (10 × 6 m) en "U": 4 estaciones (PCB y soldadura → sensores → ensamble → control y empaque). **28-42 min** por unidad.
- Mercado AMBA: 874.000 personas con movilidad reducida → 160.800 clientes posibles → **129-161 unidades el año 1**.
- Se arma contra pedido; punto de reorden: 7-10 unidades en stock.

## Números financieros (5 años, tasa 15 %)
| Indicador | Valor |
|---|---|
| Inversión inicial | $14.000.000 ARS (USD 9.859), planta alquilada |
| VAN | **+$51.410.681 ARS** |
| TIR | **87,03 %** (62,47 % con crédito) |
| Índice de rentabilidad | 4,67 |
| Recupero | 1,68 años simple / **1,98 años** descontado |

## Lo que falta (hoja de ruta del informe)
| Prioridad | Tarea | Estado |
|---|---|---|
| Alta | Armar el prototipo físico final (servo, FSR y HC-SR04 en la caja IP65) | En ejecución |
| Alta | Medir consumo real (sleep < 20 µA, picos de 900 mA) | Pendiente |
| Media | Imprimir adaptadores en PETG e impermeabilizar sensores | Pendiente |
| Media | Encuestas (Perfil A y B) y prueba piloto de 3-5 unidades | En curso |
| Baja | PCB propia en JLCPCB (lote de 100) | Planificado |

> [!warning] Para revisar antes de presentar
> - **Dos TIR distintas:** el informe final dice 87,03 % y la evaluación financiera del 19/10 dice 62,47 % (con crédito). Conviene decir siempre cuál se usa.
> - **"4,16 mA por hora":** la unidad correcta es mA (corriente media), no "mA por hora".
> - En las carpetas del 26 y 27/10 el apellido aparece como "Igesias"; en el informe final está bien (Iglesias).

## Relacionado
[[00 AutoLID]] · [[Historia del proyecto]] · [[Archivos en Drive]]
