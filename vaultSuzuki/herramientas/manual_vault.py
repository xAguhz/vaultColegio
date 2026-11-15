"""Genera la carpeta "Manual de taller/" del vault a partir de manual_datos.json.

Uso: python3 herramientas/manual_vault.py

- Una nota por capítulo del manual de taller (Swift 2005-2010, edición en castellano):
  resumen propio, temas con enlace a la página del PDF, componentes de cada despiece,
  valores estándar/límite, pares de apriete, códigos de falla y herramientas especiales.
- Notas de índice: índice general, códigos de falla, pares de apriete, herramientas, conectores.
- Una nota por circuito eléctrico con un esquema propio (Mermaid), fusibles, conectores y colores.

El PDF original queda en "Manual de taller/PDF/" (excluido de git: no se publica).
Los resúmenes están escritos con palabras propias; del manual solo se toman datos técnicos.
"""
import json
import os
import re

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(VAULT, 'Manual de taller')
PDF = 'Manual de taller Swift 2005-2010.pdf'
D = json.load(open(os.path.join(VAULT, 'herramientas', 'manual_datos.json'), encoding='utf-8'))
CAP, MAPA, CIRC, CON = D['capitulos'], D['mapa_paginas'], D['circuitos'], D['conectores']
# correcciones de conectores mal leídos de las tablas (verificados en el PDF o marcados para revisar)
for _k, _v in {'C08': 'Sensor de CMP', 'C14': 'Válvula de purga del recipiente de EVAP'}.items():
    if _k in CON:
        CON[_k][1] = _v
for _k, _v in CON.items():
    if re.match(r'^([A-Z]\d{2}/|o$|vehículo$)', _v[1]):
        _v[1] = '(ver la página del PDF)'

