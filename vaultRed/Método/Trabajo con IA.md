---
tipo: método
tags: [método, ia]
actualizado: 2026-11-14
---
# Trabajo con IA

La red se construyó trabajando **con** un asistente de IA, no delegándole todo. Se usaron dos:
- [[Claude Code]]: lee las fuentes, escribe las notas, los enlaces y los scripts, y prepara los cambios en GitHub.
- [[Gemini]]: genera las ilustraciones.

## Qué hace cada uno
| La persona | La IA |
|---|---|
| Elige el tema, las fuentes y el objetivo | Recorre Drive, baja subtítulos, lee PDF |
| Define la estructura (qué notas, cómo se agrupan) | Redacta las notas y las enlaza |
| Revisa, corrige y pide cambios | Corrige, verifica enlaces, explica de otra forma |
| Decide qué se publica | Prepara los commits con un mensaje claro |
| **Estudia y expone** | Arma guías, resúmenes y explicaciones simples |

## Reglas
1. **Las fuentes primero.** La IA trabaja sobre los apuntes, manuales y videos reales, y dice de dónde sale cada cosa. → [[Fuentes y verificación]]
2. **Separar lo que dice la fuente de lo que agrega la IA.**
3. **Revisar antes de entregar.** La IA se equivoca, sobre todo con números, nombres y transcripciones.
4. **Nada de datos personales en lo público.** → [[Privacidad]]
5. **Todo queda registrado.** Los cambios hechos con la IA se suben con un commit que lo dice ("Co-Authored-By: Claude"). → [[Git y GitHub]]
6. **Pensado para que lo lean otros**: notas en texto plano, propiedades claras y, en algunos vaults, un `AGENTS.md` para otras IA.

## Cómo se trabaja en la práctica
Una conversación con [[Claude Code]] en la nube, con el repositorio conectado y los [[Google Drive|conectores]] necesarios. Se pide en lenguaje común ("haceme un vault con este video", "explicame la diapositiva de la potencia específica más simple"), se revisa el resultado y se pide lo que falta.
