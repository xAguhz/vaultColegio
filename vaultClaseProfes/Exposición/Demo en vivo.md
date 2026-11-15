---
tipo: demo
fecha: 2026-11-19
tags: [exposición, demo]
---

# Demo en vivo

Toda la demo se hace en **[claude.ai](https://claude.ai), desde el navegador de la compu de la escuela**. No hay que instalar nada. Es el bloque 4 del [[Guion de la exposición]].

## Preparación

### El día antes (en casa)
- [ ] **Ensayar la demo completa una vez** en tu compu, con los mismos textos. Cronometrala: tiene que entrar en 20 minutos.
- [ ] **Sacar capturas** de cada resultado del ensayo (`Win + Shift + S` o la herramienta de Ubuntu) y guardarlas en el celular y en un pendrive. Son el **plan B** si se corta internet: se muestran las capturas y se cuenta lo que pasó.
- [ ] Dejar en el celular, en las notas, los textos de esta página, para copiar y pegar rápido. Pasátelos por WhatsApp o mail para abrirlos en la compu de la escuela.
- [ ] Revisar que tu cuenta de Claude tenga **uso disponible**: no hacer trabajos pesados con Claude Code esa mañana.
- [ ] Tener las **diapositivas** descargadas en PDF en el pendrive.

### En la escuela, 15 minutos antes
- [ ] Prender la compu y conectar el proyector.
- [ ] Probar internet. Si anda mal: **datos del celular** compartidos (zona Wi-Fi).
- [ ] Abrir en pestañas, en este orden:
  1. las diapositivas;
  2. [xaguhz.github.io/vaultColegio](https://xaguhz.github.io/vaultColegio/), con el visor 3D del torno abierto;
  3. [claude.ai](https://claude.ai), con **tu sesión iniciada** y un **chat nuevo**.
- [ ] Elegir el modelo **Sonnet** (es rápido; Opus tarda más frente al público).
- [ ] Hacer `Ctrl + +` dos o tres veces en la pestaña de Claude para **agrandar la letra** del proyector.
- [ ] Desactivar las notificaciones del celular si lo usás como zona Wi-Fi.

> [!warning] Compu compartida
> Al iniciar sesión, si el navegador pregunta **"¿Guardar contraseña?"**, respondé **Nunca**. Al terminar, **cerrá sesión** (ver el final de esta nota).

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
El ejercicio 3 está muy difícil para 4.° año. Simplificalo. Y agregá una versión B
de toda la evaluación con otros valores, para que no se copien.
```

## 4B. Una materia que elijan ellos (6 min) ✂️

Preguntar al público una materia y un tema. **Chat nuevo**:

```
Soy profe de [MATERIA] de [AÑO] año en una escuela técnica de la provincia de Buenos Aires.
Estoy dando [TEMA]. Necesito:
1. Una consigna de trabajo práctico para hacer en grupos en 2 clases, que obligue
   a los alumnos a aplicar el tema a algo de su vida o de la escuela
   (para que no se pueda resolver solo con IA).
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

Claude lo arma en el **panel de la derecha** (un *Artifact*). Se puede jugar ahí mismo: **invitar a un profe a pasar y jugarlo**.

Si sobra tiempo: *"Agregale un temporizador de 20 segundos por pregunta"*, para que vean que se modifica hablando.

## 4D. Cazar una alucinación (3 min) ✂️

**Chat nuevo**:

```
¿En qué año se fundó la EEST N.° 3 de San Antonio de Padua, quién fue su primer
director y cuántos alumnos tuvo en su primera promoción?
```

Pueden pasar dos cosas, y las dos sirven:
- **Inventa datos** → *"¿De dónde sacaste eso? Dame la fuente con link."* Mostrar que no puede respaldarlo. **Lección: siempre pedir la fuente.**
- **Dice que no sabe** → *"Bien: los modelos buenos ya admiten cuando no saben. Pero no siempre: por eso hay que verificar igual."*

Variante si responde muy prudente: *"Dame tres citas textuales del Diseño Curricular de la Provincia de Buenos Aires sobre [materia], con número de página."*

## Si algo falla

| Problema | Qué hago |
|---|---|
| Internet lento o cortado | Datos del celular. Si tampoco anda: **capturas del ensayo** en el pendrive o el celular |
| Claude tarda mucho | Mientras escribe, explicar lo que se está viendo. Si pasan más de 2 minutos: cambiar a Haiku o seguir con las capturas |
| "Límite de uso alcanzado" | Pasar a las capturas. (Por eso no usar Claude Code esa mañana.) |
| La respuesta sale mal | **¡Mejor!** Es el ejemplo perfecto de que hay que revisar. Corregirla en vivo |
| Letra chica en el proyector | `Ctrl + +` |

## Al terminar (importante)
1. En claude.ai: tu nombre (abajo a la izquierda) → **Cerrar sesión**.
2. Cerrar el navegador.
3. Si el navegador había guardado algo: menú **⋮ → Configuración → Privacidad → Borrar datos de navegación** → "Contraseñas" y "Cookies" → Borrar.