# ------------------------------------------------------------------ resúmenes propios por capítulo
R = {
    '00': 'Advertencias generales antes de trabajar: airbags (se desactivan desconectando la batería y esperando 90 s), manejo de líquidos y del sistema de combustible, levantar el auto por los puntos indicados y precauciones con los módulos electrónicos y los conectores.',
    '0A': 'Cómo está organizado el manual, cómo identificar el auto (número de chasis y de motor), abreviaturas, colores de cables, tipos de conectores y la tabla de pares de apriete para bulones sin valor propio. Incluye la ubicación general de los componentes.',
    '0B': 'Plan de mantenimiento en uso normal y en uso severo, y cómo hacer cada tarea: correas, aceite y filtro, refrigerante, bujías, filtros de aire y de combustible, frenos, neumáticos, suspensión, caja y una revisión final en ruta. Ver también la nota 08 del vault.',
    '1': 'Precauciones propias del capítulo del motor.',
    '1A': 'El corazón electrónico del motor: cómo la computadora (ECM) maneja la inyección, el encendido, el ralentí, el VVT, el ventilador y el aire acondicionado; ubicación de sensores y actuadores; cómo leer los datos con el escáner; y el diagnóstico paso a paso de cada código de falla P.',
    '1B': 'Dispositivos que bajan las emisiones fuera del escape: recirculación de gases (EGR), ventilación del cárter (PCV) y el sistema de vapores de nafta (canister EVAP y válvula de purga).',
    '1C': 'Sensores y actuadores eléctricos del motor (temperatura, posición de mariposa, caudal de aire, presión del colector, posición de cigüeñal y levas, detonación) con sus valores de prueba y cómo cambiarlos.',
    '1D': 'Mecánica del motor M15A: compresión y vacío, mariposa y colector de admisión, soportes, distribución por cadena, árboles de levas con VVT, válvulas, culata, pistones, bielas, cigüeñal y bloque, con todas las medidas de control.',
    '1E': 'Lubricación: presión de aceite, bomba de aceite de rotores en la tapa de distribución, colador, cárter y sensor de presión.',
    '1F': 'Refrigeración: radiador, termostato (atrás del motor), bomba de agua, ventilador eléctrico con sus relés, mangueras, calefacción y cómo vaciar, lavar y llenar el circuito.',
    '1G': 'Combustible: tanque con bomba y aforador, regulación de presión, filtro, riel e inyectores, cañerías y cómo aliviar la presión antes de desarmar.',
    '1H': 'Encendido: dos bobinas (cilindros 1-4 y 2-3) comandadas por el ECM, cables de alta, bujías y la verificación de la chispa y del avance.',
    '1I': 'Arranque: motor de arranque con su relé y el circuito que solo permite arrancar en P o N; pruebas de funcionamiento y desarme del motor de arranque.',
    '1J': 'Carga: batería 46B24R, alternador de 70 A con regulador comandado por el ECM, pruebas de tensión y desarme del alternador.',
    '1K': 'Escape: múltiple con catalizador incorporado, caño delantero, caño central con resonador, silenciador trasero, gomas de soporte y protector de calor.',
    '2': 'Precauciones propias de suspensión.',
    '2A': 'Cómo diagnosticar ruidos, vibraciones, tirones y desgaste de neumáticos, y las cotas de alineación.',
    '2B': 'Suspensión delantera McPherson: columna con resorte y amortiguador, brazo de control con rótula, barra estabilizadora con bieletas, cubo, rodamiento y mangueta.',
    '2C': 'Suspensión trasera de eje de torsión: viga, resortes, amortiguadores, cubos y rodamientos.',
    '2D': 'Ruedas y neumáticos: medidas, presiones (etiqueta del auto), rotación, balanceo y par de las tuercas.',
    '3': 'Precauciones propias de los semiejes.',
    '3A': 'Semiejes delanteros con juntas homocinéticas: desarme, cambio de fuelles y grasa.',
    '4': 'Precauciones propias de frenos.',
    '4A': 'Mando de los frenos: pedal, servofreno de vacío, bomba de freno, válvula dosificadora, cañerías, purga y diagnóstico general.',
    '4B': 'Frenos delanteros de disco ventilado: pastillas, mordaza de un pistón y disco, con espesores mínimos.',
    '4C': 'Frenos traseros de tambor: zapatas, bombín, regulación automática y medidas del tambor.',
    '4D': 'Freno de estacionamiento: palanca, cables y regulación.',
    '4E': 'ABS con distribución electrónica de frenado (EBD): unidad hidráulica con módulo de control, sensores de rueda y anillos, testigos y diagnóstico de los códigos C.',
    '5': 'Precauciones propias de la transmisión.',
    '5A': 'Caja automática de 4 marchas: cómo trabajan los embragues, frenos y el tren planetario, el TCM y sus solenoides, pruebas en el auto (presión, calado, tiempos), diagnóstico de códigos y el desarme completo de la caja.',
    '5B': 'Caja manual de 5 marchas (no la lleva el 1.5XS japonés): varillaje, aceite y desarme.',
    '5C': 'Embrague de las versiones manuales: pedal, bomba hidráulica, disco y placa.',
    '6': 'Precauciones propias de la dirección.',
    '6A': 'Diagnóstico general de la dirección (dura, con juego, con ruido).',
    '6B': 'Volante y columna de dirección, con las precauciones del airbag.',
    '6C': 'Dirección asistida eléctrica (EPS): motor y sensor de par en la columna, módulo de control, diagnóstico de sus códigos y la caja de cremallera.',
    '7': 'Diagnóstico de un código de la climatización.',
    '7A': 'Calefacción y ventilación: unidad HVAC, soplador, compuertas, mandos y conductos.',
    '7B': 'Aire acondicionado manual (y automático en otras versiones): gas R-134a, compresor (Mitsubishi o Matsushita), condensador, secador, válvula de expansión, evaporador, sensores, carga de gas y diagnóstico.',
    '8': 'Precauciones propias de los sistemas de retención.',
    '8A': 'Cinturones de seguridad delanteros con pretensor y traseros.',
    '8B': 'Airbags frontales: módulo de control y sensor (SDM), espiral del volante, módulos de airbag, pretensores, diagnóstico de sus códigos y cómo desactivar el sistema para trabajar.',
    '9': 'Precauciones propias de la carrocería.',
    '9A': 'Cableado: cómo leer los diagramas, códigos de colores, ubicación de todos los conectores (motor, principal, tablero, piso, puertas), cajas de fusibles y los diagramas de cada circuito. Ver la carpeta "Circuitos" del vault.',
    '9B': 'Iluminación: faros, antinieblas, giros, freno, marcha atrás, patente e interiores; regulación de faros.',
    '9C': 'Instrumentos, información al conductor y bocina: cuadro de instrumentos, sensores de los relojes y testigos.',
    '9D': 'Limpiaparabrisas y lavaparabrisas delantero y trasero: motores, varillajes, bomba y depósito.',
    '9E': 'Cristales, levantavidrios eléctricos, desempañador de la luneta y espejos.',
    '9F': 'Cierre centralizado, cerraduras de puertas y portón, llaves y entrada sin llave.',
    '9G': 'Asientos delanteros y traseros: desmontaje y correderas.',
    '9H': 'Guarnecidos interiores: consola, techo y tapizados.',
    '9J': 'Capó, guardabarros y puertas: desmontaje y ajuste de luces entre paneles.',
    '9K': 'Estructura de la carrocería: paragolpes, medidas de la carrocería para chequear deformaciones y piezas soldadas.',
    '9L': 'Pintura y revestimientos: selladores, antióxido y zonas a proteger.',
    '9M': 'Guarnecidos exteriores: molduras, emblemas y protectores.',
    '10': 'Códigos de falla del sistema de control de la carrocería.',
    '10B': 'Control eléctrico de la carrocería: el BCM (dentro del bloque de empalmes) maneja luces, cierre, desempañador y alarmas; red de comunicación CAN y diagnóstico.',
    '10C': 'Inmovilizador: antena en el tambor de la llave, transpondedor en la llave, comunicación con el ECM, registro de llaves y diagnóstico.',
    '10E': 'Arranque sin llave (en las versiones que lo traen): módulo, antenas, llave electrónica y diagnóstico.',
}

# notas propias del vault relacionadas con cada capítulo
NOTAS = {
    '0A': ['01 Identificación y versiones', '03 Ficha técnica'], '0B': ['08 Plan de mantenimiento', '07 Fluidos y capacidades'],
    '1A': ['06 Motor M15A', '11 Diagnóstico de fallas'], '1D': ['06 Motor M15A'], '1E': ['06 Motor M15A'],
    '1F': ['07 Fluidos y capacidades'], '1G': ['07 Fluidos y capacidades'], '1H': ['06 Motor M15A'],
    '1I': ['10 Sistema eléctrico'], '1J': ['10 Sistema eléctrico'], '1K': ['06 Motor M15A'],
    '2A': ['09 Frenos, suspensión, dirección y ruedas'], '2B': ['09 Frenos, suspensión, dirección y ruedas'],
    '2C': ['09 Frenos, suspensión, dirección y ruedas'], '2D': ['09 Frenos, suspensión, dirección y ruedas'],
    '4A': ['09 Frenos, suspensión, dirección y ruedas'], '4B': ['09 Frenos, suspensión, dirección y ruedas'],
    '4C': ['09 Frenos, suspensión, dirección y ruedas'], '4E': ['09 Frenos, suspensión, dirección y ruedas'],
    '5A': ['05 Conducción y caja automática'], '6C': ['09 Frenos, suspensión, dirección y ruedas'],
    '8B': ['12 Seguridad, airbags y carrocería'], '9A': ['10 Sistema eléctrico'], '9B': ['10 Sistema eléctrico'],
    '9C': ['04 Mandos e instrumentos'], '9K': ['12 Seguridad, airbags y carrocería'],
}

