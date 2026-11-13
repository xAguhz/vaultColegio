---
tipo: equipo
funcion: transferir calor entre dos fluidos sin mezclarlos
fluido: líquidos y gases
variable_principal: temperatura (4 temperaturas) + caudal + caída de presión
norma: TEMA (tubulares)
tps: [TP2, TP6]
tags: [equipo, intercambiador, transferencia-de-calor]
---

# Intercambiador de calor

> [!summary] Función
> Facilita que la energía térmica pase de una corriente **caliente** a una **fría**, normalmente **sin mezclarlas**. **No crea calor ni frío**: lo **redistribuye**. Eso lo diferencia de la [[Caldera]], que **genera** calor con combustible.

![[intercambiador.png|420]]

## Física
- **Convección** del fluido caliente a la pared → **conducción** a través de la pared → **convección** de la pared al fluido frío.
- **Q = ṁ · cp · ΔT:** el calor depende del caudal, del cambio de temperatura y del fluido.
- **Directo** (hay contacto, como en una torre de enfriamiento) o **indirecto** (con una pared en el medio, como en placas o en carcasa y tubos).

## Disposición del flujo
| Disposición | Comportamiento |
|---|---|
| **Paralelo** | Los dos fluidos entran por el mismo lado. Al principio hay mucha diferencia de temperatura, pero se agota rápido |
| **Contracorriente** | Los fluidos van en sentidos opuestos. Mantienen una diferencia útil en todo el equipo, y **transfieren más** en condiciones comparables |
| **Cruzado** | Los flujos son perpendiculares (radiadores, intercambio aire–líquido) |

## Tipos principales
| | Carcasa y tubos | Placas |
|---|---|---|
| Construcción | Haz de tubos, placas tubulares, cabezales y **deflectores** dentro de una carcasa | Placas corrugadas con canales alternados y **juntas**, en un bastidor (o soldadas o brasadas) |
| Ventajas | Trayectoria industrial larga; sirve para un **amplio rango de presión y temperatura** y para fluidos difíciles | **Muy compacto**, alta transferencia por volumen, se abre para limpiar, se pueden **agregar placas** |
| Límites | Más grande; limpiar el lado de la carcasa es más difícil | Límites de presión y temperatura por las **juntas**; pasos estrechos (sensibles a sólidos) |
| Detalles | **Pasos** (más velocidad: más transferencia, pero más ΔP); el fluido para tubos o carcasa se elige por presión, corrosión, suciedad y limpieza | Las juntas tienen que ser compatibles con el fluido, la temperatura y la presión |

> No hay un tipo "mejor". Elegir porque "transfiere más" es un error si después **no se puede limpiar**, si el material **no es compatible** o si la **ΔP** es excesiva.

## Variables que hay que medir
- **Cuatro temperaturas:** entrada y salida del fluido caliente y del frío.
- **Caudales** de las dos corrientes.
- **Presión de entrada y salida** de cada lado (la **ΔP**).
- Una **válvula de control** sobre el caudal de una corriente regula la temperatura de salida.

## Problemas
- **Ensuciamiento (fouling):**
  - sarro, sedimentos, óxido o materia orgánica;
  - agrega **resistencia térmica** (menos calor) y **achica el paso** (más ΔP);
  - **temperatura que baja + ΔP que sube = fouling** (caso del [[TP6 Intercambiadores de calor|TP6]]).
- **Corrosión interna:** una perforación **comunica los circuitos**: el fluido de mayor presión **contamina** al de menor presión. Es peor que una pérdida visible.
- **Juntas** dañadas: pérdidas externas o mezcla de fluidos.
- **Expansión térmica:** las partes a distinta temperatura sufren esfuerzos.
- **Caudal y velocidad:** poca velocidad hace que se ensucie; mucha velocidad aumenta la ΔP y la erosión.

## Diagnóstico
No decir "está roto" sin antes revisar:
1. la temperatura y el caudal del fluido caliente;
2. las válvulas;
3. la suciedad;
4. el caudal del fluido frío;
5. los instrumentos.

## Usos especiales
- **Condensador** y **evaporador**: hay cambio de fase.
- **Recuperación de calor:** una corriente caliente de descarte precalienta otra (también el calor del [[Compresor]]).

## Relacionado
[[Caldera]] · [[Sistema de calentamiento de agua]] · [[Variables de proceso]] · [[Pérdidas de carga]] · [[TP6 Intercambiadores de calor]]
