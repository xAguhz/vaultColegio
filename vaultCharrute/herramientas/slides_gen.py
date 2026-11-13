"""Genera los pedidos de Google Slides para una presentación de TP (plantilla del TP8 de compresores).

Uso: python3 slides_gen.py <salida_dir>   → escribe lote1.json, lote2.json... para update_presentation.
Los nombres de los integrantes NO van en el repo (es público): completá INTEGRANTES antes de correrlo.
La carátula y las diapositivas 1 y 2 están escritas para rehacer un deck existente (borran s01_cover y s02_sistema);
para un deck nuevo, sacá esos deleteObject y el insertionIndex.
"""
import json, sys

EMU = 914400
IMG = 'https://xaguhz.github.io/vaultColegio/vaultCharrute/Adjuntos/Gemini/'
BG, INK, MUTED = '#F7F8FA', '#1C2430', '#5B6675'
BLUE, ORANGE, DARK = '#1F5F99', '#E07B24', '#16324F'
LBLUE, LORANGE, WHITE = '#E3ECF5', '#FBE7D6', '#FFFFFF'
HFONT, BFONT = 'Montserrat', 'Arial'
# Completar en la copia local (no commitear nombres): una pareja por línea en INTEGRANTES.
PAREJAS = ['Integrante 1\nIntegrante 2', 'Integrante 3\nIntegrante 4', 'Integrante 5\nIntegrante 6']
INTEGRANTES = '\n'.join(p.replace('\n', ' · ') for p in PAREJAS)
ASPECT = {'portada': 1376 / 768, 'sistema_aire': 1376 / 768, 'secadores': 1376 / 768, 'caldera': 1376 / 768,
          'piston': 1200 / 896, 'compresor': 1200 / 896, 'centrifugo': 1200 / 896, 'fuga': 1200 / 896, 'recipiente': 1200 / 896}


def rgb(h):
    h = h.lstrip('#')
    return {'red': round(int(h[0:2], 16) / 255, 3), 'green': round(int(h[2:4], 16) / 255, 3), 'blue': round(int(h[4:6], 16) / 255, 3)}


def e(v):
    return int(round(v * EMU))


