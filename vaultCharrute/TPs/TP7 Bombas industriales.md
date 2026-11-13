---
tipo: tp
materia: Sistemas Mecánicos
profesor: Charrute
numero: 7
tema: Bombas industriales
consigna: 2026-09-25
entrega: 2026-10-09
modalidad: grupal (2 cuestionarios de 8 preguntas + investigación + exposición de 10 min)
tags: [tp, bombas, cavitación, NPSH, curvas, BEP]
---

# TP7 · Bombas industriales

> [!abstract] En una línea
> **"El diagnóstico de bombas es, en realidad, diagnóstico del sistema de bombeo."** El caudal real no lo decide la bomba sola: sale del cruce entre la **curva de la bomba** y la **curva del sistema**. La cavitación casi siempre viene de la **aspiración**, no del impulsor.

Anterior: [[TP6 Intercambiadores de calor]] · Siguiente: [[TP8 Compresores de aire]]

## Consigna (resumida)
- **Dos cuestionarios** del apunte, de 8 preguntas cada uno: funcionamiento y clasificación; curvas, cavitación, selección y diagnóstico.
- **Investigación grupal:**
  - clasificar las bombas y comparar centrífugas con las de desplazamiento positivo;
  - componentes de la centrífuga;
  - **curva real de una bomba comercial**, interpretando Q, H, η, BEP y NPSHR;
  - punto de operación; cavitación; NPSHA frente a NPSHR; cebado y marcha en seco; bombas en serie y en paralelo.
- **Caso real:** una bomba con documentación oficial del fabricante (no una publicación de venta).
- **Caso obligatorio:** *ruido intenso, vibraciones y menos caudal; el nivel del tanque está más bajo y el filtro de aspiración, sucio.* No vale responder "cambiar la bomba".
- **Cierre:** *¿por qué la selección correcta exige estudiar primero el sistema y no empezar por un catálogo?*

## Teoría clave del apunte
- **[[Bomba]]:** transfiere **energía mecánica** a un líquido. Más precisa que decir "mueve agua" o "crea presión".
- **Familias:**
  - **rotodinámicas**: la centrífuga, para caudales medios y altos con líquidos poco viscosos;
  - **desplazamiento positivo**: alternativas (pistón, diafragma) y rotativas (engranajes, tornillo, lóbulos), para poco caudal, alta presión, líquidos viscosos o dosificación.
- **Centrífuga:**
  - el líquido entra por el centro del **impulsor**, sale acelerado y la **voluta** convierte la velocidad en presión;
  - no "chupa" el líquido;
  - partes: impulsor, carcasa, eje, rodamientos, sello (mecánico o empaquetadura) y bocas.
- **Impulsores:**
  - **cerrado** para líquidos limpios (mejor rendimiento);
  - **semiabierto o abierto** para líquidos con sólidos.
- **Seguridad:**
  - con la salida bloqueada, una centrífuga llega a la presión de *shut-off* (finita) y calienta el líquido;
  - una de desplazamiento positivo **sigue desplazando y la presión sube hasta romper**, por eso necesita una **válvula de alivio**.
- **Caudal Q y altura H:**
  - H = desnivel + diferencia de presión + **pérdidas** (cañerías, codos, válvulas);
  - presión y altura se relacionan por la densidad: Δp = ρ·g·H.
- **Curva H–Q** de la bomba (H baja cuando Q sube) y **curva del sistema** (sube con Q²): su cruce es el **punto de funcionamiento**. Si se cambia una válvula o una cañería, el punto se mueve aunque la bomba sea la misma.
- **Potencia y rendimiento:**
  - P_hid = ρ·g·Q·H;
  - η = P_hid / P_eje;
  - el **BEP** (*best efficiency point*) es el punto de mejor rendimiento.
- **Regulación del caudal:**
  - **estrangular** con una válvula funciona, pero desperdicia energía;
  - el **variador de frecuencia** adapta la velocidad.
- **Cebado:** muchas centrífugas no son autocebantes. Con aire no bombean, y no se arregla dejando el motor girando más tiempo.
- **Marcha en seco:** destruye sellos y superficies, porque el líquido también refrigera y lubrica.
- **Cavitación:**
  - la presión local cae por debajo de la **presión de vapor** → se forman burbujas → **colapsan** al llegar a una zona de más presión;
  - síntomas: ruido de "grava", vibración, pérdida de rendimiento y erosión del impulsor.
- **Causas de cavitación:** nivel bajo, mucha altura de succión, pérdidas o filtro sucio en la aspiración, válvula entrecerrada, **líquido caliente** o caudal excesivo.
- **NPSH:** el **NPSHA** lo da la instalación; el **NPSHR** lo pide la bomba. Tiene que cumplirse NPSHA > NPSHR con margen.
- **Fallas que se repiten en sellos o rodamientos:** hay que buscar la causa (desalineación, vibración, marcha en seco, esfuerzos de las cañerías). Cambiar el repuesto no alcanza.
- **Serie y paralelo:**
  - **en serie** suma altura con un caudal parecido;
  - **en paralelo** suma caudal;
  - en ningún caso es una suma directa, porque el punto se mueve sobre la curva del sistema.
- **Sobredimensionar "por las dudas"** obliga a estrangular, desperdicia energía y saca a la bomba de su BEP.
- **Mantenimiento basado en condición:** tendencias de presión, caudal, vibración, temperatura y potencia.