# piezas del modelo 3D relacionadas (pid del visor)
PIDS = {
    '0A': ['casco'], '0B': ['filtro_aire', 'bloque', 'bobinas', 'canerias_freno', 'caja_4at'],
    '1A': ['ecu', 'sensor_maf', 'sensor_tp', 'sensor_map', 'sensor_ect', 'sensor_cmp', 'sensor_ckp', 'sensor_detonacion',
           'sonda_o2_1', 'sonda_o2_2', 'sensor_vss', 'solenoide_vvt', 'inyectores', 'bobinas', 'valvula_iac', 'valvula_purga'],
    '1B': ['canister', 'valvula_purga', 'valvula_egr', 'tapa_valvulas'],
    '1C': ['sensor_ect', 'sensor_tp', 'sensor_maf', 'sensor_map', 'sensor_ckp', 'sensor_cmp', 'sensor_detonacion', 'sensor_presion_aceite'],
    '1D': ['bloque', 'culata', 'tapa_valvulas', 'distribucion', 'admision', 'soportes_motor', 'ciguenal', 'pistones',
           'arboles_levas', 'valvulas', 'cadena'],
    '1E': ['bombas', 'bloque', 'sensor_presion_aceite'], '1F': ['radiador', 'electroventilador', 'mangueras', 'deposito_refrigerante', 'bombas'],
    '1G': ['tanque', 'inyectores', 'admision'], '1H': ['bobinas', 'sensor_ckp', 'sensor_cmp', 'sensor_detonacion'],
    '1I': ['arranque', 'cable_bateria'], '1J': ['accesorios', 'bateria', 'cable_bateria'], '1K': ['multiple_escape', 'escape'],
    '2B': ['amortiguador_del_izq', 'amortiguador_del_der', 'brazo_izq', 'brazo_der', 'estabilizadora', 'bastidor'],
    '2C': ['eje_torsion', 'amortiguador_tra_izq', 'amortiguador_tra_der'],
    '2D': ['rueda_del_izq', 'rueda_del_der', 'rueda_tra_izq', 'rueda_tra_der'], '3A': ['semieje_izq', 'semieje_der'],
    '4A': ['servofreno', 'canerias_freno', 'interruptor_freno', 'interruptor_nivel_freno', 'pedalera'],
    '4B': ['disco_izq', 'disco_der', 'mordaza_izq', 'mordaza_der'], '4C': ['tambor_izq', 'tambor_der'], '4D': ['freno_mano'],
    '4E': ['abs', 'sensores_abs'],
    '5A': ['caja_4at', 'convertidor', 'palanca', 'tcm', 'sensor_rango_caja', 'caja_bomba_aceite', 'caja_embragues',
           'caja_planetario', 'caja_cuerpo_valvulas', 'caja_diferencial', 'caja_engranajes'],
    '6B': ['volante', 'columna_eps'], '6C': ['columna_eps', 'cremallera', 'modulo_eps', 'cable_eps'],
    '7A': ['unidad_hvac'], '7B': ['condensador', 'canerias_ac', 'accesorios', 'sensor_presion_ac'],
    '8A': ['asiento_izq', 'asiento_der', 'asiento_trasero', 'pretensores'], '8B': ['volante', 'airbag_acompanante', 'sdm', 'pretensores'],
    '9A': ['cable_bateria', 'mazo_motor', 'mazo_principal', 'mazo_tablero', 'mazo_piso', 'mazo_puertas', 'mazo_porton',
           'fusibles', 'bloque_empalmes'],
    '9B': ['faro_izq', 'faro_der', 'calavera_izq', 'calavera_der', 'antiniebla_izq', 'antiniebla_der'],
    '9C': ['cuadro_instrumentos', 'bocina', 'tablero'], '9D': ['motor_limpiaparabrisas', 'limpiaparabrisas', 'lavador', 'motor_limpialuneta'],
    '9E': ['parabrisas', 'levantavidrios_izq', 'levantavidrios_der', 'desempanador'], '9F': ['cerraduras', 'antena_inmovilizador'],
    '9G': ['asiento_izq', 'asiento_der', 'asiento_trasero'], '9H': ['tapizado_izq', 'tapizado_der', 'techo_interior', 'palanca'],
    '9J': ['capo', 'puerta_del_izq', 'puerta_del_der', 'puerta_tra_izq', 'puerta_tra_der', 'tapa_combustible'],
    '9K': ['casco', 'paragolpes_del', 'paragolpes_tra'], '9L': ['casco'], '9M': ['parrilla', 'paragolpes_del', 'paragolpes_tra'],
    '10B': ['bloque_empalmes'], '10C': ['antena_inmovilizador', 'ecu'], '10E': ['modulo_keyless'],
}

VISOR = 'https://xaguhz.github.io/vaultColegio/vaultSuzuki/3D/visor/index.html'


def pag(ref):
    p = MAPA.get(ref)
    return f'[[{PDF}#page={p}|{ref}]]' if p else ref


