"""Datos técnicos por pieza para el visor y el vault: fallas, desmontaje, procedimientos, pares y herramientas.

Uso: python3 herramientas/suzuki_tecnica.py [carpeta_con_el_texto_del_manual]

- Fallas típicas (síntoma, causa probable, qué hacer) y pasos de desmontaje: escritos a mano, resumidos de las tablas
  de diagnóstico y de los procedimientos del manual de taller (con palabras propias).
- Procedimientos del manual (título y página), pares de apriete y herramientas especiales: se buscan solos en los datos
  extraídos del manual (herramientas/manual_datos.json y el índice de procedimientos).
Salidas: 3D/visor/tecnica.json, "Manual de taller/Guía técnica por pieza.md" y "Manual de taller/Diagnóstico por síntoma.md".
"""
import json
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = json.load(open(os.path.join(VAULT, 'herramientas', 'manual_datos.json'), encoding='utf-8'))
PROC = json.load(open(os.path.join(VAULT, 'herramientas', 'manual_procedimientos.json'), encoding='utf-8'))
TOOLS_PAG = json.load(open(os.path.join(VAULT, 'herramientas', 'manual_herramientas_pag.json'), encoding='utf-8'))
FICHAS = json.load(open(os.path.join(VAULT, '3D', 'visor', 'fichas.json'), encoding='utf-8'))
PDF = 'Manual de taller Swift 2005-2010.pdf'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from suzuki_kw import KW  # noqa: E402

