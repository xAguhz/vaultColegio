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
