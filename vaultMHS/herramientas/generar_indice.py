#!/usr/bin/env python3
"""Regenera indice.json (para agentes/IA) y "Mapa MHS.canvas" (para Obsidian) a partir de las notas.

Uso:  python3 herramientas/generar_indice.py        (desde la carpeta del vault)
Solo usa la biblioteca estándar. Avisa si hay links [[...]] rotos.
Correlo de nuevo cada vez que agregues o cambies notas.
"""
import json, re, pathlib, sys

VAULT = pathlib.Path(__file__).resolve().parent.parent
LINK = re.compile(r'\[\[([^\]|#\\]+)(?:#[^\]|]*)?(?:\\?\|[^\]]*)?\]\]')

def frontmatter(text):
    if not text.startswith('---\n'):
        return {}, text
    end = text.index('\n---', 4)
    meta = {}
    for line in text[4:end].splitlines():
        m = re.match(r'^(\w+):\s*(.*)$', line)
        if not m:
            continue
        k, v = m.groups()
        v = v.strip()
        if v.startswith('['):
            v = re.findall(r'"([^"]*)"', v) or [x.strip() for x in v[1:-1].split(',') if x.strip()]
        else:
            v = v.strip('"')
        meta[k] = v
    return meta, text[end + 4:]

notas = {}
for p in sorted(VAULT.rglob('*.md')):
    rel = p.relative_to(VAULT)
    if rel.parts[0].startswith('.') or rel.name == 'AGENTS.md':
        continue
    meta, body = frontmatter(p.read_text(encoding='utf8'))
    titulo = next((l[2:].strip() for l in body.splitlines() if l.startswith('# ')), p.stem)
    resumen = next((l.strip() for l in body.splitlines()
                    if l.strip() and not l.startswith(('#', '>', '|', '`', '-', '!')) ), '')
    links = sorted({m.strip() for m in LINK.findall(body + json.dumps(meta, ensure_ascii=False))} - {p.stem})
    notas[p.stem] = dict(archivo=str(rel), titulo=titulo, tipo=meta.get('tipo', ''),
                         aliases=meta.get('aliases', []), relacionado=[re.sub(r'[\[\]"]', '', r) for r in meta.get('relacionado', [])],
                         minutos=meta.get('minutos', []), tags=meta.get('tags', []),
                         resumen=re.sub(r'\[▶ [^\]]*\]\([^)]*\)', '', resumen)[:300].strip(), enlaces=links)

rotos = [(n, l) for n, d in notas.items() for l in d['enlaces'] if l not in notas and not l.endswith('.canvas')]
for k, n in notas.items():
    n['enlazado_desde'] = sorted(o for o, d in notas.items() if k in d['enlaces'])

indice = dict(
    vault='vaultMHS',
    tema='Model Hardware Standard (MHS) de Anthropic',
    fuente=dict(titulo='¿Por qué Anthropic se está metiendo en el hardware? (MHS explicado)', canal='IoT Lab',
                url='https://www.youtube.com/watch?v=3hxdHem70gw', publicado='2026-11-01', duracion='29:21'),
    advertencia='Una sola fuente (el video). Datos sin verificar contra documentación oficial.',
    tipos=sorted({d['tipo'] for d in notas.values()}),
    notas=notas)
(VAULT / 'indice.json').write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding='utf8')

# ---------- Canvas ----------
grupos = [('Inicio y guías', ['indice', 'resumen', 'guia', 'investigacion', 'recurso', 'fuente']),
          ('Conceptos', ['concepto']), ('Tecnologías', ['tecnologia']),
          ('Experimentos', ['experimento']), ('Actores', ['actor'])]
colores = {'Inicio y guías': '6', 'Conceptos': '4', 'Tecnologías': '2', 'Experimentos': '5', 'Actores': '3'}
W, H, GAP, COLS = 300, 70, 30, 2
nodes, edges, ids, x = [], [], {}, 0
for nombre, tipos in grupos:
    miembros = sorted([k for k, d in notas.items() if d['tipo'] in tipos], key=lambda k: (k[0].isdigit() is False, k))
    if not miembros:
        continue
    filas = (len(miembros) + COLS - 1) // COLS
    gw, gh = COLS * W + (COLS + 1) * GAP, filas * (H + GAP) + GAP + 40
    nodes.append(dict(id=f'g-{nombre}', type='group', label=nombre, x=x, y=0, width=gw, height=gh, color=colores[nombre]))
    for i, k in enumerate(miembros):
        nid = f'n{len(ids)}'
        ids[k] = nid
        nodes.append(dict(id=nid, type='file', file=notas[k]['archivo'], x=x + GAP + (i % COLS) * (W + GAP),
                          y=40 + GAP + (i // COLS) * (H + GAP), width=W, height=H, color=colores[nombre]))
    x += gw + 120
vistos = set()
for k, d in notas.items():
    for r in d['relacionado']:
        par = tuple(sorted((k, r)))
        if r in ids and k in ids and par not in vistos:
            vistos.add(par)
            edges.append(dict(id=f'e{len(edges)}', fromNode=ids[k], toNode=ids[r], fromSide='right', toSide='left'))
(VAULT / 'Mapa MHS.canvas').write_text(json.dumps(dict(nodes=nodes, edges=edges), ensure_ascii=False, indent=1), encoding='utf8')

print(f'{len(notas)} notas, {len(edges)} relaciones en el canvas')
if rotos:
    print('LINKS ROTOS:'); [print(f'  {n} -> [[{l}]]') for n, l in rotos]; sys.exit(1)
print('Sin links rotos.')