# ------------------------------------------------------------------ fallas típicas: (síntoma, causa probable, qué hacer)
F = {
    'bateria': [('No arranca, el arranque gira lento', 'Batería descargada o bornes sulfatados', 'Medir 12,4 V o más en reposo; limpiar y ajustar bornes; cargar o cambiar.'),
                ('Testigo de carga prendido', 'El alternador no carga', 'Medir 13,5–14,8 V con el motor en marcha; revisar correa y alternador.')],
    'arranque': [('Se escucha "clic" y no gira', 'Batería baja, masa floja o solenoide', 'Medir tensión en el borne del arranque al dar contacto.'),
                 ('No hace nada', 'Pedal de embrague no apretado a fondo, interruptor del embrague o fusible ST SIG', 'Apretar a fondo; probar el interruptor y el fusible.')],
    'accesorios': [('Chillido al arrancar o con carga eléctrica', 'Correa floja o gastada', 'Medir 4,5–5,5 mm de flecha con 100 N; ajustar o cambiar.'),
                   ('Testigo de carga', 'Alternador (escobillas, regulador, diodos)', 'Medir la tensión de carga; desarmar y medir escobillas (mín. 1,5 mm).')],
    'bloque': [('Testigo de aceite prendido', 'Aceite bajo, bomba o colador tapado', 'Parar el motor; medir nivel y presión (más de 270 kPa a 4000 rpm).'),
               ('Humo azul y consumo de aceite', 'Aros o guías de válvula gastados', 'Medir compresión (1400 kPa, mín. 1100) y diferencia entre cilindros.')],
    'culata': [('Pérdida de refrigerante sin fuga visible, humo blanco', 'Junta de tapa de cilindros', 'Prueba de presión del circuito; medir la planitud de la tapa (límite 0,03 mm).'),
               ('Ruido de válvulas (tic-tic)', 'Luz de válvulas fuera de medida', 'Medir luz en frío: admisión 0,18–0,22, escape 0,28–0,32 mm; cambiar calces.')],
    'cadena': [('Ruido de cadena al arrancar en frío', 'Tensor o guías gastadas, aceite viejo', 'Cambiar aceite; revisar tensor y guías.'),
               ('Código P0011/P0016 (fase de levas)', 'Cadena estirada o VVT trabado', 'Verificar marcas de distribución y la válvula OCV.')],
    'solenoide_vvt': [('Código P0010–P0012, ralentí irregular', 'Válvula OCV trabada o colador tapado', 'Medir 6,7–7,7 Ω; limpiar el colador; cambiar aceite.')],
    'bobinas': [('Tironeo, falla en dos cilindros a la vez (1-4 o 2-3)', 'Bobina o cable de alta', 'Cambiar de lugar los cables; probar chispa; revisar bujías.'),
                ('Código P0300–P0304', 'Falla de encendido', 'Revisar bujías (luz 1,0–1,1 mm), bobinas y compresión.')],
    'inyectores': [('Ralentí irregular, mezcla pobre (P0171)', 'Inyector tapado o junta tórica con entrada de aire', 'Escuchar el clic de cada inyector; revisar juntas.'),
                   ('Olor a nafta', 'Junta tórica dañada', 'Cambiar las juntas tóricas.')],
    'admision': [('Ralentí alto o inestable', 'Entrada de aire por juntas o mangueras', 'Revisar juntas del colector y mangueras de vacío.')],
    'valvula_iac': [('Ralentí inestable o se apaga', 'Válvula IAC o paso de aire sucio', 'Limpiar el cuerpo de mariposa y la IAC.')],
    'sensor_maf': [('Falta de potencia, código P0101–P0103', 'MAF sucio o falso contacto', 'Limpiar con producto específico; revisar el conector C13.')],
    'sensor_ect': [('Ventilador no arranca o el reloj marca mal', 'Sensor ECT o conector', 'Medir resistencia en frío y en caliente; revisar el conector C09.')],
    'sensor_ckp': [('Gira pero no arranca, sin chispa', 'Sensor CKP sin señal', 'Revisar el conector C20 y la luz del sensor; leer P0335.')],
    'sonda_o2_1': [('Consumo alto, código P0130–P0134', 'Sonda vieja o calefactor cortado', 'Leer datos con el escáner; medir el calefactor.')],
    'sonda_o2_2': [('Código P0420', 'Catalizador gastado o pérdida de escape', 'Descartar pérdidas y fallas de encendido antes de cambiar el catalizador.')],
    'multiple_escape': [('Ruido de escape adelante', 'Junta del múltiple o espárrago cortado', 'Revisar en frío; cambiar la junta.'),
                        ('Ruido de cascabel al acelerar', 'Catalizador roto por dentro', 'Golpear suavemente y escuchar; cambiar el múltiple con catalizador.')],
    'escape': [('Ruido metálico abajo', 'Cubrecalor o gomas de soporte flojas', 'Revisar soportes y abrazaderas.')],
    'radiador': [('El motor calienta', 'Radiador tapado, refrigerante bajo o ventilador', 'Revisar nivel en frío, limpiar el panal, probar el ventilador.')],
    'electroventilador': [('Calienta en tránsito', 'Ventilador, relés o fusible RDTR FAN', 'Con el motor caliente debe arrancar; probar relés y fusible.')],
    'mangueras': [('Calienta o tarda en calentar', 'Termostato trabado', 'Termostato abierto: tarda en calentar; cerrado: calienta. Cambiarlo.')],
    'bombas': [('Pérdida de refrigerante por el agujero testigo', 'Sello de la bomba de agua', 'Cambiar la bomba de agua.'),
               ('Testigo de aceite en ralentí caliente', 'Bomba de aceite o colador', 'Medir presión; revisar el colador al bajar el cárter.')],
    'tanque': [('Gira pero no arranca, no se oye la bomba', 'Bomba de nafta, relé o fusible', 'Medir presión (270–310 kPa); probar el relé.'),
               ('El reloj de nafta marca mal', 'Aforador del tanque', 'Medir la resistencia del aforador.')],
    'canister': [('Código de EVAP o olor a nafta', 'Canister, mangueras o válvula de purga', 'Revisar mangueras y la válvula de purga.')],
    'embrague': [('Patina: sube vueltas sin acelerar', 'Disco gastado o con aceite, placa débil', 'Verificar juego del pedal; medir remaches del disco (mín. 0,5 mm).'),
                 ('Arrastra: cuesta poner las marchas con el motor en marcha', 'Juego del pedal incorrecto, disco torcido o aire en el circuito', 'Purgar; revisar bomba y disco.'),
                 ('Tiembla al arrancar', 'Disco cristalizado o soportes del motor rotos', 'Revisar soportes; cambiar el disco.'),
                 ('Ruido al pisar el pedal', 'Rodamiento de empuje', 'Cambiar el rodamiento.')],
    'bomba_embrague': [('El pedal se va al piso o no vuelve', 'Pérdida o aire en el circuito del embrague', 'Revisar pérdidas, cambiar la bomba o el receptor y purgar.')],
    'caja_5mt': [('Ruido en todas las marchas', 'Aceite bajo o rodamientos gastados', 'Controlar el nivel (2,2 L GL-4 75W-90); revisar rodamientos.'),
                 ('Pérdida de aceite por los palieres', 'Retenes laterales del diferencial', 'Cambiar el retén con la herramienta especial.')],
    'eje_entrada': [('Cruje al pasar 3ª, 4ª o 5ª', 'Anillos sincronizadores gastados', 'Medir holgura anillo-engranaje (límite 0,5 mm).')],
    'contraeje': [('Cruje al pasar 1ª o 2ª', 'Sincronizador de baja gastado', 'Medir holgura de los anillos (doble cono en 2ª).')],
    'horquillas': [('Una marcha se sale sola', 'Horquilla, manguito o resorte de retención gastados', 'Revisar el desgaste y los resortes de retención.')],
    'palanca': [('Cambios duros o imprecisos', 'Cables de cambio y selección desajustados o gastados', 'Ajustar o cambiar los cables; engrasar los extremos.')],
    'eje_marcha_atras': [('Cruje al poner reversa', 'Freno de marcha atrás o embrague que arrastra', 'Esperar un segundo con el embrague apretado; revisar el embrague.')],
    'semieje_izq': [('"Tac-tac" al doblar', 'Junta homocinética gastada', 'Revisar el fuelle; cambiar la junta y la grasa.')],
    'semieje_der': [('"Tac-tac" al doblar', 'Junta homocinética gastada', 'Revisar el fuelle; cambiar la junta y la grasa.')],
    'amortiguador_del_izq': [('Rebota, ruido en pozos', 'Amortiguador gastado o copela', 'Cambiar de a pares; revisar el rodamiento superior.')],
    'amortiguador_del_der': [('Rebota, ruido en pozos', 'Amortiguador gastado o copela', 'Cambiar de a pares; revisar el rodamiento superior.')],
    'brazo_izq': [('Golpeteo y desgaste irregular de neumático', 'Rótula o bujes gastados', 'Revisar juego; el brazo se cambia completo con la rótula.')],
    'brazo_der': [('Golpeteo y desgaste irregular de neumático', 'Rótula o bujes gastados', 'Revisar juego; el brazo se cambia completo con la rótula.')],
    'estabilizadora': [('Golpeteo en pozos chicos', 'Bieletas o bujes de la barra', 'Cambiar bieletas.')],
    'cremallera': [('Juego en el volante', 'Extremos de barra o cremallera', 'Medir juego (0–30 mm en el aro); cambiar extremos y alinear.')],
    'columna_eps': [('Dirección dura y testigo EPS', 'Batería baja, fusible EPS 50 A o sensor de par', 'Revisar batería y fusible; leer códigos C de la EPS.')],
    'modulo_eps': [('Dirección dura y testigo EPS', 'Módulo o alimentación', 'Revisar el cable EPS y leer los códigos.')],
    'mordaza_izq': [('Chillido al frenar', 'Pastillas gastadas (testigo)', 'Medir: nuevas 10 mm, cambiar con 2 mm.'),
                    ('Tira para un lado', 'Mordaza trabada', 'Limpiar y engrasar los pasadores.')],
    'mordaza_der': [('Chillido al frenar', 'Pastillas gastadas (testigo)', 'Medir: nuevas 10 mm, cambiar con 2 mm.'),
                    ('Tira para un lado', 'Mordaza trabada', 'Limpiar y engrasar los pasadores.')],
    'disco_izq': [('Vibra el pedal al frenar', 'Disco alabeado o fino', 'Medir espesor (mín. 18 mm) y alabeo.')],
    'disco_der': [('Vibra el pedal al frenar', 'Disco alabeado o fino', 'Medir espesor (mín. 18 mm) y alabeo.')],
    'tambor_izq': [('Freno de mano flojo, pedal largo', 'Zapatas gastadas o regulador trabado', 'Medir tambor (máx. 202 mm) y zapatas.')],
    'tambor_der': [('Freno de mano flojo, pedal largo', 'Zapatas gastadas o regulador trabado', 'Medir tambor (máx. 202 mm) y zapatas.')],
    'servofreno': [('Pedal duro', 'Servofreno sin vacío', 'Revisar la manguera de vacío y la válvula.'),
                   ('Pedal esponjoso', 'Aire en el circuito o líquido viejo', 'Purgar y cambiar el líquido DOT 3.')],
    'abs': [('Testigo ABS prendido', 'Sensor de rueda, anillo o módulo', 'Leer códigos C; revisar sensores y conectores.')],
    'sensores_abs': [('Testigo ABS después de cambiar rulemanes', 'Sensor dañado o anillo sucio', 'Revisar el anillo y la luz del sensor.')],
    'faro_izq': [('No enciende un faro', 'Lámpara o fusible H/L L', 'Cambiar lámpara; probar el fusible propio.')],
    'faro_der': [('No enciende un faro', 'Lámpara o fusible H/L R', 'Cambiar lámpara; probar el fusible propio.')],
    'motor_limpiaparabrisas': [('No para abajo', 'Contacto de parada del motor', 'Revisar el motor y su conector E01.')],
    'levantavidrios_der': [('El vidrio no sube', 'Motor, botonera o cable en el fuelle de la puerta', 'Medir tensión en el motor; revisar el fuelle.')],
    'levantavidrios_izq': [('El vidrio no sube', 'Motor, botonera o cable en el fuelle de la puerta', 'Medir tensión en el motor; revisar el fuelle.')],
    'sdm': [('Testigo SRS prendido', 'Falla en airbag, pretensor, espiral o conector', 'Leer códigos B con el equipo; no medir airbags con tester.')],
    'antena_inmovilizador': [('Gira pero no arranca y el testigo del inmovilizador titila', 'Llave no registrada o antena', 'Probar con otra llave; registrar con el equipo.')],
    'ecu': [('Testigo de motor (MIL)', 'Código de falla guardado', 'Leer con escáner OBD-II por el conector DLC.')],
    'mazo_motor': [('Fallas intermitentes del motor', 'Conector flojo o cable rozado', 'Revisar conectores C y el paso del mazo cerca del escape.')],
    'mazo_puertas': [('Falla un levantavidrios o la cerradura al abrir la puerta', 'Cable cortado en el fuelle de la bisagra', 'Revisar los cables dentro del fuelle.')],
    'condensador': [('Aire poco frío en tránsito', 'Condensador sucio o ventilador', 'Limpiar el condensador; revisar el ventilador.')],
    'unidad_hvac': [('No sale aire', 'Soplador, resistor o fusible HTR FAN', 'Probar el soplador directo; revisar el resistor.')],
}

