---
tipo: concepto
area: electroneumática
tags: [electroneumática, memoria]
---

# Autorretención (memoria eléctrica)

- Un **contacto NA del mismo relé** conectado **en paralelo con los emisores de señal** que lo alimentan.
- Cuando la bobina recibe un pulso, el contacto se cierra y la mantiene energizada aunque los emisores se suelten.
- **Siempre** tiene que haber un **contacto NC que la desconecte**. El profe deja "el hueco" preparado y después busca en el diagrama quién lo corta (el emisor de la fase en que hay que desconectar).

## Cuándo hace falta
- Para alimentar una **válvula monoestable** (que si no, vuelve sola).
- En el [[Enclavamiento eléctrico]] (`K0`).
- En cada línea del [[Método cascada]] y en cada paso del [[Método paso a paso]].
- En el relé auxiliar del [[Método de memorias]].

## En PLC
Se hace igual (contacto de la misma memoria en paralelo) o directamente con [[Set y Reset]].
