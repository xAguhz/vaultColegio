# AGENTS.md: guía para agentes e IAs que lean este vault

## Qué es
Vault de Obsidian (Markdown plano) sobre **Model Hardware Standard (MHS)**, el estándar de Anthropic para que agentes de IA descubran y usen hardware. Se armó a partir de **una sola fuente**: el video de YouTube "¿Por qué Anthropic se está metiendo en el hardware? (MHS explicado)", del canal IoT Lab (https://www.youtube.com/watch?v=3hxdHem70gw, publicado el 2026-11-01, 29:21 min, en español).

## Confiabilidad
- Todo lo que está marcado `estado: segun-el-video` repite lo que dice el video y **no fue verificado** contra documentación oficial.
- Las secciones tituladas **"Contexto general (no del video)"** son conocimiento general agregado para dar contexto. No son afirmaciones del video.
- La transcripción (`Fuente/`) son subtítulos automáticos con nombres propios corregidos. Las correcciones están listadas al principio de ese archivo.
- Lo que hay que verificar está en `03 Preguntas abiertas.md`.

## Por dónde leer
1. `indice.json`: el mapa completo en un solo archivo. Para cada nota da archivo, título, tipo, aliases, relacionado, minutos, tags, resumen, enlaces salientes y `enlazado_desde`. **Empezá por acá** si podés leer JSON.
2. `00 Inicio.md`: índice para humanos, ordenado por tema.
3. `01 Resumen del video.md`: el contenido completo condensado.
4. `Fuente/Transcripción - MHS explicado (IoT Lab).md`: el texto original, para citar.

## Estructura
| Carpeta / archivo | `tipo` | Contenido |
|---|---|---|
| `00 Inicio.md` | indice | Mapa del vault |
| `01 Resumen del video.md` | resumen | Resumen por secciones |
| `02 Guía de estudio.md` | guia | Preguntas de repaso con la nota que las responde |
| `03 Preguntas abiertas.md` | investigacion | Pendientes y verificaciones (checklist) |
| `Analogías.md`, `Línea de tiempo.md` | recurso | Material transversal |
| `Conceptos/` | concepto | Ideas del video, una por nota |
| `Tecnologías/` | tecnologia | Protocolos y tecnologías mencionadas (MCP, PLC, Modbus…) |
| `Experimentos/` | experimento | Casos reales que cuenta el video, con cifras en `datos_clave` |
| `Actores/` | actor | Empresas, instituciones, el modelo y el canal |
| `Fuente/` | fuente | Transcripción completa |
| `Mapa MHS.canvas` | — | Grafo visual de Obsidian (JSON Canvas), generado |
| `indice.json` | — | Índice para máquinas, generado |
| `herramientas/generar_indice.py` | — | Regenera `indice.json` y el canvas, y detecta links rotos |

## Convenciones
- **Links:** `[[Nombre de nota]]` (wikilinks de Obsidian). El nombre es el del archivo sin `.md` y es único en todo el vault. `[[Nota|texto]]` muestra otro texto; dentro de tablas se escribe `[[Nota\|texto]]`.
- **Frontmatter YAML** en cada nota:
  - `tipo`: ver la tabla de arriba.
  - `tema`: siempre `MHS`.
  - `aliases`: otros nombres con los que se busca la nota.
  - `relacionado`: las relaciones **principales**, que son las aristas del canvas.
  - `fuente`: de dónde sale la información.
  - `minutos`: momentos del video (`MM:SS`) donde se trata el tema.
  - `estado`: `segun-el-video` o `abierto`.
  - `datos_clave`: cifras, solo en las notas de experimentos.
  - `tags`
- **Marcas de tiempo:** `[▶ MM:SS](https://www.youtube.com/watch?v=3hxdHem70gw&t=Ns)` abre el video en ese segundo.
- **Callouts:** `> [!warning]` y `> [!info]` son avisos de Obsidian. Las líneas que empiezan con `>` y nombran otro vault (`vaultDoñetz`, `vaultTorno`) son conexiones con otros apuntes del autor, que **no** están en este vault.
- **Idioma:** español rioplatense.

## Si agregás o cambiás notas
1. Mantené el frontmatter y los nombres únicos.
2. Si la información sale de otra fuente, ponela en `fuente` y no uses `estado: segun-el-video`.
3. Corré `python3 herramientas/generar_indice.py` (sin dependencias). Tiene que terminar con "Sin links rotos.".
