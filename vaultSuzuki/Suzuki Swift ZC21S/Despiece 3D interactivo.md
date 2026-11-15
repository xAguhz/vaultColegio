---
tags: [suzuki-swift, 3d, despiece]
tipo: nota
actualizado: 2026-11-14
---
# Despiece 3D interactivo

> [!summary] Qué es
> Modelo 3D del Swift **por conjuntos** (140 piezas en 20 conjuntos y 6 capas, unos 319 000 triángulos), con despiece animado. Al tocar una pieza se abre su ficha: qué es, sus datos del manual, su mantenimiento, las láminas y la nota del vault donde está el detalle.
> **Abrir el visor:** https://xaguhz.github.io/vaultColegio/vaultSuzuki/3D/visor/index.html (página pública del vault). También está como Artifact privado: https://claude.ai/artifact/5inUBYy9btJ8hJyYv1jBd9 (se comparte desde el menú *Compartir* de la página).

Volver a [[00 Suzuki Swift ZC21S]] · [[Mapa Suzuki Swift.canvas|🗺️ Mapa del auto]]

![[swift_34_delantera.jpg]]
*Modelo armado (render de Blender).*

![[swift_despiece.jpg]]
*El mismo modelo con el despiece al 100 %: cada conjunto sale en su dirección de montaje (la mecánica hacia arriba, las ruedas hacia afuera, el escape y el tanque hacia abajo).*

![[swift_frente_detalle.jpg]]
*Detalle del frente: parrilla de panal, faros con sus parábolas, antinieblas y patente.*

![[swift_cola_detalle.jpg]]
*Detalle de la cola: calaveras con sectores, luneta con banda negra, alerón y limpialuneta.*

![[swift_mecanica.jpg]]
*Sin carrocería: motor y caja adelante, tren rodante, tanque, escape e interior.*

## Qué se puede hacer en el visor
Es el mismo visor que el del torno TM300, adaptado al auto:
- **Despiece:** deslizador de 0 a 100 % o botón *Despiezar / Armar*.
- **Tocar una pieza:** se aísla, la cámara se acerca y aparece su ficha. **← Volver** (o Esc) regresa a la vista anterior.
- **Modo animación:** la pieza gira con sus datos flotando. Las piezas chicas (bobinas, batería, discos, mordazas…) muestran los datos por enfoques cada 7 segundos; las grandes (motor, caja, puertas, casco) muestran toda la ficha junta. El límite es una diagonal de 0,45 m (`SMALL` en `3D/visor/index.html`).
- **Color por conjunto** y **Corte** (corta el auto por la mitad a lo largo, para ver el interior y el vano motor).
- **Piezas:** lista buscable por nombre o conjunto (por ejemplo `McPherson`, `46B24R`, `embrague`).

## Capas y conjuntos
El modelo está partido en **6 capas**, cada una en su archivo: el visor carga primero lo de afuera y después el resto en segundo plano. "Por dentro" (motor y caja por dentro) se carga recién al prenderla en **Capas**.

| Capa | Conjuntos | Piezas | Triángulos | Archivo |
| --- | --- | --- | --- | --- |
| **Exterior** | Carrocería · Puertas y cristales · Iluminación | 19 | 70 mil | 1.7 MB |
| **Chasis** | Ruedas · Frenos · Suspensión y dirección · Combustible y escape | 30 | 88 mil | 3.0 MB |
| **Motor y caja** | Motor M15A · Transmisión · Refrigeración · Eléctrico | 22 | 30 mil | 1.1 MB |
| **Interior** | Interior · Airbag y cinturones · Aire acondicionado y calefacción | 13 | 15 mil | 0.5 MB |
| **Electricidad** | Sensores y actuadores · Módulos de control · Cableado · Accesorios eléctricos | 44 | 52 mil | 2.3 MB |
| **Por dentro** | Motor por dentro · Caja por dentro | 12 | 63 mil | 2.3 MB |

## Lo nuevo del visor (15/11/2026)
- **Capas:** prender y apagar exterior, chasis, motor, interior, electricidad y "por dentro". Lo apagado no se dibuja.
- **Rayos X:** carrocería e interior casi transparentes para ver la mecánica, los sensores y los mazos de cables en su lugar.
- **Circuitos:** pestaña con los 37 circuitos del capítulo 9A. Al elegir uno se resaltan sus piezas (batería, fusibles, sensores, módulos, mazos), se explica cómo circula la corriente y hay un enlace a la nota con el esquema ([[Circuitos eléctricos]]). Cada ficha de pieza dice en qué circuitos aparece.
- **Electricidad completa:** 21 sensores y actuadores con su conector del manual (C09, C20…) y sus códigos de falla, 8 módulos de control, 8 mazos de cables encintados con sus conectores y 7 accesorios eléctricos.
- **Por dentro:** motor (cigüeñal, pistones, levas, válvulas, cadena, bombas) y caja manual (eje de entrada, contraeje, marcha atrás, horquillas, diferencial).
- **Piezas:** la lista se agrupa por conjunto y los grupos se pliegan; al buscar, se abren solos.

## Indicaciones técnicas en el visor
Cada ficha de pieza suma, cuando el manual lo tiene:
- **Fallas típicas:** síntoma, causa probable y qué hacer (también en las tarjetas del modo animación).
- **Cómo se desmonta:** pasos resumidos y qué piezas hay que sacar antes. El botón **Desmontaje animado** las va sacando una por una, con el paso escrito arriba (Esc o *Salir* vuelve todo a su lugar).
- **En el manual de taller:** los procedimientos de esa pieza con su página. En la app de la compu cada uno abre el PDF justo en esa página.
- **Pares de apriete** y **herramientas especiales**.

Lo mismo está en el vault: [[Guía técnica por pieza]] y [[Diagnóstico por síntoma]].