def fname(code, nombre):
    return f'{code} {re.sub(r"[/:]", "-", nombre)}'


def esc(t):
    return str(t).replace('|', '/').replace('[', '(').replace(']', ')')


def piezas(lst):
    return ' · '.join(f'[{p}]({VISOR}#{p})' for p in lst)


os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, 'Circuitos'), exist_ok=True)
indice = []
for code, c in CAP.items():
    nombre = c['nombre']
    fn = fname(code, nombre)
    p0, p1 = c['paginas'][0], c['paginas'][-1]
    L = ['---', f'tags: [suzuki-swift, manual-de-taller, cap-{code.lower()}]', 'tipo: capitulo-manual',
         f'capitulo: "{code}"', f'paginas_pdf: "{p0}-{p1}"', '---', f'# {code} · {nombre}', '',
         f'Volver a [[00 Índice del manual de taller|Índice del manual]] · PDF: [[{PDF}#page={p0}|abrir en la página {p0}]] '
         f'(páginas {p0} a {p1}, solo en la copia local)', '']
    L += ['> [!summary] De qué trata', f'> {R.get(code, "Capítulo del manual de taller.")}', '']
    if NOTAS.get(code):
        L += ['**Notas del vault:** ' + ' · '.join(f'[[{n}]]' for n in NOTAS[code]), '']
    if PIDS.get(code):
        L += [f'**Piezas en el modelo 3D:** {piezas(PIDS[code])}', '']
    if c['temas']:
        L += ['## Temas del capítulo', '| Tema | Página |', '| --- | --- |']
        L += [f'| {esc(t)} | {pag(r)} |' for t, r in c['temas']]
        L += ['']
    if c['despieces']:
        L += ['## Despieces y ubicación de componentes']
        for titulo, items in c['despieces']:
            L += [f'### {esc(titulo)}', ', '.join(f'**{n}.** {esc(t)}' for n, t in items), '']
    if c['valores']:
        L += ['## Valores de servicio (estándar y límite)', '| Medición | Tipo | Valor |', '| --- | --- | --- |']
        L += [f'| {esc(a)} | {b} | {esc(v)} |' for a, b, v in c['valores']]
        L += ['']
    if c['pares']:
        L += ['## Pares de apriete', '| Pieza de fijación | N·m |', '| --- | --- |']
        L += [f'| {esc(a)} | {v} |' for a, v in c['pares']]
        L += ['']
    if c['dtc']:
        L += ['## Códigos de falla', '| Código | Descripción |', '| --- | --- |']
        L += [f'| {esc(a)} | {esc(b)} |' for a, b in c['dtc']]
        L += ['']
    if c['herramientas']:
        L += ['## Herramientas especiales', ', '.join(f'`{h}`' for h in c['herramientas']), '']
    open(os.path.join(OUT, fn + '.md'), 'w', encoding='utf-8').write('\n'.join(L))
    indice.append((code, nombre, fn, p0, p1, c))

# ------------------------------------------------------------------ índice general
I = ['---', 'tags: [suzuki-swift, manual-de-taller, indice]', 'tipo: indice', '---', '# Índice del manual de taller', '',
     'Volver a [[00 Suzuki Swift ZC21S]]', '',
     '> [!summary] Manual de taller Suzuki Swift 2005-2010 (edición en castellano)',
     f'> 1584 páginas para los Swift ZC11S y ZC21S, con versiones de volante a la izquierda y a la derecha. Cada capítulo tiene una nota con un resumen propio, los temas (con enlace a la página del PDF), los despieces, los valores de servicio, los pares de apriete, los códigos de falla y las herramientas especiales.',
     f'> El PDF original está en `Manual de taller/PDF/` y **no se sube a GitHub** (es material de Suzuki): los enlaces a páginas funcionan en el Obsidian de la compu, no en la página web.',
     '', '**Notas de conjunto:** [[Códigos de falla (DTC)]] · [[Pares de apriete]] · [[Herramientas especiales]] · '
     '[[Conectores del cableado]] · [[Circuitos eléctricos]]', '',
     '| Cap. | Capítulo | Páginas PDF | Temas | Despieces | Valores | Pares | DTC |', '| --- | --- | --- | --- | --- | --- | --- | --- |']
for code, nombre, fn, p0, p1, c in indice:
    I.append(f'| {code} | [[{fn}|{nombre}]] | {p0}–{p1} | {len(c["temas"])} | {len(c["despieces"])} | {len(c["valores"])} | '
             f'{len(c["pares"])} | {len(c["dtc"])} |')
open(os.path.join(OUT, '00 Índice del manual de taller.md'), 'w', encoding='utf-8').write('\n'.join(I) + '\n')

# ------------------------------------------------------------------ notas de conjunto
cab = lambda t: ['---', 'tags: [suzuki-swift, manual-de-taller]', 'tipo: referencia', '---', f'# {t}', '',
                 'Volver a [[00 Índice del manual de taller|Índice del manual]]', '']
X = cab('Códigos de falla (DTC)') + ['Todos los códigos que figuran en el manual, por sistema. El código se lee con un escáner OBD-II '
                                     '(motor y caja) o con el equipo de Suzuki (ABS, airbag, carrocería).', '']
for code, nombre, fn, p0, p1, c in indice:
    if c['dtc']:
        X += [f'## {code} · [[{fn}|{nombre}]]', '| Código | Descripción |', '| --- | --- |']
        X += [f'| {esc(a)} | {esc(b)} |' for a, b in c['dtc']] + ['']
