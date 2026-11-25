#!/bin/bash
# Abre WinUnisoft multiCNC con Wine (prefijo propio ~/.wine-winunisoft).
# Uso: winunisoft.sh            -> abre el programa
#      winunisoft.sh <carpeta>  -> antes copia los proyectos (.prj .nc .txt .wmf) de esa carpeta a Proyectos/
set -e
export WINEPREFIX="$HOME/.wine-winunisoft"
W="$WINEPREFIX/drive_c/Program Files (x86)/WinUnisoft multicnc"
[ -f "$W/wus.exe" ] || { echo "WinUnisoft no está instalado en $WINEPREFIX"; exit 1; }
if [ -n "$1" ]; then
  mkdir -p "$W/Proyectos/$(basename "$1")"
  cp -v "$1"/*.{prj,nc,txt,wmf} "$W/Proyectos/$(basename "$1")/"
fi
cd "$W" && exec wine wus.exe
