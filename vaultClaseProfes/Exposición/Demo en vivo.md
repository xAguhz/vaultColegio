---
tipo: demo
fecha: 2026-11-19
tags: [exposición, demo]
---

# Demo en vivo

Toda la demo se hace en **[claude.ai](https://claude.ai), desde el navegador de la compu de la escuela**. No hay que instalar nada. Es el bloque 4 del [[Guion de la exposición]].

## Preparación

### Unos días antes, en la escuela
- [ ] Entrar a **claude.ai** desde una compu de la escuela, con su red. Si el filtro de contenidos la bloquea, hay tiempo para pedir que la habiliten o para llevar datos del celular.
- [ ] Probar que esa compu **lea el pendrive** y abra un PDF.

### El día antes (en casa)
- [ ] **Ensayar la demo completa una vez** en tu compu, con los mismos textos. Cronometrala: tiene que entrar en 20 minutos.
- [ ] **Sacar capturas** de cada resultado del ensayo (`Win + Shift + S` o la herramienta de Ubuntu) y guardarlas en el celular y en un pendrive. Son el **plan B** si se corta internet: se muestran las capturas y se cuenta lo que pasó.
- [ ] Hacer en el ensayo **los dos temas de reserva** del 4B y guardar sus capturas: del tema que elija el público no puede haber plan B.
- [ ] **Descargar el juego** del ensayo (botón de descarga del panel) como archivo `.html` y guardarlo en el pendrive: se abre con doble clic y **se juega sin internet**.
- [ ] **Imprimir el guion.** Si el proyector duplica la pantalla, las notas de las diapositivas no se ven.
- [ ] Dejar en el celular, en las notas, los textos de esta página, para copiar y pegar rápido. Pasátelos por WhatsApp o mail para abrirlos en la compu de la escuela.
- [ ] Revisar que tu cuenta de Claude tenga **uso disponible**: no hacer trabajos pesados con Claude Code esa mañana.
- [ ] Tener las **diapositivas** descargadas en PDF en el pendrive, por si no hay internet.

### En la escuela, 15 minutos antes
- [ ] Prender la compu y conectar el proyector.
- [ ] Probar internet. Si anda mal: **datos del celular** compartidos (zona Wi-Fi).
- [ ] Abrir una **ventana de incógnito** del navegador (`Ctrl + Shift + N`) y hacer todo ahí: al cerrarla no queda ninguna sesión guardada en la compu.
- [ ] Abrir en pestañas, en este orden:
  1. las diapositivas: **[xaguhz.github.io/vaultColegio/vaultClaseProfes/diapositivas/](https://xaguhz.github.io/vaultColegio/vaultClaseProfes/diapositivas/)** (no hace falta iniciar sesión; `F` para pantalla completa);
  2. [xaguhz.github.io/vaultColegio](https://xaguhz.github.io/vaultColegio/), con el visor 3D del torno abierto;
  3. [claude.ai](https://claude.ai), con **tu sesión iniciada** y un **chat nuevo**.
- [ ] **Cerrar la barra lateral** de claude.ai: si no, en el proyector se ven los títulos de todos tus chats.
- [ ] Usar **chats incógnito** de Claude (el ícono del fantasmita o del antifaz, arriba): no usan la memoria. Si la memoria está activa, Claude puede responder sabiendo quién sos, a qué escuela vas o en qué andás, y eso arruina la demo y muestra cosas personales en pantalla.
- [ ] Elegir el modelo **Sonnet** (es rápido; Opus tarda más frente al público).
- [ ] Hacer `Ctrl + +` dos o tres veces en la pestaña de Claude para **agrandar la letra** del proyector.
- [ ] Desactivar las notificaciones del celular si lo usás como zona Wi-Fi.

> [!warning] Compu compartida
> Con la ventana de incógnito, el navegador no guarda nada. Igual, si pregunta **"¿Guardar contraseña?"**, respondé **Nunca**. Al terminar, **cerrá sesión** (ver el final de esta nota).

## 4A. Pedido vago contra pedido completo (6 min)

**Chat nuevo.** Primero, el vago:

```
Haceme una evaluación de circuitos.
```

Mientras escribe, decir: *"Fíjense: no sabe para qué año es, qué temas dimos ni cuánto dura la clase. Va a inventar algo genérico."*

Pasar a la diapo de las **5 partes**. Después, **en un chat nuevo**:

```
Soy profe de Electrotecnia de 4.° año en una escuela técnica (alumnos de 16 años).
Necesito una evaluación escrita de 80 minutos sobre circuitos serie, paralelo y mixtos
con resistencias, ley de Ohm y potencia. Todavía no vimos Kirchhoff.

Armá 6 ejercicios de menor a mayor dificultad. El último tiene que ser un caso real
(la instalación de luces de un taller). Usá valores comerciales de resistencias.

Entregá la evaluación lista para imprimir y, aparte, una rúbrica de corrección
con puntaje total de 10.
```

Mostrar la diferencia. Después, en el mismo chat, para que vean que se puede corregir:

```
El ejercicio 3 está muy difícil para 4.° año. Simplificalo.
```

✂️ **Controlar una cuenta (1 min, si hay tiempo; si no, se cuenta).** En el mismo chat:

```
Resolvé el ejercicio 2 ejecutando código y mostrame el código y la cuenta.
```

Pedirle a un profe del público que haga la misma cuenta con la calculadora del celular. *"Si coincide, bien. Si no coincide, mejor: esa es la lección. Los resultados que arma la IA se controlan siempre."*

✂️ Si sobra tiempo (si no, se cuenta): *"Agregá una versión B de toda la evaluación con otros valores, para que no se copien."* Genera mucho texto y tarda.

## 4B. Una materia que elijan ellos (6 min) ✂️

Preguntar al público una materia y un tema. **Chat nuevo**:

```
Soy profe de [MATERIA] de [AÑO] año en una escuela técnica de la provincia de Buenos Aires.
Estoy dando [TEMA]. Necesito:
1. Una consigna de trabajo práctico para hacer en grupos en 2 clases, que obligue
   a los alumnos a aplicar el tema a algo de su vida o de la escuela
   (para que resolverla exija ir, mirar o medir algo que la IA no conoce).
2. Una rúbrica de corrección con 4 criterios y 4 niveles.
3. Tres preguntas para hacerles en una defensa oral corta del trabajo.
Escribí en castellano rioplatense, con "vos".
```

**Temas de reserva** (si nadie propone o hay que elegir rápido):
- Técnico: *Máquinas eléctricas, 5.° año: arranque estrella-triángulo de motores trifásicos.*
- Teórico: *Lengua, 4.° año: el texto argumentativo.*

## 4C. Un juego para la clase (5 min)

**Chat nuevo**:

```
Creá un juego de preguntas interactivo para repasar [TEMA DEL 4B, o "la ley de Ohm"]
con alumnos de [AÑO] año. 10 preguntas de opción múltiple, de menor a mayor dificultad.
Que muestre si la respuesta es correcta, explique por qué en una línea, lleve el puntaje
y al final muestre un mensaje según el resultado. Que se vea bien y con colores.
```

Claude lo arma en el **panel de la derecha** (un *Artifact*). Se puede jugar ahí mismo: **invitar a un profe a pasar y jugar 3 preguntas**, no las 10.

Si sobra tiempo: *"Agregale un temporizador de 20 segundos por pregunta"*, para que vean que se modifica hablando.

## 4D. Cazar una alucinación (3 min) ✂️

**Chat nuevo e incógnito, con la búsqueda web desactivada** (en el ícono de herramientas). Si busca en internet puede encontrar el dato real y no inventar nada.

Antes de enviar, aclarar: *"Lo que aparezca ahora puede ser inventado. No es la historia de la escuela: no lo anoten."*

```
¿En qué año se fundó la EEST N.° 3 de San Antonio de Padua, quién fue su primer
director y cuántos alumnos tuvo en su primera promoción?
```

Pueden pasar dos cosas, y las dos sirven:
- **Inventa datos** → *"¿De dónde sacaste eso? Dame la fuente con link."* Mostrar que no puede respaldarlo. Decir: *"Ojo: sin internet, la fuente que te da también la escribe él. No sabe de dónde sacó el dato. Por eso lo que vale es abrir la fuente vos."* **Lección: siempre pedir la fuente y abrirla.**
- **Dice que no sabe** → *"Bien: los modelos buenos ya admiten cuando no saben. Pero no siempre: por eso hay que verificar igual."*

Variante si responde muy prudente: *"Dame tres citas textuales del Diseño Curricular de la Provincia de Buenos Aires sobre [materia], con número de página."*

## Si algo falla

| Problema | Qué hago |
|---|---|
| Internet lento o cortado | Datos del celular. Si tampoco anda: **capturas del ensayo** y **el juego descargado** en el pendrive, y las diapositivas en PDF |
| Claude tarda mucho | Mientras escribe, explicar lo que se está viendo. Si lo lento es Claude, cambiar a Haiku; si lo lento es internet, cambiar de modelo no sirve: pasar a las capturas |
| "Límite de uso alcanzado" | Pasar a las capturas. (Por eso no usar Claude Code esa mañana.) |
| La respuesta sale mal | **¡Mejor!** Es el ejemplo perfecto de que hay que revisar. Corregirla en vivo |
| Letra chica en el proyector | `Ctrl + +` |

## Al terminar (importante)
1. En claude.ai: tu nombre (abajo a la izquierda) → **Cerrar sesión**.
2. **Cerrar la ventana de incógnito.** Si entraste con Google, cerrar sesión en Claude no te saca de Google, pero la ventana de incógnito sí borra todo al cerrarse.
3. Si por error trabajaste en una ventana normal: menú **⋮ → Configuración → Privacidad → Borrar datos de navegación** → "Contraseñas" y "Cookies" → Borrar.
