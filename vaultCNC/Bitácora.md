---
tipo: bitácora
tags: [bitacora]
---

# Bitácora

## 2026-11-24: se crea el vault

**Qué se hizo.** Se creó vaultCNC a partir de la carpeta de Drive "CNC" (carpeta digital de la materia, catálogo Kennametal, TP Peón y TP Alfil) y de los proyectos originales de WinUnisoft.

**Agentes (Sonnet) y qué hizo cada uno**
El orquestador (Opus) repartió el trabajo en 7 agentes Sonnet. Los encargos y los informes de vuelta se escribieron en **ASD-STE100** (inglés técnico simplificado); las notas, en castellano.
- Lector 1: carpeta digital + catálogo Kennametal → `CNC-fuentes/resumenes/carpeta_digital.md`.
- Lector 2: TP Peón (hoja de proceso, plano, rótulo) → `tp_peon.md`.
- Lector 3: TP Alfil (hoja de proceso, plano, informe .docx) → `tp_alfil.md`.
- Programador 1: `herramientas/simular_nc.py` (validador y dibujo de trayectorias). Los dos programas originales pasan sin errores.
- Programador 2: `herramientas/generar_winunisoft.py` (JSON de pieza → proyecto WinUnisoft).
- Programador 3: `herramientas/plano_freecad.py` + plantilla del rótulo (JSON de pieza → plano PDF en FreeCAD).
- Documentador: las notas de este vault.
El orquestador bajó del Drive los .zip de WinUnisoft, confirmó que son texto plano (se pueden generar directo) y definió el formato común de pieza (`Piezas/FORMATO.md`).

**Decisiones del usuario**
- Se publica **sin nombres**: el repositorio es público, así que se escribe "el alumno" y "el profe".
- El desbaste se hace con **G90**, como en los TP, y no con G71.
- Cada TP nuevo lleva **informe completo** (ver [[01 Método de trabajo]]).

**Preguntas abiertas**
1. **Material.** Los rótulos dicen SAE 4140 (grupo P), pero la hoja de proceso dice "Acero Inoxidable (M)" y las velocidades se tomaron del grupo M. En el Alfil parece texto heredado del Peón. Falta confirmar con el profe.
2. **Modelo del torno real.** No figura en ninguna fuente. Ver [[Torno y control]].
3. **Wansoft vs WinUnisoft.** La carpeta usa Wansoft con FANUC 0iT; los proyectos usan WinUnisoft con Fanuc 16iTA. No sabemos si la escuela usa los dos.
4. **M03 / M04.** La carpeta los describe al revés en una tabla. Se adoptó el estándar Fanuc (ver [[Códigos M]]).
5. **Las 6 unidades de más en el tronzado** (Z-80 con largo 74; Z-99 con largo 93): se interpretan como el ancho del inserto.
6. **Páginas finales de la carpeta.** La lectura cortó en la página 80; faltan el seteo de herramienta y los parámetros del simulador.

**Pendiente**
- ~~Terminar `plano_freecad.py` y `generar_winunisoft.py`~~: hecho (ver [[00 Inicio]]).

## 2026-11-24 (tarde): TP 7°1 de Peón, Alfil y Torre
- El alumno pasó un dibujo con tres piezas y medidas aproximadas. Se armó un JSON por pieza (`Piezas/tp71_*.json`, solo local) y se generaron el plano, el proyecto WinUnisoft y el informe de cada una. Ver [[TP 7°1 - Peón, Alfil y Torre]].
- **Errores corregidos en `plano_freecad.py`:**
  - FreeCAD 1.1 proyecta las vistas en segundo plano, así que el script ahora espera a que tengan geometría (`esperar_geometria`).
  - La torre tiene la cara de arriba plana y no hay vértice en el eje: la cadena de cotas arranca de cualquier vértice en Z0.
  - Las cotas muestran el valor del JSON (antes salía 2,99 en vez de 3).
  - Los radios grandes (R25, R40) van como texto con una línea corta, porque la cota de radio trazaba la línea desde un centro que caía fuera de la hoja.
  - Dos arcos seguidos del mismo radio (collarín) llevan una sola cota.
- La mitra del alfil primero tenía dos arcos R6 con una muesca entre ellos. Se cambió por un solo arco R6 tangente.

## 2026-11-24 (noche): capturas del catálogo Kennametal en los informes
- Agentes (Sonnet, encargos en ASD-STE100):
  - Un analista estudió el TP original. Las herramientas se marcan con resaltador amarillo sobre el código, con una página por herramienta (portaherramienta arriba, inserto abajo), más las tiras de velocidad A5 y A71 y el gráfico A70.
  - Un extractor ubicó cada herramienta en el catálogo (página PDF = etiqueta + 6) y armó las capturas resaltadas.
  - Un verificador independiente revisó cada captura y cada dato contra el catálogo: todo correcto.
  - Un programador las integró a `informe_tp.py` (`--capturas`).
