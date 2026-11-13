---
tipo: tp
materia: Sistemas Mecánicos
profesor: Charrute
numero: 9
tema: Calderas industriales y sistemas de generación de vapor
consigna: 2026-11-06
entrega: pendiente
modalidad: grupal (investigación + caso integrador)
tags: [tp, calderas, vapor, combustión, tratamiento-de-agua, seguridad]
---

# TP9 · Calderas industriales y generación de vapor

> [!info] Fuera de la numeración habitual
> Los TP suelen llegar hasta el 8. Este trabajo de investigación sobre calderas lo compartió el profe el **06/11/2026** y cierra el recorrido de equipos (tanque → bomba → intercambiador → compresor → **caldera**). Al 13/11/2026 no hay una entrega en Drive.

Anterior: [[TP8 Compresores de aire]] · Siguiente: —

## Consigna (resumida)
"No hace falta un trabajo excesivamente extenso, sino comprensión técnica, buenas fuentes y criterio."

1. **Pirotubular frente a acuotubular:** disposición del agua y los gases, presión y capacidad, respuesta a la demanda, mantenimiento y aplicaciones. *¿Por qué una conviene en un caso y la otra en otro?*
2. **Una caldera real** (Bosch, Cleaver-Brooks, Miura, Fulton, Clayton, B&W…) con su ficha oficial: modelo, tipo, producción de vapor, presión, combustible, potencia, eficiencia, control y seguridad. Explicar **3 datos** de la ficha.
3. **Esquema del sistema completo:**
   - lado agua y vapor: reposición + retorno de condensado → tratamiento → tanque de alimentación → bomba → caldera → vapor → proceso → condensado → retorno;
   - lado combustión: aire + combustible → quemador → combustión → gases → chimenea;
   - marcar dónde se miden **presión, temperatura, nivel y caudal**.
4. **Combustión y eficiencia:** quemador, relación aire/combustible, **exceso de aire**, gases y **temperatura de chimenea**. *¿Por qué produce vapor pero consume más?* Al menos 3 causas.
5. **Agua de alimentación:** tratamiento, dureza, **incrustaciones**, corrosión, retorno de condensado y **purga**. Efecto de los depósitos sobre el consumo y la seguridad. Por qué **purgar de más** tampoco sirve.
6. **Controles y seguridad:**
   - elementos: control de nivel, **corte por bajo nivel**, control de presión, **válvula de seguridad**, **detección de llama**;
   - *control normal ≠ dispositivo de seguridad*, con un ejemplo.
7. **Caso integrador:**
   - síntomas: más combustible, gases de chimenea más calientes, **menos retorno de condensado**, **más purga**, **incrustaciones**, aunque el vapor todavía alcanza;
   - el jefe de mantenimiento quiere **cambiar el quemador**;
   - hay que analizar y proponer dos medidas justificadas. No valen respuestas como "hacer mantenimiento", "limpiar" o "cambiar el quemador".

## Ideas para resolverlo (guía de estudio)
> [!note] Guía propia, no es la entrega
> Armada a partir de los apuntes anteriores de la materia (intercambiadores, bombas, recipientes a presión). Hay que completarla con las fuentes que pide el profe (ASME, U.S. DOE, Spirax Sarco, B&W y fabricantes).

### Pirotubular frente a acuotubular
| | Pirotubular | Acuotubular |
|---|---|---|
| Qué va por los tubos | **Gases calientes**, rodeados de agua | **Agua y vapor**, rodeados de gases |
| Presión y capacidad | Baja a media, capacidades chicas o medianas | Alta presión y gran capacidad |
| Respuesta a la demanda | Gran volumen de agua: inercia térmica, aguanta picos pero arranca lento | Poco volumen de agua: responde rápido |
| Mantenimiento | Simple: se limpian los tubos de humo | Más complejo y exigente con la calidad del agua |
| Uso típico | Industria alimentaria, lavaderos, hospitales, calefacción | Centrales térmicas, petroquímica, grandes procesos |

### Variables en el esquema
- **Nivel** en el domo o cuerpo: si baja, los tubos quedan sin agua, se sobrecalientan y hay riesgo de explosión. Lleva control y **corte por bajo nivel**.
- **Presión** del vapor: el control de presión gobierna el quemador; la **válvula de seguridad** protege ante una sobrepresión.
- **Temperatura** de los gases de chimenea (eficiencia), del agua de alimentación y del vapor.
- **Caudal** de vapor producido, de agua de alimentación y de purga.

### Caso integrador: cómo pensarlo
- **El quemador no es lo primero que hay que sospechar.** Los gases salen **más calientes**, eso significa que el calor **no pasa al agua**: es un **problema de transferencia** y no de combustión. Es la misma lógica del *fouling* en el [[TP6 Intercambiadores de calor|TP6]].
- **La cadena probable:**
  1. llega **menos condensado** (que es agua caliente y ya tratada);
  2. entra **más agua de reposición** fría y con dureza;
  3. hay **más sales** en la caldera, y por eso hace falta **más purga** (que tira agua caliente y tratada);
  4. se forman **incrustaciones**, que aíslan;
  5. los **gases salen más calientes** y **sube el consumo**.
- **Revisar antes de cambiar nada:**
  - análisis del agua (dureza, sólidos disueltos, conductividad);
  - funcionamiento del ablandador y la dosificación química;
  - trampas de vapor y fugas en la red de condensado;
  - temperatura de chimenea y análisis de gases (O₂ y CO, para ver el exceso de aire);
  - régimen de purga;
  - temperatura del tanque de alimentación.
- **Prioridad:** **las incrustaciones y la calidad del agua**. Además de gastar combustible, el metal de la superficie de calefacción **se sobrecalienta** y puede fallar: es un riesgo de seguridad.
- **Medidas correctivas:**
  1. Recuperar el retorno de condensado (reparar trampas y fugas) y corregir el tratamiento del agua (ablandador y química), para atacar la causa.
  2. Desincrustar con un procedimiento controlado y ajustar la purga por **conductividad** (automática), no "a ojo". Después, recién si los gases lo indican, ajustar el exceso de aire del quemador.
- **Control frente a seguridad:**
  - el **control de nivel** mantiene el nivel normal mediante la bomba de alimentación: es una función operativa;
  - el **corte por bajo nivel** es independiente y **apaga el quemador** si el control falla;
  - no se reemplazan uno al otro, igual que el manómetro y la válvula de seguridad del [[TP5 Tanques y recipientes a presión|TP5]].

## Archivos en Drive
- Consigna: `Cald ind tpinv_26.docx` (compartida el 06/11/2026)

## Ver también
[[Caldera]] · [[Intercambiador de calor]] · [[Recipiente a presión]] · [[Bomba]] · [[Variables de proceso]] · [[00 Inicio]]
