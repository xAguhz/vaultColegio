#!/usr/bin/env python3
"""Prepara vaultColegio para publicarlo con Quartz.

Uso: python3 preparar.py <carpeta vaultColegio> <carpeta content de Quartz>

- Copia los dos vaults (sin configuración de Obsidian, herramientas ni plantillas).
- Convierte cada Canvas (.canvas) en una nota con el tablero dibujado.
- Convierte cada dibujo de Excalidraw (.excalidraw.md) en una nota con el dibujo en SVG.
- Cambia los links a los Artifacts privados por las copias publicadas en el sitio.
- Copia las láminas del torno al visor 3D.
Solo usa la biblioteca estándar de Python.
"""
import html
import json
import math
import os
import posixpath
import re
import shutil
import subprocess
import sys

SITIO = "https://xaguhz.github.io/vaultColegio"
VAULTS = {
    "vaultAutoLID": ("AutoLID y materias", "00 Inicio", "Proyecto grupal AutoLID, materias y entregas."),
    "vaultTorno": ("Torno TM300", "00 Torno TM300", "Manual de mantenimiento y repuestos del torno Femar TM300, con despiece 3D."),
}
IGNORAR_CARPETAS = {".obsidian", "herramientas", "Plantillas", "logs", ".trash"}
IGNORAR_EXT = {".blend", ".blend1"}
# Artifacts privados de claude.ai → su copia en el sitio
ARTIFACTS = {
    "https://claude.ai/artifact/6k1uizayAvXsBWRHKa3caD": f"{SITIO}/vaultTorno/3D/visor/index.html",
    "https://claude.ai/artifact/H3ZKnU41iqELZVsaQRg9zc": f"{SITIO}/vaultAutoLID/AutoLID/Web/index.html",
}
COLORES = {"1": "#e93147", "2": "#ec7500", "3": "#e0ac00", "4": "#08b94e", "5": "#00bfbc", "6": "#7852ee"}
IMAGENES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


# ---------------------------------------------------------------- utilidades
def slug(ruta):
    """Igual que slugifyFilePath de Quartz 4 (sin extensión para .md)."""
    base, ext = os.path.splitext(ruta)
    if ext == ".md":
        ext = ""
    partes = []
    for s in base.split("/"):
        s = re.sub(r"\s", "-", s).replace("&", "-and-").replace("%", "-percent").replace("?", "").replace("#", "")
        partes.append(s)
    return "/".join(partes) + ext


def url_relativa(desde_nota, hacia):
    """URL relativa entre dos rutas del contenido (desde una nota .md)."""
    origen = posixpath.dirname(slug(desde_nota)) or "."
    rel = posixpath.relpath(slug(hacia), origen)
    return rel if rel.startswith(".") else "./" + rel


def esc(t):
    return html.escape(str(t), quote=True)


class Indice:
    """Resuelve [[links]] como Obsidian: por nombre de archivo o por ruta."""

    def __init__(self, raiz):
        self.archivos = []
        for d, _, fs in os.walk(raiz):
            for f in fs:
                self.archivos.append(posixpath.relpath(posixpath.join(d, f), raiz))

    def buscar(self, nombre, vault):
        nombre = nombre.strip()
        cands = [nombre, nombre + ".md"]
        for a in self.archivos:  # ruta exacta dentro del vault
            if a.startswith(vault + "/") and a[len(vault) + 1:] in cands:
                return a
        mismos = [a for a in self.archivos if posixpath.basename(a) in cands or a.endswith("/" + nombre) or a.endswith("/" + nombre + ".md")]
        mismos.sort(key=lambda a: (not a.startswith(vault + "/"), len(a)))
        return mismos[0] if mismos else None