- **Decisión de coherencia:** el SAE 4140 es acero aleado, grupo P. Los programas pasaron a usar las Vc del grupo P: T0101 150 m/min (KU30T, el grado del CNMG-RP), T0303, T0909 y T1010 200 m/min (KU10T) y ranurado 120 m/min (A71). Los TP anteriores usaban el grupo M (180 y 105). Las Vc van en el JSON (`"vc"`) y `generar_winunisoft.py` las lee.
- **Nota abierta:** los insertos de ranurado A4G…GMP son para inoxidable; A70 recomienda GMN para acero. Se mantuvo GMP porque era la selección aprobada en el TP anterior. Consultar con el profe.
- Los informes se subieron a Drive como Google Docs, en la carpeta CNC/TP 7°1, junto con los PDF de los planos. Las capturas del catálogo quedan solo locales, porque son material de Kennametal.

## 2026-11-24 (noche): revisión de los informes en Google Docs
- Tres revisores (Sonnet, uno por informe) exportaron cada Google Doc a PDF y lo revisaron página por página. El plano, el programa y los datos estaban bien. Encontraron problemas de maquetación:
  - la tabla del rótulo ocupaba media hoja;
  - la trayectoria salía chica y sin epígrafe;
  - la tabla de la pieza se partía;
  - había tiras de avance huérfanas;
  - una captura cortaba una fila de la tabla;
  - faltaban acentos.
- Un programador corrigió `informe_tp.py` y volvió a recortar las capturas:
  - tablas con ancho fijo en dxa y celdas combinadas;
  - imágenes ajustadas al área útil y centradas;
  - salto de página antes de "Características pieza";
  - las tiras quedan al 75 % del ancho.
- Aprendido: Google Docs no respeta "mantener con el siguiente" en bloques largos. Hay que dejar margen de alto en lugar de confiar en keepNext.

## 2026-11-24 (noche): herramientas elegidas por el orquestador y vista lateral
- El alumno pidió que las herramientas las elija la IA. Cambios:
  - T0909 pasa a ser el portaherramienta neutro DVVNN 2020K16KC04 (código de forma 8) y termina el perfil en los dos sentidos.
  - T0505 usa el inserto A4G…GMN, el de acero, y también tronza (3 mm).
  - Se dejan de usar T1010 y T1111.
- Un agente hizo las capturas nuevas (A28 DVVNN, A73 GMN, A70 GMN). El agente del generador se cortó por el límite de uso de Sonnet a mitad de la tarea. El orquestador revisó lo que dejó, que andaba, y le agregó la salida en dos pasos de los rápidos diagonales.
- Informe: la carátula muestra un recorte de la vista lateral del plano (`recorte_vista_lateral`).
- WinUnisoft en Linux: hay Wine 10 instalado. El instalador está en un pendrive, junto a una carpeta "Crack". El orquestador no ejecuta instaladores de origen desconocido ni cracks: lo instala el alumno con la licencia de la escuela.

## 2026-11-24 (noche): consigna G90 y velocidades verificadas
- **Consigna del TP:** la mayor parte del desbaste va con el ciclo **G90**. G01 queda solo donde hace falta o para entrar y salir del bruto. Antes, los valles (cuellos detrás de los collarines) se vaciaban con muchas entradas G01 de la T0505. Ahora la T0505 abre una ranura con G01 junto a la pared y desde ahí vacía el valle con **ciclos G90** hacia −Z. El inserto A4 sirve para ranurar y para tornear (página A75).
- Pasadas de desbaste con G90: Peón 15, Alfil 14, Torre 8 (T0101 + T0505). Los G01 que quedan son el refrentado y las entradas y salidas de las ranuras.
- **Velocidades verificadas** en el catálogo, herramienta por herramienta (grupo P):

| Herramienta | Inserto | Grado | Vc | Página |
|---|---|---|---|---|
| T0101 | CNMG-RP | KU30T | 150 m/min (500 sfm) | A5 |
| T0303 y T0909 | VNMG-FP | KU10T | 200 m/min (650 sfm) | A5 |
| T0505 | A4G-GMN | KU30T | 120 m/min (400 sfm) | A71 |

  El catálogo no cambia la velocidad según la dureza, el desbaste o el rompevirutas. Solo imprime el valor de arranque; el rango sale de la barra del gráfico.
- WinUnisoft: los 3 proyectos se simulan sin colisiones ni errores. `wusctl.py` ahora cierra sola la ventana de bienvenida.

