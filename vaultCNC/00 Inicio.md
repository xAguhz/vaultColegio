---
tipo: índice
materia: Diseño y Procesamiento Mecánico (CNC)
curso: 6° 1° Electromecánica — EEST N°3, Padua
ciclo: 2025
actualizado: 2026-11-24
tags: [moc, cnc, torno]
---

# vaultCNC: programación de torno CNC

Vault de estudio de **Diseño y Procesamiento Mecánico (CNC)** de la EEST N°3. Se armó a partir de la carpeta digital de la materia, los dos trabajos prácticos (Peón y Alfil) y los proyectos originales de **WinUnisoft**.

> [!info] La idea de la materia
> Una pieza de torno se hace en cuatro pasos que siempre se repiten: **plano → hoja de proceso → programa → simulación**. Todo lo que hay acá sirve para que cada paso salga bien a la primera.

## Mapa de notas

### Cómo se trabaja
- [[01 Método de trabajo]]: el método del curso paso a paso y la estructura del informe.
- [[02 Glosario]]: vocabulario (G96, Vc, inserto, tronzado, cero pieza...).
- [[Bitácora]]: qué se hizo y qué decisiones se tomaron.

### Máquina y software
- [[Torno y control]]: Fanuc, Apolo, simulador Wansoft y WinUnisoft.
- [[Formato de archivos WinUnisoft]]: los 4 archivos de un proyecto y sus claves.

### Programación
- [[Códigos G]] y [[Códigos M]]
- [[Estructura de un programa]]
- [[Ciclos G90 G94 G71 G72 G70 G74]]
- [[Fórmulas de corte]]
- [[Herramientas y plaquitas]]

### Trabajos prácticos
- [[TP Peón]]
- [[TP Alfil]]
- [[Rótulo EEST3]]: el cajetín de los planos y de las hojas de proceso.

## Cómo se hace un TP nuevo
1. **JSON de la pieza**: se escribe `Piezas/<nombre>.json` con el perfil (ver `Piezas/FORMATO.md`). Un solo archivo alimenta todo lo demás.
2. **Plano**: con `plano_freecad.py` se genera el PDF de FreeCAD con el [[Rótulo EEST3|rótulo]].
3. **Proyecto WinUnisoft**: con `generar_winunisoft.py` se escriben el `.prj`, el `.nc`, el `.txt` y el `.wmf` (ver [[Formato de archivos WinUnisoft]]).
4. **Verificación**: con `simular_nc.py` se simula el programa y se controla que el perfil salga igual al del JSON.
5. **Informe**: carátula, hoja de proceso, programa, aclaraciones y hojas por herramienta (ver [[01 Método de trabajo]]).

## Herramientas
Están en la carpeta `herramientas/` del vault.

| Herramienta | Para qué sirve | Estado |
|---|---|---|
| `herramientas/simular_nc.py` | Simula un programa `.nc` y comprueba el perfil resultante | Disponible |
| `herramientas/plano.sh` → `plano_freecad.py` | Genera el plano (FreeCAD 1.1, 3 vistas, cotas Ø/R/largos, rótulo EEST3) en `.FCStd` + PDF a partir del JSON. Uso: `herramientas/plano.sh Piezas/peon.json Planos/PEON` | Disponible |
| `herramientas/generar_winunisoft.py` | Escribe los 4 archivos del proyecto WinUnisoft (`.prj .nc .txt .wmf`, CRLF) y un dibujo de la trayectoria. Uso: `python3 herramientas/generar_winunisoft.py Piezas/peon.json WinUnisoft/PEON` | Disponible |

> [!warning] Antes de entregar
> El generador avisa de posibles choques del portaherramientas de T1010 en las gargantas (su modelo del porta es aproximado). Abrí el proyecto en WinUnisoft y mirá la simulación de T1010 antes de entregar.

Los `Piezas/*.json` y los planos PDF llevan los datos del rótulo (nombres), así que quedan solo en la compu: no se suben al repo (ver `.gitignore`).

## Lo que todavía no sabemos
- El **modelo real del torno** de la escuela no figura en ninguna fuente.
- El material de las piezas aparece como **SAE 4140** y también como "Acero Inoxidable (M)": ver [[Bitácora]].
