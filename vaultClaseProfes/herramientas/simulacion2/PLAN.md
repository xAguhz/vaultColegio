# Segunda simulación de la charla: plan completo

Pedido del usuario (15/11/2026): *"pon a varios agentes que simulen lo mismo de antes: alumnos, profesores y terceros que supondríamos estarían en la Expo Técnica de paso (padres, madres, empleados, empresarios, gente buscando potenciales en la IA, etc.) y gente del rubro que haya estudiado IA"*. El usuario dio **permiso para decidir todo por cuenta propia**. No hay que preguntarle nada: decidir y dejarlo anotado.

La charla es el **jueves 19/11/2026** en la Expo Técnica. Todo en **castellano rioplatense**.

## Contexto (leerlo antes de empezar)
- Vault: `~/Colegio/vaultColegio/vaultClaseProfes/` (repo público `xAguhz/vaultColegio`, se publica en https://xaguhz.github.io/vaultColegio/ con cada push a `main`).
- Primera simulación y lo que se corrigió: `Exposición/Simulación de la exposición.md`. **No repetir hallazgos ya resueltos**; buscar lo nuevo.
- Material de la charla: `Exposición/Guion de la exposición.md`, `Exposición/Demo en vivo.md`, `Exposición/00 Exposición.md`, `Exposición/Hoja para imprimir.html`.
- Diapositivas, fuente principal: `herramientas/diapositivas/project/` (`deck.json` con el orden, `deck.css` y `slides/<id>.html`; el `<aside>` son las notas del orador). La versión publicada (`Exposición/Diapositivas.html`) se genera con `python3 herramientas/armar_diapositivas.py`.
- Memoria del proyecto: `~/.claude/projects/-home-chagus-Colegio/memory/vault-clase-profes.md` (y `vaultcolegio-github.md`).

## Control de límite (IMPORTANTE)
Antes de cada tanda de agentes, mirar el uso con `mcp__ccd_session_mgmt__get_usage`:
- Al empezar, agregar en `ESTADO.md` una nota "EN CURSO" con fecha y hora; al terminar o cortar, reemplazarla por lo que se hizo.
- Si la **ventana de 5 horas pasa el 80 %** o la **semanal pasa el 92 %**: guardar el avance en `ESTADO.md` y terminar. Una corrida automática **no puede** crear tareas programadas sin el usuario, así que se dejaron corridas de respaldo ya programadas: `simulacion-2-charla-ia` (lunes 16/11 a las 5:15), `simulacion-2-charla-ia-respaldo-1` (lunes 16/11 a las 11:00) y `simulacion-2-charla-ia-respaldo-2` (martes 17/11 a las 5:15). Cada una sigue desde donde dejó la anterior.
- Lanzar los agentes **de a 3 o 4 por tanda**, no todos juntos.
- **Guardar cada informe apenas llega** en `informes/NN-nombre.md`, y marcarlo en `ESTADO.md`. Si se corta, la próxima corrida solo lanza los que faltan.

## Personajes (11)
Cada uno es un subagente `general-purpose` en segundo plano, **solo lectura** ("NO modifiques ningún archivo").

| # | Personaje | Grupo | Qué lee | Foco |
|---|---|---|---|---|
| 01 | **Valentina**, 13 años, 2.° año. Usa TikTok y la IA del celular | Alumna | Diapositivas, guion (lo que se dice), hoja, `04 Cómo usamos la IA los alumnos.md`, `1.6 Usar la IA desde el celular.md` | ¿Qué entiende una chica de 13? Edad mínima (Claude pide 18): ¿qué puede usar ella? ¿Le habla a ella o solo a los profes? |
| 02 | **Lucas**, 17 años, 6.° Electromecánica. No usa IA "por principio": le parece trampa y le preocupa quedarse sin trabajo | Alumno | Guion, diapositivas, `04`, casos reales | El argumento del alumno que la rechaza. ¿La charla lo convence o lo deja afuera? Empleo futuro, dependencia |
| 03 | **Norma**, 55, profe de Matemática | Profesora | Guion, demo, niveles 0 a 2, `1.4 Recetas` | Cálculos: ¿la guía enseña a verificar cuentas? Recetas para Matemática (no hay). Errores numéricos en los ejemplos |
| 04 | **Graciela**, 60, directora de la escuela | Directivo | Todo el material de la charla, `04`, casos reales, `5.2 Publicar` | Responsabilidad institucional: datos de alumnos, normativa (DGCyE), imagen de la escuela, que se nombre a profes (Charrute, Doñetz) y la escuela en un sitio público, plan Claude for Education, qué aprobaría y qué no |
| 05 | **Diego**, 40, profe de Historia y Construcción de Ciudadanía | Profesor | Guion, diapositivas, `0.3`, `0.4`, `1.5`, `04` | Sesgos, fuentes, quién está detrás de las IA (empresas de EE. UU.), soberanía de datos, pensamiento crítico. ¿La charla es demasiado "pro IA"? |
| 06 | **Mónica**, 42, madre de un alumno de 1.° año, administrativa | Público de paso | Ve 15 minutos de la charla (bloques 3, 5 y 6 del guion y sus diapositivas), la hoja y el QR (`00 Inicio.md`) | Seguridad de los chicos, edad, costo, qué hacer en casa, si los profes "van a enseñar con robots" |
| 07 | **Carlos**, 50, padre, encargado de depósito en una distribuidora, poco tecnológico | Público de paso | Las diapositivas de corrido, la hoja y `1.1`/`1.2` si escanea el QR | ¿Le sirve a él para su trabajo (planillas, mails, pedidos)? ¿Se entiende sin ser docente? |
| 08 | **Ricardo**, 58, dueño de una PyME metalúrgica de la zona oeste (30 empleados) | Público de paso / empresario | Diapositivas, `03 Cómo llegué hasta acá.md`, casos reales (sobre todo el torno), `5.4` y `5.5` | Ve un potencial empleado o pasante. Aplicación en su empresa: manuales de máquinas, mantenimiento, costos, confidencialidad de planos. ¿Qué le preguntaría al alumno? |
| 09 | **Sofía**, 29, emprendedora que "busca oportunidades en la IA" (vende automatizaciones y cursos) | Público de paso | Diapositivas, `01 Mi entorno en una imagen.md`, nivel 4 y 5, casos | Mirada de negocio y de hype: ¿hay algo vendible? ¿Qué promete de más la charla? ¿Qué le falta para ser replicable? |
| 10 | **Dra. Laura Ferreyra**, 38, ingeniera en sistemas con doctorado en procesamiento de lenguaje natural, trabaja en IA | Especialista | Todo: `0.3`, `0.4`, `0.5`, `1.3`, `1.5`, `2.5`, `4.3`, `4.5`, guion y diapositivas | Rigor técnico: ¿"autocompletador gigante" es una buena simplificación? Entrenamiento, alucinaciones, memoria, contexto, tokens, privacidad, sesgos, consumo de energía. Errores técnicos concretos con corrección |
| 11 | **Pablo Iturbe**, 47, especialista en educación y tecnología, forma docentes en alfabetización en IA | Especialista | `04`, guion, niveles 0 a 2, casos, la simulación anterior | Pedagogía: ¿la propuesta tiene sustento? Evaluación, integridad académica, alfabetización en IA, qué recomiendan los marcos (UNESCO y otros, sin inventar citas). ¿Es replicable por otros docentes? |

### Prompt base para cada agente
> Sos un personaje en una SIMULACIÓN de una charla. Respondé siempre en castellano rioplatense.
> PERSONAJE: (descripción de la tabla, en 3 o 4 renglones, con voz propia).
> SITUACIÓN: en la Expo Técnica 2026 de una escuela técnica del oeste del conurbano bonaerense, un alumno de 7.° año da una charla de 50 minutos (más 10 de preguntas) sobre cómo usar la IA. Es para los profes, pero la Expo está abierta y pasa gente. (Si es público de paso: "Vos pasás por la Expo y te quedás un rato".)
> MATERIAL (rutas absolutas): guion, demo, diapositivas (`.../herramientas/diapositivas/project/slides/<id>.html` en el orden de `deck.json`; el `<aside>` son notas del orador que el público no ve), hoja, y las notas que le tocan.
> TAREA ESPECÍFICA: (el foco de la tabla).
> NO modifiques ningún archivo. Solo leé.
> ENTREGÁ un informe de máximo unas 700 palabras con: 1) reacciones mientras mirás o escuchás; 2) preguntas que harías en voz alta (textuales) y si el guion ya tiene respuesta; 3) problemas concretos (archivo + frase exacta + qué está mal + corrección propuesta); 4) las 3 cosas que más cambiarías; 5) veredicto en una frase.

