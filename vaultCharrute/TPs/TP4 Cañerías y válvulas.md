---
tipo: tp
materia: Sistemas Mecánicos
profesor: Charrute
numero: 4
tema: Cañerías, válvulas y recorrido del fluido en el sistema
consigna: 2026-06-12
entrega: 2026-06-26
modalidad: grupal (informe técnico de revisión + lámina A3 + defensa oral)
caso: Planta "Panadería Pilar"
tags: [tp, cañerías, válvulas, pérdidas-de-carga, panadería-pilar]
---

# TP4 · Cañerías, válvulas y recorrido del fluido

> [!abstract] En una línea
> **"El recorrido del fluido nunca es neutro."** Las cañerías, los accesorios y las válvulas son parte del diseño: condicionan la pérdida de energía, el mantenimiento y la seguridad. Una planta con los equipos correctos puede funcionar mal por culpa de la red.

Anterior: [[TP3 Variables de proceso]] · Siguiente: [[TP5 Tanques y recipientes a presión]]

## Consigna (resumida)
Esta vez **no hay cuestionario**: es un **informe técnico breve de revisión** (de 1 a 2 páginas) de un sistema: red de aire comprimido, bombeo de agua o calentamiento de agua. Hay que analizar:
1. si el recorrido del fluido es lógico;
2. qué función cumplen las válvulas y los accesorios principales;
3. qué sector puede generar más pérdidas o problemas;
4. qué mejora se propone.

**Preguntas guía:** el tramo más sensible; qué pasa con cambios bruscos de dirección, reducciones o válvulas mal elegidas; válvula de **aislamiento** frente a válvula de **regulación**, aplicado al sistema; equipos bien elegidos y red mal diseñada; por qué una línea larga con muchos accesorios no se comporta igual que una simple; dónde revisar primero (equipo, válvula o tramo); el recorrido desde la geometría, el funcionamiento y la seguridad; una mejora concreta y justificada.

**Defensa oral:** todo el grupo defiende **una sola idea fuerte**: *qué parte del sistema revisarían primero si el proceso no rindiera*.

## Teoría clave del apunte
- [[Cañerías y accesorios|La cañería no es "un tubo por donde pasa algo"]]: condiciona el recorrido, la pérdida de energía, el mantenimiento y la seguridad.
- **[[Pérdidas de carga]]:** son **continuas** (por rozamiento a lo largo del tramo) y **locales o menores** (en codos, tees, reducciones, uniones y válvulas, medidas con un coeficiente K).
- **[[Válvulas]] por función:** de **aislamiento** (abrir o cerrar del todo), de **regulación** (ajustar caudal o presión) y de **retención** o check (impedir el retorno). Una válvula globo abierta pierde mucho más que una esférica abierta.
- **Trazado y seguridad** (ejemplo del vapor de Spirax Sarco): pendiente en el sentido del flujo, drenajes en los puntos bajos, apertura lenta para evitar el golpe de ariete, buenos soportes.
- **Diseño curricular de 7° año:** P&ID, especificaciones de cañerías, uniones, pruebas, soportes y tipos de válvulas.
- **Puente al [[P&ID]]:** según ISA, es el "directorio" del piping y la instrumentación de la planta.

## Nuestra resolución · Planta "Panadería Pilar"
El grupo amplió la consigna a un **informe de ingeniería de toda la planta**, con un plano en AutoCAD (`plano v2.pdf`) y una lámina A3. La nave de producción mide **80 × 20 m** y tiene un sector comercial de 15 m de fondo al frente.

### Parámetros de diseño de las redes
| Red | Color IRAM 2507 | Presión | Caudal | Para qué |
|---|---|---|---|---|
| Aire comprimido | **Azul** | 6–7 bar en la línea / 4,5 bar en la máquina | 450 Nl/min | Cilindros de estirado y guillotina de la empaquetadora |
| Gas industrial | **Amarillo** | 19–22 mbar (baja presión) | 12 m³/h | Quemadores del horno continuo de convección |
| Agua potable | **Verde** | 2,5–3,5 bar | 2,0 m³/h | Amasadora espiral, sanitarios, vestuarios y comedor |
| Desagües | Marrón / negro | Por gravedad (pendiente del 2–3 %) | — | Cloacal (PVC de 110 mm) e industrial (con interceptora de grasa) |

