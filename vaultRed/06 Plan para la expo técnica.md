---
tipo: guía
tags: [expo, presentación, público-general]
actualizado: 2026-11-17
---

# Plan para la expo técnica

> **Supuestos:** formato stand (mesa, una notebook, quizá un monitor o TV), visitantes que pasan entre 1 y 10 minutos, vos repetís la explicación muchas veces en el día, e internet mala o nula. Si hay TV o monitor grande, el plan mejora. Si hay solo la notebook, el loop y la demo comparten pantalla (ver "Armado"). Si hay buena conexión, igual armá el Plan B: es el plan real.

Base: sitio https://xaguhz.github.io/vaultColegio/ (8 vaults, 406 notas, 2156 enlaces). Esto **no reemplaza** la charla para profes (guion, diapositivas y hoja en el vault [Clase para profes](https://xaguhz.github.io/vaultColegio/vaultClaseProfes/)): usa los mismos contenidos con otro enfoque. Para el momento en que se muestra la página de la red, ver también [[03 Guion para la presentación]].

## 1. Idea fuerza

> **"Tocá una pieza y mirá cómo funciona: un torno, un auto y un invento nuestro, desarmados en 3D. Y yo los armé con IA, revisando todo."**

Versión corta para el cartel (a preparar): **"Desarmá un torno y un auto con el dedo."**

Primero la máquina (lo que atrae a cualquiera), después la IA (cómo se hizo). La IA es la herramienta, el protagonista es la electromecánica.

## 2. Diferencias con la charla para profes

| | Charla para profes | Expo técnica |
|---|---|---|
| Enfoque | Cómo usar IA en la docencia | Qué construí y cómo funciona la máquina |
| Duración | 50 min, una sola vez, sentados | 30 s / 2 min / 5-7 min, repetida todo el día |
| Qué se muestra | 15 diapositivas, demo en vivo de Claude, hoja con QR | Visores 3D, spot de AutoLID, grafo de la red |
| Tono | Profesional, con argumentos | Cercano, de taller: "tocá, probá" |
| Interacción | Preguntas al final | Las manos del visitante sobre la pantalla |
| Se deja afuera | La IA en abstracto no se esquiva, pero se la cuenta breve | Rúbricas, consignas, detectores, normativa y todo lo específico para docentes |

## 3. Armado del stand

| Elemento | Qué muestra | Notas |
|---|---|---|
| **Notebook (en mano)** | Visor 3D para que el visitante toque | Es la estrella. Pantalla táctil si hay; si no, mouse a mano. |
| **TV / monitor (si hay)** | Loop: spot de AutoLID (42 s, mp4 local) y, en el medio, visor del Suzuki en animación/capas | Sin internet: spot en mp4 y Suzuki (PWA) funcionan. |
| **Sin TV** | La notebook corre el spot en loop cuando no hay nadie; al llegar alguien, pausás y abrís el visor | Dejá el visor ya abierto en otra pestaña. |
| **Cartel grande** (a preparar) | Idea fuerza + QR al sitio | QR a https://xaguhz.github.io/vaultColegio/ |
| **QR de cada visor** (a preparar) | Torno, Suzuki, AutoLID | En un cartel chico cada uno, con nombre de la máquina. |
| **Impreso** | Hoja A4 con QR + 3 frases (qué es, cómo se hizo, las 3 reglas) | Reutilizá la hoja de https://xaguhz.github.io/vaultColegio/vaultClaseProfes/hoja/ adaptada (a preparar versión expo). |

**Disposición:** notebook en el frente de la mesa, inclinada hacia el visitante; vos al costado (no atrás de la mesa). Cartel a la altura de los ojos, TV a la vista desde el pasillo. Una pieza física al lado (si podés traer una del taller o del auto, mejor).

