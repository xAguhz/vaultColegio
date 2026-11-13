---
tags: [torno-tm300, 3d, despiece]
tipo: nota
actualizado: 2026-11-13
---
# Despiece 3D interactivo

> [!summary] Qué es
> Modelo 3D del torno **por conjuntos** (59 piezas en 10 conjuntos), con despiece animado. Al tocar una pieza se abre su ficha: qué es, datos y códigos, mantenimiento, la lámina del manual y la nota del vault donde está el detalle.
> **Abrir el visor:** https://claude.ai/artifact/6k1uizayAvXsBWRHKa3caD (privado; se comparte desde el menú *Compartir* de la página). También está publicado en la página del vault: https://xaguhz.github.io/vaultColegio/vaultTorno/3D/visor/index.html

Volver a [[00 Torno TM300]] · Ver también [[03 Partes y movimientos]] · [[Mapa Torno TM300.canvas|🗺️ Mapa del torno]]

![[tm300_3d_armado.png]]
*Modelo armado (render de Blender).*

![[tm300_3d_despiece.png]]
*El mismo modelo con el despiece al 100 %: cada conjunto se separa en su dirección de montaje.*

## Qué se puede hacer en el visor
- **Despiece:** deslizador de 0 a 100 % o botón *Despiezar / Armar*.
- **Tocar una pieza:** se **aísla** (el resto del torno queda casi transparente), la cámara **se acerca** y aparece su ficha. Arriba a la izquierda aparece el botón grande **← Volver** (o la tecla Esc), que regresa exactamente a la vista anterior. Lo mismo pasa al elegirla desde la lista *Piezas*.
- **Modo animación** (interruptor arriba a la derecha; el visor recuerda si lo dejaste prendido): al tocar una pieza, gira lentamente con sus datos **flotando alrededor**, unidos a la pieza con líneas.
  - **Piezas chicas y medianas-chicas** (de las mordazas hasta el plato y el cuerpo del contrapunto): los datos van por **enfoques**: *Identificación* (nombre, qué es, dónde está en el vault) → *Características* → *Mantenimiento*. Cada 7 segundos la pieza da **un giro rápido** y cambia el enfoque; después vuelve al giro lento. También se cambia tocando la pieza o los botones de abajo, y se puede pausar.
  - **Piezas medianas-grandes y grandes** (base del contrapunto, delantal, carros, motor, cabezal, bancada…): giran lento con **toda la ficha** encima a la vez.
  - El límite entre los dos grupos es el tamaño de la pieza: diagonal de su caja menor a 0,34 m (constante `SMALL` en `3D/visor/index.html`).
  - En el celular, los datos van juntos en una sola tarjeta abajo de la pieza.
- **Color por conjunto:** pinta cada conjunto de un color para distinguirlos.
- **Corte:** saca la mitad delantera del torno para ver el husillo, los rodamientos y los engranajes.
- **Piezas:** lista buscable por nombre, código o conjunto (por ejemplo `30212`, `A32`, `media tuerca`).
- **Láminas:** las miniaturas del despiece del manual se amplían al tocarlas.
- Cada pieza tiene su propio link (por ejemplo `…#media-tuerca`).

## Conjuntos del modelo
| Conjunto | Piezas modeladas |
|---|---|
| Bancada y gabinete | bancada, gabinetes, bandeja, guardasalpicaduras, freno de pie, cremallera |
| Motor y transmisión | motor, poleas, correas A32 |
| Cabezal | carcasa, tapa, palancas, husillo, rodamientos 30212/30210, eje de entrada, plato, 3 mordazas, protector |
| Lira y caja Norton | tapa de la lira, engranajes de cambio (120T/127T), caja Norton, perillas |
| Delantal y barras | tornillo patrón, barra de avances, barra de mando, soporte derecho, delantal, volante, palancas, media tuerca, sinfín y corona, reloj de roscar |
| Carros | carro principal, transversal (con husillo y tuerca), base giratoria, charriot, torre, cuchilla |
| Contrapunto | base, cuerpo, caña MT3, volante, trabas |
| Lunetas | fija y móvil |
| Refrigeración | depósito, bomba AB-12, caño articulado |
| Eléctrico | tablero, botonera con seta de emergencia, lámpara |

> [!warning] Precisión del modelo
> Son reales las cotas que da el manual (C0632A): altura de centros 166 mm, ancho de guías 187 mm, altura de bancada 290 mm, 1000 mm entre puntas, tornillo patrón Ø22, barra Ø19, caña Ø32, plato Ø200. Lo que el manual no acota (gabinetes, forma del cabezal y del delantal, ubicación de palancas) sigue las proporciones de un torno 12×36 genérico. **Pendiente:** ajustar con fotos y medidas de la unidad del taller.

## Archivos y cómo regenerarlo
| Archivo | Qué es |
|---|---|
| `herramientas/torno_tm300_3d.py` | Script que arma el modelo pieza por pieza (medidas, materiales, direcciones de despiece) |
| `3D/torno_tm300.blend` | Archivo de Blender, para abrir y editar |
| `3D/torno_tm300.glb` | Modelo en formato glTF binario (sirve para otros visores o Sketchfab) |
| `3D/visor/index.html` | Página del visor (Three.js) |
| `3D/visor/fichas.json` | Texto de las fichas de cada pieza y conjunto |
| `3D/visor/torno_tm300.json` | El mismo modelo como glTF embebido, que es lo que carga el visor |

Para regenerar el modelo después de cambiar el script (no hace falta abrir Blender):

```bash
blender -b --factory-startup --python herramientas/torno_tm300_3d.py
```

Después se vuelve a publicar la página del visor. Para cambiar el texto de una ficha alcanza con editar `fichas.json` y volver a publicar.
