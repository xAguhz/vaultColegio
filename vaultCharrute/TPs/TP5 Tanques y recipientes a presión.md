---
tipo: tp
materia: Sistemas Mecánicos
profesor: Charrute
numero: 5
tema: Tanques de almacenamiento y recipientes a presión
consigna: 2026-08-07
entrega: 2026-08-20
modalidad: grupal (cuestionario de 16 preguntas + investigación técnica + exposición de 10 min)
tags: [tp, tanques, recipientes-a-presión, API-650, ASME-VIII, seguridad]
---

# TP5 · Tanques de almacenamiento y recipientes a presión

> [!abstract] En una línea
> Los dos *contienen* fluidos, pero en condiciones muy distintas. En el tanque mandan el **nivel, la presión hidrostática y la corrosión**; en el recipiente a presión mandan la **energía almacenada, los esfuerzos en la envolvente y la seguridad**. La pregunta ya no es *qué equipo es*, sino *bajo qué condiciones trabaja y qué pasa si falla*.

Anterior: [[TP4 Cañerías y válvulas]] · Siguiente: [[TP6 Intercambiadores de calor]]

## Consigna (resumida)
El TP tuvo dos partes.

**1) Cuestionario del apunte (16 preguntas).**
- *Tanques:*
  - nivel bajo y una bomba irregular;
  - misma altura con distinto líquido;
  - elevar un tanque;
  - "no pierde, entonces está bien";
  - producto, material y corrosión;
  - las conexiones "no importan";
  - capacidad para alimentación continua frente a reserva;
  - qué datos hacen falta para elegir un tanque.
- *Recipientes:*
  - por qué no se diseñan igual que un tanque aunque se parezcan;
  - por qué es peligroso que se rompa aunque el gas sea inocuo;
  - más presión con el mismo espesor;
  - esfuerzos circunferenciales y longitudinales;
  - manómetro frente a protección contra sobrepresión;
  - válvula manual frente a válvula de seguridad;
  - corrosión sin fuga;
  - analizar todo junto.

**2) Investigación grupal.** "No reunir definiciones de Internet", sino usar fuentes confiables y **ejemplos reales**.
- *Tanques:* clasificación, verticales y horizontales, techo fijo y flotante, materiales, conexiones, corrosión, variables y fallas. Un ejemplo real con sus datos. Qué es **API 650** y por qué **no** es "la norma de todos los tanques". Conclusión: *¿qué necesita saber un técnico antes de especificar un tanque?*
- *Recipientes:* envolvente y cabezales, esfuerzos, sobrepresión, válvulas de alivio, inspección y pruebas. Un ejemplo real, como un depósito de aire. Qué regula **ASME BPVC Sección VIII**. Conclusión: *¿por qué no se puede fabricar un recipiente "aumentando a ojo" el espesor de un tanque?*
- *Exposición:* unos 10 min, sin leer el informe.

## Teoría clave del apunte
- **[[Tanque]]:**
  - almacena, pero **no** aporta energía;
  - la capacidad se elige según el servicio;
  - puede ser vertical, horizontal o rectangular, con techo fijo o flotante, apoyado, elevado o enterrado.
- **Presión hidrostática** P = ρ · g · h: crece con la profundidad y con la densidad. El fondo y la fundación cargan con todo el peso del líquido.
- **Variables:** nivel (la principal), temperatura y, a veces, presión.
- **Conexiones:** entrada, salida, drenaje, venteo, instrumentos y boca de inspección.
- **Corrosión:** puede adelgazar la pared **sin que haya una pérdida visible**.
- **[[Recipiente a presión]]:**
  - contiene un fluido a una presión distinta de la exterior;
  - **almacena energía**, más todavía si es gas, por su compresibilidad;
  - no es "un tanque cerrado".
- **Forma:**
  - cilindro con cabezales (elípticos, hemisféricos o torisféricos) o esfera;
  - en el cilindro, el **esfuerzo circunferencial es mayor que el longitudinal**.
- **Presión de operación y presión de diseño:** se diseña con margen para arranques, paradas y fallas.
- **Sobrepresión:**
  - se protege con **válvulas de seguridad o alivio**, que no son válvulas de operación;
  - tener el dispositivo no autoriza a operar fuera del diseño.
- **Inspección y ensayos:** END en las soldaduras y **prueba de presión con procedimiento** (no es "ver hasta cuánto aguanta").
- **Normas:**
  - **ASME BPVC Sec. VIII** para recipientes (más de 15 psig);
  - **API 650** para tanques soldados de petróleo, y solo para eso.
- **Cuidado con el resumen** "el tanque trabaja sin presión y el recipiente con presión": sirve como primera idea, pero la diferencia real depende del servicio, la presión, la temperatura y el código.

