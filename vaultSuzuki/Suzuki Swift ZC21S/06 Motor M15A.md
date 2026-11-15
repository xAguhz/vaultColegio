---
tags: [suzuki-swift, motor, m15a]
tipo: nota
actualizado: 2026-11-14
---
# 06 · Motor M15A

Volver a [[00 Suzuki Swift ZC21S]]

![[lamina_motor_despiece.jpg|560]]
*Motor del modelo 3D en despiece: bloque, tapa de cilindros, tapa de válvulas con bobinas, múltiples, accesorios y arranque.*

## Cómo es
- **4 cilindros en línea**, montado **transversal** adelante, con la caja automática a su izquierda.
- **Bloque y tapa de cilindros de aluminio**.
- **DOHC**: dos árboles de levas en la tapa, 4 válvulas por cilindro (16 en total) en V, sin varillas.
- **Distribución por cadena** desde el cigüeñal: no tiene cambio programado como una correa.
- **VVT** (variador de fase): la computadora adelanta o atrasa el árbol de levas de **admisión** con presión de aceite, para tener más fuerza abajo y más potencia arriba con menos consumo. Por eso el motor es muy sensible al **aceite bajo o viejo**.
- **Encendido**: dos bobinas sobre la tapa de válvulas. Cada bobina enciende un cilindro directo y otro por cable de alta (chispa perdida). Orden de encendido **1-3-4-2**; el cilindro 1 está del lado de la distribución.
- **Inyección multipunto**, un inyector por cilindro, con cuerpo de mariposa y caudalímetro de aire (MAF).

## Valores de control (manual de taller)
| Control | Valor |
| ------- | ----- |
| Compresión | estándar 1400 kPa (14 kg/cm²) · mínimo 1100 kPa · diferencia máxima entre cilindros 100 kPa |
| Presión de aceite | más de 270 kPa a 4000 rpm, con el motor caliente |
| Presión de nafta | 270–310 kPa con la bomba andando o en ralentí · más de 250 kPa 1 min después de parar |
| Luz de válvulas en frío | admisión 0,18–0,22 mm · escape 0,28–0,32 mm |
| Luz de válvulas en caliente | admisión 0,21–0,27 mm · escape 0,30–0,36 mm |
| Bujías | níquel: NGK BKR6E-11 o Denso K20PR-U11 · iridio: NGK IFR6J11 |
| Luz de bujía | 1,0–1,1 mm |
| Diámetro de cilindro | 78,000–78,014 mm (límite de desgaste 78,050 mm) |
| Tensión de la correa | 4,5–5,5 mm de flecha con 100 N (10 kg) en el medio del tramo |

## Cómo se mide la compresión (resumen)
1. Motor a temperatura, después apagado. Sacar las bujías y desconectar las bobinas y los inyectores (para que no rocíe nafta).
2. Colocar el compresómetro en la bujía del cilindro 1.
3. Acelerador a fondo y dar arranque hasta que la aguja deje de subir.
4. Repetir en los cuatro cilindros y comparar con la tabla.
5. Si un cilindro da bajo, echar un poco de aceite por el agujero y repetir: si sube, son aros; si no sube, son válvulas o junta.

## Cambio de aceite y filtro (resumen)
1. Motor tibio, auto nivelado. Sacar el tapón de llenado y el de vaciado (abajo, en el cárter).
2. Dejar escurrir y colocar el tapón de vaciado con arandela nueva a **35 N·m**.
3. Aceitar la junta del filtro nuevo, enroscarlo a mano hasta que apoye y darle **¾ de vuelta** con la llave (≈ 14 N·m).
4. Cargar aceite: ≈ **3,9 L** (3,7 de cárter + 0,2 de filtro). Arrancar 3 minutos, parar, esperar 5 y completar hasta FULL en la varilla.

Aceite: grado **API SG a SL** (o más nuevo), viscosidad según la temperatura: **5W-30** sirve para todo el año en un clima templado; 10W-30 o 10W-40 si siempre hace calor.

> [!warning] Sobre el VVT y la cadena
> Un aceite pasado de kilómetros o con el nivel bajo es la causa más común del código **P0011** (fase de levas fuera de rango) y del ruido de cadena al arrancar en frío. Primero cambiar aceite y filtro; después diagnosticar.

Ver también [[07 Fluidos y capacidades]] · [[08 Plan de mantenimiento]] · [[11 Diagnóstico de fallas]] · [[Despiece 3D interactivo]]