open(os.path.join(OUT, 'Códigos de falla (DTC).md'), 'w', encoding='utf-8').write('\n'.join(X))
X = cab('Pares de apriete') + ['Pares tomados de las tablas de especificaciones de cada capítulo (N·m).', '']
for code, nombre, fn, p0, p1, c in indice:
    if c['pares']:
        X += [f'## {code} · [[{fn}|{nombre}]]', '| Pieza de fijación | N·m |', '| --- | --- |']
        X += [f'| {esc(a)} | {v} |' for a, v in c['pares']] + ['']
open(os.path.join(OUT, 'Pares de apriete.md'), 'w', encoding='utf-8').write('\n'.join(X))
X = cab('Herramientas especiales') + ['Números de herramienta especial de Suzuki citados en cada capítulo.', '',
                                     '| Capítulo | Herramientas |', '| --- | --- |']
X += [f'| [[{fn}|{code} {nombre}]] | ' + ', '.join(f'`{h}`' for h in c['herramientas']) + ' |'
      for code, nombre, fn, p0, p1, c in indice if c['herramientas']]
open(os.path.join(OUT, 'Herramientas especiales.md'), 'w', encoding='utf-8').write('\n'.join(X) + '\n')

MAZOS = {'A': ('Cable de batería', 'cable_bateria'), 'C': ('Mazo de cables del motor', 'mazo_motor'),
         'E': ('Mazo de cables principal', 'mazo_principal'), 'G': ('Mazo del panel de instrumentos', 'mazo_tablero'),
         'L': ('Mazo del piso', 'mazo_piso'), 'J': ('Mazos de puertas', 'mazo_puertas'), 'Q': ('Mazos de puertas', 'mazo_puertas'),
         'K': ('Mazo del techo y portón', 'mazo_porton'), 'M': ('Mazo del techo y portón', 'mazo_porton')}
X = cab('Conectores del cableado') + [
    'Conectores del auto según las tablas de "Ruta de cables y disposición de conectores" (capítulo 9A). La letra indica el mazo; '
    'el color es el del cuerpo del conector. Algunos nombres quedaron cortados al leer las tablas: ante la duda, ver la página del PDF.', '',
    '| Conector | Color | Se conecta a | Mazo (pieza 3D) | Página |', '| --- | --- | --- | --- | --- |']
for k in sorted(CON):
    col, nom, p = CON[k]
    mz = MAZOS.get(k[0], ('Otro mazo', ''))
    X.append(f'| {k} | {col or "-"} | {esc(nom)} | {mz[0]}' + (f' ([{mz[1]}]({VISOR}#{mz[1]}))' if mz[1] else '') +
             f' | [[{PDF}#page={p}|{p}]] |')
open(os.path.join(OUT, 'Conectores del cableado.md'), 'w', encoding='utf-8').write('\n'.join(X) + '\n')

