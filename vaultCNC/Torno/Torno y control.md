---
tipo: máquina
tags: [torno, fanuc, simulador]
---

# Torno y control

## Qué máquina se usa

| Dato | Valor | Fuente |
|---|---|---|
| Control | **Fanuc 16i-TA** | Proyectos WinUnisoft y hojas de proceso |
| Máquina en WinUnisoft | `Apolo.mch` (tipo Torno) | `.prj` |
| Control en el simulador de clase | **FANUC 0iT** | Carpeta digital |
| Simulador de clase | **Wansoft** | Carpeta digital |
| Simulador de los proyectos | **WinUnisoft MultiCNC** | `.prj` |

> [!warning] Qué no sabemos
> El **modelo real del torno de la escuela** no figura en ninguna fuente. Las hojas de proceso dicen "Fanuc 16iTA" y la carpeta digital usa "FANUC 0iT" en el simulador. Tampoco sabemos si son la misma cosa con distinto nombre. Hay que preguntarle al profe.

## Máquina Apolo en WinUnisoft

| Parámetro | Valor |
|---|---|
| Límites de máquina (X mín, Y mín, Z mín, X máx, Y máx, Z máx) | -8,5 / 0 / 0 / 85,5 / 0 / 287 |
| Cero máquina | 85,5 / 0 / 287 |
| Posición de cambio de herramienta | X 70, Y 0, Z 230 |
| Tiempo de cambio | 5 s |
| Velocidad máxima del husillo | 4000 RPM |
| Velocidad mínima | 10 RPM |
| Avance máximo | 1500 |
| Avance en G00 | 1500 |
| Unidad | 0 (milímetros) |

Esto sale del `.prj`; las claves se explican en [[Formato de archivos WinUnisoft]].

> [!note] Límite de RPM
> En la carpeta digital se usa `G50 S4500` como límite de ejemplo. El simulador WinUnisoft limita a 4000. Con G96, cerca del centro de la pieza las RPM suben mucho: por eso se limita (ver [[Fórmulas de corte]]).

## Simulador Wansoft (el de clase)

Pasos de arranque que da la carpeta digital:

1. Ejecutar el `.exe` del simulador.
2. Elegir el control **FANUC 0iT** y presionar **RUN**.
3. Elegir el panel de la máquina.
4. Encender la máquina (botones de STANDBY en secuencia).
5. **Soltar el pulsador rojo de emergencia** (el hongo), girándolo.
6. Presionar **ZERO RETURN** para llevar la herramienta al punto cero.
7. Menú "Operación de la máquina" > "Puerta de la máquina" en ON para trabajar sin la puerta.
8. Setear las herramientas en el "Manejador de herramienta": doble clic en la herramienta N, elegir la herramienta (naranja) y el inserto (azul).
9. Entrar a "Configuración de parámetros".

> [!warning] Fuente incompleta
> La lectura de la carpeta digital cortó en la página 80 de unas 85-90. Faltan las páginas finales del instructivo (seteo de herramienta y parámetros).

## Torreta

Los proyectos cargan 11 herramientas (T1 a T11) más una T0 "sin correctores". La lista completa está en [[Herramientas y plaquitas]].

Ver también: [[Estructura de un programa]], [[Bitácora]].
