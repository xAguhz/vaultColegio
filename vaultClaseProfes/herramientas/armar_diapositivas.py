"""Arma una presentación web autónoma con las diapositivas de la charla.

Uso: python3 armar_diapositivas.py
Lee  herramientas/diapositivas/project/ (deck.json, deck.css, slides/*.html, la misma fuente que el Artifact)
Crea Exposición/Diapositivas.html (el workflow la publica como vaultClaseProfes/diapositivas/).

Controles: → / espacio / clic = avanzar · ← = volver · F = pantalla completa · N = notas del orador.
"""
import html
import json
import pathlib
import re

VAULT = pathlib.Path(__file__).resolve().parent.parent
FUENTE = VAULT / "herramientas" / "diapositivas" / "project"
SALIDA = VAULT / "Exposición" / "Diapositivas.html"
# Las imágenes subidas al Artifact (/_blob/…) se reemplazan por su archivo en el vault
BLOBS = {"/_blob/377f02564864fb37bf11728454f7438d": "../Adjuntos/qr_guia.png"}

# Íconos (trazos al estilo Feather/Lucide, licencia libre), dibujados con currentColor
ICONOS = {
    "Lightning": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "Wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "Tool": '<path d="m15 12-8.5 8.5a2.12 2.12 0 0 1-3-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25a3.2 3.2 0 0 1-.93-2.25v-.86L16 4.6a5.56 5.56 0 0 0-3.94-1.64H9l.92.82A6.18 6.18 0 0 1 12 8.4v1.56l2 2h2.47l2.26 1.91"/>',
    "Play": '<polygon points="6 3 20 12 6 21 6 3"/>',
    "Settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "CheckCircle": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "Warning": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "Lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "Search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "Verified": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
}

BASE_CSS = """
* { margin: 0; }
html, body { height: 100%; background: #0f1719; overflow: hidden; }
body { font: 32px/1.2 sans-serif; }
#escenario { position: absolute; left: 50%; top: 50%; width: 1920px; height: 1080px; transform-origin: 0 0; }
#escenario > section { position: absolute; inset: 0; width: 1920px; height: 1080px; overflow: hidden; box-sizing: border-box; isolation: isolate; }
#escenario > section:not(.activa) { display: none !important; }
aside { display: none !important; }
x-icon, x-shape { display: block; }
x-icon svg { width: 100%; height: 100%; display: block; }
x-shape[kind="arrow-right"] { clip-path: polygon(0 30%, 60% 30%, 60% 0, 100% 50%, 60% 100%, 60% 70%, 0 70%); }
#barra { position: fixed; left: 0; right: 0; bottom: 0; display: flex; justify-content: space-between; align-items: center;
  padding: 6px 14px; font: 13px/1.3 system-ui, sans-serif; color: #c9d6d3; background: #0f1719cc; opacity: 0; transition: opacity .3s; }
body:hover #barra, body.mostrar-barra #barra { opacity: 1; }
#barra button { font: inherit; color: inherit; background: #24373d; border: 0; border-radius: 6px; padding: 4px 10px; cursor: pointer; margin-left: 6px; }
#notas { position: fixed; left: 0; right: 0; bottom: 34px; max-height: 32vh; overflow: auto; display: none;
  padding: 14px 18px; font: 16px/1.45 system-ui, sans-serif; color: #f6f1e6; background: #1b2a2ff2; border-top: 3px solid #e8743b; }
body.con-notas #notas { display: block; }
@media print { #barra, #notas { display: none !important; } }
"""

