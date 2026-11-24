---
tipo: referencia
tags: [programacion, estructura]
---

# Estructura de un programa

## Esqueleto de la carpeta digital

```
N10 G10 P0 Z-149
N20 T0101        (primer 01 = herramienta, segundo 01 = corrector)
N30 G96 S200 M3
N40 G00 X58 Z5
N50 G01 Z-109 F.25
```

## Esqueleto de los TP

```
%
O2222              (número del programa)
G54                (cero pieza, guardado en el proyecto)
T0101              (herramienta 01, corrector 01)
G96 S180 M3        (Vc constante 180 m/min, husillo en marcha)
G00 X50 Z5         (aproximación)
...                (ciclos y perfil)
G00 X100 Z100      (retiro a posición segura)
T0303              (próxima herramienta)
...
M30                (fin)
%
```

## Reglas
- Empieza y termina con `%`.
- `T0101`: los dos primeros dígitos son la **posición en la torreta** y los dos últimos el **corrector**.
- Cada herramienta nueva repite `G96 S.. M3`, porque cambia la Vc.
- El avance `F` se escribe la primera vez que se corta y queda activo. En los TP es en mm/vuelta.
- Antes de cambiar de herramienta se retira a `G00 X100 Z100` (posición segura). La carpeta usa también `G00 Z100`.
- Punto de aproximación típico: `X` apenas mayor que el bruto y `Z5` (5 mm antes de la cara). En los TP con bruto Ø42: `G00 X50 Z5`.
- **Cero pieza** en la punta (Z0). El bruto largo se agarra en el plato; el tronzado corta en `Z = -(largo + 6)`.
- Los programas de la carpeta digital (ejercicios) usan G10 para el cero; los TP usan G54 con el valor guardado en el `.prj`.

## Orden típico de herramientas en los TP
1. T0101 desbaste con G90.
2. T0303 semiterminación o diagonales.
3. T0505 o T1111 ranurado con G94.
4. T0909 terminación del lado derecho.
5. T1010 terminación del lado izquierdo.
6. T1111 tronzado.

Ver también: [[Códigos G]], [[Códigos M]], [[Ciclos G90 G94 G71 G72 G70 G74]], [[TP Peón]], [[TP Alfil]].