# ------------------------------------------------------- Markdown mínimo → HTML
def md_a_html(texto, nota, vault, indice):
    def link(m):
        destino, _, alias = m.group(1).partition("|")
        destino = destino.split("#")[0]
        ruta = indice.buscar(destino.replace(".canvas", ""), vault)
        etiqueta = esc(alias or posixpath.basename(destino).replace(".excalidraw", "").replace(".canvas", ""))
        if not ruta:
            return f'<span class="cv-link-roto">{etiqueta}</span>'
        return f'<a class="internal" href="{esc(url_relativa(nota, ruta))}">{etiqueta}</a>'

    salida, en_lista = [], False
    for linea in texto.split("\n"):
        t = esc(linea)
        t = re.sub(r"\[\[([^\]]+)\]\]", lambda m: link(re.match(r"(.*)", html.unescape(m.group(1)))), t)
        t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a class="external" href="\2">\1</a>', t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"==(.+?)==", r"<mark>\1</mark>", t)
        cab = re.match(r"(#{1,6})\s+(.*)", t)
        item = re.match(r"\s*(?:[-*+]|\d+\.)\s+(.*)", t)
        if item:
            if not en_lista:
                salida.append("<ul>")
                en_lista = True
            salida.append(f"<li>{item.group(1)}</li>")
            continue
        if en_lista:
            salida.append("</ul>")
            en_lista = False
        if cab:
            n = min(len(cab.group(1)) + 1, 6)
            salida.append(f"<h{n}>{cab.group(2)}</h{n}>")
        elif t.strip():
            salida.append(f"<p>{t}</p>")
    if en_lista:
        salida.append("</ul>")
    return "".join(salida)


# ------------------------------------------------------------------- Canvas
def color_canvas(c, defecto="var(--gray)"):
    if not c:
        return defecto
    return COLORES.get(str(c), c)


def lado(n, s):
    x, y, w, h = n["x"], n["y"], n["width"], n["height"]
    return {"top": (x + w / 2, y), "bottom": (x + w / 2, y + h), "left": (x, y + h / 2), "right": (x + w, y + h / 2)}[s]


def lado_auto(a, b):
    ax, ay = a["x"] + a["width"] / 2, a["y"] + a["height"] / 2
    bx, by = b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
    if abs(bx - ax) > abs(by - ay):
        return ("right", "left") if bx > ax else ("left", "right")
    return ("bottom", "top") if by > ay else ("top", "bottom")


def canvas_a_html(datos, nota, vault, indice):
    nodos = datos.get("nodes", [])
    if not nodos:
        return "<p>(Canvas vacío)</p>"
    pad = 40
    x0 = min(n["x"] for n in nodos) - pad
    y0 = min(n["y"] for n in nodos) - pad
    x1 = max(n["x"] + n["width"] for n in nodos) + pad
    y1 = max(n["y"] + n["height"] for n in nodos) + pad
    W, H = x1 - x0, y1 - y0
    por_id = {n["id"]: n for n in nodos}

    partes = []
    # grupos primero (quedan debajo)
    for n in sorted(nodos, key=lambda n: n["type"] != "group"):
        estilo = f'left:{n["x"] - x0}px;top:{n["y"] - y0}px;width:{n["width"]}px;height:{n["height"]}px;--c:{color_canvas(n.get("color"))}'
        borde = (n.get("styleAttributes") or {}).get("border")
        clase = "cv-node cv-" + n["type"] + (" cv-sin-borde" if borde == "invisible" else "") + (" cv-color" if n.get("color") else "")
        if n["type"] == "group":
            etiqueta = f'<span class="cv-group-label">{esc(n.get("label", ""))}</span>' if n.get("label") else ""
            partes.append(f'<div class="{clase}" style="{estilo}">{etiqueta}</div>')
        elif n["type"] == "text":
            partes.append(f'<div class="{clase}" style="{estilo}"><div class="cv-body">{md_a_html(n.get("text", ""), nota, vault, indice)}</div></div>')
        elif n["type"] == "file":
            ruta = indice.buscar(n["file"], vault) or indice.buscar(posixpath.basename(n["file"]), vault)
            ext = os.path.splitext(n["file"])[1].lower()
            if ruta and ext in IMAGENES:
                cuerpo = f'<img src="{esc(url_relativa(nota, ruta))}" alt="{esc(posixpath.basename(n["file"]))}" loading="lazy">'
            elif ruta:
                titulo = posixpath.basename(ruta)[:-3] if ruta.endswith(".md") else posixpath.basename(ruta)
                cuerpo = f'<div class="cv-body"><a class="internal cv-file-link" href="{esc(url_relativa(nota, ruta))}">📄 {esc(titulo)}</a></div>'
            else:
                cuerpo = f'<div class="cv-body">{esc(n["file"])}</div>'
            partes.append(f'<div class="{clase}" style="{estilo}">{cuerpo}</div>')
        elif n["type"] == "link":
            partes.append(f'<div class="{clase}" style="{estilo}"><div class="cv-body"><a class="external" href="{esc(n.get("url", ""))}">{esc(n.get("url", ""))}</a></div></div>')

    flechas = []
    for e in datos.get("edges", []):
        a, b = por_id.get(e["fromNode"]), por_id.get(e["toNode"])
        if not a or not b:
            continue
        auto = lado_auto(a, b)
        sa, sb = e.get("fromSide") or auto[0], e.get("toSide") or auto[1]
        (ax, ay), (bx, by) = lado(a, sa), lado(b, sb)
        ax, ay, bx, by = ax - x0, ay - y0, bx - x0, by - y0
        d = min(160, math.hypot(bx - ax, by - ay) / 2)
        off = {"top": (0, -1), "bottom": (0, 1), "left": (-1, 0), "right": (1, 0)}
        c1 = (ax + off[sa][0] * d, ay + off[sa][1] * d)
        c2 = (bx + off[sb][0] * d, by + off[sb][1] * d)
        col = color_canvas(e.get("color"), "var(--darkgray)")
        fin = e.get("toEnd", "arrow") == "arrow"
        ini = e.get("fromEnd") == "arrow"
        flechas.append(
            f'<path d="M{ax:.1f},{ay:.1f} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {bx:.1f},{by:.1f}" style="stroke:{col}"'
            + (' marker-end="url(#cv-flecha)"' if fin else "") + (' marker-start="url(#cv-flecha-ini)"' if ini else "") + f' class="cv-edge" color="{col}"/>'
        )
        if e.get("label"):
            mx = 0.125 * ax + 0.375 * c1[0] + 0.375 * c2[0] + 0.125 * bx
            my = 0.125 * ay + 0.375 * c1[1] + 0.375 * c2[1] + 0.125 * by
            partes.append(f'<div class="cv-edge-label" style="left:{mx:.0f}px;top:{my:.0f}px">{esc(e["label"])}</div>')

    defs = (
        '<defs><marker id="cv-flecha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker>'
        '<marker id="cv-flecha-ini" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>'
    )
    svg = f'<svg class="cv-edges" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs}{"".join(flechas)}</svg>'
    tablero = f'<div class="cv-board" style="width:{W}px;height:{H}px">{svg}{"".join(partes)}</div>'
    return f'<div class="cv-wrap" data-ancho="{W}">{tablero}</div>'