## Después de los informes
1. Leer todos los informes de `informes/`. Separar: **errores** (corregir siempre), **mejoras** (aplicar las que valgan la pena) y **opiniones** (dejar registradas).
2. **Verificar en fuentes oficiales** cualquier dato que un personaje discuta antes de cambiarlo (la simulación anterior tuvo agentes equivocados: plan Ultra, Git obligatorio, Node).
3. Corregir guía, guion, demo, hoja y diapositivas. Reglas del vault:
   - wikilinks **solo con el nombre de la nota, sin carpeta**;
   - no inventar anécdotas del usuario (si hace falta una, dejar `> [!todo]` y anotarlo para preguntarle);
   - voz en primera persona del alumno;
   - nunca nombres de compañeros.
4. Si se tocan diapositivas:
   - editar `herramientas/diapositivas/project/slides/…`;
   - correr `python3 herramientas/armar_diapositivas.py`;
   - actualizar el Artifact privado `https://claude.ai/artifact/QvCiGeS3oEQ3hX4JiLZ5sr` con la herramienta Artifact (publish, `url` ese, `root` = `.../herramientas/diapositivas`, `file_path` y `files` con las diapositivas cambiadas; leer antes con `action: read` si la sesión no lo publicó);
   - revisar cada diapositiva cambiada con capturas reales: servidor `clase-profes` de `~/Colegio/.claude/launch.json`, `http://localhost:8769/Exposición/Diapositivas.html#N`, viewport 1920×1080;
   - nunca `flex:0`.
5. Escribir `Exposición/Simulación 2 de la exposición.md` con el mismo formato que la primera (quiénes fueron, qué encontraron, qué se corrigió, qué queda para decidir el usuario, qué no se cambió y por qué). Enlazarla desde `Exposición/00 Exposición.md`.
6. Commit en `main` con mensaje en castellano y `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, push, esperar el workflow (`gh run list`) y correr `python3 vaultClaseProfes/herramientas/revisar_links.py ~/Colegio/vaultColegio vaultClaseProfes` (tiene que dar 0 rotos).
7. Actualizar la memoria `vault-clase-profes.md` con el resultado y marcar `ESTADO.md` como **TERMINADO**.
8. Al final, dejar en el resumen de la corrida qué se hizo y qué decisiones quedan para el usuario.
