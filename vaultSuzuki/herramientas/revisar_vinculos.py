"""Busca vínculos rotos en los vaults de vaultColegio, resolviendo como Obsidian.

Uso: python3 herramientas/revisar_vinculos.py [carpeta vaultColegio]

Revisa en cada vault (cada subcarpeta con .obsidian, o las conocidas):
- [[nota]], [[nota|alias]], [[nota#título]], [[carpeta/nota]] y ![[adjunto.png]]
- archivos de los canvas ("file": ...)
- enlaces markdown a archivos locales [texto](ruta)
Ignora lo que está dentro de bloques de código y los links a la web.
"""
import json
import os
import re
import sys
import urllib.parse

RAIZ = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VAULTS = [d for d in sorted(os.listdir(RAIZ)) if d.startswith('vault') and os.path.isdir(os.path.join(RAIZ, d))]
IGNORAR = {'.obsidian', '.trash', '.git', 'node_modules'}


def indice(vault):
    rutas, nombres = set(), {}
    for d, ds, fs in os.walk(vault):
        ds[:] = [x for x in ds if x not in IGNORAR]
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), vault).replace(os.sep, '/')
            rutas.add(rel)
            nombres.setdefault(f, []).append(rel)
            if f.endswith('.md'):
                nombres.setdefault(f[:-3], []).append(rel)
    return rutas, nombres


def resuelve(t, rutas, nombres, desde):
    t = t.strip()
    if not t:
        return True
    if t in rutas or t + '.md' in rutas:
        return True
    rel = os.path.normpath(os.path.join(os.path.dirname(desde), t)).replace(os.sep, '/')
    if rel in rutas or rel + '.md' in rutas:
        return True
    base = t.split('/')[-1]
    cands = nombres.get(base, []) + nombres.get(base + '.md', [])
    if '/' in t:
        cands = [c for c in cands if c.endswith(t) or c.endswith(t + '.md')]
    return bool(cands)


total = 0
for v in VAULTS:
    vp = os.path.join(RAIZ, v)
    rutas, nombres = indice(vp)
    rotos = []
    for rel in sorted(rutas):
        p = os.path.join(vp, rel)
        if rel.endswith('.md'):
            txt = open(p, encoding='utf-8', errors='replace').read()
            txt = re.sub(r'```.*?```', '', txt, flags=re.S)
            txt = re.sub(r'`[^`\n]*`', '', txt)
            for m in re.finditer(r'!?\[\[([^\]]+?)\]\]', txt):
                t = m.group(1).split('|')[0].split('#')[0].replace('\\', '')
                if t and not resuelve(t, rutas, nombres, rel):
                    rotos.append((rel, m.group(0)))
            for m in re.finditer(r'(?<!!)\[[^\]]*\]\(([^)\s]+)\)', txt):
                u = m.group(1)
                if re.match(r'^(https?:|mailto:|#|obsidian:)', u):
                    continue
                t = urllib.parse.unquote(u.split('#')[0])
                if t and not resuelve(t, rutas, nombres, rel):
                    rotos.append((rel, m.group(0)))
        elif rel.endswith('.canvas'):
            try:
                d = json.load(open(p, encoding='utf-8'))
            except Exception:
                rotos.append((rel, '(canvas ilegible)'))
                continue
            for n in d.get('nodes', []):
                if n.get('type') == 'file' and not resuelve(n.get('file', ''), rutas, nombres, rel):
                    rotos.append((rel, n.get('file')))
    total += len(rotos)
    print(f'== {v}: {len(rotos)} vínculos rotos')
    for a, b in rotos:
        print(f'   {a}  →  {b}')
print('TOTAL', total)