# --------------------------------------------------------------- Excalidraw
LZ_CLAVE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


def lz_base64(texto):
    """LZString.decompressFromBase64 (el formato 'compressed-json' de Excalidraw)."""
    texto = re.sub(r"\s", "", texto)
    if not texto:
        return ""
    inv = {c: i for i, c in enumerate(LZ_CLAVE)}
    largo, reset = len(texto), 32

    def siguiente(i):
        return inv[texto[i]] if i < largo else 0

    estado = {"val": siguiente(0), "pos": reset, "idx": 1}

    def bits(n):
        r, potencia, tope = 0, 1, 1 << n
        while potencia != tope:
            b = estado["val"] & estado["pos"]
            estado["pos"] >>= 1
            if estado["pos"] == 0:
                estado["pos"] = reset
                estado["val"] = siguiente(estado["idx"])
                estado["idx"] += 1
            r |= (1 if b > 0 else 0) * potencia
            potencia <<= 1
        return r

    dic = {0: 0, 1: 1, 2: 2}
    agrandar, tam, nbits = 4, 4, 3
    primero = bits(2)
    if primero == 0:
        c = chr(bits(8))
    elif primero == 1:
        c = chr(bits(16))
    else:
        return ""
    dic[3] = c
    w, res = c, [c]
    while True:
        if estado["idx"] > largo:
            return ""
        c = bits(nbits)
        if c in (0, 1):
            dic[tam] = chr(bits(8 if c == 0 else 16))
            tam += 1
            c = tam - 1
            agrandar -= 1
        elif c == 2:
            s = "".join(res)
            return s.encode("utf-16", "surrogatepass").decode("utf-16")
        if agrandar == 0:
            agrandar = 1 << nbits
            nbits += 1
        if c in dic:
            entrada = dic[c]
        elif c == tam:
            entrada = w + w[0]
        else:
            raise ValueError("datos de Excalidraw dañados")
        res.append(entrada)
        dic[tam] = w + entrada[0]
        tam += 1
        agrandar -= 1
        w = entrada
        if agrandar == 0:
            agrandar = 1 << nbits
            nbits += 1


