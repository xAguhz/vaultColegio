#!/usr/bin/env python3
"""Capturas de WinUnisoft (pantalla oculta) para el informe: la pieza después de cada herramienta.

Uso: DISPLAY=:99 python3 esquemas_wus.py "<subcarpeta>" "<archivo.prj>" <carpeta_salida>

Tilda "Cambio Hta." en Control parada: la simulación se pausa en cada cambio de herramienta.
En cada pausa se guarda la vista de corte (op1.png, op2.png, ...) y se sigue con Marcha.
Al terminar destilda "Cambio Hta." otra vez. Requiere WinUnisoft en el escritorio virtual de Wine
(winunisoft_oculto.sh).
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_argv, sys.argv = sys.argv, ["x"]
import wusctl as w  # noqa: E402
sys.argv = _argv

CAMBIO_HTA = (1460, 1044)          # casilla "Cambio Hta." (coordenadas de pantalla, escritorio virtual)
VISTA = (905, 105, 1790, 985)      # vista de corte (derecha)


def boton(nombre):
    w.clic(w.BOTON[nombre][0] + w.DESP[0], w.BOTON[nombre][1] + w.DESP[1])


def vista():
    return w.imagen(w.buscar("Wine Desktop")).convert("RGB").crop(VISTA)


def main(sub, archivo, salida):
    os.makedirs(salida, exist_ok=True)
    boton("abortar")
    time.sleep(1.0)
    w.combo("Escape")
    time.sleep(0.5)
    boton("abrir")
    time.sleep(2.5)
    w.escribir((sub + "\\" + archivo).lower())
    w.combo("Return")
    time.sleep(4.0)
    w.clic(*CAMBIO_HTA)
    time.sleep(0.5)
    boton("marcha")
    n, ant, quieto, t0 = 0, None, 0, time.time()
    try:
        while time.time() - t0 < 300:
            time.sleep(1.0)
            activo = w.abortar_activo_escritorio()
            im = vista()
            igual = ant is not None and im.tobytes() == ant.tobytes()
            quieto = quieto + 1 if igual else 0
            ant = im
            if not activo or quieto >= 2:       # terminó, o está en pausa por cambio de herramienta
                n += 1
                im.save(os.path.join(salida, "op%d.png" % n))
                print("op%d" % n)
                if not activo:
                    break
                boton("marcha")
                quieto, ant = 0, None
                time.sleep(1.0)
    finally:
        w.clic(*CAMBIO_HTA)                     # deja la casilla como estaba
    return n


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
