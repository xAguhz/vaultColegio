---
tipo: referencia
tags: [programacion, codigos-m]
---

# Códigos M

Los M son órdenes **auxiliares**: husillo, refrigerante, paradas y fin de programa.

| Código | Significado |
|---|---|
| **M00** | Parada de programa |
| **M01** | Parada opcional |
| **M03** | Giro del husillo (ver aviso) |
| **M04** | Giro del husillo en sentido contrario a M03 (ver aviso) |
| **M05** | Parada del husillo |
| **M08** | Activar refrigerante |
| **M09** | Desactivar refrigerante |
| **M30** | Fin de programa |
| **M98** | Llamada a subprograma |
| **M99** | Fin de subprograma |

> [!warning] Contradicción en la carpeta digital
> La tabla de la página 16 describe M03 como giro **anti-horario** y M04 como **horario**. Pero la página 4 dice "M3 horario / M4 antihorario", que es lo estándar en Fanuc. **Usá M03 = horario y M04 = antihorario.** Todos los programas de los TP usan `M3` y andan en el simulador.

La carpeta aclara que existen más códigos M y que **cambian según el fabricante**.

Los programas de los TP usan solo `M3` (en cada cambio de herramienta) y `M30` (al final). No usan M08/M09.

Ver también: [[Códigos G]], [[Estructura de un programa]].
