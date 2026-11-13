---
tipo: ruta
tags: [moc, estudio]
---

# Ruta de aprendizaje

El canal se subió desordenado (empezó por electroneumática avanzada porque era lo que se estaba dando en clase). Este es el orden **lógico** para aprender desde cero.

## Etapa 1 — Neumática pura
1. [[2020-07-14 Mando directo neumático parte 1]]: pulsador 3/2, actuador de simple efecto, nomenclatura, primer [[Diagrama espacio-fase]].
2. [[2020-07-14 Mando directo neumático parte 2]]: dos actuadores, fases con varios movimientos, señal negada.
3. [[2020-07-13 Circuito neumático de ciclo único]]: mando indirecto con válvula 5/2, entradas 12/14, [[Estructura del plano neumático]].
4. [[2020-07-13 Circuito neumático de ciclo continuo]]: "3 ≡ 1", señal de nuevo arranque, [[Válvula lógica AND]].
5. [[2020-08-19 Ejercicio con temporizador neumático]]: [[Temporizador neumático]] y [[Válvula estranguladora]].

**Conceptos de la etapa:** [[Nomenclatura ISO 1219]] · [[Válvulas distribuidoras]] · [[Actuadores neumáticos]] · [[Unidad de mantenimiento FRL]] · [[Mando directo e indirecto]] · [[Ciclo único y ciclo continuo]]

## Etapa 2 — Electroneumática básica (método intuitivo)
6. [[2020-06-26 Clase en vivo - Mando directo electroneumático]]: por qué electroneumática, fuente de 24 V, contactos, solenoides.
7. [[2020-04-26 Electroneumática 1 actuador monoestable]]: mando indirecto con relé, [[Autorretención]].
8. [[2020-06-18 Técnica Chopp en FluidSIM]] y [[2020-04-26 Circuito Chopp]]: [[Técnica Chopp]].
9. [[2020-04-20 Repaso EN 1 - Análisis del diagrama espacio-fase]], [[2020-04-20 Repaso EN 2 - Resolución del circuito eléctrico]] y [[2020-04-20 Repaso EN 3 - Circuito completo]]: ejercicio integrador con sensores y temporizador.
10. [[2021-04-10 Lógica positiva y negativa]]: [[Relés temporizados]] con retardo a la conexión y a la desconexión.

**Conceptos de la etapa:** [[Electroneumática]] · [[Contactos eléctricos]] · [[Electroválvulas monoestables y biestables]] · [[Enclavamiento eléctrico]] · [[Circuito de sensado]] · [[Método intuitivo]] · [[Lógica positiva y negativa]]

## Etapa 3 — Electroneumática avanzada (métodos sistemáticos)
11. [[2021-05-21 Cascada con lógica cableada y superposición]]: qué es la [[Superposición de señales]] y cómo detectarla en el diagrama; el [[Método cascada]] completo. *Es la explicación más clara de cascada.*
12. [[2020-05-23 Cascada eléctrica - 2 actuadores]]: cascada con una válvula mono y otra biestable.
13. [[2020-07-06 Método Paso a Paso - 1 actuador 4 fases]]: por qué cascada no alcanza cuando se repiten movimientos; el [[Método paso a paso]].
14. [[2020-08-24 Paso a Paso con monoestables y repetición]]: paso a paso con monoestables, temporizador y rodillos repetidos.
15. [[2025-05-04 Método de memorias - relé auxiliar]]: el [[Método de memorias]] (relé auxiliar que habilita o bloquea rodillos).

**Comparar los métodos:** [[04 Comparativa de métodos]]

## Etapa 4 — PLC y Ladder
16. [[2020-09-02 PLC Ladder parte I]]: [[Lógica cableada y programada]], [[PLC]], [[Lenguaje Ladder]].
17. [[2020-09-03 PLC Ladder parte II - Zelio Soft]]: primeros programas en [[Zelio Soft 2]].
18. [[2020-09-03 Automatismo electroneumático en Ladder]]: memoria de marcha, pulsador de parada NC.
19. [[2020-10-01 Cascada en Ladder - pizarrón]] → [[2020-10-01 Cascada en Ladder - simulación]]: [[Set y Reset]], [[Temporizadores en PLC]], [[Cascada en Ladder]].
20. [[2020-10-19 Paso a Paso en Ladder - pizarrón]] → [[2020-10-20 Paso a Paso en Ladder - simulación]]: [[Paso a paso en Ladder]].

## Etapa 5 — Electrónica digital
21. [[2025-05-12 Minitérminos]] → [[2025-05-12 Maxitérminos]]: [[Funciones lógicas]], [[Minitérminos]], [[Maxitérminos]].

> [!tip] Cómo estudiar cada ejercicio
> Pausá el video después del enunciado y resolvé el diagrama espacio-fase por tu cuenta. Después compará con la nota del video y con el simulador.
