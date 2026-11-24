# vaultColegio

Notas del colegio en Obsidian, publicadas como página web: **https://xaguhz.github.io/vaultColegio/**

| Vault | Contenido |
|---|---|
| `vaultAutoLID/` | Proyecto grupal AutoLID, materias y entregas |
| `vaultTorno/` | TP del torno Femar TM300: manual de mantenimiento, repuestos y despiece 3D |
| `vaultDoñetz/` | Automatización industrial estudiada a partir del canal El Profe Juanito |
| `vaultCharrute/` | Sistemas Mecánicos 2026 (profe Charrute): trabajos prácticos, equipos y guía de estudio |
| `vaultPedro/` | Taller de Metrología 2026 (profe Pedro Azuaga): Ley 19.511, SIMELA y patrones de medición |
| `vaultSuzuki/` | Manual del Suzuki Swift 1.5XS japonés (ZC21S, 2008): uso, mantenimiento y despiece 3D |
| `vaultClaseProfes/` | Guía para profes: cómo usar la IA y armar un entorno como este, desde cero |
| `vaultOficinaIA/` | Oficina de agentes de IA: un orquestador (Opus) que reparte trabajo a cinco agentes (Sonnet); costos, uso y errores. No se publica en la página todavía |
| `vaultMHS/` | Model Hardware Standard (IA y hardware), investigado a partir de un video |
| `vaultRed/` | El método detrás de todos los vaults: notas, enlaces, herramientas, conectores y trabajo con IA |

**Toda la red en una página:** https://xaguhz.github.io/vaultColegio/red/ (grafo interactivo de todos los vaults, con modo presentación).

Cada vault se abre por separado en Obsidian con *Abrir carpeta como vault*.

## Cómo se publica
Cada vez que se sube un cambio a `main`, el workflow `.github/workflows/publicar.yml`:
1. baja [Quartz 4.5.2](https://quartz.jzhao.xyz/);
2. corre `.quartz/preparar.py`, que copia las notas, convierte los Canvas y los dibujos de Excalidraw en páginas y cambia los links a los visores;
3. arma el sitio con la configuración de `.quartz/`;
4. corre `.quartz/red/red.py`, que arma la página de la red con el grafo de todos los vaults;
5. publica todo en GitHub Pages.

La página es de solo lectura. Para editar, se usa Obsidian y se suben los cambios (por ejemplo con el plugin Obsidian Git).
