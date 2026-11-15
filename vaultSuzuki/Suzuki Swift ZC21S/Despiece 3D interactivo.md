---
tags: [suzuki-swift, 3d, despiece]
tipo: nota
actualizado: 2026-11-14
---
# Despiece 3D interactivo

> [!summary] Qué es
> Modelo 3D del Swift **por conjuntos** (65 piezas en 12 conjuntos), con despiece animado. Al tocar una pieza se abre su ficha: qué es, sus datos del manual, su mantenimiento, las láminas y la nota del vault donde está el detalle.
> **Abrir el visor:** https://xaguhz.github.io/vaultColegio/vaultSuzuki/3D/visor/index.html

Volver a [[00 Suzuki Swift ZC21S]] · [[Mapa Suzuki Swift.canvas|🗺️ Mapa del auto]]

![[swift_34_delantera.jpg]]
*Modelo armado (render de Blender).*

![[swift_despiece.jpg]]
*El mismo modelo con el despiece al 100 %: cada conjunto sale en su dirección de montaje (la mecánica hacia arriba, las ruedas hacia afuera, el escape y el tanque hacia abajo).*

![[swift_mecanica.jpg]]
*Sin carrocería: motor y caja adelante, tren rodante, tanque, escape e interior.*

## Qué se puede hacer en el visor
Es el mismo visor que el del torno TM300, adaptado al auto:
- **Despiece:** deslizador de 0 a 100 % o botón *Despiezar / Armar*.
- **Tocar una pieza:** se aísla, la cámara se acerca y aparece su ficha. **← Volver** (o Esc) regresa a la vista anterior.
- **Modo animación:** la pieza gira con sus datos flotando. Las piezas chicas (bobinas, batería, discos, mordazas…) muestran los datos por enfoques cada 7 segundos; las grandes (motor, caja, puertas, casco) muestran toda la ficha junta. El límite es una diagonal de 0,45 m (`SMALL` en `3D/visor/index.html`).
- **Color por conjunto** y **Corte** (corta el auto por la mitad a lo largo, para ver el interior y el vano motor).
- **Piezas:** lista buscable por nombre o conjunto (por ejemplo `McPherson`, `46B24R`, `ATF`).

## Conjuntos
| Conjunto | Piezas |
| -------- | ------ |
| Carrocería | casco, capó, portón con luneta, paragolpes delantero y trasero, parrilla |
| Puertas y cristales | 4 puertas (con su vidrio, manija y espejo), parabrisas, vidrios fijos, limpiaparabrisas |
| Iluminación | 2 faros, 2 calaveras |
| Motor M15A | bloque y cárter, culata, tapa de válvulas con bobinas, distribución, admisión, escape, accesorios, arranque, filtro de aire |
| Transmisión | caja 4AT, 2 semiejes, palanca selectora |
| Refrigeración | radiador, electroventilador, depósito |
| Eléctrico | batería, fusibles del motor, fusibles de cabina |
| Suspensión y dirección | 2 columnas McPherson, 2 brazos, estabilizadora, eje de torsión, 2 conjuntos traseros, cremallera, columna EPS, volante |
| Frenos | 2 discos, 2 mordazas, 2 tambores, servofreno |
| Ruedas | 4 ruedas 185/60R15 |
| Combustible y escape | tanque, línea de escape |
| Interior | 3 asientos, tablero, pedalera |

## Cómo está hecho
- Script: `herramientas/suzuki_swift_3d.py` (Blender 5.3 en segundo plano, sin abrir la ventana):
  ```bash
  cd ~/Colegio/vaultColegio/vaultSuzuki
  SWIFT_LAMINAS="$PWD/Adjuntos/Suzuki Swift" blender -b --factory-startup --python herramientas/suzuki_swift_3d.py
  ```
  Genera `3D/suzuki_swift.blend`, `3D/suzuki_swift.glb`, `3D/visor/suzuki_swift.json` (el modelo que lee el visor) y, con la variable `SWIFT_LAMINAS`, las imágenes de `Adjuntos/Suzuki Swift/`.
- Fichas: `herramientas/suzuki_fichas.py` genera `3D/visor/fichas.json`. Para cambiar un texto del visor, se edita ese script y se vuelve a correr.
- **Carrocería:** se arma como una superficie que pasa por ~120 secciones transversales (como las cuadernas de un barco). El perfil, la cintura, el ancho y el techo se definen con puntos clave interpolados. Después se le da 12 mm de espesor y se corta con **booleanas** (prismas) para separar puertas, capó, portón, paragolpes, ópticas y cristales. Así cada pieza calza exacto con el hueco que deja.
- **Mecánica:** primitivas (cajas, cilindros, tubos, resortes helicoidales, sólidos de revolución para las ruedas), ubicadas con las cotas del manual (trochas, ruedas 185/60R15, disco de 20 mm, batería 46B24R, etc.).

> [!warning] Precisión
> Las cotas generales (largo, ancho, alto, entre ejes, ruedas) son las del catálogo. La **forma** de la carrocería y de las piezas mecánicas es una aproximación hecha a mano sobre fotos y proporciones: sirve para ubicar cada sistema y estudiarlo, no para medir. Si se consiguen fotos del auto real, se pueden ajustar los puntos clave del perfil en el script (`K_TECHO`, `K_CINTURA`, `K_ANCHO`…).

## Láminas
![[lamina_motor.jpg]]
*Vano motor: motor transversal, caja automática a la izquierda, radiador adelante, batería y fusibles.*

![[lamina_frenos.jpg]]
*Frenos: discos ventilados y mordazas adelante, tambores atrás y servofreno del lado del conductor.*

![[lamina_combustible.jpg]]
*Tanque bajo el asiento trasero y línea de escape.*