### Las cuatro redes
- **[[Sistema de aire comprimido|Aire comprimido]]:**
  - El compresor y el tanque pulmón van **afuera, en el estacionamiento**: el ruido (más de 80 dBA) y el calor quedan fuera de la nave, y aspiran aire limpio, sin polvo de harina.
  - La cañería aérea recorre unos 80 m con **pendiente descendente del 1–2 %** en el sentido del flujo y **piernas de purga** en los puntos bajos para sacar el condensado.
  - Antes de la empaquetadora hay una **unidad FRL** (filtro, regulador a 4,5 bar, lubricador por efecto Venturi).
- **Gas:**
  - Gabinete de regulación y medición en la línea municipal.
  - Caño de acero con revestimiento epoxi, soldado (resiste mejor las vibraciones).
  - **Válvula esférica de ¼ de vuelta** antes del horno, para cortar en una emergencia.
  - Muro ciego entre el horno y el compresor: las chispas del motor no pueden compartir el aire con los quemadores.
- **Agua:**
  - Caño de PPR termofusionado, enterrado, con derivaciones en T hacia los servicios.
  - **El diámetro pleno se mantiene hasta la amasadora**, para que abrir una canilla del baño no cambie la dosificación de agua de la masa (criterio de **simultaneidad**).
- **Desagües:**
  - **Cloacal:** de los baños a una cámara de inspección de 60 × 60 cm.
  - **Industrial:** el lavado de tinas y bandejas arrastra grasa y almidón, y pasa por una **cámara interceptora de grasa (CIG)** antes de la colectora.

### Empaquetadora neumática (automatización)
1. **Estirado:** una cinta trae el pan, y dos cilindros de doble efecto verticales abren y estiran el film.
2. **Guillotina:** un sensor de carrera comanda una **válvula 5/2 biestable**. El pistón grande baja con una cuchilla calefaccionada: corta y sella en un solo golpe.
3. **Expulsión:** la 5/2 conmuta, el pistón vuelve y el pan empaquetado sale hacia el despacho.

### Residuos de purga
El condensado del tanque y de las piernas de purga es una emulsión de agua, aceite y óxido: un **residuo peligroso** (Decreto 351/79, art. 61). Pasa por un **separador de agua y aceite** (decantación + carbón activado):
- el agua clarificada va al desagüe;
- el aceite va a un bidón estanco que retira un operador habilitado.

### Criterios de diseño contra las pérdidas de carga
- **Codos de radio largo (R = 1,5 D)** en todos los giros de 90°: tienen menos K y menos turbulencia.
- **Válvulas elegidas por función:**
  - para **aislar**, esféricas de bronce de paso total (K casi nulo);
  - para **regular**, la FRL;
  - una **check** a la salida del compresor, contra el reflujo.

> [!important] Idea fuerte de la defensa
> Si el proceso no rinde, **lo primero que revisaríamos es la unidad FRL y las trampas de agua al pie de la empaquetadora**. Si la red junta agua o el filtro se tapa con harina, la presión dinámica cae y la guillotina no corta ni sella, aunque el compresor sea excelente.

### Machete para el oral (reparto por subgrupos)
| Subgrupo | Tema |
|---|---|
| 1 | Aire comprimido y empaquetadora: abre y cierra la defensa |
| 2 | Gas industrial: baja presión, válvula de ¼ de vuelta, muro ciego |
| 3 | Agua y desagües: codos de radio largo, CIG, esféricas de bronce |

**Consejos de vocabulario:**
- decir **cañería o línea de conducción**, no "tubo";
- decir **válvula de aislamiento o de regulación**, no "llave de paso";
- repetir la frase: *"el recorrido nunca es neutro"*.

## Archivos en Drive
- Consigna y teoría: `Cañerías, válvulas y recorrido del fluido en el sistema_26.docx`
- Entrega final: `Trabajo Práctico: Sistema de Cañerías - Panadería Pilar` (Docs y PDF). Versiones anteriores: `Proyecto Técnico…` V1 y V2, `Trabajo Práctico Oficial` V1 y V4
- Plano: `plano v2.pdf` (carpeta *Charrute*)
- Oral: `Guía de Exposición Neumática e Hidráulica: Machete del Grupo` (Docs y PDF)

## Ver también
[[Cañerías y accesorios]] · [[Válvulas]] · [[Pérdidas de carga]] · [[P&ID]] · [[Sistema de aire comprimido]] · [[00 Inicio]]
