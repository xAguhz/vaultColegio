---
tipo: script
tags: [script, python, agentes]
archivo: vaultMHS/herramientas/generar_indice.py
actualizado: 2026-11-14
---
# generar_indice.py

**Archivo:** [`vaultMHS/herramientas/generar_indice.py`](https://github.com/xAguhz/vaultColegio/blob/main/vaultMHS/herramientas/generar_indice.py) · Python, solo biblioteca estándar.

Lee las [[Frontmatter y propiedades|propiedades]] y los enlaces de todas las notas de `vaultMHS` y escribe:
- `indice.json`: el vault entero en un solo archivo, para que **otra IA o un programa** lo entienda sin abrir nota por nota;
- `Mapa MHS.canvas`: el mapa visual, agrupado por tipo de nota.

Además avisa si hay **enlaces rotos**. → [[Vault - MHS]]
