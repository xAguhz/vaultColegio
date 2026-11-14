#!/usr/bin/env python3
"""Arma la página de la red: todos los vaults en un grafo interactivo.

Uso: python3 .quartz/red/red.py <carpeta vaultColegio> <carpeta de salida>

Recorre cada vault, encuentra las notas y los enlaces [[...]], y escribe
<salida>/index.html con los datos adentro (se puede abrir sin servidor).
La plantilla es .quartz/red/plantilla.html. Solo usa la biblioteca estándar.
"""
import json
import os
import posixpath
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
from preparar import SITIO, REPO, VAULTS, IGNORAR_CARPETAS, slug  # noqa: E402

# Datos de presentación de cada vault (los títulos y descripciones vienen de preparar.py)
EXTRA = {
    "vaultAutoLID": dict(color="#f2994a", fuente="Carpeta de Google Drive", icono="📦", tipo="Proyecto"),
    "vaultTorno": dict(color="#56ccf2", fuente="Manuales en PDF (uno en inglés)", icono="⚙️", tipo="Manual técnico"),
    "vaultDoñetz": dict(color="#6fcf97", fuente="27 videos de YouTube", icono="🎥", tipo="Curso en video"),
    "vaultCharrute": dict(color="#bb6bd9", fuente="Apuntes y entregas en Drive", icono="📘", tipo="Materia"),
    "vaultSuzuki": dict(color="#4f7cf0", fuente="Manual de taller y catálogo japonés", icono="🚗", tipo="Manual técnico"),
    "vaultClaseProfes": dict(color="#e86fb0", fuente="La experiencia del propio alumno", icono="🎓", tipo="Guía para docentes"),
    "vaultMHS": dict(color="#eb5757", fuente="1 video de YouTube", icono="🤖", tipo="Investigación"),
    "vaultRed": dict(color="#f2c94c", fuente="El propio método", icono="🕸️", tipo="Método"),
}
ENLACE = re.compile(r"!?\[\[([^\[\]|#\\]+?)(?:#[^\[\]|\\]*)?(?:\\?\|[^\[\]]*)?\]\]")
IMAGEN = re.compile(r"\.(png|jpe?g|gif|svg|webp|mp4|pdf|docx|glb|blend)$", re.I)


def sin_codigo(texto):
    texto = re.sub(r"```.*?```", " ", texto, flags=re.S)
    return re.sub(r"`[^`\n]*`", " ", texto)


def frontmatter(texto):
    m = re.match(r"---\n(.*?)\n---\n?", texto, re.S)
    if not m:
        return {}, texto
    datos = {}
    for linea in m.group(1).splitlines():
        k, _, v = linea.partition(":")
        if v and not linea.startswith((" ", "-")):
            datos[k.strip()] = v.strip().strip('"')
    return datos, texto[m.end():]