# ------------------------------------------------------------------ circuitos eléctricos (esquemas propios)
# (explicación, esquema Mermaid con el camino de la corriente, piezas del 3D que se resaltan)
CX = {
    'A-1': ('La llave en START (o el botón, con arranque sin llave) alimenta el relé de arranque a través del fusible ST SIG; el ECM solo lo deja cerrar con la caja en P o N (sensor de rango). El relé conecta el solenoide del motor de arranque, que toma corriente directa de la batería por el cable grueso.',
            'B[Batería] -->|fusible ST MOT 30A| RE[Relé de arranque]\n  LL[Llave en START] -->|ST SIG 10A| RE\n  RG[Sensor de rango P/N] --> ECM[ECM]\n  ECM --> RE\n  RE --> SO[Solenoide del arranque]\n  B ==>|cable de batería| MA[Motor de arranque]\n  SO --> MA',
            ['bateria', 'cable_bateria', 'fusibles', 'arranque', 'sensor_rango_caja', 'ecu', 'mazo_motor']),
    'A-2': ('El alternador carga la batería; el ECM decide la tensión de regulación (alta o baja) según el consumo y avisa con el testigo de carga en el cuadro.',
            'AL[Alternador 70 A] ==>|cable B| B[Batería]\n  ECM[ECM] -->|señal de regulación| AL\n  AL -->|señal L| CU[Cuadro: testigo de carga]\n  B --> FU[Fusibles] --> CARGAS[Consumos del auto]',
            ['accesorios', 'bateria', 'cable_bateria', 'ecu', 'cuadro_instrumentos', 'mazo_motor']),
    'A-3': ('Encendido de chispa perdida: el ECM, con la señal de los sensores de cigüeñal y levas, corta la corriente de cada bobina (1-4 y 2-3) en el momento justo; cada bobina dispara dos bujías a la vez.',
            'IG[Fusible IG COIL 15A] --> BO1[Bobina 1-4] & BO2[Bobina 2-3]\n  CKP[Sensor CKP] --> ECM[ECM]\n  CMP[Sensor CMP] --> ECM\n  ECM -->|corte| BO1\n  ECM -->|corte| BO2\n  BO1 --> BU1[Bujías 1 y 4]\n  BO2 --> BU2[Bujías 2 y 3]',
            ['bobinas', 'sensor_ckp', 'sensor_cmp', 'ecu', 'tapa_valvulas', 'mazo_motor', 'fusibles']),
    'A-4': ('Ventilador del radiador: el ECM lee la temperatura del refrigerante (ECT) y la presión del aire acondicionado y activa los relés del ventilador (en baja o alta velocidad).',
            'ECT[Sensor ECT] --> ECM[ECM]\n  PAC[Sensor de presión del A/C] --> ECM\n  ECM --> R1[Relés del ventilador]\n  F[Fusible RDTR FAN 30A] --> R1\n  R1 --> V[Electroventilador]',
            ['electroventilador', 'sensor_ect', 'sensor_presion_ac', 'ecu', 'fusibles', 'mazo_motor']),
    'A-5': ('Control del motor: el ECM recibe aire (MAF), mariposa (TP), presión del colector (MAP), temperaturas, cigüeñal y levas, detonación, sondas de oxígeno y velocidad; y maneja inyectores, bobinas, válvula de ralentí, VVT, purga del canister, relé de la bomba de nafta y el embrague del compresor del A/C.',
            'S[Sensores: MAF, TP, MAP, ECT, CKP, CMP, detonación, O2 1 y 2, VSS] --> ECM[ECM]\n  RP[Relé principal - FI 15A] --> ECM\n  ECM --> INY[4 inyectores]\n  ECM --> BOB[Bobinas]\n  ECM --> IAC[Válvula IAC]\n  ECM --> VVT[Solenoide VVT]\n  ECM --> PUR[Purga EVAP]\n  ECM --> BN[Relé bomba de nafta]\n  ECM --> AC[Relé compresor A/C]',
            ['ecu', 'sensor_maf', 'sensor_tp', 'sensor_map', 'sensor_ect', 'sensor_ckp', 'sensor_cmp', 'sensor_detonacion', 'sonda_o2_1',
             'sonda_o2_2', 'sensor_vss', 'inyectores', 'bobinas', 'valvula_iac', 'solenoide_vvt', 'valvula_purga', 'tanque',
             'accesorios', 'mazo_motor', 'mazo_principal', 'fusibles']),
    'A-6': ('Caja automática: el TCM lee el sensor de rango, las velocidades de entrada y salida, la temperatura del fluido y la mariposa (vía ECM) y maneja los solenoides de cambio y de presión.',
            'RG[Sensor de rango] --> TCM[TCM]\n  VE[Sensores de velocidad] --> TCM\n  TF[Temp. del fluido] --> TCM\n  ECM[ECM] <-->|CAN| TCM\n  F[Fusible AT ETM 15A] --> TCM\n  TCM --> SOL[Solenoides de cambio y presión]',
            ['tcm', 'sensor_rango_caja', 'caja_4at', 'caja_cuerpo_valvulas', 'ecu', 'mazo_motor', 'palanca']),
    'A-7': ('Inmovilizador: la antena del tambor de la llave lee el código del transpondedor; si coincide con el registrado, el ECM habilita la inyección y el encendido.',
            'LL[Llave con transpondedor] -.-> AN[Antena del tambor]\n  AN --> ECM[ECM]\n  ECM -->|habilita| INY[Inyección y encendido]\n  ECM --> CU[Testigo del inmovilizador]',
            ['antena_inmovilizador', 'ecu', 'cuadro_instrumentos', 'mazo_tablero']),
    'A-8': ('Control de la carrocería: el BCM, integrado en el bloque de empalmes, recibe los interruptores (puertas, luces, llave) y maneja cierre, luces de cortesía, desempañador y avisos; habla con el ECM y el cuadro por CAN.',
            'INT[Interruptores de puertas, luces y llave] --> BCM[BCM en el bloque de empalmes]\n  BCM --> CI[Cierre centralizado]\n  BCM --> LU[Luces interiores]\n  BCM --> DE[Desempañador]\n  BCM <-->|CAN| ECM[ECM]\n  BCM <-->|CAN| CU[Cuadro]',
            ['bloque_empalmes', 'cerraduras', 'desempanador', 'techo_interior', 'ecu', 'cuadro_instrumentos', 'mazo_principal', 'mazo_puertas']),
    'B-1': ('Limpiaparabrisas: la palanca elige intermitente, baja o alta; el motor tiene un contacto de parada para que las escobillas queden abajo. El lavador es una bomba en el depósito.',
            'F[Fusible WIP] --> PA[Palanca del limpia]\n  PA --> M[Motor del limpiaparabrisas]\n  PA --> BO[Bomba del lavador]\n  M --> ESC[Escobillas]',
            ['motor_limpiaparabrisas', 'limpiaparabrisas', 'lavador', 'columna_eps', 'mazo_principal']),
    'B-2': ('Limpialuneta: motor en el portón con su propia bomba de lavado.',
            'PA[Palanca] --> M[Motor del limpialuneta]\n  PA --> BO[Bomba del lavador trasero]', ['motor_limpialuneta', 'porton', 'lavador', 'mazo_porton']),
    'B-3': ('Desempañador: un relé (comandado por el BCM y el botón) alimenta las resistencias de la luneta; se corta solo a los pocos minutos.',
            'BT[Botón] --> BCM[BCM]\n  BCM --> RE[Relé del desempañador]\n  RE --> LU[Resistencias de la luneta]', ['desempanador', 'bloque_empalmes', 'porton', 'mazo_porton']),
    'B-4': ('Levantavidrios eléctricos: la botonera del conductor alimenta cada motor invirtiendo la polaridad para subir o bajar.',
            'F[Fusible P/W] --> BC[Botonera del conductor]\n  BC --> MD[Motores delanteros]\n  BC --> MT[Motores traseros]', ['levantavidrios_izq', 'levantavidrios_der', 'mazo_puertas']),
    'B-5': ('Cierre centralizado: el BCM recibe la cerradura del conductor o el control remoto y mueve los actuadores de las cuatro puertas y el portón.',
            'LL[Llave o control] --> BCM[BCM]\n  BCM --> AC[Actuadores de las cerraduras]', ['cerraduras', 'bloque_empalmes', 'mazo_puertas']),
    'B-6': ('Espejos eléctricos: un selector y una palanca mueven dos motorcitos por espejo.', 'SW[Selector] --> ME[Motores de los espejos]',
            ['puerta_del_izq', 'puerta_del_der', 'mazo_puertas']),
    'B-7': ('Bocina: el botón del volante cierra a masa el relé de la bocina.', 'F[Fusible HORN] --> R[Relé de la bocina]\n  BV[Botón del volante] --> R\n  R --> BO[Bocina]',
            ['bocina', 'volante', 'mazo_principal']),
    'B-8': ('Calefacción de asientos (si el auto la trae).', 'SW[Interruptor] --> RE[Resistencia del asiento]', ['asiento_izq', 'asiento_der']),
    'B-9': ('Arranque sin llave (si el auto lo trae): antenas en el habitáculo, módulo de control y comunicación con el ECM y el BCM.',
            'LL[Llave electrónica] -.-> AN[Antenas]\n  AN --> MK[Módulo keyless]\n  MK <--> ECM[ECM]\n  MK <--> BCM[BCM]', ['modulo_keyless', 'ecu', 'bloque_empalmes']),
    'C-1': ('Relojes del cuadro: velocidad (por CAN desde el ECM), vueltas, nafta (aforador del tanque) y temperatura.',
            'ECM[ECM] -->|CAN| CU[Cuadro]\n  AF[Aforador del tanque] --> CU', ['cuadro_instrumentos', 'ecu', 'tanque', 'mazo_tablero']),
    'C-2': ('Indicadores del cuadro: giros, luz alta, marcha seleccionada.', 'BCM[BCM] --> CU[Cuadro]\n  TCM[TCM] --> CU', ['cuadro_instrumentos', 'tcm']),
    'C-3': ('Testigos de advertencia: aceite, carga, frenos, ABS, airbag, EPS, motor, cinturón, puertas.',
            'SEN[Interruptores y módulos] --> CU[Cuadro: testigos]', ['cuadro_instrumentos', 'sensor_presion_aceite', 'interruptor_nivel_freno', 'abs', 'sdm', 'modulo_eps']),
    'D-1': ('Faros: la palanca de luces activa los relés de luz alta y baja; cada faro tiene su fusible.',
            'PA[Palanca de luces] --> RE[Relés de faros]\n  RE -->|H/L L 15A| FI[Faro izquierdo]\n  RE -->|H/L R 15A| FD[Faro derecho]', ['faro_izq', 'faro_der', 'fusibles', 'mazo_principal']),
    'D-2': ('Luces de posición, traseras y de patente.', 'PA[Palanca] --> RT[Relé TAIL]\n  RT --> PO[Posición, traseras y patente]', ['faro_izq', 'faro_der', 'calavera_izq', 'calavera_der', 'mazo_piso']),
    'D-3': ('Faros antiniebla delanteros con su relé y fusible FR FOG.', 'SW[Interruptor] --> RE[Relé FR FOG 15A]\n  RE --> AN[Antinieblas]', ['antiniebla_izq', 'antiniebla_der', 'fusibles']),
    'D-4': ('Iluminación del tablero y los mandos, con regulador de intensidad.', 'TAIL[Circuito de posición] --> RG[Regulador] --> IL[Luces del tablero]', ['tablero', 'cuadro_instrumentos']),
    'D-5': ('Luces interiores: techo y baúl, encendidas por las puertas a través del BCM.', 'PU[Contactos de puertas] --> BCM[BCM]\n  F[Fusible DOME] --> LU[Luz de techo]\n  BCM --> LU', ['techo_interior', 'bloque_empalmes']),
    'D-6': ('Giros y balizas: el destellador (relé de giros) alimenta los faros de giro, los repetidores y las calaveras.',
            'PA[Palanca de giro] --> DE[Destellador]\n  BA[Botón de balizas] --> DE\n  DE --> G[Giros delanteros, laterales y traseros]', ['faro_izq', 'faro_der', 'calavera_izq', 'calavera_der', 'casco']),
    'D-7': ('Luces de freno: el interruptor del pedal alimenta las calaveras y la tercera luz; la señal también va al ECM, al TCM y al ABS.',
            'F[Fusible STOP LAMP 15A] --> IF[Interruptor del pedal]\n  IF --> LF[Luces de freno y tercera luz]\n  IF --> ECM[ECM / TCM / ABS]', ['interruptor_freno', 'calavera_izq', 'calavera_der', 'porton', 'abs']),
    'D-8': ('Marcha atrás: el sensor de rango de la caja enciende las luces al pasar a R.', 'RG[Sensor de rango en R] --> LR[Luces de marcha atrás]', ['sensor_rango_caja', 'calavera_izq', 'calavera_der']),
    'D-9': ('Nivelación de faros (si la trae): ruedita en el tablero y motores en los faros.', 'SW[Ruedita] --> MN[Motores de nivelación]', ['faro_izq', 'faro_der']),
    'D-10': ('Antiniebla trasero (según mercado).', 'SW[Interruptor] --> RE[Relé] --> AT[Antiniebla trasero]', ['paragolpes_tra']),
    'E-1': ('Calefacción y ventilación: el soplador tiene un resistor de velocidades; las compuertas se mueven con cables o motores.',
            'F[Fusible HTR FAN 30A] --> R[Relé del soplador]\n  SW[Perilla] --> RS[Resistor de velocidades]\n  R --> SO[Soplador] --> RS', ['unidad_hvac', 'tablero', 'fusibles']),
    'E-2': ('Aire acondicionado automático (otras versiones): módulo HVAC con sensores de temperatura y motores de compuertas.',
            'SEN[Sensores de temperatura] --> MH[Módulo HVAC]\n  MH --> CMP[Compuertas y soplador]\n  MH <--> ECM[ECM: compresor]', ['unidad_hvac', 'ecu']),
    'F-1': ('Airbags: el SDM (con su sensor de impacto) dispara los airbags del conductor y del acompañante y los pretensores; el testigo SRS avisa fallas.',
            'SDM[SDM bajo la consola] --> AC[Airbag del conductor - espiral]\n  SDM --> AA[Airbag del acompañante]\n  SDM --> PR[Pretensores]\n  SDM --> CU[Testigo SRS]', ['sdm', 'volante', 'airbag_acompanante', 'pretensores', 'cuadro_instrumentos', 'mazo_tablero']),
    'F-2': ('ABS: el módulo lee los cuatro sensores de rueda y la luz de freno y modula la presión de cada freno con su bomba y válvulas.',
            'SR[4 sensores de rueda] --> AB[Módulo ABS]\n  F[Fusibles ABS MOT y ABS SOL 30A] --> AB\n  IF[Interruptor de freno] --> AB\n  AB --> FR[Presión de cada freno]\n  AB --> CU[Testigos ABS y EBD]', ['abs', 'sensores_abs', 'interruptor_freno', 'canerias_freno', 'fusibles']),
    'F-3': ('Dirección eléctrica: el módulo EPS lee el sensor de par de la columna y la velocidad del auto, y le pide más o menos fuerza al motor de asistencia.',
            'F[Fusible EPS 50A] --> ME[Módulo EPS]\n  SP[Sensor de par] --> ME\n  ECM[ECM: velocidad y vueltas] -->|CAN| ME\n  ME --> MO[Motor de la EPS]', ['modulo_eps', 'columna_eps', 'cable_eps', 'ecu']),
    'G-1': ('Sistema de sonido: radio, parlantes de puertas y antena.', 'RA[Radio] --> PA[Parlantes]\n  AN[Antena] --> RA', ['tablero', 'tapizado_izq', 'tapizado_der', 'casco']),
    'G-2': ('Tomacorriente de accesorios y pantalla de información.', 'F[Fusible ACC] --> TO[Tomacorriente]', ['palanca', 'tablero']),
}
I2 = cab('Circuitos eléctricos') + ['Los diagramas del capítulo 9A, uno por circuito. Cada nota explica cómo circula la corriente, con un esquema propio '
                                    'simplificado, los fusibles, conectores y colores de cable que aparecen en el diagrama, y las piezas del 3D '
                                    'que se resaltan al elegir el circuito en el visor (botón **Circuitos**).', '',
                                    '| Código | Circuito | Página |', '| --- | --- | --- |']
