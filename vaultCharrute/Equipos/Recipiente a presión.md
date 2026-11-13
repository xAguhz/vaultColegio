---
tipo: equipo
funcion: contener un fluido a presión distinta de la atmosférica
fluido: gases, vapor, líquidos presurizados
variable_principal: presión
norma: ASME BPVC Sección VIII Div. 1
tps: [TP2, TP5, TP8]
tags: [equipo, recipiente-a-presión, seguridad]
---

# Recipiente a presión

> [!summary] Función
> Contener un fluido cuya presión difiere de la exterior **lo suficiente como para que haya que diseñar contra esos esfuerzos**. Lo que lo define es la **condición de servicio**, no su forma. **No es un tanque cerrado.**

![[recipiente.png|420]]

## Por qué es peligroso: la energía almacenada
Un **gas comprimido** funciona como un resorte. Si el recipiente se rompe, el gas se expande en milisegundos: **onda de choque y esquirlas** (explosión física), **aunque el gas no sea inflamable ni tóxico**. Romper un tanque de agua abierto no tiene comparación.

## Forma y esfuerzos
- **Cilindro con cabezales**, o esfera.
- En un cilindro de pared delgada con presión interna:
  - **circunferencial (de aro):** σθ = P·D / (2t);
  - **longitudinal:** σL = P·D / (4t), que es **la mitad**;
  - por eso las **soldaduras longitudinales** son las más exigidas (más radiografía).
- **Cabezales:**
  - **hemisférico**: el óptimo, con la mitad de espesor, pero caro;
  - **elíptico 2:1**: el estándar;
  - **torisférico**: concentra tensiones en el nudillo;
  - **plano**: trabaja a flexión y necesita mucho espesor.
- El espesor **no se elige mirando el tamaño**: depende de la presión de diseño, las dimensiones, el material, la temperatura, las uniones y el código.

## Diseño
- **Presión de operación** < **presión de diseño / MAWP**: se deja un margen del 10–15 % para arranques, paradas y perturbaciones.
- **Temperatura:**
  - cambia la tensión admisible del material;
  - en frío, **fractura frágil**;
  - en caliente, ***creep***.
- **Eficiencia de junta E** (0,7–1): depende de cuánta soldadura se radiografía.
- **Material típico:** acero ASTM A516 Gr. 70.

## Protección contra sobrepresión
- **Causas:** falla del control, calentamiento, salida bloqueada, errores de operación.
- **Válvula de seguridad o alivio (PSV):**
  - **automática**, calibrada por resorte, abre de golpe a la *set pressure*;
  - **no es** una válvula de operación: una válvula manual de salida **no** la reemplaza;
  - un **manómetro** solo *indica* y depende de una persona.
- Tener la PSV **no autoriza** a operar fuera del diseño. La seguridad sale del conjunto: diseño + material + fabricación + protección + operación + inspección.

## Inspección y ensayos
- **END** en las soldaduras: radiografía (RT), ultrasonido (UT o PAUT), líquidos penetrantes (PT) y partículas magnetizables (MT).
- **Prueba hidrostática** con agua, que es incompresible y por eso segura, siguiendo un procedimiento. **No** es "ver hasta cuánto aguanta".
- Una **pérdida de espesor por corrosión sin fuga** se evalúa **antes** de seguir operando: si el espesor queda por debajo del mínimo, puede fallar de golpe.

## Ejemplo típico: pulmón de aire comprimido
Cilindro vertical con cabezales elípticos 2:1, PSV con palanca de prueba, manómetro, **purga de condensado** (automática o manual) y boca de inspección. Ver [[Sistema de aire comprimido]].

## Por qué no se puede hacer "a ojo"
1. Más espesor no corrige una geometría mala (cabezal plano o nudillo cerrado).
2. Más soldadura deja más tensiones residuales y riesgo de fisuras.
3. La chapa gruesa de un acero común se vuelve más frágil.
4. Sin MAWP calculada **no se puede calibrar la PSV**.

## Relacionado
[[Tanque]] · [[Caldera]] · [[Válvulas]] · [[Normas y códigos]] · [[TP5 Tanques y recipientes a presión]]
