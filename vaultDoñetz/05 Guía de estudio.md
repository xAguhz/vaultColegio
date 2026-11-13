---
tipo: guía
tags: [estudio, autoevaluación]
---

# Guía de estudio y autoevaluación

Preguntas armadas a partir de lo que el profe remarca en los videos. Las respuestas están en las notas enlazadas (están plegadas: hacé clic para abrirlas).

## Neumática
1. ¿Qué significa `1S2`? ¿Y `0S1`? ¿Por qué el `0`?
   > [!success]- Respuesta
   > Se lee de atrás para adelante: segundo switch del cilindro 1, y primer switch general para toda la máquina. El `0` = general. → [[Nomenclatura ISO 1219]]
2. En una 5/2, ¿qué hace la entrada 14? ¿Y la 12?
   > [!success]- Respuesta
   > 14 conecta 1→4 (avance, si 4 va atrás del émbolo); 12 conecta 1→2 (retroceso). → [[Válvulas distribuidoras]]
3. ¿Qué es una fase? ¿Mide tiempo?
   > [!success]- Respuesta
   > Es un movimiento completo, de principio a fin. No mide tiempo. → [[Diagrama espacio-fase]]
4. ¿Qué indica `3 ≡ 1`? ¿Qué es la señal de nuevo arranque?
   > [!success]- Respuesta
   > Ciclo continuo. La señal de nuevo arranque es el último final de carrera que se pisa en el ciclo, en AND con la marcha. → [[Ciclo único y ciclo continuo]]
5. Ordená los niveles del plano neumático de abajo hacia arriba.
   > [!success]- Respuesta
   > Alimentación → emisores → procesamiento → válvulas de mando → actuadores. → [[Estructura del plano neumático]]
6. ¿De qué tres elementos está hecho un temporizador neumático y por qué el aire va primero al tanque?
   > [!success]- Respuesta
   > Estranguladora con antirretorno + acumulador + 3/2 NC pilotada. El tanque vacío opone menos resistencia que el resorte de la 3/2. → [[Temporizador neumático]]

## Electroneumática
7. ¿Por qué las bobinas se conectan en paralelo?
   > [!success]- Respuesta
   > En serie se repartirían los 24 V. → [[Electroneumática]]
8. ¿Cómo se numera un contacto NA, uno NC y uno conmutador?
   > [!success]- Respuesta
   > NA 3-4, NC 1-2, conmutador 1-2-4; el primer dígito es el número de contacto. → [[Contactos eléctricos]]
9. ¿Por qué una monoestable necesita autorretención y una biestable no?
   > [!success]- Respuesta
   > La monoestable vuelve por resorte si se corta la corriente; la biestable memoriza mecánicamente. → [[Electroválvulas monoestables y biestables]]
10. ¿Qué es la superposición de señales y cómo se detecta sin armar el circuito?
    > [!success]- Respuesta
    > Los dos cabezales alimentados a la vez. Se detecta marcando en el diagrama cuánto tiempo queda pisado cada rodillo. → [[Superposición de señales]]
11. Técnica Chopp: ¿con qué se alimenta el cabezal nuevo?
    > [!success]- Respuesta
    > Con un NC del mismo relé que alimentaba al cabezal original. → [[Técnica Chopp]]
12. ¿Por qué el pulsador de parada es NC? ¿Qué contacto va en Ladder?
    > [!success]- Respuesta
    > Por seguridad: si se corta el cable, para. En Ladder, contacto NC para el reset (o NA en serie con la autorretención). → [[Lógica positiva y negativa]]

## Métodos
13. Cascada: ¿dónde va el cambio de línea? ¿Cuántos relés se usan?
    > [!success]- Respuesta
    > Justo antes de que se repita un actuador que ya se movió en esa línea. Relés = líneas − 1. → [[Método cascada]]
14. Cascada: ¿cómo se conecta una bobina que no está en la primera fase de su línea?
    > [!success]- Respuesta
    > A la línea, a través de un NA del emisor que inicia esa fase. → [[Método cascada]]
15. ¿Por qué cascada no sirve si un actuador repite movimiento?
    > [!success]- Respuesta
    > Habría que alimentar la misma bobina en dos líneas, y se mezclan. → [[Método paso a paso]]
16. Paso a paso: ¿qué contacto habilita, cuál desconecta y dónde va la autorretención?
    > [!success]- Respuesta
    > Habilita el NA del relé anterior, desconecta el NC del relé siguiente, y la autorretención va entre los dos. → [[Método paso a paso]]
17. Paso a paso: ¿cómo se resuelve el primer arranque?
    > [!success]- Respuesta
    > Con un NA del pulsador de marcha en paralelo con la autorretención del último paso. → [[Método paso a paso]]
18. Memorias: ¿cuándo se usa un NC del auxiliar y cuándo un NA?
    > [!success]- Respuesta
    > NC para el rodillo que tiene que actuar desde el arranque; NA para el que tiene que estar bloqueado al inicio. → [[Método de memorias]]

## PLC
19. ¿Por qué las salidas se llaman Q y no O?
    > [!success]- Respuesta
    > La O se confunde con el cero. → [[PLC]]
20. ¿Cómo se hace un NOT en Ladder con un pulsador físico NA?
    > [!success]- Respuesta
    > Con un contacto NC en Ladder. → [[Lenguaje Ladder]]
21. Paso a paso en Ladder: ¿por qué `M1` se trabaja con lógica negativa?
    > [!success]- Respuesta
    > Al arrancar, todas las memorias valen 0; con un NC de `M1` el paso 1 queda habilitado. → [[Paso a paso en Ladder]]
22. ¿Qué es la función A del temporizador de Zelio?
    > [!success]- Respuesta
    > Trabajo con comando mantenido, es decir, retardo a la conexión. → [[Temporizadores en PLC]]

## Digital
23. Escribí la suma de minitérminos y el producto de maxitérminos de la XOR.
    > [!success]- Respuesta
    > `A'B + AB'` y `(A + B)(A' + B')`. → [[Minitérminos]] · [[Maxitérminos]]

## Errores comunes que el profe marca
- No dibujar las **condiciones iniciales** (rodillo pisado, relé energizado): después falla la lógica.
- Completar el diagrama **sin mirar cómo está conectada la válvula** (alimentar `1Y1` puede hacer *retroceder* el actuador).
- Olvidarse del **NC que desconecta** una autorretención.
- Usar el **mismo contacto** para dos cosas: hay que usar contactos distintos para que no se mezclen las líneas.
- Poner un NA en Ladder para el pulsador de parada NC: el reset queda siempre activo.
