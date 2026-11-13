---
tags: [autolid, indice]
tipo: proyecto
actualizado: 2026-11-12
---
# AutoLID

> [!summary] Proyecto grupal de 7° año
> Dispositivo *retrofit* que se instala sobre las bisagras de cualquier inodoro y **abre y cierra la tapa solo**, sin contacto. Un sensor ultrasónico detecta a la persona, un servo mueve la tapa y un sensor de peso bajo el asiento impide que se cierre con alguien sentado. Funciona con batería (30-60 días por carga).

## Datos
|                       |                                                                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Escuela               | E.E.S.T. N° 3 de San Antonio de Padua, Electromecánica / Electrónica                                                                                       |
| Curso                 | 7° 1°                                                                                                                                                      |
| Integrantes           | Agustín Calderón, Thiago Iglesias, Luciano Romero                                                                                                          |
| Contacto del proyecto | contacto.autolid@gmail.com                                                                                                                                 |
| Documento principal   | ⭐ [AutoLID INFORME FINAL](https://docs.google.com/document/d/1OecoL8DSYKZxiSlKSvtnaXOIvBBHetvMpxqblyg_-EE/edit) (10/11/2026) · [[Informe final - resumen]] |
| Carpeta en Drive      | [AutoLID](https://drive.google.com/drive/folders/17AnoDAqwl5mVtQK4whX7vXpTux24UAem) (casi todo está suelto en la raíz de Drive: ver [[Archivos en Drive]]) |
| Simulación            | [Tinkercad](https://www.tinkercad.com/things/c7mtaCNG56a-autolid)                                                                                          |
| Última entrega        | 26/10/2026 (Carpeta de Campo Integral)                                                                                                                     |

## Notas
- 🌐 **Página web de demostración:** [AutoLID en Claude](https://claude.ai/artifact/H3ZKnU41iqELZVsaQRg9zc) (privada hasta que la compartas). Archivos en `AutoLID/Web/` (`index.html` + `img/`). Diseño propuesto por Gemini, imágenes de Gemini, simulador con la lógica del firmware.
- 🎬 [[Publicidad]]: spot de 42 s con relator, música y efectos (`AutoLID/Diseño/Video/AutoLID_publicidad.mp4`).
- 🗺️ [[Mapa AutoLID.canvas|Mapa AutoLID]] (Advanced Canvas): historia, cómo funciona, hardware y pendientes en un solo tablero.
- ✏️ [[Arquitectura AutoLID.excalidraw|Arquitectura del hardware]] (Excalidraw): diagrama de bloques editable.
- [[Historia del proyecto]]: de Handy al informe final, con fechas.
- [[Informe final - resumen]]: funcionamiento, hardware, costos, planta y números.
- [[Archivos en Drive]]: todos los archivos, con enlace y fechas.
- [[Handy]]: el proyecto descartado que vino antes.

## Identidad visual
_Colores, tipografía y estilo que usa el grupo. Se copian en cada pedido de imagen._
- Colores: _completar (ver el banner 150×50 y la presentación del 26/10)_
- Tipografía:
- Estilo:
- Lemas usados: "100% Touchless", "Diseñando el Futuro de la Higiene Sanitaria".

## Diseño
- [[Galería Gemini]]: todas las imágenes generadas, con su prompt.
- [[Cómo pedir imágenes]]: cómo generar banners, carteles y diapositivas con Gemini.
- Piezas ya hechas (PC Windows, 25/8): `autolid_50x150cm_impresion.pdf`, `autolid_diseno_3_impresion.pdf`. No están en Drive.

## Pendientes
Del informe final:
- [ ] Armar el prototipo físico final (servo, FSR y HC-SR04 en la caja IP65)
- [ ] Medir el consumo real (sleep y picos del servo)
- [ ] Imprimir los adaptadores en PETG e impermeabilizar sensores
- [ ] Encuestas Perfil A y B + prueba piloto de 3-5 unidades
- [ ] PCB propia en JLCPCB

Del vault:
- [ ] Definir la identidad visual
- [ ] Revisar los puntos marcados en [[Informe final - resumen]] (recuadro "Para revisar antes de presentar")
