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

Ver [[Formato de archivos WinUnisoft]].