def props(page, x, y, w, h):
    return {'pageObjectId': page, 'size': {'width': {'magnitude': e(w), 'unit': 'EMU'}, 'height': {'magnitude': e(h), 'unit': 'EMU'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': e(x), 'translateY': e(y), 'unit': 'EMU'}}


class Deck:
    def __init__(self):
        self.batches = [[]]
        self.n = 0

    @property
    def r(self):
        return self.batches[-1]

    def new_batch(self):
        self.batches.append([])

    def slide(self, sid, bg=BG, index=None):
        self.cur = sid
        self.n = 0
        cs = {'objectId': sid, 'slideLayoutReference': {'predefinedLayout': 'BLANK'}}
        if index is not None:
            cs['insertionIndex'] = index
        self.r.append({'createSlide': cs})
        self.r.append({'updatePageProperties': {'objectId': sid, 'pageProperties': {'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': rgb(bg)}}}},
                                                'fields': 'pageBackgroundFill.solidFill.color'}})

    def oid(self, kind):
        self.n += 1
        return f'{self.cur}_{kind}{self.n}'

    def shape(self, kind, x, y, w, h, fill=None, text=None, size=16, bold=False, color=INK, align='START', valign=None,
              font=BFONT, italic=False, space_below=None, bullets=False):
        oid = self.oid('t' if kind == 'TEXT_BOX' else 's')
        self.r.append({'createShape': {'objectId': oid, 'shapeType': kind, 'elementProperties': props(self.cur, x, y, w, h)}})
        sp, f = {}, []
        if fill:
            sp['shapeBackgroundFill'] = {'solidFill': {'color': {'rgbColor': rgb(fill)}}}
            f.append('shapeBackgroundFill.solidFill.color')
        if kind != 'TEXT_BOX':
            sp['outline'] = {'propertyState': 'NOT_RENDERED'}
            f.append('outline.propertyState')
        if valign:
            sp['contentAlignment'] = valign
            f.append('contentAlignment')
        if f:
            self.r.append({'updateShapeProperties': {'objectId': oid, 'shapeProperties': sp, 'fields': ','.join(f)}})
        if text:
            self.r.append({'insertText': {'objectId': oid, 'text': text}})
            st = {'fontSize': {'magnitude': size, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': {'rgbColor': rgb(color)}}}
            if bold:
                st['bold'] = True
            if italic:
                st['italic'] = True
            st['fontFamily'] = font
            self.r.append({'updateTextStyle': {'objectId': oid, 'textRange': {'type': 'ALL'}, 'style': st, 'fields': ','.join(st)}})
            ps, pf = {}, []
            if align != 'START':
                ps['alignment'] = align
                pf.append('alignment')
            if space_below is not None:
                ps['spaceBelow'] = {'magnitude': space_below, 'unit': 'PT'}
                pf.append('spaceBelow')
            if pf:
                self.r.append({'updateParagraphStyle': {'objectId': oid, 'textRange': {'type': 'ALL'}, 'style': ps, 'fields': ','.join(pf)}})
            if bullets:
                self.r.append({'createParagraphBullets': {'objectId': oid, 'textRange': {'type': 'ALL'}, 'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'}})
        return oid

    def text(self, x, y, w, h, text, **kw):
        return self.shape('TEXT_BOX', x, y, w, h, text=text, **kw)

    def style_range(self, oid, start, end, **st):
        style, f = {}, []
        if 'bold' in st:
            style['bold'] = st['bold']; f.append('bold')
        if 'color' in st:
            style['foregroundColor'] = {'opaqueColor': {'rgbColor': rgb(st['color'])}}; f.append('foregroundColor')
        if 'size' in st:
            style['fontSize'] = {'magnitude': st['size'], 'unit': 'PT'}; f.append('fontSize')
        self.r.append({'updateTextStyle': {'objectId': oid, 'textRange': {'type': 'FIXED_RANGE', 'startIndex': start, 'endIndex': end},
                                           'style': style, 'fields': ','.join(f)}})

    def title(self, text, color=INK):
        return self.text(0.5, 0.32, 9.0, 0.95, text, size=28, bold=True, color=color, font=HFONT, valign='MIDDLE')

    def image(self, name, x, y, w=None, h=None):
        a = ASPECT[name]
        if w is None:
            w = h * a
        else:
            h = w / a
        oid = self.oid('img')
        self.r.append({'createImage': {'objectId': oid, 'url': IMG + name + '.png', 'elementProperties': props(self.cur, x, y, w, h)}})
        return w, h

    def arrow(self, x, y, w, h, down=False, color='#9AA5B4'):
        return self.shape('DOWN_ARROW' if down else 'RIGHT_ARROW', x, y, w, h, fill=color)

    def footnote(self, text):
        return self.text(0.5, 5.18, 9.0, 0.32, text, size=10, color=MUTED)


d = Deck()

# 1 · Carátula (rehecha)
d.r.append({'deleteObject': {'objectId': 's01_cover'}})
d.r.append({'deleteObject': {'objectId': 's02_sistema'}})
d.slide('s01b_cover', DARK, index=0)
d.text(0.6, 0.4, 8.8, 0.35, 'SISTEMAS MECÁNICOS · 7° 1°', size=14, bold=True, color=ORANGE, font=HFONT)
d.text(0.6, 0.8, 8.8, 0.75, 'Trabajo Práctico N° 8', size=36, bold=True, color=WHITE, font=HFONT)
d.text(0.6, 1.5, 8.8, 0.5, 'Compresores de aire y sistemas de aire comprimido', size=20, color='#BFD3E6', font=HFONT)
t = d.text(0.6, 2.35, 4.5, 0.4, 'Profesor: Carlos Charrute', size=16, color=WHITE)
d.style_range(t, 0, 9, bold=True, color=ORANGE)
d.text(0.6, 2.85, 4.5, 0.35, 'Integrantes', size=14, bold=True, color=ORANGE)
d.text(0.6, 3.2, 4.6, 1.05, INTEGRANTES,
       size=15, color=WHITE, space_below=2)
d.text(0.6, 4.35, 4.5, 0.4, 'Fecha: 13 de noviembre de 2026', size=14, color='#BFD3E6')
d.text(0.6, 5.12, 8.8, 0.32, 'EEST N° 3 "15 de Noviembre" · San Antonio de Padua · Ciclo lectivo 2026', size=10, color='#8FA3B8')
d.image('portada', 5.35, 2.3, w=4.15)

# 2 · Sistema
d.slide('s02b_sistema', index=1)
d.title('Un compresor solo no alcanza: el aire recorre un sistema')
d.image('sistema_aire', 0.5, 1.5, w=5.2)
steps = [('Producir', 'eleva la presión'), ('Tratar', 'enfría, seca y filtra'),
         ('Almacenar', 'amortigua los picos'), ('Distribuir', 'lleva el aire al consumo'),
         ('Consumir', 'herramientas y cilindros')]
for i, (a, b) in enumerate(steps):
    y = 1.4 + i * 0.73
    d.shape('ELLIPSE', 6.0, y + 0.06, 0.5, 0.5, fill=BLUE if i != 1 else ORANGE, text=str(i + 1), size=16, bold=True,
            color=WHITE, align='CENTER', valign='MIDDLE')
    t = d.text(6.6, y, 2.9, 0.65, f'{a}\n{b}', size=14, color=MUTED, valign='MIDDLE')
    d.style_range(t, 0, len(a), bold=True, color=INK, size=16)


# 4 · Compresión
d.slide('s04_compresion')
d.title('Comprimir aire también lo calienta y le concentra la humedad')
d.image('compresor', 0.5, 1.4, w=4.4)
rows = [('▼  Volumen', 'el aire queda encerrado en menos espacio', BLUE), ('▲  Presión', 'es la energía útil que llega a la herramienta', BLUE),
        ('▲  Temperatura', 'hay que refrigerar el compresor y el aire', ORANGE)]
for i, (a, b, col) in enumerate(rows):
    y = 1.4 + i * 0.95
    d.shape('ROUND_RECTANGLE', 5.2, y, 4.3, 0.82, fill=LBLUE if col == BLUE else LORANGE)
    t = d.text(5.35, y + 0.04, 4.05, 0.74, f'{a}\n{b}', size=14, color=MUTED, valign='MIDDLE')
    d.style_range(t, 0, len(a), bold=True, color=col, size=18)
t = d.text(5.2, 4.3, 4.3, 0.75, 'Bomba ≠ compresor: la bomba mueve líquidos que casi no se comprimen.', size=14, color=INK)
d.style_range(t, 0, 17, bold=True)

# 5 · Tecnologías
d.slide('s05_tecnologias')
d.title('Cada tecnología responde a un tipo de demanda')
techs = [('piston', 'Pistón', 'Consumo chico e intermitente. Entrega pulsante'),
         ('compresor', 'Tornillo', 'Demanda continua y estable. Aire sin pulsaciones'),
         ('centrifugo', 'Centrífugo', 'Caudales muy grandes en servicio continuo')]
for i, (img, head, cap) in enumerate(techs):
    x = 0.5 + i * 3.08
    d.shape('ROUND_RECTANGLE', x, 1.35, 2.84, 3.75, fill=WHITE)
    d.image(img, x + 0.12, 1.45, w=2.6)
    d.text(x + 0.15, 3.45, 2.55, 0.45, head, size=18, bold=True, color=BLUE, font=HFONT)
    d.text(x + 0.15, 3.9, 2.55, 1.05, cap, size=14, color=INK)

# 6 · Interenfriador
d.slide('s06_etapas')
d.title('El interenfriador reduce el trabajo de la segunda etapa')
d.image('piston', 0.5, 1.4, w=4.6)
chain = [('Etapa 1', 'comprime el aire en parte'), ('Interenfriador', 'baja la temperatura'), ('Etapa 2', 'comprime un aire más frío y con menos volumen')]
for i, (a, b) in enumerate(chain):
    y = 1.35 + i * 0.95
    d.shape('ROUND_RECTANGLE', 5.4, y, 4.1, 0.7, fill=LBLUE if i != 1 else LORANGE)
    t = d.text(5.55, y + 0.02, 3.85, 0.66, f'{a}: {b}', size=14, color=INK, valign='MIDDLE')
    d.style_range(t, 0, len(a) + 1, bold=True, color=BLUE if i != 1 else ORANGE)
    if i < 2:
        d.arrow(7.3, y + 0.72, 0.3, 0.2, down=True)
d.shape('ROUND_RECTANGLE', 5.4, 4.25, 4.1, 0.8, fill=BLUE, text='Resultado: menos trabajo y menor temperatura final',
        size=15, bold=True, color=WHITE, valign='MIDDLE')

d.new_batch()

# 7 · Agua y punto de rocío
d.slide('s07_agua')
d.title('El agua aparece cuando el aire comprimido se enfría')
flow = [('Aire húmedo', 'el compresor aspira vapor de agua'), ('Compresión', 'el vapor queda concentrado'),
        ('Enfriamiento', 'en el tanque o en la red'), ('Condensado', 'agua líquida en las cañerías')]
for i, (a, b) in enumerate(flow):
    x = 0.5 + i * 2.33
    d.shape('ROUND_RECTANGLE', x, 1.45, 2.0, 1.25, fill=LBLUE if i < 3 else LORANGE)
    t = d.text(x + 0.1, 1.5, 1.8, 1.15, f'{a}\n{b}', size=14, color=MUTED, align='CENTER', valign='MIDDLE')
    d.style_range(t, 0, len(a), bold=True, color=BLUE if i < 3 else ORANGE, size=16)
    if i < 3:
        d.arrow(x + 2.03, 1.93, 0.27, 0.3)
d.shape('ROUND_RECTANGLE', 0.5, 3.0, 9.0, 1.05, fill=WHITE)
t = d.text(0.7, 3.05, 8.6, 0.95, 'Punto de rocío a presión: temperatura a la que el agua empieza a condensar. Si la red nunca baja de ese valor, no aparece agua líquida.',
           size=15, color=INK, valign='MIDDLE')
d.style_range(t, 0, 25, bold=True, color=BLUE)
d.text(0.5, 4.3, 9.0, 0.7, 'El agua sin drenar provoca corrosión en la red, daña herramientas y hace fallar instrumentos: por eso se separa, se purga y se seca.',
       size=14, color=MUTED)

# 8 · Secadores
d.slide('s08_secadores')
d.title('Frigorífico para la planta; adsorción solo donde hace falta')
d.image('secadores', 0.5, 1.5, w=5.4)
dry = [('Frigorífico', 'Enfría el aire para que el agua condense.\nPunto de rocío moderado, menor costo.\nAire de planta y herramientas.', BLUE, LBLUE),
       ('Adsorción', 'Un desecante retiene el vapor.\nPunto de rocío muy bajo, más consumo.\nInstrumentos, alimentos, farmacia.', ORANGE, LORANGE)]
for i, (a, b, col, fill) in enumerate(dry):
    y = 1.4 + i * 1.85
    d.shape('ROUND_RECTANGLE', 6.15, y, 3.35, 1.7, fill=fill)
    d.text(6.3, y + 0.08, 3.1, 0.4, a, size=17, bold=True, color=col, font=HFONT)
    d.text(6.3, y + 0.5, 3.1, 1.15, b, size=14, color=INK)

# 9 · Potencia específica
d.slide('s09_eficiencia')
d.title('Potencia específica: cuánta energía cuesta cada m³ de aire')
comp = [('BOGE S 55-4 LF N', 'ficha a 100 psig (6,9 bar)', 16.72, 22.54, BLUE),
        ('Atlas Copco GA45 VSD', 'ficha a 125 psig (8,6 bar)', 20.4, 27.4, ORANGE)]
for i, (name, pres, full, low, col) in enumerate(comp):
    y = 1.4 + i * 1.55
    t = d.text(0.5, y, 3.0, 1.3, f'{str(full).replace(".", ",")}\nkW por 100 acfm', size=14, color=MUTED, valign='MIDDLE')
    d.style_range(t, 0, len(str(full)), bold=True, color=col, size=40)
    d.text(3.5, y, 3.6, 0.4, name, size=15, bold=True, color=INK)
    d.text(3.5, y + 0.38, 3.6, 0.35, pres, size=14, color=MUTED)
    scale = 0.075
    d.shape('RECTANGLE', 3.5, y + 0.82, full * scale, 0.22, fill=col)
    d.text(3.5 + full * scale + 0.05, y + 0.76, 1.6, 0.32, 'caudal máximo', size=11, color=MUTED)
    d.shape('RECTANGLE', 3.5, y + 1.1, low * scale, 0.22, fill='#B9C2CD')
    d.text(3.5 + low * scale + 0.05, y + 1.04, 1.6, 0.32, f'{str(low).replace(".", ",")} a caudal mínimo', size=11, color=MUTED)
d.shape('ROUND_RECTANGLE', 7.25, 1.45, 2.25, 3.5, fill=WHITE)
d.text(7.35, 1.55, 2.05, 3.3, 'Las fichas están a distinta presión: no se comparan directo.\n\nA bajo caudal, el aire sale más caro.\n\nLa potencia del motor no mide la eficiencia.',
       size=14, color=INK)
d.footnote('Fuente: fichas CAGI de Atlas Copco GA45VSD-175 AP (2012) y BOGE S 55-4 LF N (2025); caudal medido según ISO 1217, Anexo E.')

d.new_batch()

# 10 · Control
d.slide('s10_control')
d.title('El método de control se elige según cómo varía la demanda')
ctl = [('Arranque y parada', 'Para al llegar a la presión máxima y arranca en la mínima', 'Equipos chicos, consumo intermitente'),
       ('Carga-descarga', 'El motor sigue girando; alterna entre producir y no producir', 'Equipos grandes; en vacío igual consume'),
       ('Velocidad variable', 'El variador ajusta las RPM a la demanda', 'Demanda muy variable a lo largo del día')]
for i, (a, b, c) in enumerate(ctl):
    x = 0.5 + i * 3.08
    d.shape('ROUND_RECTANGLE', x, 1.4, 2.84, 2.6, fill=WHITE)
    d.text(x + 0.18, 1.5, 2.5, 0.45, a, size=17, bold=True, color=BLUE, font=HFONT)
    d.text(x + 0.18, 2.0, 2.5, 1.0, b, size=14, color=INK)
    d.text(x + 0.18, 3.05, 2.5, 0.85, c, size=14, color=MUTED)
d.shape('ROUND_RECTANGLE', 0.5, 4.25, 9.0, 0.8, fill=LORANGE,
        text='El tanque guarda aire, no lo produce: un tanque más grande no reemplaza a un compresor chico.',
        size=15, bold=True, color=INK, valign='MIDDLE')

# 11 · Fugas
d.slide('s11_fugas')
d.title('Las fugas pierden aire las 24 horas, aun con la planta parada')
d.image('fuga', 0.5, 1.4, w=4.4)
d.text(5.2, 1.35, 4.3, 0.9, '20 a 30 %', size=44, bold=True, color=ORANGE, font=HFONT)
d.text(5.2, 2.2, 4.3, 0.75, 'de la producción del compresor puede perderse en fugas, en algunos casos.', size=15, color=INK)
d.text(5.2, 3.1, 4.3, 1.9, 'Detector ultrasónico en uniones y acoples\nPrueba de caída de presión con la planta sin consumo\nAgua jabonosa en uniones puntuales',
       size=14, color=INK, bullets=True, space_below=6)
d.footnote('Fuente: U.S. Department of Energy y Compressed Air Challenge, Fact Sheet 7: Compressed Air System Leaks.')

# 12 · Diagnóstico
d.slide('s12_diagnostico')
d.title('Si falta presión, medimos antes de comprar otro compresor')
diag = [('Producción', 'Horas en carga y presión de consigna'), ('Tratamiento', 'Caída de presión en filtros y secador'),
        ('Depósito', 'Agua acumulada y arranques por hora'), ('Distribución', 'Fugas y presión en los extremos'),
        ('Consumo', 'Usos indebidos y equipos nuevos')]
for i, (a, b) in enumerate(diag):
    x = 0.5 + i * 1.86
    d.shape('ROUND_RECTANGLE', x, 1.45, 1.62, 0.6, fill=BLUE, text=a, size=14, bold=True, color=WHITE, align='CENTER', valign='MIDDLE')
    d.text(x, 2.15, 1.62, 1.2, b, size=14, color=INK, align='CENTER')
    if i < 4:
        d.arrow(x + 1.64, 1.62, 0.2, 0.26)
d.shape('ROUND_RECTANGLE', 0.5, 3.75, 9.0, 1.25, fill=LORANGE)
t = d.text(0.7, 3.8, 8.6, 1.15, 'Subir la presión del compresor no corrige una red mala: aumenta el consumo eléctrico y las fugas, y la causa sigue ahí.',
           size=16, color=INK, valign='MIDDLE')
d.style_range(t, 0, 54, bold=True, color=ORANGE)

# 13 · Cierre
d.slide('s13_cierre', DARK)
d.text(0.8, 0.9, 8.4, 0.4, 'IDEA FUERZA DEL GRUPO', size=14, bold=True, color=ORANGE, font=HFONT)
d.text(0.8, 1.4, 8.4, 1.6, 'Antes de comprar un compresor más grande o subir la presión, hay que medir el sistema.',
       size=30, bold=True, color=WHITE, font=HFONT)
d.text(0.8, 3.15, 8.4, 0.8, 'El aire comprimido es caro: lo más barato es no desperdiciarlo.', size=20, color='#BFD3E6')
d.text(0.8, 4.4, 8.4, 0.5, '¿Preguntas?', size=20, bold=True, color=ORANGE, font=HFONT)

out = sys.argv[1]
for i, b in enumerate(d.batches):
    json.dump(b, open(f'{out}/lote{i + 1}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    print(f'lote{i + 1}: {len(b)} pedidos, {len(json.dumps(b, ensure_ascii=False, separators=(",", ":")))} caracteres')
