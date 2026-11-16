---
tags: [autolid, 3d, despiece]
tipo: nota
actualizado: 2026-11-16
---
# Despiece 3D AutoLID

> [!summary] Qué es
> Modelo 3D de AutoLID hecho en **Blender**, montado sobre un inodoro de referencia, con **vista explotada**: 25 piezas en 7 conjuntos. Al tocar una pieza se abre su ficha, con qué es, sus datos y costos del informe final, y los cuidados que necesita.
> **Abrir el visor:** https://claude.ai/artifact/U6PzRwKaJ2MU91Rp4tUbsT (privado; se comparte desde el menú *Compartir* de la página). También queda publicado en la página del vault: https://xaguhz.github.io/vaultColegio/vaultAutoLID/AutoLID/3D/visor/index.html

Volver a [[00 AutoLID]] · Ver también [[Informe final - resumen]] · [[Arquitectura AutoLID.excalidraw|✏️ Arquitectura del hardware]]

![[autolid_3d_armado.png]]
*Modelo armado (render de Blender).*

![[autolid_3d_despiece.png]]
*Vista explotada al 100 %: el gabinete se corre a la derecha y se abre en capas; la tapa y el asiento suben y el sensor de fuerza queda entre el asiento y la loza.*

![[autolid_3d_gabinete.png]]
*Detalle del gabinete despiezado: carcasa inoxidable, tapa, junta, módulos, placa, servo, celdas y portapilas.*

## Qué se puede hacer en el visor
Es el mismo visor que el del torno:
- **Despiece:** deslizador de 0 a 100 % o botón *Despiezar / Armar*.
- **Tocar una pieza:** se aísla, la cámara se acerca y aparece su ficha. **← Volver** (o Esc) regresa a la vista anterior.
- **Modo animación:** la pieza gira con sus datos flotando. Las chicas (diagonal menor a 12 cm: módulos, sensores, servo, celdas) cambian de enfoque cada 7 s: *Identificación → Características → Mantenimiento*. Las grandes muestran toda la ficha junta.
- **Corte:** saca la mitad delantera para ver el interior del gabinete.
- **Color por conjunto** y lista de **Piezas** con buscador. Cada pieza tiene su link, por ejemplo `…#servo-ds3218`.

## Conjuntos del modelo
| Conjunto | Piezas |
|---|---|
| Gabinete y carcasa | gabinete IP65, junta, tapa, tornillos M3, carcasa inoxidable AISI 304, prensacables |
| Actuador | servomotor DS3218 |
| Electrónica | placa PCB, Arduino Nano, TP4056, MT3608, cableado |
| Energía | portapilas 1S2P, 2 celdas 18650 |
| Sensores | HC-SR04, membrana Gore-Tex, FSR 402, goma de 2 mm |
| Montaje y transmisión | adaptador de bisagra PETG, brazo del servo, pletina inoxidable |
| Inodoro (referencia) | taza, mochila, asiento, tapa |

> [!warning] Precisión del modelo
> Las medidas de los componentes salen de sus hojas de datos y del informe final: gabinete 150×150×100 mm, servo 40×20×40,5 mm, celdas Ø18,4×65 mm, Arduino Nano 18×43 mm y HC-SR04 45×20 mm. La forma del adaptador PETG y de la pletina es la del diseño, no de piezas medidas, porque el prototipo físico todavía está en armado. El inodoro es genérico.

## Archivos y cómo regenerarlo
| Archivo | Qué es |
|---|---|
| `herramientas/autolid_3d.py` | Script que arma el modelo pieza por pieza (medidas, materiales y dirección de despiece) |
| `herramientas/autolid_3d_render.py` | Saca los tres renders de esta nota |
| `AutoLID/3D/autolid.blend` | Archivo de Blender, para abrir y editar |
| `AutoLID/3D/autolid.glb` | Modelo glTF binario (sirve para otros visores o Sketchfab) |
| `AutoLID/3D/visor/index.html` | Página del visor (Three.js) |
| `AutoLID/3D/visor/fichas.json` | Texto de las fichas de cada pieza y conjunto |
| `AutoLID/3D/visor/autolid.json` | El modelo como glTF embebido, que es lo que carga el visor |

Para regenerar el modelo después de cambiar el script (no hace falta abrir Blender):

```bash
blender -b --factory-startup --python herramientas/autolid_3d.py
```

```bash
blender -b AutoLID/3D/autolid.blend --python herramientas/autolid_3d_render.py
```

Después se vuelve a publicar la página del visor. Para cambiar el texto de una ficha alcanza con editar `fichas.json`.
