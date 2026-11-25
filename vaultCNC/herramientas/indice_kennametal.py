#!/usr/bin/env python3
"""Arma Kennametal/00 Kennametal.md: índice de la transcripción del catálogo, agrupado por comando.

Lee el encabezado (frontmatter) de cada nota de Kennametal/<sección>/:
  comando: T0101 | T0303 | T0505 | otros | no-torno   (puede traer dos: "T0101 | T0303")
  ajedrez: alta | media | baja | no
  paginas: "A10 (PDF 16)"
Uso: python3 indice_kennametal.py   (la carpeta Kennametal/ es local, no se sube al repositorio)
"""
import glob
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
KEN = os.path.join(AQUI, "..", "Kennametal")

GRUPOS = [
    ("T0101", "T0101: desbaste", "Insertos y portaherramientas robustos para el desbaste con G90 (C 80°, W 80°, S 90°, T 60°; rompevirutas RP, RN y MP)."),
    ("T0303", "T0303: definición del perfil", "Herramientas que copian el perfil: insertos V 35° y D 55°, portaherramientas que cortan hacia atrás (DVJN, DVVNN, SVJB, SDJC) y rompevirutas de acabado (FP, LF)."),
    ("T0505", "T0505: ranurado y tronzado", "Ranurado exterior, ranurado y torneado A4, Top Notch y tronzado A2."),
    ("otros", "Otras herramientas de torno", "Roscado, interiores (mandrilar, ranurado interior), brocas en el contrapunto y módulos KM para torretas."),
    ("no-torno", "No son de torno", "Fresado, conos y portaherramientas de centro de mecanizado, pinzas y tirantes."),
]
ORDEN_AJ = {"alta": 0, "media": 1, "baja": 2, "no": 3, "-": 4}


def campo(fm, k):
    m = re.search(r"^%s:\s*(.*)$" % k, fm, re.M)
    return m.group(1).strip().strip('"') if m else "-"


def main():
    notas = []
    for f in sorted(glob.glob(os.path.join(KEN, "*", "*.md"))):
        texto = open(f, encoding="utf-8").read()
        fm = texto.split("---")[1] if texto.startswith("---") else ""
        nombre = os.path.basename(f)[:-3]
        if nombre.startswith("00 "):
            continue
        notas.append({
            "seccion": os.path.basename(os.path.dirname(f)),
            "nombre": nombre,
            "comandos": [c.strip() for c in campo(fm, "comando").split("|")],
            "ajedrez": campo(fm, "ajedrez").split()[0] if campo(fm, "ajedrez") != "-" else "-",
            "paginas": campo(fm, "paginas"),
        })
    secciones = sorted({n["seccion"] for n in notas})

    out = ["---", "tags: [kennametal, indice]", "---",
           "# Catálogo Kennametal (transcripción)", "",
           "Transcripción local del catálogo **Kennametal Universal** (264 páginas). "
           "Es material de Kennametal: la carpeta no se sube al repositorio público.", "",
           "- **Cómo están las páginas:** sección A, torneado (página del PDF = etiqueta + 6); "
           "B, brocas (PDF = etiqueta + 118); C, fresado (PDF = etiqueta + 148); D, sistemas de sujeción (PDF = etiqueta + 196).",
           "- **Datos dudosos:** donde la página no se leía bien, la nota lo marca con `(?)`.",
           "- **Qué conviene usar en el TP:** [[Herramientas para piezas de ajedrez]].", "",
           "## Secciones"]
    for s in secciones:
        out.append("- [[00 %s]]" % s.split(" ", 1)[1] if os.path.exists(os.path.join(KEN, s, "00 %s.md" % s.split(" ", 1)[1])) else "- %s" % s)
    out.append("")
    out.append("## Por comando")
    out.append("La columna **Ajedrez** dice cuánto sirve la herramienta para las piezas del TP.")
    for clave, titulo, desc in GRUPOS:
        grupo = [n for n in notas if clave in n["comandos"]]
        if not grupo:
            continue
        out += ["", "### " + titulo, desc, "", "| Nota | Ajedrez | Páginas | Sección |", "|---|---|---|---|"]
        for n in sorted(grupo, key=lambda n: (ORDEN_AJ.get(n["ajedrez"], 4), n["nombre"])):
            aj = "**alta**" if n["ajedrez"] == "alta" else n["ajedrez"]
            out.append("| [[%s]] | %s | %s | %s |" % (n["nombre"], aj, n["paginas"], n["seccion"]))
    sin = [n for n in notas if not any(c in [g[0] for g in GRUPOS] for c in n["comandos"])]
    if sin:
        out += ["", "### Sin clasificar", ""] + ["- [[%s]]" % n["nombre"] for n in sin]
    ruta = os.path.join(KEN, "00 Kennametal.md")
    open(ruta, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("%s: %d notas" % (ruta, len(notas)))


if __name__ == "__main__":
    main()
