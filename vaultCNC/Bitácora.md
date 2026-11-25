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
