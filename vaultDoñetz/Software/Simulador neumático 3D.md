---
tipo: software
actualizado: 2026-11-26
tags: [software, simulador, neumática, cascada, 3d]
---

# Simulador neumático 3D

Página web didáctica para practicar la secuencia **A+ B+ B− A−** (en la nomenclatura ISO: `1A1+ 2A1+ 2A1− 1A1−`) con el [[Método cascada]]. Se parece a [[FluidSIM]] 4.2, pero corre en el navegador y no hay que instalar nada.

📎 [Abrir el simulador](https://xaguhz.github.io/vaultColegio/vaultDo%C3%B1etz/Simulador/index.html)

> [!info] Qué se ve
> Dos vistas sincronizadas: el **plano neumático** (2D) y una **maqueta 3D**. En la maqueta, `1A1` empuja una pieza desde un almacén y `2A1` la estampa.

## Elementos del circuito
Los nombres siguen la [[Nomenclatura ISO 1219]].

| Código | Qué es |
|---|---|
| `1A1`, `2A1` | Cilindros (A y B) |
| `1V1`, `2V1` | Válvulas 5/2 biestables: pilotaje `14` avanza, `12` retorna (ver [[Válvulas distribuidoras]]) |
| `1S1`, `1S2`, `2S1`, `2S2` | Rodillos finales de carrera |
| `0S1` | Pulsador de marcha |
| `0S2` | Ciclo continuo (ver [[Ciclo único y ciclo continuo]]) |
| `0Z1` | Alimentación de aire |
| `0V0` | Válvula de cierre |
| `0V2` | Memoria de la cascada, con las líneas `L1` y `L2` |

Grupos de la cascada:
- **L1 (grupo I):** `1A1+` `2A1+`
- **L2 (grupo II):** `2A1−` `1A1−`

## Los 3 modos
| Modo | Qué hace |
|---|---|
| **Método cascada** (por defecto) | El circuito ya está armado y funciona. Sirve para ver cómo se alternan `L1` y `L2` |
| **Método intuitivo** | Muestra la [[Superposición de señales]]: en `1V1` en reposo y en `2V1` con un botón. Sirve para entender por qué hace falta la cascada |
| **Armado libre** | El alumno conecta cada pilotaje y toca **Verificar**. Prueba el pulso, el `0S1` sostenido y el ciclo continuo |

## Controles
- Play / Pausa y **modo paso a paso**.
- Velocidad de 0,25x a 2x.
- Reset y `0V0`.
- **Diagrama espacio-fase** en vivo, con la curva teórica y la real (ver [[Diagrama espacio-fase]]).
- Panel de estado.
- Vista **Corte** en 3D.
- **Guía** con 5 ejercicios.
- Anda en el celular. Si falla el CDN de three.js, la parte 2D sigue funcionando.

## Cómo usarlo en clase
1. Proyectar el modo **Método cascada** y darle Play. Que los alumnos miren el diagrama espacio-fase.
2. Pasar a **paso a paso**: en cada fase, preguntar qué línea está activa y qué rodillo la dispara.
3. Cambiar a **Método intuitivo**: mostrar la superposición en `1V1` y en `2V1`. Preguntar por qué no se mueve.
4. Volver a la cascada y comparar. Ver también la [[04 Comparativa de métodos]].
5. Pasar a **Armado libre** y dejar que los alumnos conecten solos. Usar **Verificar**.
6. Activar el **Modo profesor** con una falla y pedir el diagnóstico. Al final, **Mostrar respuesta**.
7. Cerrar con los 5 ejercicios de la **Guía**.

## Fallas del Modo profesor
| Falla | Qué se ve |
|---|---|
| `2S2` roto | El rodillo `2S2` falla y la secuencia no sigue |
| Fuga en `L2` | El ciclo **no arranca**. La fuga es permanente |
| Sin presión | Nada se mueve |
| `1V1` trabada | La válvula no cambia de posición |

Cada falla tiene su botón **Mostrar respuesta**.

## Relación con FluidSIM 4.2
**Qué copia:**
- Plano con numeración de puertos y líneas de pilotaje punteadas.
- Movimiento real de los cilindros y diagrama de estados.
- Nombrado de los rodillos según ISO 1219.

**Qué no hace:**
- No es un editor general: está pensado para esta única secuencia.
- No abre ni guarda archivos de FluidSIM.
- No cubre electroneumática ni PLC.
- En Armado libre solo se cablean los pilotajes.

Para el método en el pizarrón, ver el video [[2020-05-23 Cascada eléctrica - 2 actuadores]].

## Errores que aparecieron y cómo se corrigieron
Prueba hecha **como docente**:

| Error | Corrección |
|---|---|
| `0V2` dibujada con escapes tapados | Escapes abiertos |
| **Verificar** daba OK falso para `0V2→L1 = 0S1` sin `1S1` | Ahora prueba `0S1` sostenido y el ciclo continuo (`0S2`) |
| Faltaban números de puertos y líneas de pilotaje punteadas | Agregados |
| La fuga en `L2` dependía de la posición | Ahora es permanente |
| Texto chico en el celular | Texto más grande |

Revisión del código:

| Error | Corrección |
|---|---|
| La pieza 3D caía después de un reset | Corregido |
| La vista en pausa no se refrescaba | Corregido |
| Memoria de la GPU crecía en cada ciclo | Se libera por ciclo |
| El scroll táctil en el celular interfería | Corregido |

> [!note] Cómo se hizo
> Lo armó la oficina de agentes de IA el 2026-11-26. El detalle está en la bitácora del vault `vaultOficinaIA`.
