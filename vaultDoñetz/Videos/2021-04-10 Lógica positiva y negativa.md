---
tipo: video
fecha: 2021-04-10
url: https://www.youtube.com/watch?v=E1FJfLKeclM
duracion: "19:21"
vistas: 2816
area: electroneumática
lista: Electro-Neumática
---

# Lógica positiva y negativa con un ejemplo electroneumático

Lo grabó **a pedido de un alumno** que tenía que rendir electroneumática.

## Ejercicio
1 actuador de doble efecto, 5/2 **monoestable**, estranguladoras, rodillos. Avanza → se mantiene **3 s** → retrocede. Ciclo continuo. Enclavamiento con marcha, parada y parada de servicio.

## Versión con lógica positiva
- `K0` · `1S1` → `K1` (autorretención); NA de `K1` → `1Y1`.
- `1S2` (NA) → `K2`, **retardo a la conexión**, 3 s.
- **NC de `K2`** corta la autorretención de `K1` → retrocede.
- Ajusta las estranguladoras al 20 % para que el movimiento sea más lento.

## Versión con lógica negativa
- `1S2` conectado del lado **NC**: hay señal mientras no está pisado.
- Se cambia el relé por `K3`, de **retardo a la desconexión**: está energizado desde que se prende la fuente y cuenta cuando se le corta la señal.
- En la autorretención, el NC se cambia por un **NA de `K3`** (que arranca cerrado). Cuando termina de contar, se abre y desconecta.
- El funcionamiento queda **idéntico** cambiando solo dos contactos.

Al final anuncia que va a volver a subir videos, cosa que no ocurrió hasta 2025.

## Conceptos
[[Lógica positiva y negativa]] · [[Relés temporizados]] · [[Autorretención]] · [[FluidSIM]]
