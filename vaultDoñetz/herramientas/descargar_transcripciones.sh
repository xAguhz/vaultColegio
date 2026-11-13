#!/usr/bin/env bash
# Descarga los subtítulos automáticos en español de todos los videos del canal
# El Profe Juanito (@juanitoprofe), incluidos los 3 ocultos de la lista de repaso,
# y los convierte a texto plano (uno por video) en ./transcripciones/
# Requisitos: yt-dlp y python3.
set -euo pipefail
DEST="${1:-./transcripciones}"
mkdir -p "$DEST"
cd "$DEST"
{
  yt-dlp --flat-playlist --print "https://www.youtube.com/watch?v=%(id)s" "https://www.youtube.com/@juanitoprofe/videos"
  for id in xPYGSYCGWQ4 7ARQojNrfUE a289iQpL39I; do echo "https://www.youtube.com/watch?v=$id"; done
} > urls.txt
yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "es-orig,es" --sub-format vtt \
  --write-info-json -o "%(upload_date)s_%(id)s.%(ext)s" --sleep-requests 1 -a urls.txt
python3 - <<'PY'
import glob, json, os, re
for info in sorted(glob.glob('*.info.json')):
    base = info[:-len('.info.json')]
    vtt = next((f for f in (base + '.es-orig.vtt', base + '.es.vtt') if os.path.exists(f)), None)
    if not vtt:
        continue
    lines, last = [], None
    for l in open(vtt, encoding='utf8'):
        l = l.strip()
        if not l or '-->' in l or l.startswith(('WEBVTT', 'Kind:', 'Language:')):
            continue
        l = re.sub(r'<[^>]+>', '', l).strip()
        if l and l != last:
            lines.append(l); last = l
    title = json.load(open(info, encoding='utf8'))['title']
    with open(base + '.txt', 'w', encoding='utf8') as f:
        f.write(title + '\n\n' + ' '.join(lines) + '\n')
    print('ok', base, title)
PY
