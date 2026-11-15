---
tags: [suzuki-swift, manual-de-taller, circuito]
tipo: circuito
circuito: "B-3"
---
# B-3 · Desempañador trasero

Volver a [[Circuitos eléctricos]] · [[9A Sistemas de cableado]]

PDF: [[Manual de taller Swift 2005-2010.pdf#page=1308|diagrama original, página 1308]] (copia local)

> [!summary] Cómo funciona
> Desempañador: un relé (comandado por el BCM y el botón) alimenta las resistencias de la luneta; se corta solo a los pocos minutos.

```mermaid
flowchart LR
  BT[Botón] --> BCM[BCM]
  BCM --> RE[Relé del desempañador]
  RE --> LU[Resistencias de la luneta]
```

**En el modelo 3D:** [desempanador](https://xaguhz.github.io/vaultColegio/vaultSuzuki/3D/visor/index.html#desempanador) · [bloque_empalmes](https://xaguhz.github.io/vaultColegio/vaultSuzuki/3D/visor/index.html#bloque_empalmes) · [porton](https://xaguhz.github.io/vaultColegio/vaultSuzuki/3D/visor/index.html#porton) · [mazo_porton](https://xaguhz.github.io/vaultColegio/vaultSuzuki/3D/visor/index.html#mazo_porton) · en el visor: **Circuitos → B-3**

**Conectores:** `G15` (J/C), `G33` (J/B), `G37` (BCM), `L05` (J/B), `L42` (Cable de la puerta trasera (a O01)), `O01` (Mazo de cables del suelo (a L42)), `O02` (Desempañador trasero (+)), `O06` (Desempañador trasero (–))

**Colores de cable:** `BLK`, `BLK/ORN`, `BLK/RED`, `BRN`