## Rendimiento (pensado para la compu: Ryzen 5 3400G, GTX 1660 Ti, 1080p, Firefox)
- **Solo dibuja cuando algo cambia** (girar, despiezar, elegir). Con el auto quieto no gasta placa de video ni procesador.
- La **búsqueda de la pieza bajo el mouse** usa un índice espacial (BVH): 0,3 ms con las 140 piezas, en lugar de recorrer los 330 000 triángulos.
- Al pasar el mouse solo se repintan las dos piezas que cambian; los materiales no se recompilan salvo al cambiar el corte o la transparencia.
- **Medido** con todo cargado: unos 5 ms por cuadro (509 llamadas de dibujo), o sea, más de 150 cuadros por segundo posibles.
- **Rendimiento** (botón): calidad alta, media o baja, y un contador de cuadros por segundo.

## Usarlo como aplicación
- **En la compu:** en el menú de aplicaciones aparece **Suzuki Swift 3D**. Abre el visor en Firefox desde la copia local del vault (`herramientas/visor_swift.sh`), con los modelos en binario (lo más rápido) y sin depender de GitHub.
- **Desde la página web:** en Chrome o Edge se puede **instalar** como aplicación (ícono de instalar en la barra de direcciones). Queda guardada y anda sin internet.
- La versión de claude.ai (Artifact) sigue andando, pero carga los modelos en texto (un poco más lento).

## Mecánica según el manual de taller (15/11/2026)
La mecánica se revisó contra la **edición en castellano del manual de taller** (ver [[13 Repuestos y fuentes]]):
- **Corregido:** el escape y el catalizador pasaron adelante y la admisión atrás (estaban al revés); el alternador y el termostato, atrás; el compresor del aire, adelante con su correa; el filtro de aceite, adelante; el recorrido del escape (caño delantero bajo el motor, caño central con resonador, silenciador y protector de calor) y los soportes del motor.
- **Agregado:** el motor por dentro con sus medidas, el embrague con su bomba y la palanca con cables, el aire acondicionado y la calefacción, el canister EVAP y los sensores de rueda del ABS.

![[lamina_vano_motor.jpg]]
*Vano motor sin carrocería: condensador y radiador adelante, múltiple de escape con catalizador detrás, admisión y servofreno contra el torpedo.*

## Cómo está hecho
- Script: `herramientas/suzuki_swift_3d.py` (Blender 5.3 en segundo plano, sin abrir la ventana):
  ```bash
  cd ~/Colegio/vaultColegio/vaultSuzuki
  SWIFT_LAMINAS="$PWD/Adjuntos/Suzuki Swift" blender -b --factory-startup --python herramientas/suzuki_swift_3d.py
  ```
  Genera `3D/suzuki_swift.blend`, `3D/suzuki_swift.glb`, `3D/visor/suzuki_swift.json` (el modelo que lee el visor) y, con la variable `SWIFT_LAMINAS`, las imágenes de `Adjuntos/Suzuki Swift/`.
- Fichas: `herramientas/suzuki_fichas.py` genera `3D/visor/fichas.json`. Para cambiar un texto del visor, se edita ese script y se vuelve a correr.
- **Carrocería:** se arma como una superficie que pasa por ~180 secciones transversales (como las cuadernas de un barco). El perfil, la cintura, el ancho y el techo se definen con puntos clave interpolados. Después se le da 12 mm de espesor y se corta con **booleanas** (prismas) para separar puertas, capó, portón, paragolpes, ópticas y cristales. Así cada pieza calza exacto con el hueco que deja, y el casco se corta 3,5 mm más grande para que quede la **luz entre paneles** como en el auto. Los vidrios tienen su marco negro y el parabrisas y la luneta, la banda negra serigrafiada.
- **Detalle (versión del 15/11/2026):** ópticas con parábolas cromadas, parrilla de panal, antinieblas, patentes, alerón con tercera luz de freno, limpialuneta, espejos con carcasa, manijas con cerradura, repetidores de giro, antena y guardabarros interiores; llantas de 6 rayos con 4 tuercas y neumáticos con surcos; discos ventilados con aletas, mordazas con soporte, tambores con aletas, ABS y caños de freno; fuelles en homocinéticas y cremallera, cuna delantera; motor con riel de inyección, inyectores, caudalímetro, cables de alta, varilla de aceite, tensor, compresor del aire y soportes; mangueras del radiador, computadora, bocina; butacas con laterales y cinturones, tablero con tres relojes y rejillas redondas, paneles de puertas, parasoles y espejo interior.
- **Mecánica:** primitivas (cajas, cilindros, tubos, resortes helicoidales, sólidos de revolución para las ruedas), ubicadas con las cotas del manual (trochas, ruedas 185/60R15, disco de 20 mm, batería 46B24R, etc.).

> [!warning] Precisión
> Las cotas generales (largo, ancho, alto, entre ejes, ruedas) son las del catálogo. El **perfil** (techo, cintura, ventanillas, cortes de puertas, faros, calaveras y tapa de combustible) se midió sobre una foto lateral del auto, y el **ancho a lo largo** y la **caída de los costados** sobre vistas de frente, cola y planta hechas con Gemini ([[Galería Gemini]]). Es mucho más fiel que la primera versión, pero sigue sin ser un relevamiento: sirve para ubicar y estudiar cada sistema, no para medir piezas.

## Láminas
![[lamina_motor.jpg]]
*Vano motor: motor transversal, caja manual a la izquierda, radiador adelante, batería y fusibles.*

![[lamina_frenos.jpg]]
*Frenos: discos ventilados y mordazas adelante, tambores atrás y servofreno del lado del conductor.*

![[lamina_combustible.jpg]]
*Tanque bajo el asiento trasero y línea de escape.*