JS = """
const slides = [...document.querySelectorAll('#escenario > section')];
const esc = document.getElementById('escenario');
let i = 0;
function escalar() {
  const k = Math.min(innerWidth / 1920, innerHeight / 1080);
  esc.style.transform = `scale(${k}) translate(-50%, -50%)`;
}
function frags(s) { return [...s.querySelectorAll('.fragment')]; }
function mostrar(n, todos) {
  i = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach((s, k) => s.classList.toggle('activa', k === i));
  frags(slides[i]).forEach(f => f.classList.toggle('visible', !!todos));
  const nota = slides[i].querySelector('aside');
  document.getElementById('notas').textContent = nota ? nota.textContent : '(Sin notas)';
  document.getElementById('cont').textContent = `${i + 1} / ${slides.length}`;
  history.replaceState(null, '', '#' + (i + 1));
  programarFin();
}
// Las animaciones de entrada arrancan transparentes: si el navegador las frena (pestaña en segundo plano,
// compu lenta), el texto queda a medio aparecer. Se fuerzan al estado final al rato y al tocar cualquier cosa.
let tFin = null;
function terminarAnimaciones() {
  const s = slides[i];
  if (s.getAnimations) s.getAnimations({ subtree: true }).forEach(a => { try { a.finish(); } catch (e) {} });
}
function programarFin() { clearTimeout(tFin); tFin = setTimeout(terminarAnimaciones, 1500); }
function avanzar() {
  const f = frags(slides[i]).find(f => !f.classList.contains('visible'));
  if (f) f.classList.add('visible'); else if (i < slides.length - 1) mostrar(i + 1);
}
function volver() { if (i > 0) mostrar(i - 1, true); }
function pantalla() { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
addEventListener('keydown', () => terminarAnimaciones(), true);
addEventListener('pointerdown', () => terminarAnimaciones(), true);
addEventListener('keydown', e => {
  if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); avanzar(); }
  else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); volver(); }
  else if (e.key === 'Home') mostrar(0);
  else if (e.key === 'End') mostrar(slides.length - 1, true);
  else if (e.key.toLowerCase() === 'f') pantalla();
  else if (e.key.toLowerCase() === 'n') document.body.classList.toggle('con-notas');
});
document.addEventListener('click', e => {
  if (e.target.closest('#barra, #notas, a')) return;
  (e.clientX < innerWidth / 3 ? volver : avanzar)();
});
let x0 = null;
addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
addEventListener('touchend', e => {
  if (x0 === null) return; const d = e.changedTouches[0].clientX - x0; x0 = null;
  if (Math.abs(d) > 40) (d < 0 ? avanzar : volver)();
});
document.getElementById('b-ant').onclick = volver;
document.getElementById('b-sig').onclick = avanzar;
document.getElementById('b-pant').onclick = pantalla;
document.getElementById('b-notas').onclick = () => document.body.classList.toggle('con-notas');
addEventListener('resize', escalar);
escalar();
const h = parseInt(location.hash.slice(1), 10);
mostrar(Number.isFinite(h) ? h - 1 : 0);
// Si la página cargó en segundo plano o antes que las tipografías, la animación de entrada puede no verse: se repite
function reanimar() { const s = slides[i]; s.classList.remove('activa'); void s.offsetWidth; s.classList.add('activa'); programarFin(); }
document.fonts && document.fonts.ready.then(reanimar);
document.addEventListener('visibilitychange', () => { if (!document.hidden) terminarAnimaciones(); });
document.body.classList.add('mostrar-barra');
setTimeout(() => document.body.classList.remove('mostrar-barra'), 3000);
"""


def icono(m):
    nombre = m.group(1)
    attrs = m.group(0)[:-1]  # la etiqueta de apertura sin el ">"
    trazos = ICONOS.get(nombre, '<circle cx="12" cy="12" r="9"/>')
    svg = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
           f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{trazos}</svg>')
    return f'{attrs} role="img" aria-label="{html.escape(nombre)}">{svg}'


def main():
    deck = json.loads((FUENTE / "deck.json").read_text())
    css = (FUENTE / "deck.css").read_text()
    fuentes = "\n".join(f'<link rel="stylesheet" href="{html.escape(f["href"])}">'
                        for f in deck["faces"].values() if f.get("href"))
    partes = []
    for sid in deck["order"]:
        s = (FUENTE / "slides" / f"{sid}.html").read_text()
        for blob, archivo in BLOBS.items():
            s = s.replace(blob, archivo)
        s = re.sub(r'<x-icon name="([^"]+)"[^>]*>', icono, s)
        partes.append(s.strip())
    pagina = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(deck["title"])} · Diapositivas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
{fuentes}
<style>{BASE_CSS}</style>
<style>{css}</style>
</head>
<body>
<div id="escenario">
{chr(10).join(partes)}
</div>
<div id="notas"></div>
<div id="barra"><span>← → o clic para avanzar · F pantalla completa · N notas del orador</span>
<span><span id="cont"></span><button id="b-ant" aria-label="Anterior">←</button><button id="b-sig" aria-label="Siguiente">→</button><button id="b-notas">Notas</button><button id="b-pant">Pantalla completa</button></span></div>
<script>{JS}</script>
</body>
</html>
"""
    SALIDA.write_text(pagina)
    print(f"{SALIDA} ({len(deck['order'])} diapositivas, {len(pagina) // 1024} KB)")


if __name__ == "__main__":
    main()
