---
tags: [autolid, diseño, guia]
tipo: guia
---
# Cómo pedir imágenes

> [!summary] Receta corta
> Pedíselo a Claude ("haceme un banner de AutoLID de 150×50 con…") o corré el script vos. Gemini genera, la imagen cae en `Adjuntos/Gemini/` y se agrega sola a la [[Galería Gemini]].

## Desde la terminal
```bash
cd ~/Colegio/vaultColegio/vaultAutoLID
herramientas/gemini_img.sh "un banner moderno para el proyecto AutoLID, ..." banner_v1.png 3:1
```

| Pieza | Proporción | Nota |
|---|---|---|
| Banner 150×50 cm | `3:1` | Para imprimir grande, pedir después un reescalado o rehacerlo en vector |
| Diapositiva | `16:9` | Portadas y fondos de presentación |
| Cartel A4/A3 vertical | `2:3` | Afiches para la expo |
| Ícono / logo | `1:1` | Mejor con fondo liso para recortarlo |

## Modelos
- `gemini-3.8-flash-medium` (default): rápido, sirve para probar ideas.
- `gemini-4-argon-medium`: más lento; usarlo cuando la imagen lleva **texto** (nombre del proyecto, escuela), que Flash a veces escribe mal.

## Consejos para el prompt
- Decir **qué es AutoLID** en una frase, para que la imagen tenga sentido (ver [[00 AutoLID]]).
- Fijar estilo y colores del grupo (anotarlos en [[00 AutoLID#Identidad visual]] y copiarlos en cada prompt).
- Si va texto, escribirlo entre comillas y corto: `with the title "AutoLID"`.
- Para iterar, copiar el prompt de la [[Galería Gemini]] y cambiar una sola cosa por vez.

## Límites
- La cuota de Antigravity es de unas 13 imágenes cada ~4,5 h (compartida con el juego).
- Las imágenes salen en resolución de pantalla (~1–2 K px): alcanzan para presentaciones; para imprimir 150×50 cm conviene usarlas de fondo y poner textos y logo en vector (Figma, Inkscape o Canva).
