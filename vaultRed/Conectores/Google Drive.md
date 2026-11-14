---
tipo: conector
tags: [conector, google]
actualizado: 2026-11-14
---
# Google Drive

**Conector** que deja a [[Claude Code]] **buscar y leer** los archivos de Drive de la cuenta: Google Docs, Word, PDF con texto, presentaciones y planillas.

## Qué se hizo con él
- `vaultCharrute`: leer las teorías y consignas del profe y las resoluciones del grupo, TP por TP.
- `vaultAutoLID`: recorrer la carpeta del proyecto y reconstruir la historia con las fechas de cada archivo.
- Responder preguntas sobre un archivo puntual, como el reparto de puntos del PDF del TP8.

## Límites
- Los **PDF escaneados** no tienen texto y no se pueden leer sin OCR.
- La IA lee **solo lo que la cuenta puede ver**, y no cambia ni borra nada sin que se lo pidan.
