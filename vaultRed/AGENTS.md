# AGENTS.md: guía para agentes e IA que lean este vault

**vaultRed** explica el método con el que se construyeron los vaults del repositorio `vaultColegio` (Obsidian + Git + Quartz + asistentes de IA). Es Markdown plano con wikilinks de Obsidian.

## Estructura
| Carpeta / archivo | Contenido |
|---|---|
| `00 Inicio.md` | Índice del vault |
| `01`–`05` | Qué es la red, el método en 7 pasos, guion de la presentación, tutorial y preguntas frecuentes |
| `Vaults/` | Una nota por vault del repositorio (`vault:` en el frontmatter apunta a la carpeta) |
| `Método/` | Principios: notas atómicas, enlaces, MOC, frontmatter, Canvas, fuentes, privacidad, IA, sincronización y publicación |
| `Programas/` | Software usado (Obsidian, Git, Quartz, Claude Code, Gemini, Blender, yt-dlp) |
| `Conectores/` | Cómo accede la IA a servicios externos (Drive, Slides, Gemini API, YouTube, Artifacts) |
| `Scripts/` | Una nota por script del repositorio; la propiedad `archivo:` da su ruta |
| `Mapa de la red.canvas` | Mapa visual (JSON Canvas) |

## Convenciones
- Frontmatter YAML con `tipo` (índice, explicación, método, guía, vault, programa, conector, script), `tags` y `actualizado`.
- Los nombres de nota son únicos dentro del vault. Las notas de scripts se llaman `<nombre> (script)`.
- Los otros vaults son carpetas hermanas (`../vaultCharrute/`, etc.) y se abren por separado en Obsidian, así que no hay wikilinks entre vaults: se enlazan por URL del sitio.
- El grafo completo de todos los vaults está en la página https://xaguhz.github.io/vaultColegio/red/ y, como datos, en `red/red.json` del sitio (lo genera `.quartz/red/red.py`).
- Privacidad: no hay nombres de compañeros ni datos de contacto, y no se deben agregar.
