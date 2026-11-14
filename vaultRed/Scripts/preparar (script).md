---
tipo: script
tags: [script, python, web]
archivo: .quartz/preparar.py
actualizado: 2026-11-14
---
# preparar.py

**Archivo:** [`.quartz/preparar.py`](https://github.com/xAguhz/vaultColegio/blob/main/.quartz/preparar.py) · Python, solo biblioteca estándar.

Prepara los vaults para que [[Quartz y GitHub Pages|Quartz]] los publique. Lo corre el workflow en cada push. → [[Publicación automática]]

## Qué hace
1. Copia cada vault **sin** la configuración de Obsidian, las herramientas ni las plantillas.
2. Convierte cada **Canvas** en una nota con el tablero dibujado en HTML, y cada **Excalidraw** en un dibujo SVG. → [[Canvas y diagramas]]
3. Resuelve los **enlaces ambiguos**: si dos vaults tienen una nota `00 Inicio`, cada enlace va a la de su propio vault. → [[Enlaces y backlinks]]
4. Cambia los links a páginas privadas ([[Artifacts de Claude]]) por su copia publicada, y los links a `herramientas/` por el archivo en GitHub.
5. Pone a cada nota la **fecha real** de su último cambio, tomada del historial de Git.
6. Arma las portadas: la del sitio y la de cada vault.