## Nuestra resolución
### Cuestionario, en resumen
| Pregunta | Respuesta del grupo |
|---|---|
| Bomba irregular con nivel bajo | Había que mirar el **nivel**. Con poca columna hay **cavitación** o vórtices de aire. No es culpa de la bomba |
| Misma altura, distinto líquido | **No** hay la misma presión: P = ρ·g·h depende de la densidad |
| Elevar el tanque | Cambian la estructura y las fundaciones (más viento y sismo), sube la presión disponible aguas abajo y la bomba de llenado necesita más altura |
| Sin pérdidas visibles | Solo prueba que es estanco. Puede haber **picado (pitting)**, fisuras en las soldaduras o asentamientos |
| Producto, material y corrosión | Hay que elegir por compatibilidad química: acero al carbono, inoxidable o recubrimientos |
| "Las conexiones no importan" | **Falso**: una boquilla mal puesta da vórtices, un venteo tapado da **implosión** por vacío y las válvulas son las que permiten cortar |
| Alimentación frente a reserva | Una se dimensiona por caudal y tiempo de retención (pulmón); la otra por autonomía y logística |
| Recipiente y tanque "parecidos" | El estado mecánico y la energía son distintos. Hacen falta código ASME, espesores, cabezales y radiografías |
| Rotura de un gas inocuo | La expansión instantánea produce una **onda de choque** y esquirlas (explosión física) |
| Más presión, mismo espesor | σ = P·D / (2·t): el esfuerzo crece con P y se pierde el margen de seguridad |
| Esfuerzos | La envolvente es una **estructura resistente** con tensión biaxial, no un contenedor pasivo |
| Manómetro y protección | El manómetro solo **indica** y depende de una persona. La **PSV** actúa sola, en milisegundos |
| Válvula manual y de seguridad | Afirmación **errónea y peligrosa**: la manual es de maniobra; la de seguridad está calibrada por resorte y es automática |
| Corrosión sin fuga | Si el espesor queda por debajo del mínimo de diseño, puede fallar de golpe sin avisar |
| Analizar todo junto | Temperatura → material; presión + geometría → esfuerzos; soldadura → eficiencia de junta; END → que las hipótesis sigan valiendo |

### Investigación (informe técnico)
- **Tipos de tanque:**
  - vertical sobre terreno (el más común; la pared trabaja a tracción de aro);
  - horizontal sobre cunas (con flexión entre apoyos);
  - elevado (presión constante sin bomba);
  - enterrado (empuje del suelo, napa y flotabilidad).
- **Techos:**
  - *fijo* para productos poco volátiles;
  - *flotante* (externo o interno, IFR) para reducir la evaporación de naftas y alcoholes.
- **Materiales y corrosión:**
  - acero al carbono ASTM A36 o A283; inoxidable 304L o 316L; PRFV;
  - pitting por agua decantada en el fondo; corrosión microbiológica (MIC);
  - **sobreespesor de corrosión**.
- **Accesorios del tanque:**
  - placa **antivórtice** en la succión;
  - **válvula de presión y vacío** (PVV);
  - *manholes* de DN 600;
  - sumidero de drenaje.
- **Fallas del tanque y su prevención:**
  - **sobrellenado** → corte por nivel alto-alto (SIS, API 2350);
  - **colapso por vacío**;
  - **cubeto de retención** para el 110 % del tanque mayor.
- **Ejemplos reales:**
  - tanque de nafta de techo cónico con IFR de aluminio, radar de nivel y RTD;
  - pulmón de aire comprimido de chapa ASTM A516 Gr. 70 con cabezales elípticos 2:1, PSV con palanca de prueba, manómetro con glicerina y purga automática.
- **API 650:**
  - tanques soldados, verticales, de fondo plano, casi atmosféricos (hasta 2,5 psig, Apéndice F);
  - para presiones de hasta 15 psig se usa la API 620; para enterrados, UL 58 o IRAM; para tanques de incendio, NFPA 22.
- **Esfuerzos en el cilindro:**
  - σ_circ = P·D / (2t), que es **el doble** de σ_long = P·D / (4t);
  - por eso las **soldaduras longitudinales** son las más exigidas.
- **Cabezales:**
  - hemisférico: el óptimo, con la mitad de espesor;
  - **elíptico 2:1**: el estándar;
  - torisférico: concentra tensiones en el nudillo;
  - plano: trabaja a flexión y es el peor.
- **Diseño del recipiente:**
  - presión de diseño y MAWP de un 10–15 % sobre la de operación;
  - la temperatura cambia la tensión admisible (fragilidad en frío, *creep* en caliente);
  - la eficiencia de junta E va de 0,7 a 1, según cuánta soldadura se radiografía.
- **Ensayos:**
  - END: RT, PAUT, PT y MT;
  - **prueba hidrostática** con agua, que es incompresible y por eso segura.
- **ASME VIII Div. 1:**
  - regula materiales, cálculo, WPS/PQR, calificación de soldadores, inspección y certificación;
  - el recipiente aprobado lleva la **estampa "U"**.
- **Por qué no "a ojo":**
  - el espesor no corrige una geometría mala;
  - más soldadura deja más tensiones residuales;
  - la chapa gruesa es más frágil;
  - sin MAWP no se puede calibrar la PSV.

### Tanque y recipiente a presión, comparados
| Criterio | Tanque | Recipiente a presión |
|---|---|---|
| Presión | Atmosférica o muy baja | Distinta de la atmosférica (más de 15 psig) |
| Carga principal | Columna hidrostática y peso | Tensión biaxial por la presión |
| Energía almacenada | Baja | Alta (gas comprimido) |
| Protección | Venteo o PVV | **PSV** calibrada |
| Falla peligrosa | Derrame o implosión | Estallido con onda de choque y esquirlas |
| Norma | API 650 (petróleo) | ASME VIII Div. 1 |

> [!warning] Datos que faltan
> El informe en Google Docs perdió al exportarse las fórmulas y varios números de los ejemplos (capacidades, diámetros, espesores). La versión completa está en el PDF `tp5 charrute investigación.pdf`.

## Archivos en Drive
- Teoría y cuestionario: `Tanques y rec a presion_26.docx`
- Consigna de la investigación: `TP de Inv Grupal RECIP A PRESION_26.docx`
- Cuestionario resuelto: `TP Resuelto: Tanques de Almacenamiento y Recipientes a Presión - EEST N°3`
- Investigación: `Tanques y Recipientes a Presión` (Google Docs; tres copias: 20/08, 18/09 y 09/10) y `tp5 charrute investigación.pdf` (carpeta *Charrute*)

## Ver también
[[Tanque]] · [[Recipiente a presión]] · [[Válvulas]] · [[Normas y códigos]] · [[00 Inicio]]
