---
tipo: explicación
tags: [red, introducción]
actualizado: 2026-11-14
---
# Qué es la red

## El problema
El material del colegio está **desparramado**: apuntes del profe en Word dentro de Google Drive, entregas del grupo en Google Docs, PDF escaneados, manuales en inglés, videos de YouTube, fotos y planos. Cada archivo vive aparte, y para estudiar hay que abrir diez cosas y acordarse de dónde estaba cada dato.

## La idea
Pasar todo eso a **notas cortas en texto plano, enlazadas entre sí**. Cada nota trata **una sola idea** (un equipo, un concepto, un TP, un video) y se conecta con las demás mediante enlaces. El conjunto forma una **red** (un grafo): se puede recorrer por temas, buscar, y ver qué está relacionado con qué. → [[Notas atómicas]], [[Enlaces y backlinks]]

> Un apunte en Word es una lista. Un vault es un mapa.

## Qué es un vault
Un **vault** es simplemente una carpeta con archivos Markdown (`.md`) que [[Obsidian]] abre como una base de notas. Cada materia o proyecto tiene su propio vault, y todos viven juntos en un repositorio de [[Git y GitHub|GitHub]]:

```
vaultColegio/              ← repositorio
├── vaultAutoLID/          proyecto grupal
├── vaultTorno/            TP del torno
├── vaultDoñetz/           canal de YouTube de automatización
├── vaultCharrute/         Sistemas Mecánicos
├── vaultSuzuki/           manual del Suzuki Swift con modelo 3D
├── vaultClaseProfes/      la charla para profes: IA desde cero
├── vaultMHS/              un video sobre IA y hardware
├── vaultRed/              este vault: el método
└── .quartz/               lo que arma la página web
```

## Tres formas de usarla
1. **En Obsidian**, para estudiar y editar: buscador, grafo, backlinks, Canvas.
2. **En la página web** (https://xaguhz.github.io/vaultColegio/), para leer desde cualquier lado, incluso el celular. Se actualiza sola. → [[Publicación automática]]
3. **En la [página de la red](https://xaguhz.github.io/vaultColegio/red/)**, para verla entera de un vistazo.

## Lo que salió de la red
No son solo notas. A partir de ellas se generaron entregas y materiales:
- El **manual de mantenimiento del torno** en Word, armado desde las notas → [[torno_tm300_docx (script)|torno_tm300_docx.py]].
- Un **visor 3D** del torno con despiece y ficha de cada pieza → [[torno_tm300_3d (script)|torno_tm300_3d.py]].
- La **web de demostración** y un **spot publicitario** de AutoLID → [[Publicidad AutoLID]].
- Informes, presentaciones de Google Slides y **guías de estudio por integrante** para los TP de Sistemas Mecánicos → [[html2docx (script)|html2docx.py]], [[slides_gen (script)|slides_gen.py]], [[Guías de estudio]].
- Ilustraciones de equipos para las presentaciones → [[gemini_img (script)|gemini_img.sh]].

## Por qué texto plano
- Se abre con **cualquier programa**, hoy y dentro de 20 años. No depende de una empresa.
- Lo pueden leer **otras personas y otras IA**: por eso algunos vaults traen un `AGENTS.md` que explica su estructura.
- Se puede **versionar con Git**: cada cambio queda registrado con fecha. → [[Sincronización]]
