---
tags: [suzuki-swift, manual-de-taller, cap-10c]
tipo: capitulo-manual
capitulo: "10C"
paginas_pdf: "1520-1541"
---
# 10C · Sistema de control del inmovilizador

Volver a [[00 Índice del manual de taller|Índice del manual]] · PDF: [[Manual de taller Swift 2005-2010.pdf#page=1520|abrir en la página 1520]] (páginas 1520 a 1541, solo en la copia local)

> [!summary] De qué trata
> Inmovilizador: antena en el tambor de la llave, transpondedor en la llave, comunicación con el ECM, registro de llaves y diagnóstico.

**Piezas en el modelo 3D:** [antena_inmovilizador](https://xaguhz.github.io/vaultColegio/vaultSuzuki/3D/visor/index.html#antena_inmovilizador) · [ecu](https://xaguhz.github.io/vaultColegio/vaultSuzuki/3D/visor/index.html#ecu)

## Temas del capítulo
| Tema | Página |
| --- | --- |
| Precauciones | [[Manual de taller Swift 2005-2010.pdf#page=1520|10C-1]] |
| Precaución para la sustitución del ECM | [[Manual de taller Swift 2005-2010.pdf#page=1520|10C-1]] |
| B1133 (N° DTC 1133): Tensión de del inmovilizador | [[Manual de taller Swift 2005-2010.pdf#page=1520|10C-1]] |
| Descripción general | [[Manual de taller Swift 2005-2010.pdf#page=1521|10C-2]] |
| Diagrama esquemático y de disposición | [[Manual de taller Swift 2005-2010.pdf#page=1523|10C-4]] |
| DTC) | [[Manual de taller Swift 2005-2010.pdf#page=1525|10C-6]] |
| Borrado de códigos de diagnóstico (DTC) | [[Manual de taller Swift 2005-2010.pdf#page=1525|10C-6]] |
| Tabla de códigos de diagnóstico (DTC) | [[Manual de taller Swift 2005-2010.pdf#page=1525|10C-6]] |
| Datos de la herramienta de escaneado | [[Manual de taller Swift 2005-2010.pdf#page=1526|10C-7]] |
| EEPROM | [[Manual de taller Swift 2005-2010.pdf#page=1534|10C-15]] |
| DTC P1623: Transpondedor no registrado | [[Manual de taller Swift 2005-2010.pdf#page=1534|10C-15]] |
| Inmovilizador | [[Manual de taller Swift 2005-2010.pdf#page=1535|10C-16]] |
| Información del Inmovilizador | [[Manual de taller Swift 2005-2010.pdf#page=1536|10C-17]] |
| ICM) y su circuito | [[Manual de taller Swift 2005-2010.pdf#page=1537|10C-18]] |
| Instrucciones de reparación | [[Manual de taller Swift 2005-2010.pdf#page=1539|10C-20]] |
| ICM) | [[Manual de taller Swift 2005-2010.pdf#page=1539|10C-20]] |
| Registro de la llave de encendido | [[Manual de taller Swift 2005-2010.pdf#page=1540|10C-21]] |
| Herramientas y equipos especiales | [[Manual de taller Swift 2005-2010.pdf#page=1541|10C-22]] |
| Herramienta especial | [[Manual de taller Swift 2005-2010.pdf#page=1541|10C-22]] |

## Despieces y ubicación de componentes
### Ubicación de los componentes del sistema de control del inmovilizador
**1.** ECM, **2.** Indicador luminoso del inmovilizador, **3.** Módulo de control del inmovilizador (ICM), **4.** Llave de encendido con sistema de entrada sin llave, **5.** Llave de encendido sin sistema de entrada sin llave, **6.** Llave de encendido con sistema de arranque sin llave

## Códigos de falla
| Código | Descripción |
| --- | --- |
| P1674 | Comunicación de la |
| P1614 | Error de respuesta del transpondedor |
| P1615 | Código ID no registrado (vehículo equipado sólo con el sistema de arranque sin llave) |
| P1616 | Registro diferente de códigos ID (vehículo equipado sólo con el sistema de arranque |
| P1618 | Error de comunicación de la CAN (error de recepción de módulo de control de arranque |
| P1621 | Error de línea de comunicación del inmovilizador |
| P1622 | Error de lectura/escritura en la EEPROM |
| P1623 | Transpondedor no registrado |
| P1625 | Error de Antena del Inmovilizador |
| P1636 | Fallo en el Registro de la Información del Inmovilizador |
| P1638 | La información del inmovilizador no es real |