for cod, nombre in CIRC['lista']:
    info = CIRC['info'][cod]
    titulo = nombre.replace('Diagrama del circuito del ', '').replace('Diagrama de circuito del ', '').replace('Diagrama del circuito de ', '')
    titulo = titulo[0].upper() + titulo[1:]
    expl, mer, pz = CX.get(cod, ('', '', []))
    fn = f'{cod} {re.sub(r"[/:]", "-", titulo)}'
    L = ['---', 'tags: [suzuki-swift, manual-de-taller, circuito]', 'tipo: circuito', f'circuito: "{cod}"', '---',
         f'# {cod} · {titulo}', '', 'Volver a [[Circuitos eléctricos]] · [[9A Sistemas de cableado]]', '',
         f'PDF: [[{PDF}#page={info["pagina"]}|diagrama original, página {info["pagina"]}]] (copia local)', '']
    if expl:
        L += ['> [!summary] Cómo funciona', f'> {expl}', '']
    if mer:
        L += ['```mermaid', 'flowchart LR', '  ' + mer, '```', '']
    if pz:
        L += [f'**En el modelo 3D:** {piezas(pz)} · en el visor: **Circuitos → {cod}**', '']
    if info['fusibles']:
        L += ['**Fusibles:** ' + ', '.join(f'`{f}`' for f in info['fusibles']), '']
    if info['conectores']:
        L += ['**Conectores:** ' + ', '.join(f'`{c}`' + (f' ({esc(CON[c][1])})' if c in CON else '') for c in info['conectores']), '']
    if info['colores']:
        L += ['**Colores de cable:** ' + ', '.join(f'`{c}`' for c in info['colores']), '']
    open(os.path.join(OUT, 'Circuitos', fn + '.md'), 'w', encoding='utf-8').write('\n'.join(L))
    I2.append(f'| {cod} | [[{fn}|{titulo}]] | [[{PDF}#page={info["pagina"]}|{info["pagina"]}]] |')
open(os.path.join(OUT, 'Circuitos eléctricos.md'), 'w', encoding='utf-8').write('\n'.join(I2) + '\n')
_nota = lambda cod, n: f"{cod} " + re.sub(r'[/:]', '-', (lambda t: t[0].upper() + t[1:])(n.replace('Diagrama del circuito del ', '').replace('Diagrama de circuito del ', '').replace('Diagrama del circuito de ', '')))
json.dump({k: {'nombre': n, 'nota': _nota(k, n), 'piezas': CX.get(k, ('', '', []))[2], 'explicacion': CX.get(k, ('', '', []))[0],
               'pagina': CIRC['info'][k]['pagina']}
           for k, n in CIRC['lista']}, open(os.path.join(VAULT, '3D', 'visor', 'circuitos.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=0)

print('capítulos:', len(indice), 'circuitos:', len(CIRC['lista']))
