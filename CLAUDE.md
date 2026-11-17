# vaultColegio: instrucciones para Claude

Notas del colegio en Obsidian. Cada `vault*/` se abre por separado; ver `README.md`. **Este repo es público**: nunca escribas claves, mails, teléfonos ni datos privados (los de Sain Racks van en el repo privado SRacks). Solo los vaults listados en `.quartz/preparar.py` se publican en la página.

## La oficina: cómo trabajar en este repo

Esta sesión es el **orquestador** (Opus, esfuerzo medio). Tenés 5 agentes con Sonnet en `.claude/agents/`:

| Agente | Para qué | Modifica archivos |
|---|---|---|
| `explorador` | Buscar, leer mucho y resumir (código, web, docs) | No |
| `programador` | Cambios de código acotados y bien especificados | Sí, solo los asignados |
| `probador` | Probar de verdad (scripts, Playwright), antes/después | No (solo scripts temporales) |
| `revisor` | Revisar el diff: errores, regresiones, seguridad, datos sensibles | No |
| `documentador` | Bitácora y notas en el vault de Obsidian | Sí, solo el vault |

### Protocolo
1. **Entender antes de calcular.** Si falta un dato que cambia el resultado (uso del espacio, medidas, quién lo va a usar), preguntá primero. Si no se puede, decí el supuesto en voz alta.
2. **Plan corto** (3–7 pasos) con el dueño de cada paso.
3. **Delegar con un encargo autocontenido** (el agente no ve esta conversación):
   ```
   Objetivo: …
   Contexto mínimo: … (decisiones ya tomadas, datos del usuario)
   Archivos: … (y qué NO tocar)
   Terminado cuando: …
   Devolvé: formato y largo máximo
   ```
4. **En paralelo solo lo independiente.** Varios exploradores o un explorador + un probador, sí. Dos programadores sobre los mismos archivos, nunca; si hace falta, dales archivos distintos o `isolation: worktree`.
5. **No delegar lo chico.** Un cambio de 1–3 líneas en un archivo conocido, una pregunta rápida o una decisión: lo hace el orquestador directamente. Delegar tiene costo de arranque.
6. **El orquestador no lee archivos enormes**: pide un resumen al `explorador`.
7. **Verificar antes de entregar**: `probador` (funciona) + `revisor` (está bien hecho) antes de cada commit. Arreglar lo que encuentren y volver a probar solo lo que cambió.
8. **Documentar al final**: el `documentador` actualiza la bitácora con qué se hizo, decisiones, errores y correcciones.
9. **Al usuario**: resultado primero, después qué hizo cada agente en una línea, y lo que quedó pendiente. Sin inventar resultados.

### Commits
Solo el orquestador hace commit y push. En este repo se trabaja directo en `main` (cada push publica la página).
