---
tipo: revisión
actualizado: 2026-11-17
tags: [oficina-ia, errores, mejoras]
---

# Errores, contradicciones y mejoras

## Contradicciones en la idea original
| # | La idea | Lo que pasa en realidad | Qué se hizo |
|---|---|---|---|
| 1 | "Menor costo" | Sonnet cuesta la mitad, pero cada agente arranca de cero y el orquestador coordina. El ahorro real ronda el 20 % en tareas pesadas, y en tareas chicas **cuesta más** | Regla "no delegar lo chico"; ver [[Costo y velocidad]] |
| 2 | "Más rápido" | Solo se acelera lo independiente; lo que va en cadena no. Coordinar también lleva tiempo | Regla "en paralelo solo lo independiente" |
| 3 | "5 agentes" | Tener 5 roles no significa usar 5 cada vez; usar agentes de más es gastar de más | 5 es el **máximo** simultáneo, no la cantidad obligatoria |
| 4 | "Opus en medium" | En Opus 5.5 **medio ya es el nivel de fábrica**; la configuración solo lo deja explícito. Para decisiones difíciles conviene subirlo (`/effort high`) | `modelSettings` con `medium` |
| 5 | Calidad igual con Sonnet | Sonnet es muy bueno en tareas acotadas, pero se equivoca más en razonamientos largos o ambiguos | Lo difícil (diseño, decisiones) lo hace Opus; todo cambio pasa por probador y revisor |
| 6 | Los agentes "saben" de qué se habla | No ven la conversación | Encargo autocontenido obligatorio (objetivo, contexto, archivos, criterio, formato) |
| 7 | Varios trabajando a la vez sin problemas | Dos agentes editando el mismo archivo se pisan | Un archivo, un dueño; si no, copia aislada (`isolation: worktree`) |

## Errores y límites de la configuración
- **Sesiones en la nube con varios repos:** no se aplican `model`, `env` ni permisos del `.claude/settings.json` de cada repo. Hay que abrir la sesión con un solo repo o elegir modelo y esfuerzo con `/model` y `/effort`. Ver [[Instalación y uso]].
- **La configuración de usuario no viaja a la nube:** `~/.claude/settings.json` solo vale en tu computadora. Por eso la oficina se guardó **en los repos**.
- **Se activa en sesiones nuevas:** los agentes se leen al empezar la sesión.
- **Permisos de GitHub:** al habilitar solo SRacks en la app de Claude, se perdió el permiso de escritura en `vaultColegio` (error 403). Hay que tildar **los dos** repos.

## Errores míos que la oficina tiene que evitar
Revisando el trabajo de las sesiones anteriores sobre Sain Racks:

| Error | Qué pasó | Qué regla o agente lo evita |
|---|---|---|
| Calcular sin preguntar el uso | Calculé el depósito para **pallets** y era para **largueros**; hubo que rehacer todo | Protocolo, paso 1: "entender antes de calcular" |
| Supuesto tomado como dato | Modelé el techo como 8 m al costado y 12 m al centro; las fotos sugerían ~6 / 7,5 m, y eso cambia la capacidad | El revisor marca "supuestos sin confirmar"; decir los supuestos en voz alta |
| Datos de la empresa en un repo público | El primer vault de Sain Racks se armó dentro de `vaultColegio` (público); después se movió | El revisor revisa privacidad; el `CLAUDE.md` de vaultColegio lo advierte |
| Errores de código al reorganizar | Un nombre mal leído (`first.title`), imports duplicados, nombres cortados | Se detectaron con pruebas: el probador lo vuelve obligatorio |
| Detalles visuales rotos | Botones visibles fuera de lugar, paquetes flotando, escala que "se sentía chica" (ángulo de visión angosto y velocidad irreal) | Probador con capturas; comparar con referencias reales (fotos, medidas) |
| Falso error en una prueba | Una prueba sin UTF-8 rompió los acentos y parecía un error del programa | El probador prueba en condiciones iguales a las reales |
| Trabajo largo de una sola vez | Muchas notas escritas por un solo modelo, en serie | El documentador escribe al final y en paralelo con la verificación |

> [!note] Sobre "23 horas escribiendo notas"
> En la rama `modular` de SRacks hay 10 commits del 16 y 17/11 que no son de la sesión que armó esta oficina: el botón Foto → 3D, pruebas con fotos reales, la lente del EXIF y modelos en Blender. Hubo **otra sesión trabajando en paralelo** sobre el mismo repo, y eso explica las horas. Lección: dos sesiones en la misma rama pueden pisarse. Conviene una sesión por rama, o que el orquestador haga `git fetch` antes de empezar y antes de subir.

## Mejoras propuestas (no aplicadas todavía)
1. **Haiku para lo trivial** (renombrar, ordenar, formatear): cuesta 20 veces menos que Sonnet. No se usó porque el pedido era Sonnet.
2. **Memoria por proyecto** en los agentes (`memory: project`), para que recuerden convenciones entre sesiones.
3. **Hooks**: correr las pruebas automáticamente después de cada edición del programador.
4. **Medir**: comparar `/usage` con y sin oficina en tareas parecidas (ver [[Costo y velocidad]]).
5. **Un agente de diseño 3D** si el editor de la nave sigue creciendo.

## Pendiente
- **Los dos videos de referencia** no se pudieron ver: YouTube bloquea esta sesión como bot. Cuando estén las transcripciones, se suman sus ideas acá. Ver [[Fuentes]].