# ------------------------------------------------------------------ desmontaje: piezas que hay que sacar antes (para la animación) y pasos propios
DESM = {
    'multiple_escape': (['paragolpes_del', 'parrilla', 'electroventilador', 'radiador', 'condensador', 'sonda_o2_1', 'sonda_o2_2'],
                        ['Desconectar el negativo de la batería y trabajar con el escape frío.', 'Sacar el paragolpes delantero con la parrilla.',
                         'Sacar el radiador y correr el condensador del A/C sin abrir el circuito.', 'Desconectar y sacar las dos sondas de oxígeno.',
                         'Sacar el refuerzo y soltar el caño de escape n° 1.', 'Sacar el múltiple con su junta (junta nueva al armar).']),
    'radiador': (['paragolpes_del', 'parrilla', 'electroventilador', 'mangueras'],
                 ['Desconectar el negativo y vaciar el refrigerante en frío.', 'Sacar el electroventilador con su conector.',
                  'Soltar las mangueras superior e inferior.', 'Sacar el radiador hacia arriba.', 'Al armar, llenar y purgar el circuito (refrigerante 50 %).']),
    'accesorios': (['semieje_der'], ['Desconectar el negativo.', 'Sacar el semieje derecho (el alternador queda detrás, abajo).',
                                     'Aflojar el tensor y sacar la correa.', 'Desconectar el cable B y el conector; sacar los bulones y el alternador.',
                                     'Al armar, tensar la correa a 4,5–5,5 mm de flecha.']),
    'arranque': (['bateria', 'filtro_aire'], ['Desconectar el negativo.', 'Desconectar el cable principal y el del solenoide.',
                                              'Separar de la caja el soporte de los cables de cambio.', 'Sacar los dos bulones y el motor de arranque.']),
    'tapa_valvulas': (['filtro_aire', 'bobinas'], ['Sacar la caja del filtro de aire.', 'Desconectar las bobinas y los cables de alta; sacarlos.',
                                                   'Soltar la manguera del PCV y los bulones; sacar la tapa.', 'Junta nueva y sellador en las esquinas al armar.']),
    'bobinas': ([], ['Desconectar los conectores C02 y C03.', 'Soltar el bulón de cada bobina y sacarla junto con el cable de alta.',
                     'Para cambiar bujías: con las bobinas afuera, sacar las bujías con llave de 16 mm; luz 1,0–1,1 mm.']),
    'admision': (['filtro_aire', 'sensor_map', 'sensor_tp', 'valvula_iac', 'valvula_purga', 'inyectores'],
                 ['Desconectar el negativo y aliviar la presión de nafta.', 'Sacar la manguera de admisión y la caja del filtro.',
                  'Desconectar sensores (MAP, TP), IAC, purga y los inyectores.', 'Sacar los bulones y el colector; juntas tóricas nuevas.']),
    'culata': (['capo', 'filtro_aire', 'tapa_valvulas', 'bobinas', 'admision', 'multiple_escape', 'distribucion', 'cadena', 'arboles_levas'],
               ['Vaciar refrigerante y aceite; aliviar la presión de nafta.', 'Sacar admisión y escape (ver sus pasos).',
                'Sacar la tapa de válvulas, la tapa de distribución y la cadena.', 'Sacar los árboles de levas en el orden del manual.',
                'Aflojar los bulones de la tapa de afuera hacia adentro y sacarla.', 'Al armar: junta nueva y bulones en el orden y ángulos del manual.']),
    'distribucion': (['accesorios', 'tapa_valvulas'], ['El manual lo hace con el motor afuera del auto.', 'Sacar la correa, la polea del cigüeñal (150 N·m) y la de la bomba de agua.',
                                                     'Sacar la tapa de válvulas, el cárter y el soporte del compresor.', 'Sacar la tapa de distribución y la válvula OCV.']),
    'cadena': (['distribucion'], ['Poner el cilindro 1 en punto muerto superior con las marcas alineadas.', 'Sacar el tensor, las guías y la cadena.',
                                  'Al armar, alinear las marcas de los piñones con los eslabones marcados.']),
    'arboles_levas': (['tapa_valvulas', 'cadena'], ['Con la cadena afuera, aflojar los sombreretes de a poco en el orden del manual.',
                                                     'Sacar los árboles; no mezclar los botadores ni los calces.', 'Medir altura de leva y luz de válvulas al armar.']),
    'pistones': (['culata', 'bloque'], ['Con la tapa y el cárter afuera, sacar los sombreretes de biela (marcados).', 'Empujar cada pistón hacia arriba con un mango de madera.',
                                       'Medir pistón (77,969–77,984 mm) y cilindro; cambiar aros.']),
    'caja_5mt': (['bateria', 'filtro_aire', 'cable_bateria', 'arranque', 'semieje_izq', 'semieje_der'],
                 ['Vaciar refrigerante y aceite de la caja.', 'Sacar el depósito, la batería con su bandeja y la caja del filtro de aire.',
                  'Desconectar los cables de cambio, el interruptor de marcha atrás, la masa y el cilindro receptor del embrague.',
                  'Sacar el motor de arranque y los semiejes.', 'Sostener el motor con un aparejo y soltar el soporte izquierdo.',
                  'Sacar los bulones caja-motor y bajar la caja.']),
    'embrague': (['caja_5mt', 'semieje_izq', 'semieje_der'], ['Sacar la caja (ver sus pasos).', 'Aflojar los bulones de la placa en cruz y sacar placa y disco.',
                                                              'Revisar volante, rodamiento y horquilla.', 'Al armar, centrar el disco con la herramienta y apretar a 23 N·m.']),
    'bomba_embrague': (['pedalera'], ['Vaciar el depósito, soltar el tubo del embrague.', 'Soltar la varilla del pedal y las tuercas de la bomba.',
                                      'Al armar, purgar por el cilindro receptor y verificar el juego del pedal (2–8 mm).']),
    'semieje_izq': (['rueda_del_izq'], ['Aflojar la tuerca del cubo con la rueda en el piso.', 'Levantar, sacar la rueda y separar la rótula del brazo.',
                                        'Sacar el semieje del cubo y luego de la caja con una palanca.', 'Retén y anillo nuevos; tuerca del cubo al par del manual.']),
    'semieje_der': (['rueda_del_der'], ['Aflojar la tuerca del cubo con la rueda en el piso.', 'Levantar, sacar la rueda y separar la rótula del brazo.',
                                        'Sacar el semieje del cubo y luego de la caja con una palanca.', 'Retén y anillo nuevos; tuerca del cubo al par del manual.']),
    'amortiguador_del_izq': (['rueda_del_izq'], ['Sacar el burlete trasero del capó y la tapa de la torreta.', 'Levantar el auto y sacar la rueda.',
                                                 'Soltar la bieleta de la estabilizadora y el sensor ABS del soporte.', 'Sacar los bulones de la mangueta y las tuercas de arriba.',
                                                 'Sacar la columna; desarmar el resorte solo con compresor.']),
    'amortiguador_del_der': (['rueda_del_der'], ['Sacar el burlete trasero del capó y la tapa de la torreta.', 'Levantar el auto y sacar la rueda.',
                                                 'Soltar la bieleta de la estabilizadora y el sensor ABS del soporte.', 'Sacar los bulones de la mangueta y las tuercas de arriba.',
                                                 'Sacar la columna; desarmar el resorte solo con compresor.']),
    'mordaza_izq': (['rueda_del_izq'], ['Sacar la rueda.', 'Soltar los pernos del pasador y levantar la mordaza.', 'Cambiar pastillas (las 4 del eje) y engrasar pasadores.',
                                        'Bombear el pedal antes de andar.']),
    'mordaza_der': (['rueda_del_der'], ['Sacar la rueda.', 'Soltar los pernos del pasador y levantar la mordaza.', 'Cambiar pastillas (las 4 del eje) y engrasar pasadores.',
                                        'Bombear el pedal antes de andar.']),
    'disco_izq': (['rueda_del_izq', 'mordaza_izq'], ['Sacar rueda y mordaza (colgarla, sin estirar el flexible).', 'Sacar el disco; medir espesor y alabeo.']),
    'disco_der': (['rueda_del_der', 'mordaza_der'], ['Sacar rueda y mordaza (colgarla, sin estirar el flexible).', 'Sacar el disco; medir espesor y alabeo.']),
    'tambor_izq': (['rueda_tra_izq'], ['Sacar la rueda y la tapa del cubo.', 'Soltar el freno de mano y quitar el calafateado de la tuerca.',
                                       'Sacar la tuerca y el tambor con extractor.', 'Tuerca nueva al armar; calafatear.']),
    'tambor_der': (['rueda_tra_der'], ['Sacar la rueda y la tapa del cubo.', 'Soltar el freno de mano y quitar el calafateado de la tuerca.',
                                       'Sacar la tuerca y el tambor con extractor.', 'Tuerca nueva al armar; calafatear.']),
    'servofreno': (['abs'], ['Sacar la bomba de freno del servofreno (sin abrir el circuito si se puede).', 'Sacar la manguera de vacío.',
                             'Desde adentro, soltar la horquilla del pedal y las tuercas.', 'Sacar el servofreno.']),
    'volante': (['airbag_acompanante'], ['Desconectar el negativo y esperar 90 s.', 'Sacar el módulo del airbag (dejarlo con la tapa hacia arriba).',
                                         'Desconectar la bocina; marcar la posición y sacar la tuerca.', 'Sacar el volante con extractor.']),
    'tanque': (['asiento_trasero', 'escape'], ['Aliviar la presión y vaciar el tanque.', 'Desconectar el conector de la bomba (bajo el asiento) y las mangueras.',
                                               'Sostener el tanque y soltar los flejes.', 'Bajar el tanque.']),
    'electroventilador': (['paragolpes_del'], ['Desconectar el conector del ventilador.', 'Soltar los bulones del marco y sacarlo hacia arriba.']),
    'bateria': ([], ['Desconectar primero el negativo y después el positivo.', 'Sacar la traba y la batería.', 'Al armar, conectar primero el positivo.']),
    'filtro_aire': ([], ['Soltar las trabas de la tapa.', 'Sacar el elemento; limpiar con aire de adentro hacia afuera o cambiarlo.']),
    'sensor_ect': (['filtro_aire'], ['Con el motor frío, desconectar el conector C09.', 'Sacar el sensor y reponer el refrigerante.']),
    'sonda_o2_1': (['paragolpes_del'], ['Desconectar el conector (verde).', 'Sacar con la llave para sondas; grasa antiadherente en la rosca nueva.']),
    'faro_izq': (['paragolpes_del'], ['Sacar el paragolpes delantero.', 'Desconectar y soltar los bulones del faro.', 'Regular la altura al montarlo.']),
    'faro_der': (['paragolpes_del'], ['Sacar el paragolpes delantero.', 'Desconectar y soltar los bulones del faro.', 'Regular la altura al montarlo.']),
    'capo': ([], ['Marcar las bisagras, sacar la varilla y los bulones (con ayuda).']),
}


