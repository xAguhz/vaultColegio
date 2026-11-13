#!/bin/bash
# gemini_img.sh - genera UNA imagen con Gemini (vía Antigravity, `agy`) y la deja en el vault.
#
# Uso:
#   herramientas/gemini_img.sh "<prompt o archivo.txt>" <nombre.png> [proporcion] [modelo]
#
#   proporcion: 1:1 (default), 3:1 (banner 150x50), 16:9 (diapositiva), 2:3 (cartel A3/A4 vertical), 3:2, 4:5, 9:16
#   modelo:     gemini-3.8-flash-medium (default) | gemini-4-argon-medium (más lento, mejor texto)
#
# Resultado:
#   - Adjuntos/Gemini/<nombre>.png
#   - una entrada nueva (imagen + prompt) al principio de Galería Gemini.md
#   - el registro del pedido en Adjuntos/Gemini/logs/<nombre>.log.jsonl
#
# Seguridad: agy corre con --dangerously-skip-permissions SOLO dentro de una carpeta temporal
# vacía, con modelo fijo y tiempo límite. Lo único que se copia afuera es el PNG pedido.
set -euo pipefail

[ $# -ge 2 ] || { sed -n '2,15p' "$0"; exit 2; }
PROMPT_ARG="$1"
OUT_NAME="$2"
RATIO="${3:-1:1}"
MODEL="${4:-gemini-3.8-flash-medium}"

[[ "$OUT_NAME" =~ ^[A-Za-z0-9_-]+\.png$ ]] || { echo "Nombre inválido (solo letras, números, - y _; termina en .png): $OUT_NAME" >&2; exit 2; }
[[ "$RATIO" =~ ^[0-9]+:[0-9]+$ ]] || { echo "Proporción inválida: $RATIO" >&2; exit 2; }
case "$MODEL" in gemini-*) ;; *) echo "Solo modelos gemini-*: $MODEL" >&2; exit 2;; esac

if [ -f "$PROMPT_ARG" ]; then PROMPT="$(cat "$PROMPT_ARG")"; else PROMPT="$PROMPT_ARG"; fi

AGY="${AGY:-$HOME/.local/bin/agy}"
VAULT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$VAULT/Adjuntos/Gemini"
LOG_DIR="$OUT_DIR/logs"
GALERIA="$VAULT/Galería Gemini.md"
mkdir -p "$OUT_DIR" "$LOG_DIR"

if [ -e "$OUT_DIR/$OUT_NAME" ]; then
    echo "Ya existe $OUT_DIR/$OUT_NAME. Usá otro nombre (ej. ${OUT_NAME%.png}_v2.png)." >&2; exit 2
fi

WORK="$(mktemp -d -t gemini_img_XXXXXXXX)"
trap 'rm -rf "$WORK"' EXIT

REQ="Generate an image with aspect ratio $RATIO using exactly this prompt:

$PROMPT

Save it as $OUT_NAME in the current directory. Do nothing else. Reply only with the file path."

LOG_FILE="$LOG_DIR/${OUT_NAME%.png}.log.jsonl"
echo "Generando $OUT_NAME ($RATIO, $MODEL)... puede tardar 1-3 min."
( cd "$WORK" && "$AGY" -p "$REQ" --model "$MODEL" --dangerously-skip-permissions \
    --print-timeout 300s --output-format stream-json ) >"$LOG_FILE" 2>&1 || true

if [ ! -f "$WORK/$OUT_NAME" ]; then
    echo "FALLÓ: no se creó $OUT_NAME. Archivos en la carpeta: $(cd "$WORK" && find . -type f -printf '%P ')" >&2
    echo "Mirá el registro: $LOG_FILE" >&2
    exit 1
fi
cp -f "$WORK/$OUT_NAME" "$OUT_DIR/$OUT_NAME"

# Entrada nueva al principio de la galería (debajo del encabezado)
FECHA="$(date '+%Y-%m-%d %H:%M')"
ENTRADA="$(mktemp)"
{
    echo "### ${OUT_NAME%.png} · $FECHA"
    echo "![[$OUT_NAME|600]]"
    echo "- **Proporción:** $RATIO · **Modelo:** $MODEL"
    echo "- **Prompt:**"
    echo '```'
    echo "$PROMPT"
    echo '```'
    echo
} >"$ENTRADA"
if [ -f "$GALERIA" ] && grep -q '^<!-- entradas -->$' "$GALERIA"; then
    sed -i "/^<!-- entradas -->\$/r $ENTRADA" "$GALERIA"
else
    cat "$ENTRADA" >>"$GALERIA"
fi
rm -f "$ENTRADA"

echo "OK $OUT_DIR/$OUT_NAME"
echo "Agregada a: $GALERIA"
