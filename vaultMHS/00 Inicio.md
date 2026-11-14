---
tipo: indice
tema: MHS
aliases: [Inicio, MOC MHS]
fuente: "[[Transcripción - MHS explicado (IoT Lab)]]"
tags: [indice]
---
# Model Hardware Standard (MHS): mapa del vault

Vault armado a partir de un solo video: **"¿Por qué Anthropic se está metiendo en el hardware? (MHS explicado)"**, del canal [[IoT Lab]] (29 min, publicado el 1/11/2026). → [Ver en YouTube](https://www.youtube.com/watch?v=3hxdHem70gw)

> [!warning] Una sola fuente
> Todo lo que hay acá sale del video. Fechas, cifras y nombres de empresas están **según el video** y no fueron contrastados con la documentación oficial de Anthropic. Lo que falta verificar está en [[03 Preguntas abiertas]].

## Por dónde empezar
1. [[01 Resumen del video]]: la idea entera en 5 minutos.
2. [[Model Hardware Standard (MHS)]]: el concepto central.
3. [[Capas de control]]: dónde se ubica la IA y dónde no.
4. Los experimentos, que es donde se entiende para qué sirve.
5. [[02 Guía de estudio]]: preguntas para repasar.
6. [[03 Preguntas abiertas]]: por dónde seguir investigando.

## El problema
- [[Interoperabilidad]]: cada máquina "habla" distinto.
- [[API, SDK y protocolo]]: las formas que existen hoy de controlar un equipo.
- [[Código pegamento]]: el trabajo de conectar A con B con C.
- [[Razonamiento físico]]: saber de una máquina no es lo mismo que entenderla.

## La propuesta de MHS
- [[Model Hardware Standard (MHS)]]
- [[Driver MHS]]: el traductor entre la máquina y la capa común.
- [[Ficha del dispositivo]]: capacidades, restricciones y etiquetas en lenguaje natural.
- [[Operaciones read y write]]
- [[Interlock]] y límites: la seguridad no puede depender de que la IA "se acuerde".
- [[Model agnostic]]: no es solo para Claude.
- [[Model Context Protocol (MCP)]]: el antecesor en el mundo del software.

## Cómo encaja la IA
- [[Capas de control]]: la IA arriba, el control rápido y determinista abajo.
- [[Código determinista]]: la IA desarrolla el controlador; no es el controlador.
- [[Orquestación]]: coordinar máquinas distintas.
- [[Interfaz digital]]: sin una "puerta digital", MHS no puede entrar.

## Experimentos que cuenta el video
| Experimento | Qué muestra |
|---|---|
| [[Automatización de laboratorio - curva de dilución]] | 8 horas en vez de semanas de integración |
| [[Alineación de un láser con cámara]] | La IA prueba, corrige y deja un script |
| [[QuEra - recuperación del clock del láser]] | De 58 % a 99,3 % de éxito con código generado |
| [[Líquidos viscosos y burbujas]] | El límite: le falta conocimiento físico |

## Tecnologías mencionadas
[[PLC]] · [[Modbus]] · [[OPC UA]] · [[ActiveX y COM]] · [[USB]] · [[Model Context Protocol (MCP)]]

## Actores
[[Anthropic]] · [[Claude]] · [[HHMI Janelia]] · [[Raspberry Pi]] · [[Universal Robots]] · [[Hugging Face]] · [[QuEra Computing]] · [[IoT Lab]]

## Material de apoyo
- [[Analogías]]: todas las comparaciones del video juntas (impresora, excavadora, lavadora, jefe de cocina…).
- [[Línea de tiempo]]
- [[Mapa MHS.canvas|Mapa visual]]
- [[Transcripción - MHS explicado (IoT Lab)]]: el texto completo con marcas de tiempo.

## Relación con otros vaults
Si también tenés `vaultDoñetz` (automatización industrial), los conceptos de [[PLC]], Ladder y lógica cableada son la "capa de abajo" de la que habla el video. MHS no los reemplaza: se monta encima.
