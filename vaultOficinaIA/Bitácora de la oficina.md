---
tipo: bitácora
actualizado: 2026-11-26
tags: [oficina-ia, bitácora]
---

# Bitácora de la oficina

Registro de las tareas hechas por la oficina (ver [[Cómo funciona la oficina]]). Lo más nuevo, arriba. Cada entrada tiene qué se hizo, decisiones, errores y correcciones.

## 2026-11-26 · Simulador neumático 3D (vaultDoñetz)

**Qué se hizo.** Una página didáctica nueva, parecida a Festo FluidSIM 4.2, para la secuencia `1A1+ 2A1+ 2A1− 1A1−` (A+ B+ B− A−) con el método cascada. Tiene vista 3D sincronizada (three.js): `1A1` empuja una pieza del almacén y `2A1` la estampa. Está en `vaultDoñetz/Simulador/index.html`, dentro del vault público de la página. La nota de uso está en el vault `vaultDoñetz`: *Simulador neumático 3D*.

**Quién hizo qué.**
| Agente | Tarea |
|---|---|
| `explorador` | Relevó el material y las notas del vault |
| `programador` | Armó la página y las correcciones |
| `probador` | Probó la página **como docente** |
| `revisor` | Revisó el código |
| `documentador` | Nota de uso, enlaces y esta entrada |

Los agentes se comunicaron entre sí en inglés técnico simplificado (ASD-STE100).

**Decisiones.**
- 3 modos: cascada (por defecto y funciona), intuitivo (muestra la superposición) y armado libre (con botón **Verificar**).
- Modo profesor con 4 fallas: `2S2` roto, fuga en `L2`, sin presión y `1V1` trabada, con **Mostrar respuesta**.
- Guía con 5 ejercicios, vista de corte en 3D y diseño que anda en el celular.
- Si el CDN de three.js falla, la parte 2D sigue funcionando.

**Errores que encontró el probador (como docente) y corrección.**
| Error | Corrección |
|---|---|
| `0V2` dibujada con escapes tapados | Escapes abiertos |
| **Verificar** daba OK falso para `0V2→L1 = 0S1` sin `1S1` | Prueba `0S1` sostenido y ciclo continuo `0S2` |
| Faltaban números de puertos y líneas de pilotaje punteadas | Agregados |
| La fuga en `L2` dependía de la posición | Fuga permanente |
| Texto chico en el celular | Texto más grande |

**Errores que encontró el revisor y corrección.**
| Error | Corrección |
|---|---|
| La pieza 3D caía después del reset | Corregido |
| La vista en pausa no se refrescaba | Corregido |
| Memoria de la GPU crecía en cada ciclo | Corregido |
| El scroll táctil en el celular interfería | Corregido |

**Pendiente.** Nada informado por el orquestador al cierre de esta nota.