def leer_excalidraw(texto):
    m = re.search(r"```compressed-json\n(.*?)\n```", texto, re.S)
    if m:
        datos = json.loads(lz_base64(m.group(1)))
    else:
        m = re.search(r"```json\n(.*?)\n```", texto, re.S)
        datos = json.loads(m.group(1)) if m else None
    if not datos:
        return None
    # Como el plugin: el texto vale lo que dice la sección "Text Elements" (el JSON puede estar viejo)
    sec = re.search(r"## Text Elements\n(.*?)(?=\n%%|\n## |\Z)", texto, re.S)
    textos = {}
    if sec:
        for t, i in re.findall(r"([\s\S]*?) \^([A-Za-z0-9_-]+)\n", sec.group(1) + "\n"):
            textos.setdefault(i, t.strip("\n"))
    for e in datos.get("elements", []):
        nuevo = textos.get(e.get("id"))
        if e.get("type") == "text" and nuevo is not None and nuevo != e.get("originalText", e.get("text")):
            e["text"] = nuevo
    return datos


def excalidraw_a_svg(datos):
    els = [e for e in datos.get("elements", []) if not e.get("isDeleted")]
    if not els:
        return None

    def caja(e):
        if e.get("points"):
            xs = [e["x"] + p[0] for p in e["points"]]
            ys = [e["y"] + p[1] for p in e["points"]]
            return min(xs), min(ys), max(xs), max(ys)
        return e["x"], e["y"], e["x"] + e.get("width", 0), e["y"] + e.get("height", 0)

    cajas = [caja(e) for e in els]
    pad = 30
    x0, y0 = min(c[0] for c in cajas) - pad, min(c[1] for c in cajas) - pad
    x1, y1 = max(c[2] for c in cajas) + pad, max(c[3] for c in cajas) + pad
    W, H = x1 - x0, y1 - y0
    fondo = (datos.get("appState") or {}).get("viewBackgroundColor", "#ffffff")
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}" class="ex-svg">',
        f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{W:.1f}" height="{H:.1f}" fill="{fondo}"/>',
    ]
    for e in els:
        t = e["type"]
        trazo = e.get("strokeColor", "#1e1e1e")
        relleno = e.get("backgroundColor", "transparent")
        relleno = "none" if relleno == "transparent" else relleno
        sw = e.get("strokeWidth", 2)
        op = e.get("opacity", 100) / 100
        guiones = {"dashed": ' stroke-dasharray="8 6"', "dotted": ' stroke-dasharray="2 6"'}.get(e.get("strokeStyle"), "")
        comun = f'stroke="{trazo}" stroke-width="{sw}" opacity="{op}"{guiones} stroke-linecap="round" stroke-linejoin="round"'
        x, y, w, h = e["x"], e["y"], e.get("width", 0), e.get("height", 0)
        giro = f' transform="rotate({math.degrees(e.get("angle", 0)):.2f} {x + w / 2:.1f} {y + h / 2:.1f})"' if e.get("angle") else ""
        if t == "rectangle":
            r = min(32, min(w, h) * 0.25) if e.get("roundness") else 0
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r:.1f}" fill="{relleno}" {comun}{giro}/>')
        elif t == "ellipse":
            out.append(f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 2}" ry="{h / 2}" fill="{relleno}" {comun}{giro}/>')
        elif t == "diamond":
            pts = f"{x + w / 2},{y} {x + w},{y + h / 2} {x + w / 2},{y + h} {x},{y + h / 2}"
            out.append(f'<polygon points="{pts}" fill="{relleno}" {comun}{giro}/>')
        elif t in ("arrow", "line", "freedraw"):
            pts = [(x + p[0], y + p[1]) for p in e.get("points", [])]
            if len(pts) < 2:
                continue
            d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
            out.append(f'<path d="{d}" fill="none" {comun}/>')
            for punta, (p, q) in (("endArrowhead", (pts[-2], pts[-1])), ("startArrowhead", (pts[1], pts[0]))):
                if e.get(punta):
                    ang = math.atan2(q[1] - p[1], q[0] - p[0])
                    L = 10 + 2 * sw
                    a1 = (q[0] - L * math.cos(ang - 0.45), q[1] - L * math.sin(ang - 0.45))
                    a2 = (q[0] - L * math.cos(ang + 0.45), q[1] - L * math.sin(ang + 0.45))
                    if e[punta] in ("triangle", "dot"):
                        out.append(f'<polygon points="{q[0]:.1f},{q[1]:.1f} {a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f}" fill="{trazo}" opacity="{op}"/>')
                    else:
                        out.append(f'<path d="M{a1[0]:.1f},{a1[1]:.1f} L{q[0]:.1f},{q[1]:.1f} L{a2[0]:.1f},{a2[1]:.1f}" fill="none" {comun}/>')
        elif t == "text":
            fs = e.get("fontSize", 20)
            lh = e.get("lineHeight", 1.25) * fs
            alin = e.get("textAlign", "left")
            ax = {"left": x, "center": x + w / 2, "right": x + w}[alin]
            anc = {"left": "start", "center": "middle", "right": "end"}[alin]
            familia = "'Cascadia Code', monospace" if e.get("fontFamily") == 3 else "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
            lineas = e.get("text", "").split("\n")
            tsp = "".join(
                f'<tspan x="{ax:.1f}" y="{y + (i + 0.5) * lh:.1f}">{esc(l) if l else " "}</tspan>' for i, l in enumerate(lineas)
            )
            out.append(f'<text font-size="{fs}" font-family="{familia}" fill="{trazo}" opacity="{op}" text-anchor="{anc}" dominant-baseline="central"{giro}>{tsp}</text>')
    out.append("</svg>")
    return "".join(out)


