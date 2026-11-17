---
tipo: guía
actualizado: 2026-11-17
tags: [oficina-ia, configuración]
---

# Instalación y uso

## Archivos
```
.claude/
├── settings.json        ← orquestador: Opus, esfuerzo medio, máx. 5 agentes a la vez
└── agents/
    ├── explorador.md
    ├── programador.md
    ├── probador.md
    ├── revisor.md
    └── documentador.md
CLAUDE.md                ← reglas del proyecto + protocolo de la oficina
```
Están en **SRacks** (rama `modular`) y en **vaultColegio**.

## Configuración del orquestador (`.claude/settings.json`)
```json
{
  "model": "opus",
  "modelSettings": { "claude-opus-5-5": { "effortLevel": "medium" } },
  "env": {
    "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS": "5",
    "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1"
  }
}
```
- `model: "opus"` usa el Opus más nuevo (hoy Opus 5.5).
- `modelSettings` fija el esfuerzo **por modelo**. El campo viejo `effortLevel` suelto lo ignora Opus 5.5 cuando está en la configuración de usuario; por eso se usa esta forma.
- Como máximo **5 agentes a la vez** (el valor de fábrica es 20), y **los agentes no pueden crear otros agentes**.

## Encabezado de un agente (ejemplo)
```yaml
---
name: revisor
description: Revisa cambios (git diff) buscando errores… Úsalo antes de cada commit…
tools: Read, Grep, Glob, Bash
disallowedTools: Edit, Write, Agent
model: sonnet
effort: high
maxTurns: 30
color: red
---
```
La `description` es lo que usa el orquestador para decidir a quién llamar: tiene que decir **cuándo** usarlo.

## Cómo usarla
- **Abrí una sesión nueva** sobre el repo. Los agentes y la configuración se leen al empezar, no a mitad de una sesión.
- Pedí las cosas normalmente. El orquestador delega solo cuando conviene, siguiendo el `CLAUDE.md`.
- Para forzar a uno: *"usá al revisor para mirar el diff"*, *"mandá dos exploradores: uno al cotizador y otro a órdenes"*.
- En la terminal, `/agents` muestra y edita los agentes; `/model` y `/effort` cambian el modelo y el esfuerzo de la sesión.
- Para tareas difíciles de diseño, subile el esfuerzo al orquestador: `/effort high`.

> [!warning] Sesiones en la nube con varios repos
> En una sesión en la nube con **varios repos a la vez**, Claude Code **no lee** `model`, `env` ni los permisos de `.claude/settings.json` de cada repo. Para que la configuración aplique, abrí la sesión con **un solo repo**, o elegí el modelo y el esfuerzo a mano con `/model` y `/effort`. La configuración de usuario (`~/.claude/settings.json`) tampoco llega a las sesiones en la nube.

## Cómo saber si está funcionando
- Al delegar, la sesión muestra qué agente arrancó y con qué modelo.
- `/status` muestra qué archivos de configuración se cargaron.
- Mirá el consumo con `/usage` (o `/cost`) antes y después de una tarea parecida, para comparar. Ver [[Costo y velocidad]].
