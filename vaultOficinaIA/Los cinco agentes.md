---
tipo: referencia
actualizado: 2026-11-17
tags: [oficina-ia, agentes]
---

# Los cinco agentes

Todos usan **Sonnet**. Cada uno tiene herramientas limitadas a su rol (así un error no puede hacer daño fuera de su trabajo) y un tope de turnos (`maxTurns`) para que no se quede dando vueltas.

| Agente | Esfuerzo | Puede | No puede | Devuelve |
|---|---|---|---|---|
| **explorador** 🔵 | medio | leer, buscar, usar la web, comandos de solo lectura | editar, escribir | respuesta + `ruta:línea` + dudas (≤ 40 líneas) |
| **programador** 🟠 | alto | leer, editar, escribir, correr comandos | crear agentes, hacer commit | qué cambió, archivos, verificación (≤ 30 líneas) |
| **probador** 🟢 | medio | leer, correr pruebas, escribir scripts temporales | editar el proyecto | OK / FALLA / NO SE PUDO + fallas exactas |
| **revisor** 🔴 | alto | leer, `git diff` | editar, escribir | APROBADO / CAMBIOS + hallazgos por gravedad |
| **documentador** 🟣 | medio | leer, editar y escribir notas | correr comandos | lista de notas tocadas |

## explorador
Lee mucho y devuelve poco. Empieza siempre por los índices (`MAPA.md`, `GEMINI.md`, `CLAUDE.md`, el inicio del vault). Ideal para: "¿dónde se calcula el total del cotizador?", "resumime esta documentación", "¿qué archivos usan Firebase?". Se pueden lanzar varios en paralelo con preguntas distintas.

## programador
Cambios **chicos y bien definidos**. Toca solo lo asignado, respeta las reglas del proyecto (archivos de menos de ~40 KB, orden de carga, nada de claves) y verifica lo que puede antes de terminar. No hace commit.

## probador
Prueba **de verdad**: corre scripts, abre las páginas con el navegador automático (Playwright), recorre botones, compara antes y después. Simula Firebase para no tocar datos reales de la empresa. No arregla: reporta con el error exacto.

## revisor
Un segundo par de ojos, escéptico. Busca errores, regresiones, problemas de seguridad, **datos sensibles en repos públicos** y supuestos sin confirmar. Solo hallazgos con evidencia.

## documentador
Mantiene los vaults de Obsidian: bitácora, notas de proyecto, glosario. Escribe en el estilo de las notas que ya existen, registra también los errores y sus correcciones, y nunca pone datos sensibles.

## Por qué estos cinco
Salen de lo que se hizo en el proyecto Sain Racks: buscar en código grande (**explorador**), cambiar código (**programador**), probar con el navegador (**probador**), cuidar la privacidad y los errores (**revisor**) y anotar todo en Obsidian (**documentador**). Ver también [[Errores, contradicciones y mejoras]].

Los archivos están en `.claude/agents/` de cada repo. Se pueden editar: cada uno es un `.md` con un encabezado de configuración y las instrucciones del rol.
