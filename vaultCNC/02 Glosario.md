---
tipo: glosario
tags: [glosario, cnc]
---

# Glosario

| Término | Significado | Ver |
|---|---|---|
| **CNC** | Control numérico por computadora: la máquina sigue un programa de códigos | [[Torno y control]] |
| **Control Fanuc** | El "cerebro" de la máquina; el programa se escribe en su lenguaje | [[Torno y control]] |
| **Código G** | Orden de movimiento o modo de trabajo (G00, G01, G71...) | [[Códigos G]] |
| **Código M** | Orden auxiliar de la máquina (husillo, refrigerante, fin de programa) | [[Códigos M]] |
| **Cero pieza** | Punto de la pieza que se toma como X0 Z0 (la punta); se fija con G54 o G10 | [[Estructura de un programa]] |
| **Cero máquina** | Punto de referencia fijo de la máquina | [[Formato de archivos WinUnisoft]] |
| **Sistema de trabajo (G54)** | Origen de coordenadas guardado para la pieza | [[Códigos G]] |
| **Coordenada absoluta** | X y Z medidas desde el cero pieza | [[Códigos G]] |
| **Coordenada incremental** | U y W: movimiento relativo a la posición actual | [[Códigos G]] |
| **X en diámetro** | En torno X se programa como diámetro, no como radio | [[Estructura de un programa]] |
| **Vc (velocidad de corte)** | Velocidad del filo respecto de la pieza, en m/min | [[Fórmulas de corte]] |
| **G96** | Velocidad de corte constante: la máquina varía las RPM al cambiar el diámetro | [[Códigos G]] |
| **G97** | RPM constantes | [[Códigos G]] |
| **G50 S** | Límite máximo de RPM | [[Códigos G]] |
| **Avance (F)** | Cuánto avanza la herramienta: mm/vuelta (G99) o mm/min (G98) | [[Fórmulas de corte]] |
| **Profundidad de corte** | Cuánto material saca cada pasada | [[Ciclos G90 G94 G71 G72 G70 G74]] |
| **Sobrematerial** | Material que se deja para la terminación (U y W en G71/G72) | [[Ciclos G90 G94 G71 G72 G70 G74]] |
| **Desbaste** | Sacar mucho material rápido, sin precisión final | [[01 Método de trabajo]] |
| **Terminación** | Pasada final que da la medida y el acabado | [[01 Método de trabajo]] |
| **Cilindrado** | Mecanizar a lo largo de la pieza (reduce el diámetro) | [[Ciclos G90 G94 G71 G72 G70 G74]] |
| **Frenteado** | Mecanizar la cara de la pieza (reduce el largo) | [[Ciclos G90 G94 G71 G72 G70 G74]] |
| **Ranurado** | Hacer una ranura con un inserto angosto | [[Herramientas y plaquitas]] |
| **Tronzado** | Cortar la pieza terminada del resto de la barra | [[TP Peón]] |
| **Taladrado** | Hacer un agujero con broca (ciclo G74) | [[Ciclos G90 G94 G71 G72 G70 G74]] |
| **Inserto (plaquita)** | Pastilla de metal duro intercambiable que corta | [[Herramientas y plaquitas]] |
| **Portaherramienta** | Cuerpo de acero que sostiene al inserto | [[Herramientas y plaquitas]] |
| **Torreta** | Disco que guarda varias herramientas y las cambia | [[Torno y control]] |
| **T0101** | Herramienta 01 de la torreta con el corrector 01 | [[Estructura de un programa]] |
| **Corrector** | Datos de medida de la herramienta que corrigen su posición | [[Estructura de un programa]] |
| **Código de forma** | Número (3 o 4) que indica cómo está orientada la herramienta; exterior 3 o 4, interior 2 | [[Herramientas y plaquitas]] |
| **Radio de punta (r)** | Radio redondeado de la punta del inserto | [[Herramientas y plaquitas]] |
| **Calidad (KU10T, KU30T)** | Tipo de metal duro del inserto, según el material a cortar | [[Herramientas y plaquitas]] |
| **Grupo ISO P, M, K, N, S, H** | Clasificación de materiales: acero, inoxidable, fundición, no ferroso, alta temperatura, endurecidos | [[Fórmulas de corte]] |
| **Bruto** | Pieza sin mecanizar (barra de partida), por ejemplo Ø42 x 130 | [[TP Peón]] |
| **Agarre** | Parte de la barra que sujeta el plato y no se mecaniza | [[TP Peón]] |
| **Hoja de proceso** | Tabla que describe cada operación, sus parámetros y herramientas | [[01 Método de trabajo]] |
| **Rótulo (cajetín)** | Cuadro de datos al pie del plano | [[Rótulo EEST3]] |
| **Subprograma** | Parte de programa que se llama con M98 y termina con M99 | [[Códigos M]] |
| **Simulador** | Programa que muestra la máquina y la pieza sin cortar metal | [[Torno y control]] |
