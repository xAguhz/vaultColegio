---
tipo: guía
tags: [tutorial, empezar]
actualizado: 2026-11-14
---
# Cómo empezar una red propia

Lo mínimo para que un alumno o un profesor arranque. **No hace falta IA ni programar** para los pasos 1 a 4.

## 1. Instalar Obsidian (gratis)
Bajarlo de obsidian.md, elegir *Crear vault nuevo* y ponerle el nombre de la materia. → [[Obsidian]]

## 2. Escribir las primeras notas
- Una nota `00 Inicio` con la lista de temas.
- Una nota por tema, con un título claro. → [[Notas atómicas]]
- Para enlazar, escribir `[[` y el nombre de otra nota. Si la nota todavía no existe, el enlace queda "pendiente" y se crea al hacerle clic. → [[Enlaces y backlinks]]

## 3. Mirar el grafo
El botón de grafo muestra la red. Las notas sin conexiones quedan sueltas: es una pista de qué falta enlazar.

## 4. Dibujar un mapa
Un *Canvas* nuevo, arrastrando las notas al tablero. → [[Canvas y diagramas]]

## 5. Guardarlo y compartirlo (opcional)
- Crear un repositorio en [[Git y GitHub|GitHub]] e instalar el plugin **Obsidian Git**, que sube los cambios solo. → [[Sincronización]]
- Para tener página web, copiar la carpeta `.quartz/` y el workflow de este repositorio. → [[Publicación automática]]

## 6. Sumar la IA (opcional)
Con un asistente como [[Claude Code]] se pueden pasar a notas los apuntes que ya existen, transcribir videos o armar guías. Siempre con las reglas de [[Trabajo con IA]] y [[Privacidad]].

## Plantilla de nota
```markdown
---
tipo: concepto
tags: [materia]
fuente: "apunte del profe, TP3"
---
# Nombre del concepto

> [!summary] En una frase
> Qué es y para qué sirve.

## Detalle
...

## Relacionado
[[Otro concepto]] · [[TP donde aparece]]
```