def fechas_git(origen):
    """{ruta relativa: (creado, modificado)} según el historial de git del vault."""
    try:
        salida = subprocess.run(
            ["git", "-C", origen, "log", "--format=@%cI", "--name-only", "--no-renames"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return {}
    fechas, actual = {}, None
    for linea in salida.splitlines():
        if linea.startswith("@"):
            actual = linea[1:]
        elif linea.strip() and actual:
            creado, modif = fechas.get(linea, (actual, actual))
            fechas[linea] = (actual, modif)  # log va de más nuevo a más viejo
    return fechas


def frontmatter(texto):
    m = re.match(r"---\n(.*?)\n---\n?", texto, re.S)
    return (m.group(0), texto[m.end():]) if m else ("", texto)


# ---------------------------------------------------------------- principal
def main(origen, destino):
    if os.path.exists(destino):
        for x in os.listdir(destino):
            if x not in (".gitkeep",):
                p = os.path.join(destino, x)
                shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(destino, exist_ok=True)

    def ignorar(_dir, nombres):
        return [n for n in nombres if n in IGNORAR_CARPETAS or os.path.splitext(n)[1] in IGNORAR_EXT or n.startswith(".")]

    for v in VAULTS:
        shutil.copytree(os.path.join(origen, v), os.path.join(destino, v), ignore=ignorar)

    # láminas del torno → visor 3D
    lam_src = os.path.join(destino, "vaultTorno", "Adjuntos", "Torno TM300")
    lam_dst = os.path.join(destino, "vaultTorno", "3D", "visor", "laminas")
    if os.path.isdir(lam_src) and os.path.isdir(os.path.dirname(lam_dst)):
        os.makedirs(lam_dst, exist_ok=True)
        for f in os.listdir(lam_src):
            if f.endswith(".png"):
                shutil.copy2(os.path.join(lam_src, f), lam_dst)

    indice = Indice(destino)

    # Canvas → nota
    for d, _, fs in os.walk(destino):
        for f in fs:
            if not f.endswith(".canvas"):
                continue
            ruta = posixpath.relpath(posixpath.join(d, f), destino)
            vault = ruta.split("/")[0]
            nota = ruta[: -len(".canvas")] + ".md"
            with open(os.path.join(destino, ruta), encoding="utf-8") as fh:
                datos = json.load(fh)
            cuerpo = canvas_a_html(datos, nota, vault, indice)
            titulo = posixpath.basename(nota)[:-3]
            with open(os.path.join(destino, nota), "w", encoding="utf-8") as fh:
                fh.write(f"---\ntitle: \"{titulo}\"\ntags: [canvas]\n---\n> [!info] Canvas de Obsidian\n> Tablero de solo lectura. Deslizá para recorrerlo; los links abren las notas.\n\n{cuerpo}\n")
            os.remove(os.path.join(destino, ruta))
    indice = Indice(destino)

    # Excalidraw → nota con SVG
    for d, _, fs in os.walk(destino):
        for f in fs:
            if not f.endswith(".excalidraw.md"):
                continue
            p = os.path.join(d, f)
            with open(p, encoding="utf-8") as fh:
                texto = fh.read()
            datos = leer_excalidraw(texto)
            svg = excalidraw_a_svg(datos) if datos else None
            fm, _ = frontmatter(texto)
            fm = re.sub(r"excalidraw-plugin:.*\n", "", fm)
            nombre = f[: -len(".excalidraw.md")]
            svg_nombre = nombre + ".excalidraw.svg"
            if svg:
                with open(os.path.join(d, svg_nombre), "w", encoding="utf-8") as fh:
                    fh.write(svg)
                cuerpo = (
                    "> [!info] Dibujo de Excalidraw\n> Versión de solo lectura. Para editarlo, abrilo en Obsidian.\n\n"
                    f'<div class="cv-wrap ex-wrap">{svg}</div>\n\n'
                    f"[Abrir el dibujo en tamaño completo](./{slug(svg_nombre)})\n"
                )
            else:
                cuerpo = "No se pudo leer el dibujo.\n"
            if "title:" not in fm:
                fm = fm.replace("---\n", f"---\ntitle: \"{nombre}\"\n", 1) if fm else f"---\ntitle: \"{nombre}\"\n---\n"
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(fm + cuerpo)

    # Reescrituras en todas las notas
    for d, _, fs in os.walk(destino):
        for f in fs:
            if not f.endswith(".md"):
                continue
            p = os.path.join(d, f)
            with open(p, encoding="utf-8") as fh:
                t = fh.read()
            nuevo = re.sub(r"(\[\[[^\]|#]+?)\.canvas", r"\1", t)
            for viejo, sitio in ARTIFACTS.items():
                nuevo = nuevo.replace(viejo, sitio)
            nuevo = nuevo.replace("(privado; se comparte desde el menú *Compartir* de la página)", "")
            nuevo = nuevo.replace("(privada hasta que la compartas)", "")
            if nuevo != t:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(nuevo)

    # Fechas reales (último cambio en git) para que la página no muestre la fecha de compilación
    fechas = fechas_git(origen)
    for d, _, fs in os.walk(destino):
        for f in fs:
            if not f.endswith(".md"):
                continue
            rel = posixpath.relpath(posixpath.join(d, f), destino)
            fuente = fechas.get(rel) or fechas.get(rel[:-3] + ".canvas")
            if not fuente:
                continue
            p = os.path.join(d, f)
            with open(p, encoding="utf-8") as fh:
                t = fh.read()
            fm, cuerpo = frontmatter(t)
            extra = f"created: {fuente[0]}\nmodified: {fuente[1]}\n"
            fm = fm.replace("---\n", "---\n" + extra, 1) if fm else f"---\n{extra}---\n"
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(fm + cuerpo)

    # Portadas
    tarjetas = []
    for v, (titulo, inicio, desc) in VAULTS.items():
        with open(os.path.join(destino, v, "index.md"), "w", encoding="utf-8") as fh:
            fh.write(f"---\ntitle: \"{titulo}\"\n---\nVault `{v}`. {desc}\n\nEmpezá por [[{inicio}]].\n")
        tarjetas.append(f"- **[[{inicio}|{titulo}]]**: {desc}")
    with open(os.path.join(destino, "index.md"), "w", encoding="utf-8") as fh:
        fh.write(
            "---\ntitle: Colegio\n---\n"
            "Las notas del colegio, publicadas desde Obsidian. Se actualizan solas cada vez que se suben cambios al repositorio.\n\n"
            "## Vaults\n" + "\n".join(tarjetas) + "\n\n"
            "> [!tip] Cómo moverse\n"
            "> A la izquierda está el **explorador** de carpetas, como en Obsidian. A la derecha, el **grafo** de enlaces y los **backlinks** de cada nota. "
            "Con **Ctrl+K** (o la lupa) se busca en todas las notas.\n"
        )
    print("Contenido listo en", destino)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
