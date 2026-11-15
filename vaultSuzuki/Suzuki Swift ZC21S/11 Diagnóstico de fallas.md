---
tags: [suzuki-swift, diagnostico, fallas, obd2]
tipo: nota
actualizado: 2026-11-14
---
# 11 · Diagnóstico de fallas

Volver a [[00 Suzuki Swift ZC21S]]

> [!tip] Diagnóstico completo
> Esta nota es el resumen. El troubleshooting por sistema está en [[Diagnóstico por síntoma]], el de cada pieza (con cómo se desmonta) en la [[Guía técnica por pieza]] y todos los códigos en [[Códigos de falla (DTC)]].

## Leer los códigos
El auto tiene **conector de diagnóstico OBD-II** (16 pines) debajo del tablero, del lado del conductor. Con cualquier escáner OBD-II se leen los códigos de la computadora del motor (y con uno más completo, los de la caja, el ABS y los airbags).

**Método:** 1) anotar el código y los datos congelados (*freeze frame*), 2) revisar lo simple (fusible, conector, manguera), 3) borrar y probar, 4) si vuelve, seguir la prueba del manual.

## Códigos frecuentes en el M15A
| Código | Qué significa | Primero revisar |
| ------ | ------------- | --------------- |
| P0011 / P0012 | Fase del árbol de admisión (VVT) adelantada o atrasada | Nivel y estado del **aceite**; válvula de control de aceite (OCV) y su filtro |
| P0031 / P0032 | Calefactor de la sonda de oxígeno 1 | Fusible, conector, sonda |
| P0101 / P0102 | Caudalímetro de aire (MAF) fuera de rango o bajo | Filtro de aire, entradas de aire falsas, limpiar el sensor |
| P0171 / P0172 | Mezcla pobre / rica | Entradas de aire, presión de nafta (270–310 kPa), inyectores |
| P0300–P0304 | Falla de encendido (aleatoria o cilindro 1 a 4) | Bujías, bobinas y cables de alta, compresión |
| P0420 | Catalizador con baja eficiencia | Primero descartar fallas de encendido y de mezcla |
| P0500 | Sensor de velocidad | Conector y sensor |

## Por síntoma
| Síntoma | Causas posibles | Ver |
| ------- | --------------- | --- |
| No arranca, no gira | Batería, bornes, fusible ST MOT, pedal de embrague sin apretar a fondo | [[10 Sistema eléctrico]] |
| Gira pero no arranca | Sin nafta (bomba, relé, fusible FI o IG COIL), sin chispa, inmovilizador | [[06 Motor M15A]] |
| Ralentí inestable | Cuerpo de mariposa sucio, entrada de aire, bujías | [[06 Motor M15A]] |
| Tironea al acelerar | Bujías o bobinas, filtro de nafta, presión de nafta | [[08 Plan de mantenimiento]] |
| Calienta en tránsito | Electroventilador o su fusible (RDTR FAN), refrigerante bajo, radiador tapado | [[07 Fluidos y capacidades]] |
| Testigo de aceite prendido | Aceite bajo, sensor, bomba: **parar el motor** | [[04 Mandos e instrumentos]] |
| El embrague patina o arrastra | Disco gastado, aire en el circuito, juego del pedal | [[05 Conducción y caja manual]] |
| Cruje al pasar una marcha | Sincronizador gastado, embrague que arrastra | [[05 Conducción y caja manual]] |
| Dirección dura | Batería baja, fusible EPS, falla del motor EPS | [[09 Frenos, suspensión, dirección y ruedas]] |
| Ruido "tac-tac" al doblar | Junta homocinética gastada (fuelle roto) | [[09 Frenos, suspensión, dirección y ruedas]] |
| Pedal de freno vibra | Discos alabeados o bajo espesor | [[09 Frenos, suspensión, dirección y ruedas]] |
| Testigo de carga | Correa, alternador, fusible | [[10 Sistema eléctrico]] |

> [!warning] Inmovilizador
> La llave tiene un chip. Si se usa una copia sin programar, el motor gira pero no arranca y el testigo del inmovilizador parpadea. Las llaves nuevas se programan con el equipo del concesionario o de un cerrajero de autos.

Ver también [[08 Plan de mantenimiento]]