## Nuestra resolución (informe técnico)
El grupo se repartió en **3 subgrupos**:
1. Termohidráulica, NPSH y cebado.
2. Máquinas, sellos y seguridad.
3. Curvas, BEP y diagnóstico.

### Cuestionario 1
| # | Caso | Respuesta |
|---|---|---|
| 1 | Aceite viscoso, poco caudal y mucha presión | Una centrífuga con líquido viscoso se degrada (baja H y Q, y η cae por debajo del 30 %; HI 9.6.7). Va una **de desplazamiento positivo** (engranajes o tornillo) |
| 2 | Dos bombas iguales con distinto caudal | Las **curvas del sistema** son distintas: la red corta y ancha da más Q; la larga o con más desnivel, menos Q |
| 3 | ¿"Crea presión" o "entrega energía"? | **Entrega energía**. La presión es la manifestación de la resistencia que opone el sistema |
| 4 | Bomba sobre el nivel del tanque que no arranca | Revisar el **cebado**: el aire es unas 800 veces menos denso que el agua. Mirar la válvula de pie, el llenado y las entradas de aire |
| 5 | Agua limpia o con sólidos | Impulsor **cerrado** para agua limpia (η de 80–85 %); **semiabierto, abierto o vórtex** con sólidos |
| 6 | Descarga más larga, con más accesorios | Sube k_sistema en h_f = k·Q², la curva se empina y baja Q. La bomba no perdió fuerza |
| 7 | El sello falla una y otra vez | El sello es la **víctima**: desalineación, eje flexionado, cavitación, marcha en seco, esfuerzos de las cañerías |
| 8 | Salida bloqueada | Centrífuga: presión de *shut-off* y el líquido hierve. Desplazamiento positivo: la presión sube hasta reventar, así que lleva una **PRV obligatoria** |

### Cuestionario 2
| # | Caso | Respuesta |
|---|---|---|
| 1 | Bomba grande con la válvula entrecerrada | Funciona, pero desperdicia energía, la bomba queda lejos del BEP y aparecen **empuje radial**, recirculación y desgaste. Alternativas: variador o rebajar el impulsor |
| 2 | Elevar 15 m con 20 m de cañería o con 300 m | Lo que cuenta es la **H total** = 15 m + pérdidas: unos 16–17 m en un caso y unos 30–40 m en el otro |
| 3 | Ruido de grava con el tanque bajo | **Cavitación**: baja z_nivel, el NPSHA queda por debajo del NPSHR y las burbujas implotan |
| 4 | El NPSHR solo no alcanza | Es la **demanda** de la bomba; el **NPSHA** es la **oferta** de la instalación. Hay que verificar NPSHA ≥ NPSHR + 0,6–1 m |
| 5 | Lejos del BEP, pero con el caudal requerido | Empuje radial, fatiga del eje, recirculación, calor y costo energético |
| 6 | Sube la temperatura del líquido | Sube la presión de vapor (agua a 20 °C: 0,24 m.c.a.; a 75 °C: 3,93 m.c.a.), y así se pierden unos 3,7 m de NPSHA |
| 7 | Bomba en su BEP o bomba grande estrangulada | **La del BEP**: fuerzas balanceadas, menos vibración (ISO 10816), la válvula no se erosiona y el motor trabaja en su zona |
| 8 | Caudal insuficiente | **Protocolo en 3 fases**: (1) instalación: válvulas, filtros, nivel, entradas de aire; (2) grupo motor: sentido de giro, RPM, amperes, alineación, presiones reales; (3) interior: impulsor, anillos de desgaste, erosión |

### Idea fuerza del grupo
> *"Una bomba nunca se analiza ni se diagnostica de manera aislada: el caudal, la altura y las fallas son el resultado de la interacción entre la máquina y la instalación."*

### Preguntas trampa preparadas para la mesa
- **Si se agranda el diámetro de la descarga,** la curva del sistema se aplana: hay **más** Q, **más** potencia y el motor consume **más** corriente.
- **Con la válvula cerrada,** Q = 0, así que P_hid = 0 y la potencia es mínima (aunque no hay que dejarla así: se calienta).
- **La reducción excéntrica** de la aspiración se pone **con la cara plana hacia arriba**, para que no se junten bolsas de aire.

### Caso obligatorio, en síntesis
Con nivel bajo + filtro sucio + ruido + vibración + menos caudal, el diagnóstico es **cavitación por NPSHA insuficiente**.
1. **Verificar:** nivel, ΔP en el filtro, posición de las válvulas, presión en la succión, temperatura del líquido y entradas de aire.
2. **Medidas:** recuperar el nivel mínimo con una alarma de nivel bajo, limpiar el filtro con un plan periódico (o poner un ΔP que avise) y revisar el impulsor recién después.

## Archivos en Drive
- Teoría y cuestionarios: `Bombas_26.docx` (dos copias)
- Consigna de la investigación: `Bomb indTPgrup_26.docx`
- Entrega: `TP7 Investigacion - Bombas Industriales` (Google Docs, 09/10/2026)

## Ver también
[[Bomba]] · [[Sistema de bombeo de agua]] · [[Pérdidas de carga]] · [[Variables de proceso]] · [[00 Inicio]]
