---
tipo: método
tags: [método, git]
actualizado: 2026-11-14
---
# Sincronización

Los vaults viven en **un repositorio de [[Git y GitHub|GitHub]]** y se sincronizan entre la computadora, otros dispositivos y la IA.

## Cómo
- En Obsidian, el plugin **Obsidian Git** hace commit, pull y push **cada 10 minutos** y trae los cambios al abrir el vault. Los commits automáticos se llaman, por ejemplo, *"pcUbuntu: copia automática del 2026-11-13 08:06"*. → [[Plugins de Obsidian]]
- La IA trabaja sobre una copia del repositorio y sube sus cambios con un mensaje que explica qué hizo.
- Antes se usaba Syncthing. Se cambió a Obsidian Git para tener **historial** y para que la página se actualice sola.

## Qué se gana
- **Historial completo:** se puede ver qué cambió, cuándo y volver atrás.
- **Copia de seguridad** en la nube.
- Cada push dispara la [[Publicación automática]].

## Qué no se sube
El estado de la ventana de Obsidian, cachés y archivos temporales (`.gitignore`).