## 2026-11-25: radios de punta y simulación pausada
- Los radios de punta de T1 y T3 venían de la plantilla (0,2). `generar_winunisoft.py` ahora escribe los de los insertos elegidos: **0,8** (CNMG120408) y **0,4** (VNMG160404). Los `.nc` no cambian porque no hay compensación de radio.
- **Error encontrado en `wusctl.py`:** al arrancar, WinUnisoft escribe un `.LOG` con `Ttime=0.00`, y el script lo tomaba como final. Si en "Control parada" está tildado **Cambio Hta.**, la simulación se pausa en el primer cambio de herramienta y el script daba "sin colisiones" sin haber terminado. Ahora espera un `Ttime` mayor que 0 y, si no llega, avisa que la simulación quedó pausada.
- **Pantalla oculta (Xvfb).** El alumno instaló xvfb. WinUnisoft corre en Xvfb :99 dentro del escritorio virtual de Wine, así las simulaciones no aparecen en el escritorio. Sin gestor de ventanas Wine ignoraba los clics, y dentro del escritorio virtual sí funcionan con XTest. Lanzador: `herramientas/winunisoft_oculto.sh`. `wusctl.py` detecta el fin de la simulación mirando el botón Abortar, porque el `.LOG` queda en `Ttime=0.00`.
- Los 3 TP, con los radios nuevos, se simularon en la pantalla oculta: llegan a M30 sin colisiones y con la forma correcta.

## 2026-11-25: transcripción del catálogo Kennametal
- **Pedido del alumno:** transcribir el catálogo completo al vault, con imágenes donde hagan falta, y clasificar cada herramienta por comando: T0101 desbaste, T0303 definición, T0505 ranurado, y un sector aparte para el resto. También filtrar las más útiles para las piezas de ajedrez.
- **Agentes:** 9 agentes Sonnet, uno por sección, con los encargos en ASD-STE100 y un formato común (`Kennametal/_FORMATO agentes.md`):
  - insertos de torneado
  - portaherramientas exteriores
  - barras de mandrilar
  - Top Notch
  - A4/A2
  - roscado
  - brocas
  - fresado
  - sistemas de sujeción

  Lanzados los 9 juntos, fallaron sin dar el motivo. De a 3 o 4 anduvieron. Dos se cortaron por el límite de 5 horas de Sonnet y se retomaron después.
- **Método:** el texto extraído del PDF desarma las tablas, así que cada tabla se comparó con la imagen de la página. Los datos que no se leían bien quedaron marcados con `(?)`. Los textos explicativos se resumieron; las tablas se transcribieron completas.
- **Resultado:** más de 110 notas y unas 85 imágenes en `Kennametal/`. La carpeta queda **solo local**, excluida en `.gitignore`, porque es material de Kennametal. El índice por comando se arma con `herramientas/indice_kennametal.py`. Las elegidas para ajedrez están en la nota "Herramientas para piezas de ajedrez".
- **Hallazgos para el TP:**
  - El rompevirutas RP pide pasadas de 1,1 mm o más por lado, y el programa desbasta con 1 mm.
  - El rompevirutas FP pide 0,3 mm o más, y el semiacabado corta 0,2 mm.
  - El inserto A4G0305 mide 3,05 mm de ancho y tiene radio 0,2.
  - El portaherramientas A4SM 2016K0317 tiene mango de 20×16. Existe el 2020K0317, de 20×20.

  Todavía no se cambió nada en el programa.

## 2026-11-25: pasadas y cuchilla según el catálogo
- **Desbaste:** el G90 pasó a 2,4 mm en diámetro (1,2 por lado) desde la primera pasada. Antes arrancaba en Ø29, o sea 0,5 por lado, y RP pide de 1,1 a 6,4 mm.
- **Sobremetal:** el desbaste deja 0,6 mm por lado. La T0303 corta 0,3 y la T0909 0,3, ambas dentro del rango de 0,3 a 2,5 mm de FP.
- **T0505:** el ancho pasó a 3,05 mm, con radio 0,2 en el `.prj` (A73).
- **Simulación en la pantalla oculta:** los 3 programas llegan a M30 sin colisiones. Los tiempos bajaron: Peón 25:35, Alfil 29:32 y Torre 18:23.
- **Informes:** se regeneraron con una aclaración sobre las profundidades de pasada y se subieron a Drive como Google Docs nuevos. Los anteriores quedaron renombrados "(versión anterior)".

## 2026-11-25: TP Completacarrera, herramientas en par
- **Pedido del alumno:**
  - Pasó dos croquis (peón y alfil) para ponerles medidas y corregir la simetría.
  - Pidió que la IA inventara una torre.
  - Pidió usar las herramientas invertidas (T0202, T0404…) donde el catálogo lo permita, con solo los códigos de los TP originales.
  - Pidió minimizar pasadas y tiempo.
