---
tipo: script
tags: [script, bash, imágenes, ia]
archivo: vaultCharrute/herramientas/gemini_img.sh
actualizado: 2026-11-14
---
# gemini_img.sh

**Archivo:** [`vaultCharrute/herramientas/gemini_img.sh`](https://github.com/xAguhz/vaultColegio/blob/main/vaultCharrute/herramientas/gemini_img.sh) (también en `vaultAutoLID`) · Bash.

Genera **una imagen** con [[Gemini]] y la deja en el vault:
```bash
herramientas/gemini_img.sh "<prompt>" nombre.png 16:9
```
- La guarda en `Adjuntos/Gemini/`.
- Agrega la imagen **y el prompt** al principio de la *Galería Gemini*.
- Guarda el registro del pedido en `Adjuntos/Gemini/logs/`.
- Proporciones según el uso: `16:9` para diapositivas, `3:1` para un banner, `2:3` para un cartel.

**Seguridad:** el generador corre en una carpeta temporal vacía, con modelo fijo y tiempo límite, y lo único que se copia afuera es la imagen pedida.
