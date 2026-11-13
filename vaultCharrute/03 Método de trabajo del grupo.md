---
tipo: guía
tags: [método, organización, exposición]
---

# Método de trabajo del grupo

Esta es la forma en que el grupo resuelve los TP de Charrute. Se fue armando en el [[TP4 Cañerías y válvulas|TP4]] y el [[TP7 Bombas industriales|TP7]], y se usó completa en el [[TP8 Compresores de aire|TP8]]. Sirve como receta para el [[TP9 Calderas industriales|TP9]] y los siguientes.

## 1. Repartir por tramos del sistema, no por preguntas sueltas
- El grupo se divide en **tres parejas**. Cada pareja toma **un tramo del sistema** que estudia el TP.
- **Cada pregunta y cada parte de la investigación se asigna al tramo donde se origina el problema** que plantea. Así las preguntas del mismo tema quedan en las mismas manos.
- Cada pareja estudia a fondo su parte y puede defenderla sola en el oral.
- La **pareja 1 coordina**: abre y cierra la exposición y une los textos en el informe.
- Se busca que la carga quede pareja: unas 5 o 6 preguntas por pareja.

| TP | Pareja 1 (coordina) | Pareja 2 | Pareja 3 |
|---|---|---|---|
| TP7 Bombas | Energía, cebado y NPSH | Tipos de bomba, sellos y seguridad | Curvas, BEP y diagnóstico |
| TP8 Compresores | **Producción**: tecnologías, etapas y temperatura | **Tratamiento**: agua, punto de rocío, secadores y filtros | **Distribución y control**: depósito, control, eficiencia, fugas y diagnóstico |
| TP9 Calderas (propuesta) | Tipos de caldera y combustión | Agua de alimentación, incrustaciones y purga | Controles, seguridad y caso integrador |

## 2. Reglas de redacción
- Responder **aplicado al caso** de la consigna. El profe no acepta definiciones copiadas.
- **Nunca** contestar solo "cambiar el equipo", "hacer mantenimiento" o "limpiar": siempre un **diagnóstico ordenado** (de lo externo y barato a lo interno).
- Usar el vocabulario de la materia: cañería o línea, válvula de aislamiento o regulación, variable de proceso.
- **Revisión cruzada:** la pareja 1 revisa a la 2, la 2 a la 3 y la 3 a la 1.

## 3. Investigación con fuentes reales
- Usar al menos una fuente de **fabricante** (ficha técnica oficial, por ejemplo una ficha CAGI) y otra de bibliografía, norma u organismo técnico (ASME, DOE, ISO, Spirax Sarco).
- Los números se copian **de la fuente**, con modelo, fecha y condiciones de medición.
- Comparar datos solo si están medidos en las mismas condiciones. Si no lo están, se aclara (como las fichas a 100 y 125 psig del TP8).

## 4. Exposición (unos 10 minutos)
- **Una sola idea fuerza** que defiende todo el grupo, al principio y al final.
- **Libreto por minutos:** cada pareja tiene unos 3 minutos; la pareja 1 abre y cierra.
- **Preguntas trampa preparadas:** 4 o 5 preguntas que el profe podría hacer, con su respuesta corta.
- No leer el informe: la presentación es **visual** (ilustraciones, flujos, números grandes) y el detalle queda en el documento.

## 5. Qué se entrega
1. **Google Docs** con:
   - carátula: escuela, materia, TP N°, título, profesor Carlos Charrute, curso 7° 1°, integrantes y fecha;
   - organización del grupo;
   - respuestas;
   - investigación;
   - conclusión con la idea fuerza;
   - guía de exposición;
   - bibliografía.
2. **El mismo documento en PDF.**
3. **Google Slides** ilustrativo (unas 13 diapositivas):
   - carátula con los mismos datos;
   - una idea por diapositiva, con el título contando la conclusión;
   - ilustraciones de Gemini y poco texto;
   - cierre con la idea fuerza.

## Integrantes
Son 6 integrantes, en tres parejas fijas. Los nombres van en la carátula de cada entrega; acá no se publican porque la página es pública.

## Herramientas
- `herramientas/html2docx.py`: convierte el informe escrito en HTML en un `.docx`. Drive lo convierte en Google Docs respetando el salto de página después de la carátula y el número de página. Al importar HTML directo, Drive ignora los saltos de página.
- `herramientas/slides_gen.py`: genera los pedidos para armar la presentación en Google Slides (fondos, tarjetas, flechas e imágenes).
  - Las imágenes tienen que estar en una URL pública. Se usan las de `Adjuntos/Gemini/` publicadas en la página de GitHub.
- `herramientas/gemini_img.sh`: genera una ilustración con Gemini y la agrega a la [[Galería Gemini]].

## Relacionado
[[00 Inicio]] · [[01 Guía de estudio]]
