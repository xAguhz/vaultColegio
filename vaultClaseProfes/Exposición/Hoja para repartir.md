---
tipo: material
tags: [exposición, imprimir]
---

# Hoja para repartir

Una carilla A4 que resume la charla, con el QR de la guía. Está en `Exposición/Hoja para imprimir.html`, junto a esta nota.

![[qr_guia.png|220]]

## Cómo imprimirla
1. Abrí `Hoja para imprimir.html` con Chrome o Edge (doble clic).
2. `Ctrl + P`.
3. Tamaño **A4**, márgenes **Predeterminados** y activá **Gráficos de fondo** (si no, salen sin los recuadros de color).
4. **Imprimir**, o **Guardar como PDF** para llevarla en el pendrive.

> [!tip] Para ahorrar tinta
> Se puede imprimir en blanco y negro: los colores son de fondo suave y se lee igual.

## Qué dice
1. **Para empezar hoy mismo**: entrar a claude.ai y pedir como a un practicante.
2. **Las cinco partes de un buen pedido**: contexto, tarea, material, formato y criterios. Ver [[1.3 Cómo pedir bien]].
3. **Tres pedidos para copiar**: rúbrica, variantes de un ejercicio, "haceme las preguntas que necesites". Ver [[1.4 Recetas para docentes]].
4. **Tres reglas**: nada de datos de alumnos, verificar lo duro y "vos firmás". Ver [[0.4 Lo que la IA hace bien y lo que hace mal]].
5. **Consignas que obligan a pensar**: ver [[04 Cómo usamos la IA los alumnos]].
6. **Los niveles de la guía.**

El QR lleva directo al Inicio: `https://xaguhz.github.io/vaultColegio/vaultClaseProfes/00-Inicio`. Si cambia la dirección, se regenera con `herramientas/qr_v4m.py`. El último argumento es el nivel de corrección: `L` admite hasta 78 letras y `M`, más resistente a manchas, hasta 62.

```bash
python3 herramientas/qr_v4m.py "https://xaguhz.github.io/vaultColegio/vaultClaseProfes/00-Inicio" Adjuntos/qr_guia.png 24 "#1B2A2F" "#F6F1E6" L
```