Visores (todos bajo https://xaguhz.github.io/vaultColegio/):
- Torno Femar TM300: `vaultTorno/3D/visor/` (59 piezas, 10 conjuntos; necesita internet).
- Suzuki Swift ZC21S: `vaultSuzuki/3D/visor/` (140 piezas, 20 conjuntos; PWA, ~25 MB, anda sin internet).
- AutoLID: `vaultAutoLID/AutoLID/3D/visor/` (25 piezas, 7 conjuntos) y `vaultAutoLID/AutoLID/Web/` (simulador).

## 4. Recorrido por capas

### Gancho de 30 segundos (el que pasa caminando)

1. **Mostrá:** el visor del Suzuki o del torno ya en pleno despiece.
2. **Decí:** *"¿Querés desarmar un auto con el dedo? Tocá cualquier pieza."*
3. Dejá que toque. Cuando aparece la ficha: *"Esto lo armé con IA, pieza por pieza, y lo revisé yo."*
4. Entregá la hoja o señalá el QR.

### Versión de 2 minutos

| Paso | Qué mostrás | Qué decís |
|---|---|---|
| 1 | Visor del torno: despiece animado, tocar una pieza (la cámara se acerca, aparece la ficha) | "Este es el torno del taller, un Femar TM300: 59 piezas en 10 conjuntos. Tocá una." |
| 2 | Suzuki: capas y rayos X | "Y este es un Suzuki Swift: 140 piezas, 20 conjuntos, 37 circuitos eléctricos." |
| 3 | Spot de AutoLID o su visor | "Este lo inventamos en grupo: abre y cierra la tapa del inodoro sin tocarla. Sensor ultrasónico, servo y batería de unos 60 días." |
| 4 | QR | "Todo está en internet, gratis. Escaneá y seguilo en tu casa." |

### Versión de 5 a 7 minutos (el que se queda)

1. **La máquina (2 min):** torno y Suzuki, dejándole tocar. Mostrá un circuito eléctrico y un conector del Suzuki (37 circuitos, 193 conectores).
2. **El invento (1,5 min):** AutoLID: simulador de la web, visor 3D, spot. Si hay interés de empresa: cifras de costos y evaluación financiera del informe.
3. **Cómo lo hice (2 min):** grafo de la red (`red/`): "406 notas y 2156 enlaces; cada punto es una nota". Explicá el método en una línea: fuente → texto → notas → enlaces → mapas → producir → publicar ([[02 El método paso a paso]]).
4. **La IA, en tres frases (1 min):**
   - "La IA es un autocompletador gigante: escribe palabra por palabra y puede inventar con total seguridad."
   - "Un buen pedido tiene contexto, tarea, material, formato y criterios."
   - "Tres reglas: no darle datos privados, verificar los datos duros y **vos firmás**." (más en [[Trabajo con IA]] y [[Privacidad]])
5. **Cierre:** "Lo que no revisé, no lo aprendí. Por eso reviso todo." QR y hoja.

## 5. Adaptaciones por público

| Público | Mostrá primero | Frase |
|---|---|---|
| **Chicos** | Visor 3D: dejalos tocar y "explotar" el auto | "Tocá lo que quieras. ¿Qué pieza será esta?" Spot de AutoLID después. |
| **Familias** | Spot de AutoLID, después el torno | "Esto lo hace un chico de 7.° año de una escuela técnica de Buenos Aires." |
| **Alumnos de otros años** | Grafo de la red y método | "Cualquiera puede armar su red desde cero: [[04 Cómo empezar una red propia]]." |
| **Docentes de otras áreas** | Cómo se arma una red de notas y el sitio completo | "Esto sirve para cualquier materia: partís de una fuente y la convertís en notas enlazadas." (La guía por niveles queda en el QR, no la explicás.) |
| **Gente de empresas o del rubro** | Suzuki (circuitos, conectores) y AutoLID con costos del informe | "El manual de taller está ordenado y se busca en segundos. ¿Qué documentación de tu rubro estaría bien así?" |
| **Escépticos de la IA** | Una pieza del visor y su ficha, y tu revisión | "Tenés razón en desconfiar. Por eso verifico los datos duros y firmo yo. Lo que no revisé, no lo aprendí." |

## 6. Preguntas frecuentes (ampliadas en [[05 Preguntas frecuentes]])

| Pregunta | Respuesta corta |
|---|---|
| ¿Lo hizo la IA? | "Me ayudó, pero el trabajo es mío: yo elijo, reviso y firmo. Sin revisar no se entrega." |
| ¿Es copiarse? | "Copiarse es entregar sin mirar. Acá yo lo tengo que exponer, y si lo expongo, aprendo." |
| ¿Cuánto cuesta? | "Verlo es gratis. Para armarlo: Obsidian, GitHub, la página web y Blender son gratis; el asistente de IA es pago (una suscripción). De AutoLID hay cifras de costos y evaluación financiera en el informe." |
| ¿Lo puedo usar yo / mi hijo? | "Depende de la edad mínima: Claude pide 18; ChatGPT 13 con permiso; Gemini 13. Para menores, siempre con un adulto." |
| ¿La IA aprende de lo que le digo? | "Por eso no le doy datos privados ni planos de clientes: tratalo como si fuera un lugar público." ([[Privacidad]]) |
| ¿Me va a reemplazar? | "No reemplaza al que revisa y firma. Una máquina o un circuito mal explicados los tiene que detectar alguien que sepa." |
| ¿Es exacto el modelo 3D? | "Es una representación de estudio, armada desde el manual y revisada por mí. Para trabajar, siempre manda el manual original." |
| ¿Por qué hacerlo en casa? | "Porque en casa puedo practicar y repasar a mi ritmo, y en el taller uso la máquina de verdad." |
| ¿Y mis planos de clientes? | "Nunca los subas. Anonimizá o no los uses." |
| ¿Está en internet? ¿Lo puedo ver? | "Sí, escaneá el QR. Es gratis." |

No improvises cifras: si te preguntan algo que no sabés, decí "eso no lo verifiqué" y anotalo.

## 7. Plan B sin internet

| Qué | Cómo |
|---|---|
| **Suzuki** | Abrilo en la notebook **con internet, la noche anterior**; es PWA y queda guardado (~25 MB). Probalo en modo avión. |
| **Spot de AutoLID** | Bajá el mp4 (42 s) y guardalo en el escritorio. |
| **Torno, AutoLID 3D y grafo** | Dependen del CDN (three.js / d3): **no andan sin internet**. Preparación: grabá un video corto de pantalla de cada uno (a preparar) y sacá capturas (a preparar). |
| **Sitio entero** | Cloná/descargá el repositorio y abrilo localmente: con Obsidian, abrí la carpeta de cada vault como bóveda; Obsidian funciona sin internet y alcanza para mostrar las notas, los Canvas y el grafo de cada vault (los visores 3D no, para eso están los videos de respaldo). |
| **Celular como respaldo** | Datos móviles del celular o anclaje (hotspot) para la notebook; probalo el día anterior. |

Ante la falta de internet decí: *"Sin conexión, se ve igual: acá tengo el video y el visor del auto guardados."*

## 8. Checklist cronológico

### Una semana antes
- [ ] **Revisar AutoLID en el sitio público:** hay notas con nombres completos de los integrantes y un correo de contacto. Quitar o reemplazar (por ejemplo, "integrante A"), republicar y verificar en la web. Ver [[Privacidad]].
- [ ] Decidir si se muestran las traducciones de manuales con derechos de autor (torno y Suzuki); mostrar el visor sí, el manual completo, solo si lo definís con el docente.
- [ ] Imprimir cartel, QR y hoja (a preparar).
- [ ] Grabar los videos cortos de respaldo (a preparar). Tener en cuenta que los videos de AutoLID son pesados.
- [ ] Avisar a la escuela: necesitás mesa, toma de corriente, y TV si hay.

### El día anterior
- [ ] Abrir el Suzuki con internet para que se guarde. Probar en modo avión.
- [ ] Copiar el mp4 y los videos a la notebook y a un pendrive.
- [ ] Cargar notebook y celular; llevar cargador y alargue.
- [ ] Ensayar el gancho de 30 s y la versión de 2 min en voz alta.

### La mañana de la expo
- [ ] Llegar temprano, armar el stand, probar la conexión.
- [ ] Dejar abiertas las pestañas: Suzuki, torno, AutoLID, grafo y el video.
- [ ] Poner el loop en marcha.

### Durante
- [ ] Tomá agua y comé algo; no hables todo el día sin pausa.
- [ ] Si hay compañeros, rotá cada 45-60 minutos.
- [ ] Anotá las preguntas en un cuaderno (una marca por vez).
- [ ] Si se traba algo, pasá al Plan B sin explicar.

### Después
- [ ] Pasar las preguntas anotadas a [[05 Preguntas frecuentes]] y mejorar la respuesta.
- [ ] Anotar qué funcionó y qué no (gancho, orden, carteles).
- [ ] Guardar los carteles y videos para la próxima.

## 9. Las dos "presentaciones estilo diapositiva"

| | Diapositivas de la charla para profes (15) | Página de la red en modo presentación (`red/`) |
|---|---|---|
| **En la expo** | **No conviene** como recurso principal: es lineal, larga y pensada para docentes sentados | **Sí, pero como complemento**, no como apertura |
| **Cuándo** | Solo para una charla breve a un grupo (por ejemplo, un curso que llega junto) | En la versión de 5-7 min, para mostrar "cómo se conecta todo" |
| **Cómo** | Elegí 3 diapositivas: qué es la IA, las cinco partes de un buen pedido y las tres reglas | Avanzá con flechas por los vaults |
| **Límite** | Requiere ajustar el contenido docente | Sin internet no dibuja el grafo (d3 viene de un CDN): tené el video de respaldo |

Regla simple: **en el stand, las manos del visitante van primero a los visores 3D; las diapositivas son solo apoyo.**