def pag_pdf(ref):
    return MD['mapa_paginas'].get(ref)


salida = {}
for pid in FICHAS['piezas']:
    rx, caps = KW.get(pid, (None, None))
    proc = []
    if rx:
        for t, p, c in PROC:
            if re.fullmatch(caps, c or '') and re.search(rx, t, re.I) and not re.search(r'A/T|automátic', t):
                if (t, p) not in proc:
                    proc.append((t, p))
    proc = proc[:10]
    pares = []
    if rx:
        for c in caps.split('|'):
            for n, v in MD['capitulos'].get(c, {}).get('pares', []):
                if re.search(rx, n, re.I) and (n, v) not in pares:
                    pares.append((n, v))
    herr = []
    for t, p in proc[:4]:
        for q in (p, p + 1):
            for h in TOOLS_PAG.get(str(q), []):
                if h not in herr:
                    herr.append(h)
    d, pasos = DESM.get(pid, ([], []))
    item = {}
    if F.get(pid):
        item['fallas'] = F[pid]
    if pasos:
        item['desmontaje'] = {'antes': d, 'pasos': pasos}
    if proc:
        item['procedimientos'] = proc
    if pares:
        item['pares'] = pares[:8]
    if herr:
        item['herramientas'] = herr[:6]
    if item:
        salida[pid] = item
