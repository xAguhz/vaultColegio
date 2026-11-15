"""Fichas del visor 3D del Suzuki Swift ZC21S → 3D/visor/fichas.json

Uso: python3 herramientas/suzuki_fichas.py
Cada pieza: que (qué es), datos (pares nombre/valor), mant (mantenimiento), ver (nota del vault).
Los datos salen del manual de taller RS415 (ZC21S, motor M15A) y del catálogo japonés del 1.5XS.
"""
import json
import os

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONJ = {
    'Carrocería': {
        'color': '#b3121f', 'nota': '03 Ficha técnica · 12 Seguridad, airbags y carrocería',
        'resumen': 'Casco autoportante de acero de 5 puertas: 3755 mm de largo, 1690 de ancho y 1510 de alto, con 2390 mm entre ejes. Capó, portón y paragolpes se desmontan; el resto va soldado.',
        'laminas': [['lamina_carroceria.jpg', 'Carrocería, puertas y ópticas en despiece'], ['swift_perfil.jpg', 'Perfil del modelo']]},
    'Puertas y cristales': {
        'color': '#5a7ea6', 'nota': '04 Mandos e instrumentos · 12 Seguridad, airbags y carrocería',
        'resumen': 'Cuatro puertas con levantavidrios, parabrisas laminado pegado y luneta en el portón. En el Swift los parantes A y B van en negro y el techo parece "flotar".',
        'laminas': [['lamina_carroceria.jpg', 'Puertas y cristales separados del casco']]},
    'Iluminación': {
        'color': '#e0ac00', 'nota': '10 Sistema eléctrico',
        'resumen': 'Faros grandes que suben por el guardabarros y calaveras verticales en los parantes traseros. Cada faro tiene su fusible propio (H/L L y H/L R).',
        'laminas': [['swift_34_delantera.jpg', 'Vista delantera'], ['swift_34_trasera.jpg', 'Vista trasera']]},
    'Motor M15A': {
        'color': '#c0623b', 'nota': '06 Motor M15A',
        'resumen': 'Naftero de 4 cilindros en línea, 1490 cm³, DOHC de 16 válvulas con distribución por cadena y variador de fase de admisión (VVT). 110 PS a 6000 rpm y 143 N·m a 4000 rpm en la versión japonesa.',
        'laminas': [['lamina_motor.jpg', 'Vano motor: motor transversal, caja, radiador y batería'], ['lamina_motor_despiece.jpg', 'Motor M15A en despiece']]},
    'Transmisión': {
        'color': '#7852ee', 'nota': '05 Conducción y caja manual',
        'resumen': 'Caja automática de 4 marchas con convertidor de par y diferencial integrado (transeje), tracción delantera. Relación final 4,052.',
        'laminas': [['lamina_motor.jpg', 'La caja va a la izquierda del motor']]},
    'Refrigeración': {
        'color': '#00bfbc', 'nota': '07 Fluidos y capacidades',
        'resumen': 'Circuito presurizado con radiador, electroventilador y depósito recuperador. Lleva 6,1 L de refrigerante al 50 % (versión automática).',
        'laminas': [['lamina_motor.jpg', 'Radiador y electroventilador al frente']]},
    'Eléctrico': {
        'color': '#08b94e', 'nota': '10 Sistema eléctrico',
        'resumen': 'Sistema de 12 V con negativo a masa: batería 46B24R de 36 Ah, alternador de 70 A y dos cajas de fusibles (motor y cabina).',
        'laminas': [['lamina_motor.jpg', 'Batería y caja de fusibles en el vano motor']]},
    'Suspensión y dirección': {
        'color': '#3f7fb5', 'nota': '09 Frenos, suspensión, dirección y ruedas',
        'resumen': 'Adelante McPherson con barra estabilizadora; atrás eje de torsión con resortes y amortiguadores separados. Dirección a cremallera con asistencia eléctrica en la columna (EPS).',
        'laminas': [['lamina_suspension.jpg', 'Tren delantero, trasero y dirección'], ['lamina_interior.jpg', 'Columna y volante (mano derecha)']]},
    'Frenos': {
        'color': '#e93147', 'nota': '09 Frenos, suspensión, dirección y ruedas',
        'resumen': 'Discos ventilados adelante y tambores atrás, con servofreno de vacío y ABS. Líquido DOT 3, cambio cada 30 000 km o 2 años.',
        'laminas': [['lamina_frenos.jpg', 'Discos, mordazas, tambores y servofreno']]},
    'Ruedas': {
        'color': '#55606a', 'nota': '09 Frenos, suspensión, dirección y ruedas',
        'resumen': 'Neumáticos 185/60R15 84H en llantas 15 × 5½ JJ. Tuercas a 85 N·m.',
        'laminas': [['lamina_suspension.jpg', 'Ruedas con el tren rodante']]},
    'Combustible y escape': {
        'color': '#8a7f6a', 'nota': '07 Fluidos y capacidades · 08 Plan de mantenimiento',
        'resumen': 'Tanque de 43 L bajo el asiento trasero con la bomba adentro (inyección multipunto). El escape pasa por el catalizador, va por debajo del piso y termina en el silenciador trasero.',
        'laminas': [['lamina_combustible.jpg', 'Tanque y línea de escape']]},
    'Interior': {
        'color': '#7a7d84', 'nota': '04 Mandos e instrumentos',
        'resumen': 'Cinco plazas, volante a la derecha (mano japonesa) y cuadro de tres relojes. Respaldo trasero rebatible.',
        'laminas': [['lamina_interior.jpg', 'Puesto de manejo y asientos']]},
}