def palabras(texto):
    return len(re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+", texto))


def recorrer(origen):
    notas = []
    for v in VAULTS:
        raiz = os.path.join(origen, v)
        for d, carpetas, archivos in os.walk(raiz):
            carpetas[:] = [c for c in carpetas if c not in IGNORAR_CARPETAS and not c.startswith(".")]
            for f in sorted(archivos):
                if not (f.endswith(".md") or f.endswith(".canvas")) or f == "AGENTS.md":
                    continue
                ruta = posixpath.relpath(posixpath.join(d, f), origen)
                notas.append(ruta)
    return notas


def nombre(ruta):
    base = posixpath.basename(ruta)
    for ext in (".excalidraw.md", ".md", ".canvas"):
        if base.endswith(ext):
            return base[: -len(ext)]
    return base


def url(ruta):
    r = ruta[:-7] if ruta.endswith(".canvas") else ruta  # el canvas se publica como nota
    return f"{SITIO}/{slug(r)}"


def main(origen, salida):
    rutas = recorrer(origen)
    por_nombre, por_ruta = {}, {}
    for r in rutas:
        por_nombre.setdefault(nombre(r).lower(), []).append(r)
        sin_ext = r[:-3] if r.endswith(".md") else r
        por_ruta[sin_ext.lower()] = r
        por_ruta[r.lower()] = r

    def resolver(destino, vault):
        d = destino.strip().lower()
        if IMAGEN.search(d) or d.startswith("herramientas/"):
            return None
        for cand in (f"{vault.lower()}/{d}", d):
            if cand in por_ruta:
                return por_ruta[cand]
        base = posixpath.basename(d)
        for suf in (".md", ".canvas"):
            if base.endswith(suf):
                base = base[: -len(suf)]
        if base.endswith(".excalidraw"):
            base = base[: -len(".excalidraw")]
        cands = por_nombre.get(base, [])
        cands = sorted(cands, key=lambda c: (not c.startswith(vault + "/"), len(c)))
        cands = [c for c in cands if c.startswith(vault + "/")]  # cada vault se abre por separado en Obsidian
        return cands[0] if cands else None

    nodos, aristas, rotos = [], set(), []
    idx = {r: i for i, r in enumerate(rutas)}
    inicio_de = {}
    for v, (titulo, inicio, _desc) in VAULTS.items():
        inicio_de[v] = resolver(inicio, v)
    for r in rutas:
        vault = r.split("/")[0]
        with open(os.path.join(origen, r), encoding="utf-8") as fh:
            texto = fh.read()
        if r.endswith(".canvas"):
            datos = json.loads(texto or "{}")
            meta, cuerpo = {"tipo": "canvas"}, ""
            destinos = [n["file"] for n in datos.get("nodes", []) if n.get("type") == "file"]
            destinos += [m.group(1) for n in datos.get("nodes", []) if n.get("type") == "text" for m in ENLACE.finditer(n.get("text", ""))]
        else:
            meta, cuerpo = frontmatter(texto)
            if r.endswith(".excalidraw.md"):
                meta["tipo"] = "dibujo"
                cuerpo = cuerpo.split("%%")[0]
            limpio = sin_codigo(cuerpo)
            destinos = [m.group(1) for m in ENLACE.finditer(limpio)]
            if meta.get("vault") in VAULTS and inicio_de.get(meta["vault"]):
                aristas.add((idx[r], idx[inicio_de[meta["vault"]]], 1))  # puente entre vaults
        partes = r.split("/")
        nodos.append(dict(
            t=nombre(r), v=vault, c=partes[1] if len(partes) > 2 else "", u=url(r),
            k=(meta.get("tipo") or ("canvas" if r.endswith(".canvas") else "nota")).replace("í", "i"),
            w=palabras(sin_codigo(cuerpo)) if not r.endswith(".canvas") else 0,
        ))
        for d in destinos:
            dest = resolver(d, vault)
            if dest is None:
                if not IMAGEN.search(d.strip()) and not d.strip().startswith("herramientas/"):
                    rotos.append((r, d))
                continue
            if dest != r:
                a, b = idx[r], idx[dest]
                aristas.add((a, b, 0))

    grado = [0] * len(nodos)
    entrantes = [0] * len(nodos)
    for a, b, _ in aristas:
        grado[a] += 1
        grado[b] += 1
        entrantes[b] += 1
    for i, n in enumerate(nodos):
        n["g"] = grado[i]

    vaults = []
    for v, (titulo, inicio, desc) in VAULTS.items():
        ids = [i for i, n in enumerate(nodos) if n["v"] == v]
        enl = sum(1 for a, b, p in aristas if nodos[a]["v"] == v and not p)
        top = sorted(ids, key=lambda i: -entrantes[i])[:5]
        raiz = os.path.join(origen, v)
        imgs = sum(1 for d, cs, fs in os.walk(raiz) if "/." not in d and "/herramientas" not in d for f in fs
                   if f.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".webp")))
        scripts = sum(1 for d, cs, fs in os.walk(os.path.join(raiz, "herramientas")) for f in fs if f.endswith((".py", ".sh")))
        vaults.append(dict(
            id=v, titulo=titulo, desc=desc, u=f"{SITIO}/{slug(v)}/", inicio=url(inicio_de[v]) if inicio_de.get(v) else f"{SITIO}/{slug(v)}/",
            notas=len(ids), enlaces=enl, palabras=sum(nodos[i]["w"] for i in ids),
            canvas=sum(1 for i in ids if nodos[i]["k"] == "canvas"), dibujos=sum(1 for i in ids if nodos[i]["k"] == "dibujo"),
            imagenes=imgs, scripts=scripts, top=[nodos[i]["t"] for i in top if entrantes[i]], **EXTRA.get(v, {}),
        ))

    try:
        log = subprocess.run(["git", "-C", origen, "log", "--format=%cs\t%s"], capture_output=True, text=True, check=True).stdout
        historia = [dict(f=f, s=s) for f, _, s in (l.partition("\t") for l in log.splitlines())
                    if s and "copia automática" not in s and "cambios del" not in s]
    except (OSError, subprocess.CalledProcessError):
        historia = []

    datos = dict(
        sitio=SITIO, repo=REPO, vaults=vaults, historia=historia[::-1],
        nodos=nodos, aristas=[[a, b, p] for a, b, p in sorted(aristas)],
        total=dict(notas=len(nodos), enlaces=sum(1 for *_, p in aristas if not p), palabras=sum(n["w"] for n in nodos), vaults=len(vaults)),
    )
    os.makedirs(salida, exist_ok=True)
    with open(os.path.join(AQUI, "plantilla.html"), encoding="utf-8") as fh:
        plantilla = fh.read()
    js = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    with open(os.path.join(salida, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(plantilla.replace("/*__DATOS__*/null", js))
    with open(os.path.join(salida, "red.json"), "w", encoding="utf-8") as fh:
        fh.write(js)
    print(f"Red: {len(nodos)} notas, {datos['total']['enlaces']} enlaces, {len(vaults)} vaults → {salida}")
    if rotos:
        print(f"{len(rotos)} enlaces sin nota (pendientes o rotos):")
        for r, d in rotos[:40]:
            print(f"  {r} → [[{d}]]")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
