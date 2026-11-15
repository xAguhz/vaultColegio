#!/bin/bash
# Abre el visor 3D del Swift como aplicación local: sirve el vault en la compu (modelos binarios .glb,
# más rápidos) y lo abre en una ventana de Firefox. La primera vez necesita internet para bajar la
# librería 3D; después queda guardada y anda sin conexión.
DIR="$(cd "$(dirname "$0")/.." && pwd)"
PUERTO=8780
URL="http://127.0.0.1:$PUERTO/3D/visor/index.html"
if ! curl -s -o /dev/null "$URL"; then
  nohup python3 -m http.server "$PUERTO" --bind 127.0.0.1 --directory "$DIR" >/dev/null 2>&1 &
  for _ in $(seq 20); do curl -s -o /dev/null "$URL" && break; sleep 0.2; done
fi
exec firefox --new-window "$URL"