- **Decisiones del orquestador:**
  - La base es Ø26 y el resto se escala en proporción.
  - El collarín del alfil tiene una cara socavada en el croquis: se hizo radial porque ninguna herramienta del catálogo la alcanza.
  - Herramientas: T0101 (DCLN R), T0505 (A4SM 2020K0317, de 20×20), T0303 (DVJN R) y T0404 (DVJN L). No se usan T0202 ni T0606. Ver [[TP Completacarrera - herramientas en par]].
- **Generador (`generar_par`):**
  - G90 de 6 mm en diámetro con F0,4, seguido de una pasada de contorno.
  - En los valles, la T0505 entra en el punto más hondo y hace G90 en los dos sentidos.
  - Las ranuras se cortan a medida.
  - Hay una medición del espesor que corta cada herramienta.
- **Errores corregidos en el camino:**
  - El contorno de la T0101 tomaba como obstáculo material que su misma pasada ya sacaba.
  - El valle se desbastaba desde una entrada pegada a la pared alta, y quedaban 3,8 mm para el acabado.
  - El arco de la bola, desplazado solo en X, no quedaba paralelo.
  - En el plano, la cadena de cotas de la torre pisaba el rótulo (`distribuir` ahora calcula el lugar con la misma cuenta que la cadena).
- **Resultado:** los 3 programas se simulan sin colisiones y tardan unos 10–11 minutos, contra 18–30 del TP anterior.
- **Drive:** los informes están en la carpeta "TP Completacarrera - Peón, Alfil y Torre (herramientas en par)".
- **Papelera:** a pedido del alumno se mandaron a la papelera las 12 versiones anteriores de los informes del primer TP.
- **Revisión de los informes contra el PDF del TP original** (agente Sonnet): faltaban los esquemas de la hoja de proceso y las páginas por herramienta con la ficha de WinUnisoft. Se agregaron con capturas del simulador en la pantalla oculta (`esquemas_wus.py` y Gestor → Herramientas). También se corrigieron estas cosas:
  - el gráfico A70 era chico;
  - la T0404 se nombraba en el alfil, que no la usa;
  - los títulos quedaban pegados a las tablas;
  - las cotas encadenadas se pisaban (`DIM_PASO` pasó de 4,6 a 5,5).
- El TP es de otra alumna, del curso **Completacarrera**, no de 7°1. Se corrigieron el rótulo de los planos y los datos de los informes, y se renombraron la carpeta de Drive y esta nota.

## 2026-11-28: TP Completacarrera, Rey, Alfil y Reina
- **Pedido del alumno:** un croquis a mano con tres piezas, para otro alumno del mismo curso. Se pidió que FreeCAD también corra en segundo plano: ya lo hacía (`QT_QPA_PLATFORM=offscreen`).
- **Medidas:** base Ø26 y lo demás en proporción. Las piezas miden 73 a 88 mm. Ver [[TP Completacarrera - Rey, Alfil y Reina]].
- **El generador tuvo que cambiar para piezas largas:**
  - El G90 termina contra las paredes.
  - La T0505 frena a 0,05 mm de la pared.
  - El acabado hace una pasada previa si le quedan más de 2,4 mm.
  - El control de choque del contorno se recalcula con los tramos que de verdad recorre.
  - El corte de arcos ya no falla cuando el ápice cae en un extremo.
- **Errores encontrados y corregidos:**
  - La medición de profundidad contaba como pasada las caras verticales (daba 6,8 mm y 7,3 mm). Ahora no cuenta la celda que está justo en la pared.
  - En la reina, la unión de la bola con la cúpula daba cotas de Ø3,18 y 3,21. La bola pasó a R2,5 y la unión quedó en Ø4 y Z−4.
- **Resultado:** las tres simulan sin colisiones, en 20 a 23 minutos. Los informes están en Drive, en la carpeta "TP Completacarrera - Rey, Alfil y Reina (herramientas en par)".
- **Compensación del radio de punta (28/11):**
  - El alumno vio en WinUnisoft una marca en la garganta y otra en la bolita de la reina, y material de más en la diagonal de la copa.
  - **Causa:** el programa no tenía en cuenta el radio de punta del inserto.
  - Se le presentaron cuatro métodos y eligió compensar en el programa (`compensar()` y `sin_gubias()`). Ver [[TP Completacarrera - Rey, Alfil y Reina]].
  - **Errores corregidos en el camino:**
    - Al salir de la pasada, la herramienta bajaba en X al lado de una ranura, y el radio mordía el disco (sobrecorte de 2,5 mm).
    - Una pasada que empezaba a mitad de la cara mordía la mitra del alfil (0,26 mm).
    - El verificador no tomaba el ancho de la cuchilla en los G90 de la T0505 que avanzan hacia +Z.
  - Las tres piezas simulan lisas y sin colisiones. Los informes nuevos explican la compensación.
