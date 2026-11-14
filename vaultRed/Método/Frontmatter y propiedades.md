---
tipo: método
tags: [método, metadatos]
aliases: [propiedades, YAML]
actualizado: 2026-11-14
---
# Frontmatter y propiedades

Son unas líneas al principio de la nota, entre `---`, con datos **sobre** la nota:

```yaml
---
tipo: concepto
tags: [sistemas-mecánicos, aire-comprimido]
fuente: "Compresores de aire_26.docx"
actualizado: 2026-11-13
---
```

## Para qué sirven
- **Filtrar y buscar**: todas las notas `tipo: video`, o todas con el tag `#plc`.
- **Que otra IA o un programa entienda la nota** sin leerla entera: `vaultMHS` usa `minutos` (en qué parte del video está el tema) y `estado: segun-el-video` (sin verificar). → [[generar_indice (script)|generar_indice.py]]
- **La web**: la fecha de cada nota sale del historial de Git, no de la propiedad. → [[preparar (script)|preparar.py]]

## Propiedades que más se usan
| Propiedad | Para qué |
|---|---|
| `tipo` | índice, concepto, equipo, tp, video, guía… |
| `tags` | temas, para filtrar |
| `fuente` | de dónde sale lo que dice la nota |
| `actualizado` | última revisión a mano |
| `aliases` | otros nombres con los que se busca la nota |
