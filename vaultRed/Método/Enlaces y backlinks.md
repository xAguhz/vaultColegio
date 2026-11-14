---
tipo: método
tags: [método, enlaces, grafo]
actualizado: 2026-11-14
---
# Enlaces y backlinks

Los enlaces son lo que convierte un montón de notas en una **red**.

## Enlace
Se escribe el nombre de la nota entre dobles corchetes: `[[Compresor]]`. En [[Obsidian]] y en la web se convierte en un link. Con `[[Compresor|el compresor]]` se muestra otro texto.

## Backlink
Es el enlace **visto desde el otro lado**: cada nota muestra qué notas la mencionan. Nadie tiene que escribirlo, aparece solo. En la nota *Compresor* se ven, sin haberlo anotado, el TP2, el TP8, el sistema de aire comprimido y el glosario.

## Grafo
Con todos los enlaces juntos sale el grafo: cada nota es un punto y cada enlace, una línea. La [página de la red](https://xaguhz.github.io/vaultColegio/red/) muestra el grafo de **todos los vaults a la vez**.
- Los puntos grandes con muchas líneas son los **conceptos centrales**.
- Los puntos sueltos son notas que **falta conectar**.

## Reglas que se siguieron
- Enlazar la **primera vez** que se nombra algo con nota propia, no todas las veces.
- Enlazar **en las dos direcciones** cuando tiene sentido: los TP a los equipos, y los equipos a los TP.
- Títulos **únicos**, para que el enlace no sea ambiguo. Si dos vaults tienen una nota con el mismo nombre (por ejemplo `00 Inicio`), [[preparar (script)|preparar.py]] resuelve cada enlace hacia la del propio vault.
- **Cero enlaces rotos** antes de publicar.

Volver a [[02 El método paso a paso]]
