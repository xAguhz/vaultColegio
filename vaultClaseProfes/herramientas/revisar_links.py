"""Recorre las páginas publicadas de un vault y prueba cada link interno.
Uso: python3 revisar_links.py <carpeta vaultColegio> <vault>"""
import pathlib
import posixpath
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

RAIZ, VAULT = sys.argv[1], sys.argv[2]
B = "https://xaguhz.github.io/vaultColegio/"
vistos = {}


def estado(u):
    if u not in vistos:
        try:
            vistos[u] = urllib.request.urlopen(urllib.parse.quote(u, safe=":/?=&%()"), timeout=20).status
        except urllib.error.HTTPError as e:
            vistos[u] = e.code
    return vistos[u]


paginas = [str(p.relative_to(RAIZ).with_suffix("")).replace(" ", "-")
           for p in pathlib.Path(RAIZ, VAULT).rglob("*.md") if ".obsidian" not in p.parts]
rotos = 0
for pg in paginas:
    html = urllib.request.urlopen(urllib.parse.quote(B + pg, safe=":/") + "?v=6").read().decode()
    art = html.split("<article", 1)[-1].split("</article>", 1)[0]
    for h in sorted(set(re.findall(r'href="([^"#]+)"', art))):
        if h.startswith("http"):
            continue
        dest = posixpath.normpath(posixpath.join(posixpath.dirname("/vaultColegio/" + pg), h))
        c = estado("https://xaguhz.github.io" + dest)
        if c != 200:
            rotos += 1
            print("ROTO", pg, "->", h, c)
print(len(paginas), "páginas,", len(vistos), "destinos,", rotos, "rotos")