json.dump(salida, open(os.path.join(VAULT, '3D', 'visor', 'tecnica.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

# ------------------------------------------------------------------ notas del vault
nombre = {pid: FICHAS['piezas'][pid].get('que', '')[:0] for pid in FICHAS['piezas']}
CJ_DE = {}
for c in json.load(open(os.path.join(VAULT, '3D', 'visor', 'capas.json')))['capas']:
    for cj in c['conjuntos']:
        CJ_DE[cj] = c['titulo']
VISOR = 'https://xaguhz.github.io/vaultColegio/vaultSuzuki/3D/visor/index.html'
NOMBRES = json.load(open(os.path.join(VAULT, 'herramientas', 'nombres_piezas.json'), encoding='utf-8'))

L = ['---', 'tags: [suzuki-swift, manual-de-taller, diagnostico]', 'tipo: referencia', '---', '# Guía técnica por pieza', '',
     'Volver a [[00 Índice del manual de taller|Índice del manual]] · [[Diagnóstico por síntoma]] · [[11 Diagnóstico de fallas]]', '',
     '> [!summary] Qué hay acá', '> Para cada pieza del modelo 3D: fallas típicas, cómo se desmonta (resumido con palabras propias), los procedimientos '
     'del manual con su página, los pares de apriete y las herramientas especiales. Es lo mismo que muestra la ficha de cada pieza en el visor, '
     'donde además el botón **Desmontaje animado** saca en orden las piezas que estorban.', '']
for pid in sorted(salida, key=lambda k: NOMBRES.get(k, k)):
    it = salida[pid]
    L += [f'## {NOMBRES.get(pid, pid)}', f'[Ver en 3D]({VISOR}#{pid.replace("_", "-")})', '']
    if it.get('fallas'):
        L += ['| Síntoma | Causa probable | Qué hacer |', '| --- | --- | --- |'] + [f'| {a} | {b} | {c} |' for a, b, c in it['fallas']] + ['']
    if it.get('desmontaje'):
        de = it['desmontaje']
        if de['antes']:
            L += ['**Antes hay que sacar:** ' + ', '.join(NOMBRES.get(x, x) for x in de['antes'])]
        L += [f'{i + 1}. {p}' for i, p in enumerate(de['pasos'])] + ['']
    if it.get('procedimientos'):
        L += ['**En el manual:** ' + ' · '.join(f'{t} ([[{PDF}#page={p}|pág. {p}]])' for t, p in it['procedimientos'])]
    if it.get('pares'):
        L += ['**Pares de apriete:** ' + ' · '.join(f'{n}: {v} N·m' for n, v in it['pares'])]
    if it.get('herramientas'):
        L += ['**Herramientas especiales:** ' + ', '.join(f'`{h}`' for h in it['herramientas'])]
    L += ['']
open(os.path.join(VAULT, 'Manual de taller', 'Guía técnica por pieza.md'), 'w', encoding='utf-8').write('\n'.join(L))

# diagnóstico por síntoma (todas las fallas juntas, por sistema)
porcj = {}
for pid, it in salida.items():
    for a, b, c in it.get('fallas', []):
        porcj.setdefault(NOMBRES.get(pid + '__cj', 'Otros'), []).append((a, NOMBRES.get(pid, pid), b, c, pid))
L = ['---', 'tags: [suzuki-swift, manual-de-taller, diagnostico, troubleshooting]', 'tipo: referencia', '---', '# Diagnóstico por síntoma', '',
     'Volver a [[00 Índice del manual de taller|Índice del manual]] · [[Guía técnica por pieza]] · [[Códigos de falla (DTC)]] · [[11 Diagnóstico de fallas]]', '',
     '> [!tip] Método', '> 1) Anotar el síntoma y cuándo aparece. 2) Leer los códigos de falla. 3) Revisar lo simple (fusible, conector, nivel, masa). '
     '4) Seguir la tabla y la prueba del manual. 5) Borrar códigos y probar en ruta.', '']
for cj in sorted(porcj):
    L += [f'## {cj}', '| Síntoma | Pieza | Causa probable | Qué hacer |', '| --- | --- | --- | --- |']
    L += [f'| {a} | [{n}]({VISOR}#{pid.replace("_", "-")}) | {b} | {c} |' for a, n, b, c, pid in sorted(porcj[cj])] + ['']
open(os.path.join(VAULT, 'Manual de taller', 'Diagnóstico por síntoma.md'), 'w', encoding='utf-8').write('\n'.join(L))
print('piezas con datos técnicos:', len(salida), '· con fallas:', sum(1 for v in salida.values() if 'fallas' in v),
      '· con desmontaje:', sum(1 for v in salida.values() if 'desmontaje' in v))