PIEZAS = {
    # ------------------------------------------------------------ Carrocería
    'casco': {
        'que': 'La estructura soldada del auto: piso, parantes, techo, guardabarros y laterales. No tiene chasis aparte; el casco mismo resiste las cargas (carrocería autoportante).',
        'datos': [['Largo × ancho × alto', '3755 × 1690 × 1510 mm'], ['Entre ejes', '2390 mm'], ['Despeje', '140 mm'], ['Peso en orden de marcha', '1030 kg (1.5XS 2WD)']],
        'mant': ['Revisar el piso y los zócalos por óxido, sobre todo atrás de las ruedas.', 'Mantener libres los desagotes de puertas y zócalos.', 'Antes de soldar o pintar al horno (más de 93 °C), sacar los módulos de airbag y los pretensores.'],
        'ver': '12 Seguridad, airbags y carrocería'},
    'capo': {
        'que': 'Tapa del vano motor, abisagrada atrás y trabada adelante con la cerradura y el gancho de seguridad.',
        'datos': [['Apertura', 'palanca en la cabina + gancho de seguridad'], ['Lubricación', 'cerradura con aceite de motor o grasa']],
        'mant': ['Lubricar la cerradura y el gancho en cada service.', 'Verificar que trabe en el segundo gancho antes de circular.'],
        'ver': '08 Plan de mantenimiento'},
    'porton': {
        'que': 'Puerta trasera del baúl con la luneta térmica y el limpialuneta. Se sostiene abierta con dos amortiguadores a gas.',
        'datos': [['Luneta', 'con desempañador eléctrico'], ['Soporte', '2 amortiguadores a gas']],
        'mant': ['Si el portón no se sostiene solo, cambiar los dos amortiguadores juntos.', 'Lubricar bisagras y cerradura.'],
        'ver': '12 Seguridad, airbags y carrocería'},
    'paragolpes_del': {
        'que': 'Cubierta plástica del frente. Atrás lleva el travesaño de acero que absorbe los golpes.',
        'datos': [['Material', 'polipropileno pintado'], ['Fijación', 'tornillos y grampas']],
        'mant': ['Después de un golpe, revisar el travesaño, el radiador y los soportes de los faros.'],
        'ver': '12 Seguridad, airbags y carrocería'},
    'paragolpes_tra': {
        'que': 'Cubierta plástica trasera, por debajo del portón. Detrás va el travesaño trasero.',
        'datos': [['Material', 'polipropileno pintado']],
        'mant': ['Revisar las grampas: si está flojo, vibra a alta velocidad.'],
        'ver': '12 Seguridad, airbags y carrocería'},
    'parrilla': {
        'que': 'Rejillas que dejan entrar el aire al radiador (arriba) y a la toma inferior.',
        'datos': [['Función', 'entrada de aire al radiador']],
        'mant': ['Sacar hojas e insectos del frente del radiador; si se tapa, el motor calienta.'],
        'ver': '11 Diagnóstico de fallas'},
    # ------------------------------------------------------------ Puertas y cristales
    'puerta_del_izq': {
        'que': 'Puerta del acompañante (en el auto japonés el conductor va a la derecha). Lleva el espejo retrovisor, la manija y el levantavidrios.',
        'datos': [['Espejo', 'montado en la puerta'], ['Levantavidrios', 'eléctrico']],
        'mant': ['Lubricar bisagras, retenes y cerradura.', 'Limpiar los desagotes de la parte de abajo.'],
        'ver': '04 Mandos e instrumentos'},
    'puerta_del_der': {
        'que': 'Puerta del conductor (mano derecha, mercado japonés), con la botonera de levantavidrios y espejos.',
        'datos': [['Lado', 'conductor (volante a la derecha)'], ['Espejos', 'regulación eléctrica']],
        'mant': ['Lubricar bisagras, retenes y cerradura.', 'Si el vidrio sube lento, limpiar las guías antes de cambiar el motor.'],
        'ver': '04 Mandos e instrumentos'},
    'puerta_tra_izq': {
        'que': 'Puerta trasera izquierda. Su borde de atrás rodea el pasarueda.',
        'datos': [['Traba de niños', 'en el canto de la puerta']],
        'mant': ['Lubricar bisagras y cerradura.', 'Probar la traba de niños.'],
        'ver': '04 Mandos e instrumentos'},
    'puerta_tra_der': {
        'que': 'Puerta trasera derecha, igual a la izquierda pero simétrica.',
        'datos': [['Traba de niños', 'en el canto de la puerta']],
        'mant': ['Lubricar bisagras y cerradura.', 'Probar la traba de niños.'],
        'ver': '04 Mandos e instrumentos'},
    'parabrisas': {
        'que': 'Vidrio delantero laminado (dos capas con una lámina plástica en el medio), pegado a la carrocería. Forma parte de la rigidez del techo.',
        'datos': [['Tipo', 'laminado, pegado con uretano']],
        'mant': ['Cambiar las escobillas si dejan franjas.', 'Un impacto chico se puede reparar antes de que se extienda.'],
        'ver': '12 Seguridad, airbags y carrocería'},
    'vidrios_fijos': {
        'que': 'Pequeños vidrios fijos detrás de las puertas traseras, en el parante C.',
        'datos': [['Tipo', 'templado, fijo']],
        'mant': ['Revisar el burlete si entra agua.'],
        'ver': '12 Seguridad, airbags y carrocería'},
    'limpiaparabrisas': {
        'que': 'Brazos y escobillas del parabrisas, movidos por un motor con varillaje en el torpedo.',
        'datos': [['Velocidades', 'intermitente, baja y alta'], ['Lavador', 'depósito en el vano motor']],
        'mant': ['Cambiar las escobillas una vez por año.', 'Usar líquido lavaparabrisas, no detergente.'],
        'ver': '04 Mandos e instrumentos'},
    # ------------------------------------------------------------ Iluminación
    'faro_izq': {
        'que': 'Óptica delantera izquierda: luz alta y baja, posición y giro.',
        'datos': [['Fusible', 'H/L L, 15 A'], ['Regulación', 'tornillos de altura y de lado']],
        'mant': ['Revisar la regulación después de cambiar una lámpara.', 'No tocar el vidrio de la lámpara halógena con los dedos.'],
        'ver': '10 Sistema eléctrico'},
    'faro_der': {
        'que': 'Óptica delantera derecha: luz alta y baja, posición y giro.',
        'datos': [['Fusible', 'H/L R, 15 A'], ['Regulación', 'tornillos de altura y de lado']],
        'mant': ['Revisar la regulación después de cambiar una lámpara.', 'Si un solo faro no anda, mirar primero su fusible propio.'],
        'ver': '10 Sistema eléctrico'},
    'calavera_izq': {
        'que': 'Luz trasera izquierda vertical: posición, freno, giro y marcha atrás.',
        'datos': [['Fusible de freno', 'STOP LAMP, 15 A']],
        'mant': ['Probar las luces de freno con ayuda o contra una pared.'],
        'ver': '10 Sistema eléctrico'},
    'calavera_der': {
        'que': 'Luz trasera derecha vertical: posición, freno, giro y marcha atrás.',
        'datos': [['Fusible de freno', 'STOP LAMP, 15 A']],
        'mant': ['Revisar que no entre agua (empañado por dentro).'],
        'ver': '10 Sistema eléctrico'},
    # ------------------------------------------------------------ Motor
    'bloque': {
        'que': 'Bloque de aluminio con las camisas de los 4 cilindros, el cigüeñal y el cárter de aceite abajo. Atrás va el filtro de aceite.',
        'datos': [['Cilindrada', '1490 cm³'], ['Diámetro × carrera', '78 × 78 mm'], ['Compresión', '1400 kPa (mín. 1100; dif. máx. 100)'], ['Presión de aceite', 'más de 270 kPa a 4000 rpm'], ['Aceite', '≈ 3,7 L cárter + 0,2 L filtro']],
        'mant': ['Aceite y filtro cada 15 000 km o 12 meses (7500 km o 6 meses en uso severo).', 'Tapón de vaciado a 35 N·m; filtro ¾ de vuelta después de que apoya (≈ 14 N·m).'],
        'ver': '06 Motor M15A'},
    'culata': {
        'que': 'Tapa de cilindros con dos árboles de levas (DOHC) y 4 válvulas por cilindro. El árbol de admisión tiene el variador de fase (VVT).',
        'datos': [['Válvulas', '16'], ['Luz en frío', 'admisión 0,18–0,22 · escape 0,28–0,32 mm'], ['Luz en caliente', 'admisión 0,21–0,27 · escape 0,30–0,36 mm']],
        'mant': ['Controlar la luz de válvulas cada 30 000 km o 24 meses.', 'Se ajusta cambiando las pastillas de los botadores.'],
        'ver': '06 Motor M15A'},
    'tapa_valvulas': {
        'que': 'Tapa superior con la boca de llenado de aceite. Arriba van las dos bobinas: cada una enciende un cilindro directo y otro por cable de alta.',
        'datos': [['Orden de encendido', '1-3-4-2'], ['Bujía níquel', 'NGK BKR6E-11 / Denso K20PR-U11'], ['Bujía iridio', 'NGK IFR6J11'], ['Luz de bujía', '1,0–1,1 mm']],
        'mant': ['Bujías de níquel cada 45 000 km; de iridio cada 105 000 km (según el plan).', 'Revisar los cables de alta y la junta de la tapa.'],
        'ver': '06 Motor M15A'},
    'distribucion': {
        'que': 'Tapa de la cadena de distribución, del lado derecho del motor. La cadena no tiene cambio programado.',
        'datos': [['Accionamiento', 'cadena (sin cambio periódico)']],
        'mant': ['Si hay ruido de cadena en frío, revisar el tensor y el nivel de aceite.', 'Un aceite viejo o bajo daña primero el variador VVT y el tensor.'],
        'ver': '06 Motor M15A'},
    'admision': {
        'que': 'Múltiple plástico que reparte el aire a los 4 cilindros, con el cuerpo de mariposa a la entrada. Los inyectores van en los conductos.',
        'datos': [['Inyección', 'multipunto (EPI)'], ['Presión de nafta', '270–310 kPa (bomba andando)']],
        'mant': ['Limpiar el cuerpo de mariposa si el ralentí es inestable.', 'Revisar mangueras de vacío por fisuras.'],
        'ver': '06 Motor M15A'},
    'multiple_escape': {
        'que': 'Colector que junta los gases de los 4 cilindros y los lleva al catalizador. Va cubierto por una chapa contra el calor.',
        'datos': [['Sonda de oxígeno', 'antes y después del catalizador']],
        'mant': ['Revisar las tuercas y el cubrecalor en cada service con el auto levantado.', 'No tocar con el motor caliente.'],
        'ver': '08 Plan de mantenimiento'},
    'accesorios': {
        'que': 'Lado de la correa: polea del cigüeñal, bomba de agua y alternador, movidos por una correa en V.',
        'datos': [['Tensión de correa', '4,5–5,5 mm de flecha con 100 N'], ['Alternador', '70 A, 14,2–14,8 V']],
        'mant': ['Inspeccionar la correa a los 45 000 km y cambiarla a los 90 000 km.', 'La tensión se ajusta moviendo el alternador.'],
        'ver': '08 Plan de mantenimiento'},
    'arranque': {
        'que': 'Motor eléctrico que hace girar el motor para arrancar, montado en la caja. Con caja automática solo arranca en P o N.',
        'datos': [['Potencia', '1,2 kW'], ['Fusible', 'ST MOT, 30 A']],
        'mant': ['Si hace "clic" y no gira, medir primero la batería y los bornes.'],
        'ver': '10 Sistema eléctrico'},
    'filtro_aire': {
        'que': 'Caja con el elemento filtrante del aire de admisión, sobre la caja de cambios.',
        'datos': [['Elemento', 'papel seco']],
        'mant': ['Inspeccionar cada 15 000 km y cambiar cada 45 000 km (en calles de tierra, mucho más seguido).'],
        'ver': '08 Plan de mantenimiento'},
    # ------------------------------------------------------------ Transmisión
    'caja_4at': {
        'que': 'Transeje automático de 4 marchas con convertidor de par, engranajes planetarios y diferencial. Los cambios los decide la computadora de la caja (TCM).',
        'datos': [['Relaciones', '1ª 2,875 · 2ª 1,568 · 3ª 1,000 · 4ª 0,697 · R 2,300'], ['Final', '4,052'], ['Fluido', 'SUZUKI ATF 3317 o Mobil ATF 3309'], ['Capacidad', '3,3 L en un cambio · 5,6 L total']],
        'mant': ['Controlar el nivel cada 30 000 km; cambiar el fluido cada 165 000 km (30 000 km en uso severo).', 'El nivel se mide en caliente, en P y con el motor en marcha.'],
        'ver': '05 Conducción y caja manual'},
    'semieje_izq': {
        'que': 'Palier que lleva el giro del diferencial a la rueda izquierda, con juntas homocinéticas en cada punta.',
        'datos': [['Juntas', 'homocinéticas con fuelles de goma']],
        'mant': ['Revisar los fuelles cada 45 000 km: si se rompen, entra tierra y se pierde la grasa.', 'Un "tac-tac" al doblar indica junta gastada.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'semieje_der': {
        'que': 'Palier derecho, igual al izquierdo pero de otro largo (el diferencial no está en el centro).',
        'datos': [['Juntas', 'homocinéticas con fuelles de goma']],
        'mant': ['Revisar los fuelles cada 45 000 km.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'palanca': {
        'que': 'Palanca selectora de la caja automática en la consola central.',
        'datos': [['Posiciones', 'P · R · N · D · 3 · 2 · L'], ['Arranque', 'solo en P o N']],
        'mant': ['Para salir de P hay que pisar el freno.', 'No pasar a P o R con el auto en movimiento.'],
        'ver': '05 Conducción y caja manual'},
    # ------------------------------------------------------------ Refrigeración
    'radiador': {
        'que': 'Intercambiador de aluminio con tanques plásticos que enfría el líquido del motor con el aire de la marcha.',
        'datos': [['Refrigerante', 'etilenglicol al 50 %'], ['Capacidad (AT)', '5,4 L motor + radiador + 0,7 L depósito']],
        'mant': ['Cambiar el refrigerante cada 45 000 km o 36 meses.', 'No abrir la tapa con el motor caliente.'],
        'ver': '07 Fluidos y capacidades'},
    'electroventilador': {
        'que': 'Ventilador eléctrico detrás del radiador. La computadora del motor lo prende según la temperatura y el aire acondicionado.',
        'datos': [['Fusible', 'RDTR FAN, 30 A']],
        'mant': ['Si el motor calienta en tránsito, revisar que el ventilador arranque y su fusible.'],
        'ver': '11 Diagnóstico de fallas'},
    'deposito_refrigerante': {
        'que': 'Depósito recuperador: recibe el líquido que se dilata en caliente y lo devuelve al enfriar.',
        'datos': [['Marcas', 'FULL y LOW']],
        'mant': ['Controlar el nivel en frío, entre FULL y LOW, una vez por semana.'],
        'ver': '07 Fluidos y capacidades'},
    # ------------------------------------------------------------ Eléctrico
    'bateria': {
        'que': 'Batería de plomo de 12 V que alimenta el arranque y todo el auto con el motor parado.',
        'datos': [['Tipo', '46B24R'], ['Capacidad', '36 Ah (5 h)'], ['Carga del alternador', '14,2–14,8 V']],
        'mant': ['Mantener los bornes limpios y ajustados.', 'Desconectar primero el negativo y conectarlo último.'],
        'ver': '10 Sistema eléctrico'},
    'fusibles': {
        'que': 'Caja de fusibles y relés del vano motor: alimenta el ventilador, la inyección, el ABS, la dirección eléctrica, los faros y el arranque.',
        'datos': [['Ejemplos', 'FI 15 A · ABS MOT 30 A · EPS 50 A · RDTR FAN 30 A · H/L L/R 15 A']],
        'mant': ['Cambiar un fusible siempre por uno del mismo amperaje.', 'Si se vuelve a quemar, buscar el cortocircuito.'],
        'ver': '10 Sistema eléctrico'},
    'fusibles_cabina': {
        'que': 'Caja de empalmes con los fusibles de la cabina, del lado del conductor bajo el tablero.',
        'datos': [['Ejemplos', 'IG COIL 15 A · DOME · tablero · encendedor']],
        'mant': ['Si se apagan a la vez varias cosas del tablero, revisar esta caja.'],
        'ver': '10 Sistema eléctrico'},
    # ------------------------------------------------------------ Suspensión y dirección
    'amortiguador_del_izq': {
        'que': 'Columna McPherson: amortiguador y resorte en un solo conjunto que además guía la rueda al doblar.',
        'datos': [['Caída', '0° ± 1° (no regulable)'], ['Avance', '5° 12′ ± 2° (no regulable)']],
        'mant': ['Revisar pérdidas de aceite y los topes de goma.', 'Cambiar los amortiguadores de a pares.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'amortiguador_del_der': {
        'que': 'Columna McPherson derecha, igual a la izquierda.',
        'datos': [['Caída', '0° ± 1° (no regulable)'], ['Avance', '5° 12′ ± 2° (no regulable)']],
        'mant': ['Revisar pérdidas de aceite y los topes de goma.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'brazo_izq': {
        'que': 'Brazo inferior en L que une la mangueta con el bastidor delantero por dos bujes y una rótula.',
        'datos': [['Uniones', 'rótula + 2 bujes de goma']],
        'mant': ['Revisar el juego de la rótula y las grietas en los bujes.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'brazo_der': {
        'que': 'Brazo inferior derecho, simétrico al izquierdo.',
        'datos': [['Uniones', 'rótula + 2 bujes de goma']],
        'mant': ['Revisar el juego de la rótula y las grietas en los bujes.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'estabilizadora': {
        'que': 'Barra de torsión que une las dos ruedas delanteras y reduce el balanceo al doblar.',
        'datos': [['Uniones', 'bujes al bastidor y bieletas a las columnas']],
        'mant': ['Un golpeteo en pozos suele ser una bieleta gastada.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'eje_torsion': {
        'que': 'Eje trasero semirrígido: dos brazos longitudinales unidos por una viga que se tuerce. Simple y liviano.',
        'datos': [['Convergencia trasera', '5,2 ± 5,2 mm (no regulable)'], ['Caída trasera', '−1° ± 1°']],
        'mant': ['Revisar los bujes delanteros de los brazos.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'amortiguador_tra_izq': {
        'que': 'Atrás, el resorte y el amortiguador van separados: el resorte apoya sobre el brazo y el amortiguador queda detrás del eje.',
        'datos': [['Tipo', 'resorte helicoidal + amortiguador telescópico']],
        'mant': ['Revisar pérdidas y los bujes de los extremos.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'amortiguador_tra_der': {
        'que': 'Resorte y amortiguador trasero derecho.',
        'datos': [['Tipo', 'resorte helicoidal + amortiguador telescópico']],
        'mant': ['Revisar pérdidas y los bujes de los extremos.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'cremallera': {
        'que': 'Caja de dirección de piñón y cremallera con las bieletas a las manguetas. La convergencia se regula girando las bieletas.',
        'datos': [['Convergencia delantera', '0 (+1,0 / −0,5) mm'], ['Giro de rueda', 'interior 39,1° · exterior 33,3°']],
        'mant': ['Revisar los fuelles y el juego de los extremos.', 'Alinear después de cambiar cualquier pieza de la dirección.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'columna_eps': {
        'que': 'Columna de dirección con un motor eléctrico que ayuda a girar (EPS). No tiene bomba ni líquido hidráulico.',
        'datos': [['Asistencia', 'eléctrica en la columna'], ['Fusible', 'EPS, 50 A'], ['Juego del volante', '0–30 mm']],
        'mant': ['Si se pone dura y se prende el testigo EPS, revisar batería y fusible antes que nada.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'volante': {
        'que': 'Volante de 3 rayos con el airbag del conductor en el centro. En el Swift japonés va a la derecha.',
        'datos': [['Lado', 'derecho'], ['Airbag', 'módulo en el centro']],
        'mant': ['No desarmar ni golpear el módulo del airbag: lo hace solo un taller habilitado.'],
        'ver': '12 Seguridad, airbags y carrocería'},
    # ------------------------------------------------------------ Frenos
    'disco_izq': {
        'que': 'Disco ventilado delantero: dos caras unidas por aletas para que se enfríe mejor.',
        'datos': [['Espesor', '20,0 mm (mín. 18,0)'], ['Torque de tuercas', '85 N·m']],
        'mant': ['Medir el espesor con micrómetro al cambiar pastillas.', 'Si vibra el pedal al frenar, revisar el alabeo.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'disco_der': {
        'que': 'Disco ventilado delantero derecho.',
        'datos': [['Espesor', '20,0 mm (mín. 18,0)']],
        'mant': ['Cambiar los discos de a pares.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'mordaza_izq': {
        'que': 'Mordaza (caliper) flotante de un pistón que aprieta las pastillas contra el disco.',
        'datos': [['Pastillas', '10 mm nuevas · cambiar con 2 mm']],
        'mant': ['Revisar las pastillas cada 15 000 km.', 'Cambiar las 4 pastillas del eje juntas.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'mordaza_der': {
        'que': 'Mordaza delantera derecha.',
        'datos': [['Pastillas', '10 mm nuevas · cambiar con 2 mm']],
        'mant': ['Revisar las pastillas cada 15 000 km.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'tambor_izq': {
        'que': 'Freno trasero a tambor con zapatas (tipo zapata primaria y secundaria). También actúa el freno de mano.',
        'datos': [['Diámetro interior', '200 mm (máx. 202)']],
        'mant': ['Revisar zapatas y tambor cada 30 000 km.', 'Si el freno de mano sube mucho, regular.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'tambor_der': {
        'que': 'Freno trasero derecho a tambor.',
        'datos': [['Diámetro interior', '200 mm (máx. 202)']],
        'mant': ['Revisar zapatas y tambor cada 30 000 km.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'servofreno': {
        'que': 'Servofreno de vacío que multiplica la fuerza del pie, con la bomba de freno y su depósito adelante. Va del lado del conductor.',
        'datos': [['Líquido', 'DOT 3 / SAE J1703'], ['Altura del pedal', '130–150 mm desde el piso']],
        'mant': ['Cambiar el líquido cada 30 000 km o 24 meses.', 'Si el nivel baja, revisar pastillas y pérdidas.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    # ------------------------------------------------------------ Ruedas
    'rueda_del_izq': {
        'que': 'Rueda delantera: llanta de aleación de 15" y neumático radial.',
        'datos': [['Neumático', '185/60R15 84H'], ['Llanta', '15 × 5½ JJ'], ['Tuercas', '85 N·m']],
        'mant': ['Presión en frío según la etiqueta del marco de la puerta del conductor.', 'Rotar las ruedas cada 15 000 km.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'rueda_del_der': {
        'que': 'Rueda delantera derecha.',
        'datos': [['Neumático', '185/60R15 84H'], ['Tuercas', '85 N·m']],
        'mant': ['Ajustar las tuercas en cruz.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'rueda_tra_izq': {
        'que': 'Rueda trasera izquierda.',
        'datos': [['Neumático', '185/60R15 84H'], ['Tuercas', '85 N·m']],
        'mant': ['Revisar desgaste irregular: puede indicar bujes del eje gastados.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'rueda_tra_der': {
        'que': 'Rueda trasera derecha.',
        'datos': [['Neumático', '185/60R15 84H'], ['Tuercas', '85 N·m']],
        'mant': ['Revisar desgaste y daños en cada service.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    # ------------------------------------------------------------ Combustible y escape
    'tanque': {
        'que': 'Tanque de 43 L debajo del asiento trasero, con la bomba eléctrica y el aforador adentro.',
        'datos': [['Capacidad', '43 L'], ['Combustible', 'nafta sin plomo regular (91 RON en Japón)'], ['Filtro', 'cambio cada 105 000 km']],
        'mant': ['No andar siempre en reserva: la bomba se enfría con la nafta.', 'Revisar el tanque y sus caños cada 45 000 km.'],
        'ver': '07 Fluidos y capacidades'},
    'escape': {
        'que': 'Caño de escape con el catalizador debajo del piso y el silenciador atrás.',
        'datos': [['Tramos', 'bajada · catalizador · caño central · silenciador']],
        'mant': ['Revisar soportes de goma y pérdidas cada 30 000 km.', 'Un ruido metálico abajo suele ser un cubrecalor flojo.'],
        'ver': '08 Plan de mantenimiento'},
    # ------------------------------------------------------------ Interior
    'asiento_izq': {
        'que': 'Asiento del acompañante con apoyacabeza y cinturón de 3 puntos con pretensor.',
        'datos': [['Cinturón', '3 puntos, pretensor']],
        'mant': ['Revisar que el cinturón se trabe con un tirón fuerte.'],
        'ver': '12 Seguridad, airbags y carrocería'},
    'asiento_der': {
        'que': 'Asiento del conductor (mano derecha), regulable en largo y respaldo.',
        'datos': [['Cinturón', '3 puntos, pretensor']],
        'mant': ['Revisar las correderas y que trabe en cada posición.'],
        'ver': '04 Mandos e instrumentos'},
    'asiento_trasero': {
        'que': 'Asiento trasero de 3 plazas con respaldo rebatible para agrandar el baúl.',
        'datos': [['Plazas', '3']],
        'mant': ['Al volver a levantar el respaldo, verificar que trabe.'],
        'ver': '04 Mandos e instrumentos'},
    'tablero': {
        'que': 'Tablero con el cuadro de tres relojes (velocímetro, cuentavueltas y combustible/temperatura), el audio y los mandos del aire.',
        'datos': [['Cuadro', '3 relojes + testigos'], ['Lado', 'conductor a la derecha']],
        'mant': ['Al dar contacto, todos los testigos deben prenderse y apagarse al arrancar.'],
        'ver': '04 Mandos e instrumentos'},
    'pedalera': {
        'que': 'Con caja automática hay solo dos pedales: freno (ancho) y acelerador.',
        'datos': [['Pedales', 'freno y acelerador'], ['Altura del freno', '130–150 mm']],
        'mant': ['Manejar con el pie derecho solo; el izquierdo descansa.'],
        'ver': '05 Conducción y caja manual'},
}

# ------------------------------------------------------------ piezas agregadas en la versión detallada (15/11/2026)
PIEZAS.pop('vidrios_fijos', None)
PIEZAS['puerta_tra_izq']['que'] = 'Puerta trasera izquierda. Su borde de atrás rodea el pasarrueda y el vidrio tiene un sector fijo detrás de un parante negro.'
PIEZAS['puerta_tra_der']['que'] = 'Puerta trasera derecha, simétrica a la izquierda, con el mismo vidrio fijo atrás.'
PIEZAS.update({
    'tapa_combustible': {
        'que': 'Tapa redonda de la boca de carga de nafta, en el costado trasero izquierdo. Se abre con una palanca desde el asiento del conductor.',
        'datos': [['Lado', 'izquierdo'], ['Combustible', 'nafta sin plomo regular']],
        'mant': ['Apretar el tapón hasta que haga clic: si queda flojo puede prender el testigo de motor por el sistema de vapores (EVAP).'],
        'ver': '07 Fluidos y capacidades'},
    'antiniebla_izq': {
        'que': 'Faro antiniebla redondo en el paragolpes, debajo del faro principal.',
        'datos': [['Fusible', 'FR FOG, 15 A']],
        'mant': ['Usar solo con niebla o lluvia intensa: encandila a los demás.'],
        'ver': '10 Sistema eléctrico'},
    'antiniebla_der': {
        'que': 'Faro antiniebla derecho, igual al izquierdo.',
        'datos': [['Fusible', 'FR FOG, 15 A']],
        'mant': ['Revisar que el vidrio no esté roto: entra agua y quema la lámpara.'],
        'ver': '10 Sistema eléctrico'},
    'abs': {
        'que': 'Unidad hidráulica del ABS con su bomba y su computadora. Si una rueda se bloquea, baja y sube la presión de ese freno varias veces por segundo.',
        'datos': [['Fusibles', 'ABS MOT 30 A · ABS SOL 30 A'], ['Testigo', 'ABS en el tablero']],
        'mant': ['Al purgar los frenos, seguir el orden del manual para no meter aire en la unidad.', 'Con el testigo prendido los frenos andan, pero sin antibloqueo.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'freno_mano': {
        'que': 'Palanca del freno de estacionamiento entre los asientos. Tira de dos cables que abren las zapatas de los tambores traseros.',
        'datos': [['Actúa sobre', 'tambores traseros']],
        'mant': ['Revisar el recorrido a los primeros 15 000 km.', 'En pendiente, poner el freno de mano antes de pasar a P.'],
        'ver': '05 Conducción y caja manual'},
    'bastidor': {
        'que': 'Cuna de acero abulonada abajo del vano motor. Sostiene los brazos de la suspensión y un soporte del motor.',
        'datos': [['Fijación', '4 bulones a la carrocería']],
        'mant': ['Después de un golpe abajo, revisar que no esté doblada: cambia la alineación.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'mangueras': {
        'que': 'Mangueras del circuito de refrigeración: la superior lleva el líquido caliente al radiador, la inferior lo devuelve frío y dos más van a la calefacción. El termostato abre el paso al radiador cuando el motor calienta.',
        'datos': [['Refrigerante', 'etilenglicol al 50 %']],
        'mant': ['Revisar grietas y abrazaderas en cada service.', 'Si la superior queda fría con el motor caliente, el termostato no abre.'],
        'ver': '07 Fluidos y capacidades'},
    'ecu': {
        'que': 'Computadora del motor (ECM): lee los sensores y maneja la inyección, el encendido, el VVT y el electroventilador. Guarda los códigos de falla.',
        'datos': [['Diagnóstico', 'conector OBD-II bajo el tablero']],
        'mant': ['Leer los códigos con un escáner antes de cambiar piezas.', 'No desconectarla con el contacto puesto.'],
        'ver': '11 Diagnóstico de fallas'},
    'bocina': {
        'que': 'Bocina eléctrica detrás del paragolpes delantero.',
        'datos': [['Tensión', '12 V']],
        'mant': ['Si no suena, revisar el fusible y el relé antes que la bocina.'],
        'ver': '10 Sistema eléctrico'},
    'techo_interior': {
        'que': 'Espejo retrovisor interior pegado al parabrisas, parasoles y luz de techo.',
        'datos': [['Fusible de la luz', 'DOME']],
        'mant': ['Si el espejo se despega, se vuelve a pegar con adhesivo especial para vidrio.'],
        'ver': '04 Mandos e instrumentos'},
    'tapizado_izq': {
        'que': 'Paneles interiores de las puertas izquierdas: apoyabrazos, manija interior y parlante.',
        'datos': [['Fijación', 'grampas y tornillos']],
        'mant': ['Para sacarlos, primero los tornillos del apoyabrazos y después las grampas, de abajo hacia arriba.'],
        'ver': '12 Seguridad, airbags y carrocería'},
    'tapizado_der': {
        'que': 'Paneles interiores de las puertas derechas, con la botonera de levantavidrios en la del conductor.',
        'datos': [['Fijación', 'grampas y tornillos']],
        'mant': ['Cuidar la lámina de nylon de adentro: evita que entre agua al panel.'],
        'ver': '04 Mandos e instrumentos'},
})
CONJ['Carrocería']['laminas'].insert(0, ['swift_frente_detalle.jpg', 'Frente: parrilla de panal, faros, antinieblas y patente'])
CONJ['Iluminación']['laminas'] = [['swift_frente_detalle.jpg', 'Faros con sus reflectores y antinieblas'],
                                  ['swift_cola_detalle.jpg', 'Calaveras con sectores de giro y marcha atrás']]
CONJ['Puertas y cristales']['laminas'].append(['swift_cola_detalle.jpg', 'Luneta con banda negra, alerón y limpialuneta'])


# ------------------------------------------------------------ mecánica corregida y completada con el manual de taller en castellano (15/11/2026)
CONJ['Motor M15A']['resumen'] = ('Naftero de 4 cilindros en línea, 1490 cm³, DOHC de 16 válvulas con distribución por cadena y VVT en la admisión. '
                                 'Va transversal: escape y catalizador adelante (hacia el radiador), admisión atrás (hacia el torpedo), '
                                 'distribución a la derecha y caja a la izquierda.')
CONJ['Motor M15A']['laminas'].insert(0, ['lamina_vano_motor.jpg', 'Vano motor visto de adelante: escape y catalizador al frente, admisión atrás'])
CONJ['Motor por dentro'] = {
    'color': '#d98b2b', 'nota': '06 Motor M15A',
    'resumen': 'Lo que está adentro del bloque y la tapa: cigüeñal con 5 bancadas, 4 pistones con sus bielas, dos árboles de levas (el de admisión con VVT), 16 válvulas con botadores a calce, cadena de distribución y las bombas de aceite y de agua. Medidas del manual de taller.',
    'laminas': [['lamina_motor_dentro.jpg', 'Motor por dentro: cigüeñal, pistones, levas, válvulas y cadena']]}
CONJ['Aire acondicionado y calefacción'] = {
    'color': '#2fa3c9', 'nota': '10 Sistema eléctrico',
    'resumen': 'Aire acondicionado manual con gas HFC-134a: compresor movido por correa, condensador delante del radiador, filtro secador, cañerías y la unidad HVAC detrás del tablero con el evaporador, el radiador de calefacción y el soplador.',
    'laminas': [['lamina_vano_motor.jpg', 'Condensador al frente del radiador y compresor adelante, abajo']]}
CONJ['Combustible y escape']['resumen'] = ('Tanque de 43 L bajo el asiento trasero con la bomba adentro y el canister EVAP en el vano motor. '
    'El escape sale del múltiple con catalizador incorporado (adelante), pasa bajo el motor, sigue por el caño central con resonador y termina en el silenciador trasero.')
PIEZAS['multiple_escape'] = {
    'que': 'Múltiple de escape de acero con el catalizador incorporado, montado adelante del motor (mirando al radiador). Lleva la sonda de oxígeno 1 antes del catalizador y la 2 después.',
    'datos': [['Ubicación', 'frente del motor'], ['Sondas', 'n° 1 (conector verde) y n° 2 (conector gris)']],
    'mant': ['Para sacarlo hay que retirar el paragolpes, el radiador y separar el condensador del A/C.', 'Trabajar siempre con el escape frío; juntas nuevas al armar.'],
    'ver': '06 Motor M15A'}
PIEZAS['admision']['que'] = 'Múltiple de admisión plástico, montado atrás del motor (mirando al torpedo), con la cámara, los conductos, los 4 inyectores con su riel y el cuerpo de mariposa en la punta izquierda.'
PIEZAS['admision']['datos'] = [['Ubicación', 'atrás del motor'], ['Inyección', 'multipunto (EPI)'], ['Presión de nafta', '270–310 kPa (bomba andando)'], ['Sensores', 'TP en la mariposa, MAP en la cámara']]
PIEZAS['accesorios']['que'] = ('Del lado derecho, dos correas: una mueve la bomba de agua y el alternador (atrás, arriba) y la otra el compresor del aire acondicionado (adelante, abajo).')
PIEZAS['accesorios']['datos'] = [['Alternador', '70 A, atrás del motor'], ['Compresor', 'adelante, abajo (Mitsubishi o Matsushita)'], ['Tensión de correa', '4,5–5,5 mm con 100 N']]
PIEZAS['distribucion']['que'] = 'Tapa de la cadena de distribución, del lado derecho. Tiene adentro la bomba de aceite de rotores, movida directo por el cigüeñal.'
PIEZAS['bloque']['que'] = 'Bloque de aluminio con las camisas de los 4 cilindros y el cárter abajo. El filtro de aceite va adelante, del lado del escape.'
PIEZAS['mangueras']['que'] = ('Mangueras y caños del agua: la superior sale de la tapa de salida de agua (en la tapa de cilindros, lado de la caja) al radiador; '
                              'la inferior vuelve a la caja del termostato, que está atrás del motor. Dos más van al radiador de la calefacción.')
PIEZAS['mangueras']['mant'] = ['Revisar grietas y abrazaderas en cada service.', 'Para cambiar el termostato hay que sacar antes el múltiple de admisión y el alternador.']
PIEZAS['escape']['que'] = 'Caño delantero bajo el motor con flexible, caño central con resonador, silenciador trasero y protector de calor bajo el piso. Va colgado con gomas.'
PIEZAS['escape']['datos'] = [['Tramos', 'caño n° 1 · central con resonador · silenciador'], ['Salida', 'derecha']]
PIEZAS.update({
    'soportes_motor': {
        'que': 'Tres soportes de goma sostienen el motor y la caja: el derecho sobre la distribución, el izquierdo sobre la caja y uno trasero (barra de reacción) a la cuna, que frena el giro del motor al acelerar.',
        'datos': [['Cantidad', '3 (derecho, izquierdo y trasero)']],
        'mant': ['Un golpe al pasar de P a D o al acelerar suele ser un soporte roto.', 'Algunos pernos son con adhesivo y no se reutilizan.'],
        'ver': '06 Motor M15A'},
    'ciguenal': {
        'que': 'Eje que convierte el movimiento de los pistones en giro. Tiene 5 muñones de bancada, 4 muñequillas (1 y 4 arriba, 2 y 3 abajo) y contrapesos. Adelante lleva el piñón de la cadena y atrás la placa de arrastre con la corona del arranque.',
        'datos': [['Muñón de bancada', 'Ø 51,994–52,000 mm'], ['Muñequilla', 'Ø 44,994–45,000 mm'], ['Carrera', '78 mm']],
        'mant': ['Al rectificar, elegir los cojinetes por las letras y números grabados en el bloque y el cigüeñal.'],
        'ver': '06 Motor M15A'},
    'pistones': {
        'que': 'Cuatro pistones de aluminio con dos aros de compresión y uno de aceite, unidos al cigüeñal por las bielas.',
        'datos': [['Diámetro del pistón', '77,969–77,984 mm'], ['Sobremedida', '+0,50 mm'], ['Perno', 'Ø 19,997–20,000 mm'], ['Biela', 'largo aproximado en el modelo']],
        'mant': ['Medir el pistón en la falda, perpendicular al perno.', 'Las tuercas de biela llevan apriete en ángulo.'],
        'ver': '06 Motor M15A'},
    'arboles_levas': {
        'que': 'Dos árboles de levas en la tapa: el de admisión atrás, con el actuador del VVT en el piñón, y el de escape adelante. Cada leva empuja un botador.',
        'datos': [['Altura de leva admisión', '44,929–45,089 mm (mín. 44,80)'], ['Altura de leva escape', '44,399–44,559 mm (mín. 44,28)'], ['Válvula OCV', '6,7–7,7 Ω a 20 °C']],
        'mant': ['Al armar, alinear las marcas de los piñones con la cadena.', 'Un VVT trabado da el código P0011: revisar aceite y la válvula OCV.'],
        'ver': '06 Motor M15A'},
    'valvulas': {
        'que': 'Dieciséis válvulas (cuatro por cilindro) con sus resortes y botadores tipo vaso. La luz se ajusta cambiando el calce del botador.',
        'datos': [['Vástago (admisión)', 'Ø 5,465–5,480 mm'], ['Resorte libre', '36,83 mm (mín. 35,83)'], ['Precarga', '107–125 N a 31,5 mm'], ['Botador', 'Ø 30,959–30,975 mm']],
        'mant': ['Luz de válvulas cada 30 000 km (ver la nota 06).', 'Lapear al reemplazar una válvula.'],
        'ver': '06 Motor M15A'},
    'cadena': {
        'que': 'Cadena de distribución con guía fija, guía móvil y tensor hidráulico. Mueve los dos árboles de levas a la mitad de vueltas del cigüeñal.',
        'datos': [['Relación', '2 : 1'], ['Cambio', 'sin intervalo fijo']],
        'mant': ['Ruido de cadena al arrancar en frío: revisar el tensor y el aceite.'],
        'ver': '06 Motor M15A'},
    'bombas': {
        'que': 'Bomba de aceite de rotores (interior y exterior) dentro de la tapa de distribución, con su colador en el cárter; y la bomba de agua, movida por la correa.',
        'datos': [['Presión de aceite', 'más de 270 kPa a 4000 rpm'], ['Bomba de agua', 'por correa, lado derecho']],
        'mant': ['Limpiar el colador cuando se baja el cárter.', 'Pérdida por el agujero testigo de la bomba de agua: cambiarla.'],
        'ver': '06 Motor M15A'},
    'convertidor': {
        'que': 'Convertidor de par: acople hidráulico entre el motor y la caja automática, abulonado a la placa de arrastre del cigüeñal. Permite que el auto quede parado en D con el motor en marcha.',
        'datos': [['Fijación', '3 pernos a la placa de arrastre']],
        'mant': ['Al montar la caja, verificar que el convertidor entró hasta el fondo antes de apretar.'],
        'ver': '05 Conducción y caja manual'},
    'canister': {
        'que': 'Recipiente con carbón activado que junta los vapores de nafta del tanque. La computadora abre la válvula de purga para quemarlos en el motor.',
        'datos': [['Sistema', 'EVAP'], ['Control', 'válvula de purga comandada por el ECM']],
        'mant': ['Revisar el sistema EVAP a los 90 000 km.', 'No cargar el tanque de más: el líquido daña el canister.'],
        'ver': '08 Plan de mantenimiento'},
    'sensores_abs': {
        'que': 'Un sensor magnético por rueda, frente a un anillo dentado, le dice al ABS a qué velocidad gira cada una.',
        'datos': [['Cantidad', '4'], ['Luz sensor-anillo', 'no se ajusta']],
        'mant': ['Limpiar viruta o barro del anillo si se prende el testigo ABS.', 'Cuidar el cable al cambiar amortiguadores.'],
        'ver': '09 Frenos, suspensión, dirección y ruedas'},
    'condensador': {
        'que': 'Intercambiador delante del radiador que enfría y condensa el gas del aire acondicionado, con el filtro secador al costado.',
        'datos': [['Gas', 'HFC-134a (R-134a)'], ['Ubicación', 'adelante del radiador']],
        'mant': ['Limpiarlo con agua a baja presión desde atrás.', 'Al abrir el circuito, cambiar el secador.'],
        'ver': '10 Sistema eléctrico'},
    'canerias_ac': {
        'que': 'Cañerías de aluminio del aire acondicionado: alta presión (compresor → condensador), líquido (condensador → evaporador) y succión (evaporador → compresor).',
        'datos': [['Gas', 'HFC-134a'], ['Sensor', 'presión del refrigerante']],
        'mant': ['El gas y el aceite del compresor no se mezclan con los de otros sistemas.', 'Cargar con equipo y la cantidad del manual.'],
        'ver': '10 Sistema eléctrico'},
    'unidad_hvac': {
        'que': 'Caja detrás del tablero con el evaporador del aire acondicionado, el radiador de calefacción, el soplador y las compuertas que reparten el aire a los conductos.',
        'datos': [['Soplador', 'lado del acompañante'], ['Fusible del soplador', 'HTR FAN, 30 A']],
        'mant': ['Cambiar el filtro de habitáculo (si tiene) cada 45 000 km.', 'Olor a humedad: limpiar el evaporador.'],
        'ver': '10 Sistema eléctrico'},
})


# ------------------------------------------------------------ sistema eléctrico, caja por dentro y detalle del manual completo (15/11/2026)
import json as _json, os as _os, re as _re
_MD = _json.load(open(_os.path.join(VAULT, 'herramientas', 'manual_datos.json'), encoding='utf-8'))
_DTC = [(c, t) for cap in ('1A', '5A', '4E', '6C', '8B', '7B') for c, t in _MD['capitulos'][cap]['dtc']]
_CON = _MD['conectores']


def _dtc(*palabras):
    out = []
    for c, t in _DTC:
        if any(_re.search(w, t, _re.I) for w in palabras) and c not in out:
            out.append(c)
    return ', '.join(out[:6]) or '—'


def _con(*codigos):
    return ' · '.join(f"{c} ({_CON[c][0]})" if c in _CON and _CON[c][0] not in ('', '-', 'N') else c for c in codigos)


PIEZAS.pop('fusibles_cabina', None)
for cj, color, nota, resumen, lam in (
    ('Sensores y actuadores', '#f2c14e', 'Manual de taller › 1A, 1C', 'Todos los sensores que lee la computadora del motor y los actuadores que maneja, en su lugar real según el diagrama de ubicación del manual (1A) y con su conector del mazo del motor (tabla del capítulo 9A).',
     [['lamina_electrico_motor.jpg', 'Sensores, actuadores y mazo del motor']]),
    ('Módulos de control', '#9b5de5', 'Manual de taller › 1A, 5A, 6C, 8B, 10B, 10C', 'Las computadoras del auto: ECM (motor), TCM (caja), BCM dentro del bloque de empalmes, EPS (dirección), SDM (airbag), módulo de arranque sin llave, antena del inmovilizador y el cuadro de instrumentos.',
     [['lamina_electrico.jpg', 'Módulos y mazos de cables']]),
    ('Cableado', '#2b2d30', 'Manual de taller › 9A Sistemas de cableado', 'Mazos de cables con sus conectores: batería (A), motor (C), principal (E), tablero (G), piso (L), puertas y portón. Cada circuito del manual se puede resaltar en el visor (pestaña Circuitos).',
     [['lamina_electrico.jpg', 'Recorrido de los mazos'], ['lamina_electrico_motor.jpg', 'Mazo del motor y sus ramas']]),
    ('Accesorios eléctricos', '#4cc9a0', 'Manual de taller › 9D, 9E, 9F', 'Limpiaparabrisas y limpialuneta, lavadores, levantavidrios, cierre centralizado y desempañador.', []),
    ('Airbag y cinturones', '#e07a5f', 'Manual de taller › 8A, 8B', 'Airbags frontales, SDM y cinturones delanteros con pretensor. Trabajar siempre con la batería desconectada y esperando 90 s.', []),
    ('Caja por dentro', '#6c757d', 'Manual de taller › 5A', 'Lo que está dentro del transeje automático: bomba de aceite, embragues, tren planetario Ravigneaux, cuerpo de válvulas con solenoides, engranajes de salida y diferencial.',
     [['lamina_caja_dentro.jpg', 'Caja automática por dentro']])):
    CONJ[cj] = {'color': color, 'nota': nota, 'resumen': resumen, 'laminas': lam}
CONJ.setdefault('Eléctrico', {'color': '#08b94e'})['resumen'] = 'Batería, caja de fusibles del motor y bocina.'


def F(que, datos, mant, ver):
    return {'que': que, 'datos': datos, 'mant': mant, 'ver': ver}


V1C = 'Manual › 1C Dispositivos eléctricos del motor'
PIEZAS.update({
    'sensor_maf': F('Mide la masa de aire que entra al motor (hilo caliente) y, en el mismo cuerpo, la temperatura del aire (IAT). Con ese dato el ECM calcula cuánta nafta inyectar.',
                    [['Conector', _con('C13')], ['Códigos', _dtc('caudal de masa', 'temperatura del aire de admisión')]],
                    ['No tocar el elemento sensor; limpiar solo con limpiador específico para MAF.'], V1C),
    'sensor_tp': F('Potenciómetro en el eje de la mariposa: le dice al ECM cuánto se pisa el acelerador.',
                   [['Conector', _con('C11')], ['Códigos', _dtc('posición de la mariposa')]], ['Después de cambiarlo, verificar la tensión en ralentí con el escáner.'], V1C),
    'valvula_iac': F('Válvula de control del aire de ralentí: deja pasar aire alrededor de la mariposa para mantener las vueltas en ralentí.',
                     [['Conector', _con('C01')], ['Códigos', _dtc('ralentí', 'IAC')]], ['Ralentí inestable: limpiar el cuerpo de mariposa y el paso de la IAC.'], 'Manual › 1D Mecánica del motor'),
    'sensor_map': F('Mide la presión (vacío) dentro del colector de admisión.', [['Conector', _con('C12')], ['Códigos', _dtc('presión absoluta')]],
                    ['Revisar la manguera de vacío si da lecturas raras.'], V1C),
    'sensor_ect': F('Termistor en la tapa de salida de agua: informa la temperatura del refrigerante al ECM (inyección, ventilador, reloj).',
                    [['Conector', _con('C09')], ['Códigos', _dtc('temperatura del refrigerante')]], ['Cambiar con el motor frío y reponer refrigerante.'], V1C),
    'sensor_cmp': F('Lee la posición del árbol de levas para identificar el cilindro 1 y controlar el VVT.', [['Conector', _con('C08')], ['Códigos', _dtc('árbol de levas')]],
                    ['Una falla puede dar arranque largo o el código del VVT.'], 'Manual › 1H Sistema de encendido'),
    'sensor_ckp': F('Lee los dientes de la rueda del cigüeñal: régimen del motor y posición de los pistones para inyectar y encender.',
                    [['Conector', _con('C20')], ['Códigos', _dtc('cigüeñal')]], ['Sin esta señal el motor no arranca: es lo primero a revisar si no hay chispa.'], 'Manual › 1H Sistema de encendido'),
    'sensor_detonacion': F('Piezoeléctrico abulonado al bloque: detecta el "pistoneo" para que el ECM atrase el encendido.', [['Conector', _con('C26')], ['Códigos', _dtc('detonación')]],
                           ['Respetar el par de apriete: flojo o muy apretado cambia la lectura.'], V1C),
    'sensor_presion_aceite': F('Interruptor que prende el testigo de aceite cuando la presión cae.', [['Conector', _con('C18')], ['Presión', 'más de 270 kPa a 4000 rpm']],
                               ['Si el testigo se prende andando, parar el motor y medir la presión con manómetro.'], 'Manual › 1E Sistema de lubricación del motor'),
    'solenoide_vvt': F('Válvula de control de aceite (OCV): manda aceite al actuador del árbol de levas de admisión para adelantar o atrasar la distribución.',
                       [['Conector', _con('C19')], ['Resistencia', '6,7–7,7 Ω a 20 °C'], ['Códigos', _dtc('actuador de posición', 'demasiado avanzada')]],
                       ['Limpiar su colador si hay códigos del VVT.'], 'Manual › 1D Mecánica del motor'),
    'sonda_o2_1': F('Sonda de oxígeno calentada antes del catalizador: el ECM ajusta la mezcla con su señal.', [['Conector', _con('C15')], ['Códigos', _dtc('HO2S', 'oxígeno')]],
                    ['Ajustar con la llave especial; no usar productos con siliconas cerca.'], 'Manual › 1K Sistema de escape'),
    'sonda_o2_2': F('Sonda de oxígeno después del catalizador: controla que el catalizador funcione (código P0420).', [['Conector', _con('C16')], ['Códigos', _dtc('catalizador')]],
                    ['Revisar primero pérdidas de escape antes de cambiarla.'], 'Manual › 1K Sistema de escape'),
    'sensor_vss': F('Sensor de velocidad del vehículo en la caja: lo usan el velocímetro, el ECM, el TCM y la dirección eléctrica.', [['Conector', _con('C25')], ['Códigos', _dtc('velocidad del vehículo')]],
                    ['Si el velocímetro marca 0, revisar este sensor y su conector.'], 'Manual › 1A Información general y diagnóstico del motor'),
    'valvula_purga': F('Solenoide que abre el paso de los vapores del canister al colector cuando el motor está caliente.', [['Conector', _con('C14')], ['Códigos', _dtc('purga', 'EVAP')]],
                       ['Un chasquido suave en marcha es normal.'], 'Manual › 1B Dispositivos auxiliares de control de emisiones'),
    'valvula_egr': F('Válvula de recirculación de gases movida por un motor paso a paso: devuelve un poco de gas de escape a la admisión para bajar la temperatura de combustión.',
                     [['Conector', _con('C10')], ['Códigos', _dtc('EGR')]], ['Con carbón, el ralentí se vuelve inestable: limpiar los conductos.'], 'Manual › 1B Dispositivos auxiliares de control de emisiones'),
    'sensor_rango_caja': F('Interruptor en el eje de la palanca de la caja: le dice al TCM y al ECM en qué posición está (P R N D 3 2 L), permite el arranque solo en P o N y prende la luz de marcha atrás.',
                           [['Códigos', _dtc('rango de la transmisión', 'interruptor de rango')]], ['Si no arranca en P, probar en N: puede estar desajustado.'], 'Manual › 5A Transmisión automática - Transeje automático'),
    'interruptor_freno': F('Interruptor sobre el pedal de freno: enciende las luces de freno y avisa al ECM, al TCM y al ABS que se está frenando.', [['Fusible', 'STOP LAMP 15 A']],
                           ['Regular la luz con el pedal si las luces quedan prendidas.'], 'Manual › 4A Sistema de mando de los frenos y diagnósticos'),
    'interruptor_nivel_freno': F('Flotante en el depósito de la bomba de freno: prende el testigo de frenos si baja el líquido.', [['Conector', _con('E02')]],
                                 ['Testigo prendido con freno de mano bajo: revisar nivel y pastillas.'], 'Manual › 4A Sistema de mando de los frenos y diagnósticos'),
    'sensor_presion_ac': F('Mide la presión del gas del aire acondicionado: protege el compresor y comanda el ventilador.', [['Conector', _con('E04')], ['Gas', 'R-134a']],
                           ['Se cambia con el circuito descargado.'], 'Manual › 7B Sistema de aire acondicionado'),
    'inyectores': F('Cuatro inyectores electromagnéticos que pulverizan la nafta en cada conducto de admisión, uno por cilindro, comandados por el ECM.',
                    [['Conectores', _con('C04', 'C05', 'C06', 'C07')], ['Presión', '270–310 kPa']], ['Juntas tóricas nuevas al montarlos.'], 'Manual › 1G Sistema de combustible'),
    'bobinas': F('Dos bobinas de chispa perdida: una dispara los cilindros 1 y 4 y la otra el 2 y 3, con cables de alta a las bujías que no tienen bobina encima.',
                 [['Conectores', _con('C02', 'C03')], ['Orden de encendido', '1-3-4-2'], ['Códigos', _dtc('encendido')]], ['Revisar los cables de alta si hay fallas en un solo par de cilindros.'], 'Manual › 1H Sistema de encendido'),
    'tcm': F('Computadora de la caja automática: decide los cambios con la velocidad, la mariposa y el rango; maneja los solenoides de cambio y de presión.',
             [['Conectores', _con('C34', 'C35')], ['Fusible', 'AT ETM 15 A'], ['Códigos', _dtc('TCM', 'solenoide')]], ['Leer los códigos P07xx con escáner antes de tocar la caja.'], 'Manual › 5A Transmisión automática - Transeje automático'),
    'modulo_eps': F('Módulo de la dirección eléctrica: lee el sensor de par y la velocidad y controla el motor de asistencia.', [['Fusible', 'EPS 50 A'], ['Códigos', _dtc('EPS', 'par', 'motor de P/S')]],
                    ['Si la dirección se pone dura, revisar batería y fusible primero.'], 'Manual › 6C Sistema de servodirección asistida'),
    'sdm': F('Módulo de diagnóstico y sensor del airbag, bajo la consola: detecta el choque y dispara airbags y pretensores; guarda los códigos del sistema SRS.',
             [['Códigos', _dtc('airbag', 'pretensor')]], ['No golpear ni desconectar con la batería conectada.'], 'Manual › 8B Sistema de airbag'),
    'modulo_keyless': F('Módulo del arranque sin llave (en las versiones que lo traen): habla con la llave electrónica por antenas y habilita el arranque.', [['Capítulo', '10E']],
                        ['Registrar las llaves con el equipo de Suzuki.'], 'Manual › 10E Sistema de arranque sin llave'),
    'bloque_empalmes': F('Bloque de empalmes del lado del conductor: fusibles y relés de la cabina y, adentro, el BCM que maneja luces, cierre, desempañador y avisos.',
                         [['Fusibles', 'IG COIL, DOME y otros'], ['Comunicación', 'CAN con ECM y cuadro']], ['Fusible quemado: cambiar por uno igual y buscar el corto.'], 'Manual › 10B Sistema de control eléctrico de la carrocería'),
    'cuadro_instrumentos': F('Cuadro de tres relojes (velocímetro, cuentavueltas y combustible/temperatura) con testigos; recibe los datos por CAN.',
                             [['Relojes', '3'], ['Testigos', 'aceite, carga, frenos, ABS, airbag, EPS, motor']], ['Con el contacto puesto todos los testigos se prenden un momento.'], 'Manual › 9C Instrumentos - Información para el conductor - Bocina'),
    'antena_inmovilizador': F('Bobina-antena alrededor del tambor de la llave: lee el transpondedor de la llave y se lo pasa al ECM para habilitar el arranque.',
                              [['Códigos', _dtc('inmovilizador')]], ['Una llave nueva se registra en el ECM con el equipo de diagnóstico.'], 'Manual › 10C Sistema de control del inmovilizador'),
    'cable_bateria': F('Cable positivo grueso a la caja de fusibles, al arranque y al alternador, y cables de masa a la caja y a la carrocería.',
                       [['Batería', '46B24R']], ['Masas flojas causan fallas raras en todo el auto: limpiar y ajustar.'], 'Manual › 1I Sistema de arranque'),
    'mazo_motor': F('Mazo del motor: lleva todos los sensores y actuadores del motor hasta el ECM y se une al principal por el conector C36/E24.',
                    [['Conectores', 'C01 a C41'], ['ECM', _con('C37')]], ['Revisar que no roce el escape ni piezas móviles.'], 'Manual › 9A Sistemas de cableado'),
    'mazo_principal': F('Mazo principal del vano motor: faros, ventilador, bocina, ABS, limpiaparabrisas y relés; entra a la cabina por el pasacables del torpedo.',
                        [['Conectores', 'E01 en adelante']], ['El pasacables debe quedar bien puesto para que no entre agua.'], 'Manual › 9A Sistemas de cableado'),
    'cable_eps': F('Cable grueso que alimenta la dirección eléctrica desde la caja de fusibles.', [['Fusible', 'EPS 50 A']], ['Conector bien trabado: un falso contacto deja la dirección dura.'], 'Manual › 6C Sistema de servodirección asistida'),
    'mazo_tablero': F('Mazo del tablero sobre el travesaño: cuadro, radio, climatizador, columna, airbag del acompañante, TCM y bloque de empalmes.', [['Conectores', 'G01 en adelante']],
                      ['Para trabajar detrás del tablero, desconectar la batería (airbag).'], 'Manual › 9A Sistemas de cableado'),
    'mazo_piso': F('Mazo del piso: corre por los zócalos hasta atrás; alimenta bomba de nafta, cinturones, calaveras y el SDM.', [['Conectores', 'L01 en adelante']],
                   ['Al sacar alfombras, no pisar los conectores.'], 'Manual › 9A Sistemas de cableado'),
    'mazo_puertas': F('Mazos de las puertas: pasan por un fuelle de goma en la bisagra y llevan levantavidrios, cerraduras, parlantes y espejos.', [['Fuelle', 'entre el parante y la puerta']],
                      ['Cables cortados dentro del fuelle son una falla típica de puertas que se abren mucho.'], 'Manual › 9E Cristales - Ventanas - Retrovisores'),
    'mazo_porton': F('Mazo del techo y el portón: limpialuneta, desempañador, tercera luz de freno y cerradura del portón.', [['Fuelle', 'entre el techo y el portón']],
                     ['Revisar el fuelle si el limpialuneta o el desempañador fallan.'], 'Manual › 9A Sistemas de cableado'),
    'motor_limpiaparabrisas': F('Motor del limpiaparabrisas bajo la rejilla del torpedo, con el varillaje que mueve los dos brazos.', [['Conector', _con('E01')]],
                                ['Si las escobillas no quedan abajo, revisar el contacto de parada del motor.'], 'Manual › 9D Limpiaparabrisas - Lavaparabrisas'),
    'motor_limpialuneta': F('Motor del limpialuneta dentro del portón.', [['Circuito', 'B-2']], ['Lubricar el eje del brazo una vez por año.'], 'Manual › 9D Limpiaparabrisas - Lavaparabrisas'),
    'lavador': F('Depósito del lavaparabrisas con su bomba eléctrica y las mangueras a los picos del capó.', [['Circuito', 'B-1']], ['Usar líquido limpiavidrios, no detergente.'], 'Manual › 9D Limpiaparabrisas - Lavaparabrisas'),
    'levantavidrios_izq': F('Mecanismos de tijera con motor eléctrico de las puertas izquierdas.', [['Circuito', 'B-4']], ['Si el vidrio baja trabado, limpiar y lubricar las guías.'], 'Manual › 9E Cristales - Ventanas - Retrovisores'),
    'levantavidrios_der': F('Mecanismos de tijera con motor eléctrico de las puertas derechas (la del conductor lleva la botonera).', [['Circuito', 'B-4']], ['Si el vidrio baja trabado, limpiar y lubricar las guías.'], 'Manual › 9E Cristales - Ventanas - Retrovisores'),
    'cerraduras': F('Actuadores del cierre centralizado en las cuatro puertas y el portón, comandados por el BCM.', [['Circuito', 'B-5']], ['Lubricar las cerraduras en cada service.'], 'Manual › 9F Seguridad y bloqueos'),
    'desempanador': F('Resistencias impresas en la luneta que calientan el vidrio; las maneja un relé del BCM y se apagan solas.', [['Circuito', 'B-3']],
                      ['No raspar la luneta por dentro: se cortan las líneas.'], 'Manual › 9E Cristales - Ventanas - Retrovisores'),
    'airbag_acompanante': F('Módulo del airbag del acompañante en la parte superior del tablero.', [['Circuito', 'F-1']], ['Guardarlo con la tapa hacia arriba; nunca medirlo con tester.'], 'Manual › 8B Sistema de airbag'),
    'pretensores': F('Cinturones delanteros con pretensor pirotécnico: tensan el cinturón en el instante del choque.', [['Circuito', 'F-1']], ['Un pretensor disparado se cambia completo.'], 'Manual › 8A Cinturones de seguridad'),
    'canerias_freno': F('Cañerías rígidas de freno: de la bomba al ABS y de ahí a cada rueda, con flexibles en las ruedas.', [['Líquido', 'DOT 3']],
                        ['Purgar en el orden del manual después de abrir el circuito.'], 'Manual › 4A Sistema de mando de los frenos y diagnósticos'),
    'caja_bomba_aceite': F('Bomba de aceite de la caja, movida por el convertidor: da la presión para embragues, frenos y lubricación.', [['Fluido', 'ATF 3317 / 3309']],
                           ['Fluido quemado o bajo daña la bomba: controlar el nivel.'], 'Manual › 5A Transmisión automática - Transeje automático'),
    'caja_embragues': F('Paquetes de discos de fricción y de acero de los embragues de directa, avance y reversa; se aprietan con presión de aceite.', [['Elementos', '3 embragues, 3 frenos, 2 ruedas libres']],
                        ['Patinamiento al cambiar: revisar nivel y presión antes de desarmar.'], 'Manual › 5A Transmisión automática - Transeje automático'),
    'caja_planetario': F('Tren planetario tipo Ravigneaux: dos solares, piñones largos y cortos y una corona; según qué se frena o se une, da las 4 marchas y la reversa.',
                         [['Dientes', 'solar del. 24 · solar tras. 30 · piñón largo 20 · corto 19 · corona 69'], ['Relaciones', '2,875 · 1,568 · 1,000 · 0,697 · R 2,300']],
                         ['Ruido en una sola marcha suele ser un piñón del planetario.'], 'Manual › 5A Transmisión automática - Transeje automático'),
    'caja_cuerpo_valvulas': F('Cuerpo de válvulas: reparte la presión a cada embrague y freno; los solenoides de cambio y de presión los maneja el TCM.', [['Solenoides', 'cambio A y B, control de presión, TCC']],
                              ['Muy sensible a la suciedad: fluido limpio y del tipo indicado.'], 'Manual › 5A Transmisión automática - Transeje automático'),
    'caja_engranajes': F('Engranaje de salida del planetario, intermedio y piñón de ataque al diferencial.', [['Reducción', '1,023']], ['—'], 'Manual › 5A Transmisión automática - Transeje automático'),
    'caja_diferencial': F('Diferencial: la corona recibe el giro y los satélites y planetarios reparten entre las dos ruedas permitiendo que giren distinto en las curvas.',
                          [['Reducción final', '4,052']], ['Ruido al doblar: revisar satélites y rodamientos.'], 'Manual › 5A Transmisión automática - Transeje automático'),
})


# ------------------------------------------------------------ el auto es de CAJA MANUAL de 5 marchas (corrección del 15/11/2026)
for _k in ('caja_4at', 'convertidor', 'tcm', 'sensor_rango_caja', 'caja_bomba_aceite', 'caja_embragues', 'caja_planetario',
           'caja_cuerpo_valvulas', 'caja_engranajes'):
    PIEZAS.pop(_k, None)
V5B, V5C = 'Manual › 5B Transmisión - Transeje manual', 'Manual › 5C Embrague'
CONJ['Transmisión']['resumen'] = ('Caja manual de 5 marchas y marcha atrás con diferencial incorporado (transeje), tracción delantera, '
                                  'embrague de disco en seco con mando hidráulico y palanca con dos cables (cambio y selección).')
CONJ['Transmisión']['nota'] = '05 Conducción y caja manual'
CONJ['Caja por dentro']['resumen'] = ('Por dentro del transeje manual: eje de entrada, contraeje con el piñón de ataque, eje de marcha atrás con piñón loco '
                                      'deslizante, tres sincronizadores (baja en el contraeje con doble cono en 2ª, alta y 5ª en el eje de entrada), '
                                      'horquillas y diferencial.')
CONJ['Caja por dentro']['nota'] = 'Manual de taller › 5B'
CONJ['Módulos de control']['resumen'] = CONJ['Módulos de control']['resumen'].replace('TCM (caja), ', '')
CONJ['Refrigeración']['resumen'] = CONJ['Refrigeración']['resumen'].replace('Lleva 6,1 L de refrigerante al 50 % (versión automática).',
                                                                          'Lleva 6,2 L de refrigerante al 50 % (versión manual).')
PIEZAS['arranque']['que'] = PIEZAS['arranque']['que'].replace('Con caja automática solo arranca en P o N.', 'Con caja manual solo arranca con el pedal de embrague apretado.')
PIEZAS['sensor_vss']['que'] = 'Sensor de velocidad del vehículo en la caja: lo usan el velocímetro, el ECM y la dirección eléctrica.'
PIEZAS['interruptor_freno']['que'] = 'Interruptor sobre el pedal de freno: enciende las luces de freno y avisa al ECM y al ABS que se está frenando.'
PIEZAS['mazo_tablero']['que'] = PIEZAS['mazo_tablero']['que'].replace('TCM y bloque', 'interruptor del embrague y bloque')
PIEZAS['freno_mano']['ver'] = '05 Conducción y caja manual'
PIEZAS['radiador']['datos'] = [['Refrigerante', 'etilenglicol al 50 %'], ['Capacidad (M/T)', '5,5 L motor + radiador + 0,7 L depósito = 6,2 L']]
PIEZAS['semieje_der']['que'] = 'Palier derecho, igual al izquierdo pero de otro largo (el diferencial no está en el centro).'
PIEZAS['caja_diferencial']['ver'] = V5B
PIEZAS['caja_diferencial']['datos'] = [['Juego de empuje de los engranajes', '0,03–0,31 mm'], ['Perno de la corona', '90 N·m']]
PIEZAS.update({
    'caja_5mt': {
        'que': 'Transeje manual: caja de 5 marchas y marcha atrás con el diferencial adentro, de aluminio, a la izquierda del motor. Arriba tiene el mecanismo de cambio, al que llegan los cables de la palanca.',
        'datos': [['Aceite', 'API GL-4 75W-90'], ['Capacidad', '2,2 L (referencia)'], ['Tapones de llenado y vaciado', '21 N·m'], ['Interruptor de marcha atrás', '23 N·m']],
        'mant': ['Revisar pérdidas y nivel a los primeros 15 000 km; cambiar el aceite a los 45 000 y 90 000 km (cada 30 000 en uso severo).',
                 'El nivel llega al borde del agujero del tapón de llenado; sellador en la rosca al cerrarlo.'],
        'ver': '05 Conducción y caja manual'},
    'embrague': {
        'que': 'Embrague de disco en seco: la placa de presión aprieta el disco contra el volante motor. Al pisar el pedal, el cilindro receptor mueve la horquilla y el rodamiento empuja el diafragma y libera el disco.',
        'datos': [['Profundidad de los remaches del disco', '1,65–2,25 mm (límite 0,5)'], ['Pernos de la placa', '23 N·m'], ['Pernos del volante', '70 N·m'],
                  ['Juego libre del pedal', '2–8 mm']],
        'mant': ['Patina (sube vueltas y no acelera): disco gastado o con aceite.', 'Al cambiarlo, centrar el disco con la herramienta y revisar el volante y el rodamiento.'],
        'ver': V5C},
    'bomba_embrague': {
        'que': 'Cilindro maestro del embrague en el torpedo, empujado por el pedal. Toma líquido del depósito de frenos y manda presión por el tubo y la manguera al cilindro receptor de la caja.',
        'datos': [['Líquido', 'DOT 3 (compartido con los frenos)'], ['Juego de la varilla', 'hasta 3 mm']],
        'mant': ['Pedal que se va al piso o no vuelve: pérdida o aire en el circuito; purgar por el receptor.', 'Revisar nivel y pérdidas cada 30 000 km.'],
        'ver': V5C},
    'palanca': {
        'que': 'Palanca de cambios en la consola: dos cables la unen con la caja, uno para el movimiento de cambio (adelante-atrás) y otro para el de selección (izquierda-derecha).',
        'datos': [['Esquema', '5 marchas y reversa'], ['Fijación de la palanca', '10 N·m'], ['Soporte de los cables', '55 N·m']],
        'mant': ['Cambios duros o imprecisos: revisar el ajuste y el desgaste de los cables antes que la caja.', 'Grasa en los extremos de los cables al montarlos.'],
        'ver': '05 Conducción y caja manual'},
    'pedalera': {
        'que': 'Tres pedales (de izquierda a derecha): embrague, freno y acelerador. El interruptor del embrague solo deja arrancar con el pedal a fondo.',
        'datos': [['Juego libre del embrague', '2–8 mm'], ['Altura del freno', '130–150 mm']],
        'mant': ['Pedal de embrague duro o con ruido: lubricar el pivote y revisar la bomba.'],
        'ver': '05 Conducción y caja manual'},
    'eje_entrada': {
        'que': 'Eje de entrada: recibe el giro del disco de embrague. Lleva los engranajes de 1ª a 5ª y los sincronizadores de alta (3ª-4ª) y de 5ª.',
        'datos': [['Sincronizadores', 'alta (3ª-4ª) y 5ª'], ['Holgura anillo-engranaje', '1,0–1,3 mm (límite 0,5)']],
        'mant': ['Los anillos sincronizadores no se pulen: si están bajo el límite, se cambian.'], 'ver': V5B},
    'contraeje': {
        'que': 'Contraeje: los engranajes que engranan con los del eje de entrada, el sincronizador de baja (1ª-2ª, con doble cono en 2ª) y el piñón de ataque que mueve la corona del diferencial.',
        'datos': [['Rodamientos', 'de rodillos cónicos con precarga'], ['Tuerca del contraeje', '70–100 N·m según el lado']],
        'mant': ['Al armar, ajustar la precarga de los rodamientos cónicos como indica el manual.'], 'ver': V5B},
    'eje_marcha_atras': {
        'que': 'Eje de marcha atrás con el piñón loco deslizante: se mete entre el eje de entrada y el contraeje e invierte el giro. Un freno de marcha atrás (sincronización de 5ª) frena el eje de entrada para que no cruja.',
        'datos': [['Perno del eje', '23 N·m']], 'mant': ['Poner reversa con el auto detenido y el embrague a fondo.'], 'ver': V5B},
    'horquillas': {
        'que': 'Eje de cambio y horquillas: mueven los manguitos de los sincronizadores según la palanca.',
        'datos': [['Perno de la horquilla', '10 N·m']], 'mant': ['Marchas que se salen solas: horquillas, manguitos o resortes de retención gastados.'], 'ver': V5B},
    'interruptor_marcha_atras': {
        'que': 'Interruptor en la caja que cierra cuando se pone reversa y enciende las luces de marcha atrás.',
        'datos': [['Par de apriete', '23 N·m'], ['Circuito', 'D-8']], 'mant': ['Si no prenden las luces de marcha atrás, revisar el interruptor y su conector.'], 'ver': V5B},
    'interruptor_embrague': {
        'que': 'Interruptor sobre el pedal de embrague: el motor de arranque solo funciona con el pedal apretado a fondo.',
        'datos': [['Conector', 'E74'], ['Circuito', 'A-1']], 'mant': ['Si no arranca, probar el interruptor y su regulación con el pedal.'], 'ver': V5C},
})


if __name__ == '__main__':
    out = os.path.join(VAULT, '3D', 'visor', 'fichas.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump({'conjuntos': CONJ, 'piezas': PIEZAS}, fh, ensure_ascii=False, indent=1)
    print('fichas:', len(PIEZAS), '→', out)
