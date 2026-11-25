---
tags: [cnc, winunisoft, linux, wine]
fecha: 2026-11-24
---
# WinUnisoft en Linux (Wine)

WinUnisoft multiCNC 4.2 (Alecop) es un programa de Windows. En esta compu corre con **Wine 10**, en un prefijo propio, `~/.wine-winunisoft`.

## Instalación (una sola vez)
Wine 10 trabaja en modo *wow64*: los prefijos son de 64 bits y corren igual los programas de 32 bits. Con `WINEARCH=win32` da error.
```bash
WINEPREFIX="$HOME/.wine-winunisoft" wine "<ruta>/Winunisoft multiCNC 4.2 Setup.exe"
```
- Queda instalado en `C:\Program Files (x86)\WinUnisoft multicnc\`, la misma ruta que usan los `.prj`. La máquina `Lib\Apolo.mch` está incluida.
- Los mensajes `err:ole…`, `err:setupapi…` y "experimental wow64 mode" son normales en Wine.
- **Licencia:** WinUnisoft usa una protección propia (`Proteccion.exe`, llave HASP). Se activa con la licencia de la escuela. No se usan cracks.

## Abrir
- Desde el menú de aplicaciones: **WinUnisoft multiCNC** (`~/.local/share/applications/winunisoft.desktop`).
- Desde la terminal, copiando antes los proyectos de una carpeta:
```bash
vaultCNC/herramientas/winunisoft.sh "vaultCNC/WinUnisoft/TP71 PEON"
```
Los proyectos de los TP 7°1 ya están copiados en `Proyectos\TP 7-1\` dentro de la instalación.

## Qué verificar al abrir un proyecto generado
- Que el `.prj` cargue la máquina Apolo (Fanuc 16i-TA) y el bruto Ø30 × 130.
- La herramienta neutra **T9 (DVVNN)**: que la plaquita se dibuje apuntando hacia −X y que no choque en las gargantas. Su línea en `[TOOLS]` se escribió por analogía con las otras herramientas.
- Correr la simulación completa y revisar que no aparezcan choques del portaherramientas.

## Manejarlo desde Claude: `herramientas/wusctl.py`
Controlador hecho con Python y ctypes (libX11), sin instalar nada:
```bash
python3 vaultCNC/herramientas/wusctl.py ventanas                       # ventanas abiertas
python3 vaultCNC/herramientas/wusctl.py captura salida.png              # captura de WinUnisoft
python3 vaultCNC/herramientas/wusctl.py clic X Y [--ventana "Abrir..."]
python3 vaultCNC/herramientas/wusctl.py simular "TP 7-1" "alfil tp.prj"  # abre, simula y muestra el .ERR
```
Lo que costó y conviene saber:
- **XTest no anda.** GNOME en Wayland no deja que XWayland mueva el puntero sin una sesión de escritorio remoto autorizada. Los clics y las teclas se mandan con **XSendEvent** directo a la ventana de Wine, que sí los acepta.
- **Diálogos.** Dentro del diálogo "Abrir..." los clics lo cierran, así que se maneja solo con teclado: carpeta + Enter, archivo + Enter.
- **Mayúsculas y barra invertida.** Con eventos sintéticos y teclado en español no salen, pero Windows no distingue mayúsculas en las rutas.
- **Capturas.** Se saca la ventana, no la pantalla: XGetImage sobre la raíz falla en XWayland.
- **Errores.** WinUnisoft escribe los resultados en archivos de texto junto al proyecto: `<proyecto>.ERR` (colisiones, con línea y herramienta) y `<proyecto>.LOG`. En pantalla, el listado sale con cuadraditos porque a Wine le falta una fuente. El `.LOG` queda con `Ttime=0.00` y no avisa cuándo termina la simulación. Por eso `simular` mira la pantalla: mientras simula, el botón **Abortar** está activo; cuando termina, se apaga. En "Control parada" tiene que estar destildado **Cambio Hta.**: si no, la simulación se pausa en cada cambio de herramienta.

## Simular en segundo plano (pantalla oculta)
Para que WinUnisoft no aparezca en el escritorio, se lo corre en una pantalla virtual **Xvfb** (hay que instalarla una vez: `sudo apt install xvfb`):
```bash
vaultCNC/herramientas/winunisoft_oculto.sh                                   # Xvfb :99 + WinUnisoft
DISPLAY=:99 python3 vaultCNC/herramientas/wusctl.py simular "TP 7-1" "Peon TP.prj"
DISPLAY=:99 python3 vaultCNC/herramientas/wusctl.py captura fin.png --ventana "Wine Desktop"
```
- WinUnisoft admite **una sola copia abierta**. Si está abierto en la pantalla normal, hay que cerrarlo antes.
- **En Xvfb no hay gestor de ventanas y Wine ignora los clics.** Por eso corre dentro del *escritorio virtual* de Wine (`wine explorer /desktop=wus,1920x1080 …`), donde se maximiza solo.
- **Ahí sí funciona XTest**, sin tocar el escritorio del usuario. `wusctl` detecta el escritorio virtual y usa coordenadas de pantalla: la barra de título de Wine corre todo (+4, +34). Las teclas con Shift y la barra invertida también salen, así que la ruta se escribe completa en el diálogo Abrir.
- **Es mucho más rápido:** una pieza tarda unos 12 s, contra varios minutos en pantalla.

## Lo que encontró la simulación real (2026-11-24)
| Problema en WinUnisoft | Causa | Arreglo en `generar_winunisoft.py` |
|---|---|---|
| Colisión T1 en la línea 7 | Refrentado hacia el centro (G00 Z0 y luego G01 X0) | Refrentar desde el centro hacia afuera, como en los programas del curso |
| Colisión T1 en la línea 75 | Rápidos G00 que bajan en X con Z<0 y rozan material | Bajar con avance (G01) cuando ya está dentro de la pieza |
| Corona de la torre en cono | El porta neutro (inserto de 35°, flancos a 17,5°) no puede seguir caras planas ni paredes de más de ~62° | Esas paredes se sacan de la T0909: las de frente las termina la T0303 sin sobremetal; la cara en Z0 ya la refrentó la T0101 |
| `_Orient.` de la T9 | Regla de WinUnisoft: `Orient. = 180 − (_Orient. + Alpha)` | Para DVVNN: `Orient.` = `_Orient.` = 72,5 |

Resultado: **Peón, Alfil y Torre se simulan sin colisiones ni errores** y la forma final coincide con el plano. El Alfil original del alumno también da 0 colisiones (se usó como referencia).

Ver [[Formato de archivos WinUnisoft]].
