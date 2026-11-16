---
tipo: informe
fecha: 2026-11-15
tags: [exposición, simulación, revisión]
---

# Simulación de la exposición

Antes del jueves, Claude simuló la charla con **cinco agentes de IA**, cada uno haciendo de una persona del público. Cada uno "asistió" leyendo el guion, la demo, las diapositivas y la hoja, y después intentó seguir la guía como lo haría esa persona. Ninguno modificó nada: solo leyeron y opinaron.

## Quiénes fueron

| Personaje | Quién es | Qué le tocó revisar | Su veredicto |
|---|---|---|---|
| **Rubén** | Profe de Taller (torno y fresa), 58 años, usa el celular y poco más, escéptico | Seguir los niveles 0 y 1 al pie de la letra | *"La voy a probar para la hoja de seguridad y para traducir el manual de la fresadora, pero desde el celular y revisando cada renglón."* |
| **Silvia** | Profe de Lengua, 45 años, preocupada por los textos hechos con IA | La sección de alumnos, las recetas y la redacción | *"Es la charla más honesta que escuché sobre IA, pero para Lengua le falta resolver cuándo y cómo escribe el alumno solo."* |
| **Martín** | Profe de Electrónica y PLC, 32 años, usa ChatGPT, Windows 11 | Los niveles 2 a 5, la exactitud técnica y si la demo es realista | *"Las ideas son excelentes y los niveles 1 y 2 me sirven mañana; del 3 al 5 me iba a trabar con Git y con el Drive."* |
| **Camila** | Alumna de 4.° año, usa IA para casi todo | Si las consignas la frenarían de verdad | *"Lo más real fue cuando admitió que no lee lo que entrega. Lo demás sirve si el profe te pregunta de verdad en el aula."* |
| **Tomás** | Compañero de 7.°, directo | Tiempos, riesgos en vivo, coherencia y tono | Calculó que la demo dura 27 a 30 minutos y no 20, y marcó riesgos de privacidad en el proyector. |

## Lo que encontraron y se corrigió

### En la exposición
- **La demo se estira.** La versión mínima del guion estaba mal sumada y dejaba afuera Cuidados. Ahora la mínima dura unos 35 minutos, **Cuidados no se corta nunca**, y hay un orden de recorte: la versión B de 4A, jugar solo 3 preguntas, sacar el 4B y achicar el bloque 2.
- **Privacidad en el proyector.** La barra lateral de claude.ai muestra todos tus chats, y la memoria podía hacer que Claude respondiera sabiendo quién sos. Ahora la demo se hace en una **ventana de incógnito del navegador**, con la **barra lateral cerrada** y **chats incógnito de Claude**.
- **La alucinación podía no aparecer.** Si Claude busca en internet, encuentra el dato real de la escuela. Ahora el 4D se hace **con la búsqueda web apagada**.
- **Plan B más completo.**
  - Probar claude.ai en la red de la escuela días antes, por el filtro de contenidos.
  - Llevar el juego descargado como `.html`, que anda sin internet, y las capturas de los dos temas de reserva.
  - Imprimir el guion, porque si el proyector duplica la pantalla no se ven las notas de las diapositivas.
- **La dirección impresa** en la hoja y en la diapositiva 14 ahora es la misma a la que lleva el QR (`…/vaultClaseProfes/00-Inicio`).
- **Tono.** "De horas de trabajo a dos minutos" pasó a "Del pedido al juego, en minutos". "Para quien casi no usa la compu" pasó a "para empezar desde cero". Lo de los alumnos ahora se presenta como **"lo que veo desde mi lado de alumno"**, no como una lección sobre cómo evaluar.
- **Nuevas respuestas preparadas** en el guion:
  - "¿A mí en el taller de qué me sirve?"
  - "¿Aprende de lo que le digo?"
  - "¿Lo puedo usar desde el celular?"
  - "¿Los alumnos pueden usar Claude?" (pide 18 años)
  - "¿Cuándo aprenden a escribir?"
  - "¿Defensa oral con 35 alumnos?"
  - "¿Qué hago si me entregan un texto hecho con IA?"
  - "Si ustedes la usan, ¿por qué nosotros no?"

