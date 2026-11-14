---
tipo: script
tags: [script, python, web, grafo]
archivo: .quartz/red/red.py
actualizado: 2026-11-14
---
# red.py

**Archivo:** [`.quartz/red/red.py`](https://github.com/xAguhz/vaultColegio/blob/main/.quartz/red/red.py) · Python, solo biblioteca estándar.

Arma la **[página de la red](https://xaguhz.github.io/vaultColegio/red/)**: recorre todos los vaults, encuentra cada nota y cada enlace `[[...]]`, y escribe un archivo `red.json` con el grafo completo y los números de cada vault. La página lo dibuja como un grafo interactivo.

- Lo corre el workflow después de armar el sitio, así **la página siempre está al día**. → [[Publicación automática]]
- También se puede correr a mano para verla en la computadora:
  `python3 .quartz/red/red.py . salida/` y abrir `salida/index.html`.
- Avisa los **enlaces rotos** que encuentra.
