---
tags: [autolid, diseño, video]
tipo: pieza
actualizado: 2026-11-12
---
# Publicidad (video de 42 s)

> [!summary] Qué es
> Spot de 42 segundos, 1920×1080 a 30 fps, con relator, música y efectos. Arranca por la necesidad (personas con discapacidad, adultos mayores, higiene) y cierra con AutoLID funcionando. Archivo: `AutoLID/Diseño/Video/AutoLID_publicidad.mp4`.

## Guion
| Tiempo | Imagen | Relator |
|---|---|---|
| 0-6 s | Baño a oscuras. La tapa intenta subir y vuelve a caer. "Levantar la tapa." / "Para millones, no es tan simple." | *Para millones de argentinos, algo tan simple como levantar la tapa del inodoro... no es tan simple.* |
| 6-17 s | Tres datos con íconos: 1 de cada 10 personas (una se ilumina), 1 de cada 4 hogares, +5,5 millones (contador). | *Uno de cada diez argentinos vive con alguna discapacidad. En uno de cada cuatro hogares, hay alguien que la tiene. Y más de cinco millones y medio tienen sesenta y cinco años o más.* |
| 17-23 s | Inodoro abierto: una nube de gérmenes se expande y una regla marca 2 m. | *Además, cada vez que tiramos la cadena con la tapa abierta, los gérmenes viajan hasta dos metros.* |
| 23-36 s | Baño claro con AutoLID. Aparece el logo, se ilumina la caja; una persona se acerca (ondas del sensor), la tapa sube, se sienta (el sensor de peso se ilumina), se va y la tapa baja. | *Por eso creamos AutoLID. Se instala en tu inodoro, en minutos. Te acercás, y la tapa se abre sola. Te sentás, y no se cierra. Te vas, y se cierra.* |
| 36-42 s | Logo AutoLID con anillos de "ultrasonido", lema, escuela y correo. | *AutoLID. Higiene y autonomía, sin tocar nada.* |

## Datos usados (verificados)
- **10,2 %** de la población (6 años o más, zonas urbanas) tiene alguna dificultad, y en el **25,3 %** de los hogares vive al menos una persona con discapacidad. INDEC, *Estudio Nacional sobre el Perfil de las Personas con Discapacidad*, 2018.
- **11,9 %** de la población tiene 65 años o más: unos 5,5 millones sobre 46.234.830 habitantes. INDEC, Censo 2022.
- **Hasta 2 metros** de alcance del *toilet plume*: dato del [[Informe final - resumen|informe final]], que cita a Best et al. (2012) y Johnson et al. (2013).

> [!note] Licencias creativas
> En el video la tapa abre en 1,6 s; el AutoLID real tarda 5 s (3 RPM). Las figuras son esquemáticas y el inodoro es un modelo simple hecho en Blender, no el prototipo.

## Cómo se hizo
| Parte | Herramienta |
|---|---|
| Animación 3D y textos | Blender 5.3 en segundo plano (EEVEE, GPU), generado por código: `herramientas/publicidad/build_ad.py` |
| Relator | **ElevenLabs** (desde el 12/11; antes, Piper es_AR "Daniela"). `herramientas/publicidad/split_vo.py` corta el MP3 en las 11 líneas por sus pausas y acelera apenas (máx. 4 %, sin cambiar el tono) las que no entran en su escena |
| Música y efectos | Sintetizados en Python (`herramientas/publicidad/audio.py`): piano, pads, ritmo, whoosh, servo, ultrasonido, descarga, campanita |
| Tiempos | `herramientas/publicidad/schedule.json` (comparten los tiempos el audio y la animación) |
| Montaje | ffmpeg (H.264 + AAC) |

Para cambiar una frase: editar la línea, regenerar la voz, ajustar el tiempo en `schedule.json` y volver a correr los dos scripts.

## Relacionado
[[00 AutoLID]] · [[Galería Gemini]] · [[Cómo pedir imágenes]]
