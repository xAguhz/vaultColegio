# vaultColegio

Notas del colegio en Obsidian, publicadas como página web: **https://xaguhz.github.io/vaultColegio/**

| Vault | Contenido |
|---|---|
| `vaultAutoLID/` | Proyecto grupal AutoLID, materias y entregas |
| `vaultTorno/` | TP del torno Femar TM300: manual de mantenimiento, repuestos y despiece 3D |
| `vaultDoñetz/` | Automatización industrial estudiada a partir del canal El Profe Juanito |
| `vaultCharrute/` | Sistemas Mecánicos 2026 (profe Charrute): trabajos prácticos, equipos y guía de estudio |

Cada vault se abre por separado en Obsidian con *Abrir carpeta como vault*.

## Cómo se publica
Cada vez que se sube un cambio a `main`, el workflow `.github/workflows/publicar.yml`:
1. baja [Quartz 4.5.2](https://quartz.jzhao.xyz/);
2. corre `.quartz/preparar.py`, que copia las notas, convierte los Canvas y los dibujos de Excalidraw en páginas y cambia los links a los visores;
3. arma el sitio con la configuración de `.quartz/` y lo publica en GitHub Pages.

La página es de solo lectura. Para editar, se usa Obsidian y se suben los cambios (por ejemplo con el plugin Obsidian Git).
