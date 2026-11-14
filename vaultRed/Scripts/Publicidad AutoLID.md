---
tipo: script
tags: [script, python, video]
archivo: vaultAutoLID/herramientas/publicidad/
actualizado: 2026-11-14
---
# Publicidad AutoLID

**Carpeta:** [`vaultAutoLID/herramientas/publicidad/`](https://github.com/xAguhz/vaultColegio/tree/main/vaultAutoLID/herramientas/publicidad) · Python.

Los scripts que generaron el **spot publicitario de 42 segundos** de AutoLID:
| Archivo | Qué hace |
|---|---|
| `schedule.json` | El guion en el tiempo: cortes, duración, cuadros por segundo |
| `build_ad.py` | Arma la escena completa en [[Blender]] y la renderiza cuadro por cuadro |
| `audio.py` | Sintetiza la música y los efectos, y los mezcla con la voz del relator |
| `split_vo.py` y `guion_relator.txt` | Separan y ordenan las frases del relator |

→ [[Vault - AutoLID]]
