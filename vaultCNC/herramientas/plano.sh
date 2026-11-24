#!/bin/bash
# Uso: plano.sh <pieza.json> <carpeta_salida>
# Genera <NOMBRE>.FCStd y "<NOMBRE> plano.pdf" con FreeCAD (flatpak) en modo offscreen.
set -e
if [ $# -lt 2 ]; then echo "Uso: $0 <pieza.json> <carpeta_salida>"; exit 2; fi
AQUI="$(cd "$(dirname "$0")" && pwd)"
JSON="$(realpath "$1")"
mkdir -p "$2"
OUT="$(realpath "$2")"
# FreeCAD (GUI) abriria el .json como archivo si lo pasamos por argumento: se pasan por entorno
QT_QPA_PLATFORM=offscreen flatpak run --env=PLANO_JSON="$JSON" --env=PLANO_OUT="$OUT" org.freecad.FreeCAD "$AQUI/plano_freecad.py"
