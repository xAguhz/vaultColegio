#!/bin/bash
# Abre WinUnisoft en una pantalla virtual oculta (Xvfb :99) para simular sin tocar el escritorio.
# Después: DISPLAY=:99 python3 wusctl.py simular "<subcarpeta>" "<archivo.prj>"
# Requiere: sudo apt install xvfb
# Ojo: WinUnisoft admite una sola copia abierta; si está abierto en la pantalla normal, cerralo antes.
#
# Sin gestor de ventanas, Wine no acepta los clics. Por eso corre dentro del "escritorio virtual"
# de Wine (explorer /desktop): ahí WinUnisoft se maximiza solo y wusctl lo maneja con XTest.
set -e
PANT=:99
AQUI="$(cd "$(dirname "$0")" && pwd)"
export WINEPREFIX="$HOME/.wine-winunisoft"
EXE='C:\Program Files (x86)\WinUnisoft multicnc\wus.exe'

if ! pgrep -f "Xvfb $PANT" >/dev/null; then
  setsid nohup Xvfb $PANT -screen 0 1920x1080x24 -nolisten tcp >/dev/null 2>&1 &
  sleep 2
fi
export DISPLAY=$PANT
if ! pgrep -f "wus.exe" >/dev/null; then
  setsid nohup wine explorer "/desktop=wus,1920x1080" "$EXE" >/dev/null 2>&1 &
  sleep 25
  # cierra la ventana de bienvenida (botón Cancelar)
  python3 - "$AQUI" <<'EOF'
import sys
sys.path.insert(0, sys.argv[1]); sys.argv = ["x"]
import wusctl as w
w.clic(1102, 535)
EOF
fi
echo "WinUnisoft abierto en la pantalla oculta $PANT"