### En la guía
- **Una contradicción**: "ya no aprende de lo que le decimos" chocaba con "se puede desactivar que entrene con tus conversaciones". Ahora dice en todos lados: *no aprende mientras charlás; la empresa puede usar las conversaciones para entrenar modelos futuros, y eso se desactiva*.
- **Nueva nota [[1.6 Usar la IA desde el celular]]**, para quien no usa la compu.
- **Recetas de taller**: hoja de proceso, parámetros de corte con la fórmula a la vista y caso de falla en el torno. También un aviso en la hoja de seguridad: la IA puede poner **guantes** para el torno, y en el torno están prohibidos.
- **Recetas de formación general**: guía de lectura, corrección que respeta el voseo, comparar el borrador propio con el de la IA, y el aviso de que la IA **inventa citas** de obras.
- **[[04 Cómo usamos la IA los alumnos]]** ahora explica:
  - **por qué** lo hacemos y que también la usamos para aprender;
  - que **todo se esquiva si nadie lo sigue de cerca**;
  - qué conviene en Lengua (escritura en clase y por etapas, con el historial de versiones de Docs);
  - las **normas**: edad mínima de cada plataforma, el acuerdo de la escuela y la normativa de la Provincia, y cómo declarar el uso de IA.
- **Windows**:
  - los menús de Windows 10 y 11;
  - cómo crear una carpeta;
  - dónde queda una captura;
  - "Documentos" en pantalla contra `Documents` en la ruta;
  - OneDrive;
  - `Shift + Enter`.
- **Datos técnicos**:
  - **Git para Windows**: recomendado (la documentación lo da como opcional).
  - **Cómo volver atrás** en Claude Code, con los puntos de control.
  - **Las skills pueden traer programas que se ejecutan**, y cómo se instalan.
  - **El conector de Drive** lee en el chat y crea archivos desde Claude Code.
  - **Syncthing**: se agrega una carpeta nueva, no se edita la que viene por defecto.
  - **Git**: lo que se sube queda en el historial aunque se borre.
  - **Obsidian Git**: viene apagado de fábrica.
  - **Antigravity**: está mejor descrito.
  - **El visor 3D**: necesita un servidor local.
  - **Python**: hace falta para generar el Word.
- **Redacción** (lo marcó Silvia):
  - comas entre sujeto y verbo;
  - el "80 %" sin fuente;
  - "Materias teóricas" pasó a "materias de formación general";
  - el ejemplo de "interruptor";
  - "ni lo leo" y "ni lo miro" unificados como "ni lo miro".

## Lo que queda para decidir vos

> [!warning] Antes del jueves
> 1. **Hablar con Charrute y con Doñetz.** Tomás lo marcó como el riesgo social más grande. En vivo decís que a veces no mirás lo que entregás, y en la guía (a la que lleva el QR) figura cómo se hizo el TP8 con IA y el vault del canal de Doñetz, con su apellido. Ya aclaré en el caso que cada pareja defendió su parte en el oral, pero conviene que los dos profes lo sepan **antes** y no se enteren en la charla.
> 2. **Tus compañeros de grupo.** No aparecen con nombre, pero todos saben quiénes son. Conviene contarles que se menciona el método del grupo.
> 3. **El guion es público.** Está en la página, junto con las respuestas preparadas. Si preferís que los profes no lo lean antes, se puede sacar de la publicación y dejar solo en tu compu.
> 4. **Revisar las diapositivas en pantalla completa**: no se pudieron previsualizar automáticamente.
> 5. **Escanear el QR** con el celular.

## Lo que se decidió no cambiar
- **El plan "Ultra"**: dos personajes creían que no existía, pero figura en la página oficial de precios (noviembre de 2026).
- **"Git es obligatorio en Windows"**: Martín lo daba por obligatorio; la documentación oficial actual lo da como opcional. Quedó como **recomendado**.
- **"Hace falta Node.js para Quartz"**: no en la compu del profe, porque la página la arma GitHub. Se aclaró en [[5.2 Publicar el vault como página]].
