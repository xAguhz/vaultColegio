#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera un proyecto WinUnisoft (.prj .nc .txt .wmf) a partir de una pieza .json.

Uso:  generar_winunisoft.py <pieza.json> <carpeta_salida> [--plantilla DIR]

Solo libreria estandar. Formato del .json: ver Piezas/FORMATO.md.
Maquina Apolo, control Fanuc16iTA. Mismo estilo que "Peon TP.nc" y "Alfil TP.nc".

Orden del programa (SAE 4140):
  T0101 desbaste (frenteado + G90)
  T0505 canales (solo si hay valles) y zona de base con G94 (solo si hace falta)
  T0303 semiacabado
  T0909 acabado neutro (DVVNN, 72.5 grados) de TODO el perfil; los flancos muy empinados
        que bajan de diametro se cortan aparte, acercandose desde la base (hacia +Z)
  T0505 tronzado en Z-(largo+3)
"""
import argparse
import json
import math
import os
import re
import struct
import subprocess
import sys
import zlib

DZ = 0.05            # paso del mapa de material (mm)
PASO_G90 = 2.0       # profundidad maxima por pasada en diametro (mm)
SOBRE_DESB = 0.5     # sobremetal radial que deja el desbaste (mm)
SOBRE_SEMI = 0.6     # sobremetal en diametro que deja el semiacabado (mm)
MARGEN_Z = 0.5       # el desbaste frena antes de las paredes (mm)
UMBRAL_VALLE = 1.6   # sobremetal radial a partir del cual hay un valle que limpiar (mm)
ANCHO_T5 = 3.0       # ancho de T0505 (canales, zona de base y tronzado)
PASO_T5 = 2.5        # paso de T0505 al limpiar la base (menor que el ancho: solapa)
# angulo libre del porta respecto de Z. T0303: el prj dice 30 pero los originales bajan 45 grados
# con ella. T0909 es neutro (DVVNN, acercamiento 72.5): mismo angulo a los dos lados.
ANG_PORTA = {3: 46.0, 9: 72.5}
TOL_PORTA = {3: 0.8, 9: 0.4}   # holgura del modelo de porta (sobremetal de acabado)
LIM_FLANCO = 70.0    # flanco que baja de diametro mas empinado que esto: T0909 lo corta desde la base


# ----------------------------------------------------------------- utilidades
def fmt(v):
    s = ("%.3f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def aviso(lista, texto):
    if texto not in lista:
        lista.append(texto)


# ------------------------------------------------------------------ geometria
class Prim:
    """Tramo del perfil entre dos puntos (x diametro, z). Recto o arco."""

    def __init__(self, p0, p1, R=None, g=None):
        self.p0 = (p0[0], p0[1])
        self.p1 = (p1[0], p1[1])
        self.R = R
        self.g = g
        self.herr = None
        if R:
            z0, r0, z1, r1 = p0[1], p0[0] / 2, p1[1], p1[0] / 2
            dz, dr = z1 - z0, r1 - r0
            c = math.hypot(dz, dr)
            if c > 2 * R + 1e-6:
                raise ValueError("Arco con cuerda %.3f mayor que 2R=%.3f entre %s y %s"
                                 % (c, 2 * R, p0, p1))
            if c > 2 * R:
                self.R = R = c / 2
            h = math.sqrt(max(R * R - (c / 2) ** 2, 0.0))
            s = 1 if g == "G02" else -1
            self.zc = (z0 + z1) / 2 + s * h * dr / c
            self.rc = (r0 + r1) / 2 - s * h * dz / c
            self.a0 = math.atan2(r0 - self.rc, z0 - self.zc)
            a1 = math.atan2(r1 - self.rc, z1 - self.zc)
            da = a1 - self.a0
            if g == "G02":
                while da > 1e-12:
                    da -= 2 * math.pi
            else:
                while da < -1e-12:
                    da += 2 * math.pi
            self.sweep = da

    @property
    def dx(self):
        return self.p1[0] - self.p0[0]

    @property
    def dz(self):
        return self.p1[1] - self.p0[1]

    def largo(self):
        if self.R:
            return self.R * abs(self.sweep)
        return math.hypot(self.dx / 2, self.dz)

    def pt(self, t):
        if t <= 0:
            return self.p0
        if t >= 1:
            return self.p1
        if not self.R:
            return (self.p0[0] + t * self.dx, self.p0[1] + t * self.dz)
        a = self.a0 + t * self.sweep
        return (2 * (self.rc + self.R * math.sin(a)), self.zc + self.R * math.cos(a))

    def muestras(self, paso=0.4):
        n = max(2, int(math.ceil(self.largo() / paso)))
        return [self.pt(k / n) for k in range(n + 1)]

    def cortar(self, t):
        """Parte el tramo en t (0..1). Redondea el punto a 3 decimales."""
        q = self.pt(t)
        q = (round(q[0], 3), round(q[1], 3))
        return (Prim(self.p0, q, self.R, self.g), Prim(q, self.p1, self.R, self.g))

    def invertido(self):
        g = None
        if self.g:
            g = "G03" if self.g == "G02" else "G02"
        return Prim(self.p1, self.p0, self.R, g)

    def trasladado(self, ddx):
        return Prim((self.p0[0] + ddx, self.p0[1]), (self.p1[0] + ddx, self.p1[1]),
                    self.R, self.g)

    def angulo_bajada(self):
        """Angulo maximo (grados, respecto de Z) con el que el diametro baja hacia la base."""
        mx = 0.0
        pts = self.muestras(0.25)
        for a, b in zip(pts, pts[1:]):
            dr = (b[0] - a[0]) / 2
            dz = b[1] - a[1]
            if dr < -1e-9:
                mx = max(mx, math.degrees(math.atan2(-dr, abs(dz))))
        return mx


def partir_en_apice(prim):
    """Un arco que sube y luego baja de diametro se parte en el punto de tangente axial."""
    if not prim.R:
        return [prim]
    cortes = []
    for k in range(-4, 5):
        ang = math.pi / 2 + k * math.pi
        t = (ang - prim.a0) / prim.sweep if abs(prim.sweep) > 1e-12 else -1
        if 1e-6 < t < 1 - 1e-6:
            cortes.append(t)
    cortes.sort()
    piezas, resto, t0 = [], prim, 0.0
    for t in cortes:
        tt = (t - t0) / (1 - t0)
        a, b = resto.cortar(tt)
        piezas.append(a)
        resto, t0 = b, t
    piezas.append(resto)
    return piezas


# ---------------------------------------------------- mapa de material (heightmap)
class Mapa:
    """Radio del material en funcion de Z (una celda cada DZ)."""

    def __init__(self, ztop, zmin, r0, zcara):
        n = int(round((ztop - zmin) / DZ)) + 1
        self.ztop = ztop
        self.z = [ztop - i * DZ for i in range(n)]
        self.R = [r0 if z <= zcara + 1e-9 else 0.0 for z in self.z]

    def i(self, z):
        return min(max(int(round((self.ztop - z) / DZ)), 0), len(self.R) - 1)

    def celdas(self, za, zb):
        ia, ib = self.i(za), self.i(zb)
        return range(min(ia, ib), max(ia, ib) + 1)

    def corte_recta(self, z0, r0, z1, r1):
        if abs(z1 - z0) < 1e-9:
            i = self.i(z0)
            self.R[i] = min(self.R[i], r0, r1)
            return
        for i in self.celdas(z0, z1):
            t = (self.z[i] - z0) / (z1 - z0)
            t = min(max(t, 0.0), 1.0)
            self.R[i] = min(self.R[i], r0 + t * (r1 - r0))

    def corte_ancho(self, za, zb, r):
        for i in self.celdas(za, zb):
            self.R[i] = min(self.R[i], r)

    def maximo(self, za, zb):
        return max(self.R[i] for i in self.celdas(za, zb))

    def porta_libre(self, z, r, hacia_mas_z, tang, tol=0.03, alcance=25.0):
        """El porta sale de la punta con pendiente tang. Falso si choca con material."""
        i0 = self.i(z)
        n = len(self.R)
        for k in range(1, int(alcance / DZ)):
            i = i0 - k if hacia_mas_z else i0 + k
            if i < 0 or i >= n:
                break
            if self.R[i] > r + tang * k * DZ + tol:
                return False
        return True


def perfil_en_mapa(mapa, prims):
    """Radio maximo y minimo de la pieza terminada en cada celda."""
    n = len(mapa.R)
    pmax, pmin = [0.0] * n, [0.0] * n
    for i, z in enumerate(mapa.z):
        vals = []
        for p in prims:
            z0, z1 = p.p0[1], p.p1[1]
            if z < min(z0, z1) - 1e-9 or z > max(z0, z1) + 1e-9:
                continue
            if not p.R:
                if abs(z1 - z0) < 1e-9:
                    vals += [p.p0[0] / 2, p.p1[0] / 2]
                else:
                    t = (z - z0) / (z1 - z0)
                    vals.append((p.p0[0] + t * p.dx) / 2)
            else:
                d = z - p.zc
                if abs(d) > p.R + 1e-9:
                    continue
                h = math.sqrt(max(p.R * p.R - d * d, 0.0))
                for r in (p.rc + h, p.rc - h):
                    a = math.atan2(r - p.rc, d)
                    u = (a - p.a0) * (1 if p.sweep >= 0 else -1)
                    u %= 2 * math.pi
                    if u <= abs(p.sweep) + 1e-6 or u >= 2 * math.pi - 1e-6:
                        vals.append(r)
        if vals:
            pmax[i], pmin[i] = max(vals), min(vals)
    return pmax, pmin


# ------------------------------------------------------------- generador de G-code
class Prog:
    def __init__(self, mapa, xseg, bruto_d, avisos):
        self.m = mapa
        self.xseg = xseg
        self.bd = bruto_d
        self.av = avisos
        self.l = []
        self.x, self.z = 100.0, 100.0
        self.f = None
        self.tool = None
        self.ancho = 0.0
        self.porta = None
        self.camino = []      # (tipo, herramienta, [(z, r), ...]) para dibujar

    # --- texto
    def linea(self, t):
        self.l.append(t)

    def herramienta(self, num, vc, ancho=0.0, porta=None):
        # la Vc del JSON ("vc": {"1": 150, ...}) manda sobre la de por defecto
        vc = VC_PIEZA.get(num, vc)
        self.linea("T%02d%02d" % (num, num))
        self.linea("G96 S%d M3" % vc)
        self.tool, self.ancho, self.porta, self.f = num, ancho, porta, None
        self.x, self.z = 100.0, 100.0

    def _coords(self, x, z, ambos=False):
        p = []
        if x is not None and (ambos or abs(x - self.x) > 1e-9):
            p.append("X" + fmt(x))
        if z is not None and (ambos or abs(z - self.z) > 1e-9):
            p.append("Z" + fmt(z))
        return p

    def g00(self, x=None, z=None):
        p = self._coords(x, z)
        if not p:
            return
        # el rapido no puede entrar en el material
        x1 = self.x if x is None else x
        z1 = self.z if z is None else z
        # rapido diagonal que baja en X y sale hacia +Z por encima de la pieza
        # (p. ej. X33 Z-17 -> X0 Z5): primero se va a Z y despues baja en X,
        # como en los programas del curso, para que el porta no pase cerca
        if (x is not None and z is not None and x1 < self.x - 1e-9
                and z1 > self.z + 1e-9 and self.z < 0):
            self.g00(z=z1)
            self.g00(x=x1)
            return
        self._revisar_rapido(self.x, self.z, x1, z1)
        self.linea("G00 " + " ".join(p))
        self.camino.append(("R", self.tool, [(self.z, self.x / 2), (z1, x1 / 2)]))
        self.x, self.z = x1, z1

    def _revisar_rapido(self, x0, z0, x1, z1):
        n = max(2, int(math.hypot(abs(x1 - x0) / 2, abs(z1 - z0)) / 0.5))
        for k in range(n + 1):
            t = k / n
            x, z = x0 + t * (x1 - x0), z0 + t * (z1 - z0)
            za, zb = (z, z + self.ancho) if self.ancho else (z, z)
            if z > self.m.ztop + 0.01 + (self.ancho or 0):
                continue
            if x / 2 < self.m.maximo(za, zb) - 0.02:
                aviso(self.av, "G00 dentro del material en X%s Z%s (T%d)"
                      % (fmt(x), fmt(z), self.tool or 0))
                return

    def _pone_f(self, feed):
        if self.f != feed:
            self.f = feed
            return " F" + feed
        return ""

    def _barrido(self, p0, p1):
        """Aplica el corte de la herramienta al mapa. p = (x, z)."""
        z0, r0, z1, r1 = p0[1], p0[0] / 2, p1[1], p1[0] / 2
        if self.ancho:
            n = max(2, int(math.hypot(abs(r1 - r0), abs(z1 - z0)) / 0.1))
            for k in range(n + 1):
                t = k / n
                self.m.corte_ancho(z0 + t * (z1 - z0), z0 + t * (z1 - z0) + self.ancho,
                                   r0 + t * (r1 - r0))
        else:
            self.m.corte_recta(z0, r0, z1, r1)

    def _porta(self, p):
        if self.porta is None:
            return
        # herramienta que avanza hacia -Z: el porta queda hacia +Z, y al reves
        tg = math.tan(math.radians(self.porta))
        tol = TOL_PORTA.get(self.tool, 0.4)
        if self.tool == 9:
            # porta neutro: simetrico, el cuerpo sale por los dos lados de la punta
            libre = (self.m.porta_libre(p[1], p[0] / 2, True, tg, tol)
                     and self.m.porta_libre(p[1], p[0] / 2, False, tg, tol))
        else:
            libre = self.m.porta_libre(p[1], p[0] / 2, self.tool == 3, tg, tol)
        if not libre:
            aviso(self.av, "Posible choque del porta T%d cerca de X%s Z%s"
                  % (self.tool, fmt(p[0]), fmt(p[1])))

    def g01(self, x=None, z=None, feed=None):
        p = self._coords(x, z)
        if not p:
            return
        x1 = self.x if x is None else x
        z1 = self.z if z is None else z
        f = self._pone_f(feed) if feed else ""
        self.linea("G01 " + " ".join(p) + f)
        self._sigue((self.x, self.z), (x1, z1), None)
        self.camino.append(("F", self.tool, [(self.z, self.x / 2), (z1, x1 / 2)]))
        self.x, self.z = x1, z1

    def arco(self, prim, feed=None):
        f = self._pone_f(feed) if feed else ""
        self.linea("%s X%s Z%s R%s%s" % (prim.g, fmt(prim.p1[0]), fmt(prim.p1[1]),
                                         fmt(prim.R), f))
        pts = prim.muestras(0.4)
        for a, b in zip(pts, pts[1:]):
            self._sigue(a, b, None)
        self.camino.append(("F", self.tool, [(q[1], q[0] / 2) for q in prim.muestras(0.2)]))
        self.x, self.z = prim.p1

    def _sigue(self, a, b, _):
        """Mueve la punta de a a b en pasos de 0.5 mm: corta y revisa el porta."""
        n = max(1, int(math.hypot(abs(b[0] - a[0]) / 2, abs(b[1] - a[1])) / 0.5))
        ant = a
        for k in range(1, n + 1):
            t = k / n
            q = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
            self._barrido(ant, q)
            self._porta(q)
            ant = q

    # --- movimientos compuestos
    def xl_local(self, z):
        return 2 * self.m.maximo(z - 0.35, z + 0.35) + 1.0

    def aproximar(self, x, z, feed):
        """Del cambio de herramienta (o de X seguro) al punto (x, z), sin rapido en material."""
        if z >= -1e-6:
            self.g00(x, 5.0)
            self.g01(z=z, feed=feed)
            return
        self.g00(self.xseg, z)
        xl = self.xl_local(z)
        if x < xl - 0.01 and xl < self.xseg:
            self.g00(xl)
        self.g01(x, feed=feed)

    def salir(self):
        xl = self.xl_local(self.z)
        if xl < self.xseg - 0.01:
            self.g01(xl)
            self.g00(self.xseg)
        else:
            self.g01(self.xseg)

    def fin_herramienta(self):
        self.g00(100.0, 100.0)


# ------------------------------------------------------------------ lectura de datos
def leer_pieza(ruta):
    with open(ruta, encoding="utf-8") as f:
        d = json.load(f)
    for k in ("nombre", "bruto", "largo", "perfil"):
        if k not in d:
            raise ValueError("Falta '%s' en %s" % (k, ruta))
    per = d["perfil"]
    if len(per) < 2:
        raise ValueError("El perfil necesita al menos dos puntos")
    if abs(per[0]["z"]) > 1e-9:
        raise ValueError("El primer punto debe estar en Z0")
    if abs(per[-1]["z"] + d["largo"]) > 1e-6:
        raise ValueError("El ultimo punto debe estar en z = -largo")
    for a, b in zip(per, per[1:]):
        if b["z"] > a["z"] + 1e-9:
            raise ValueError("Los puntos deben ir de la punta a la base (Z decrece)")
    if max(p["x"] for p in per) > d["bruto"]["d"] + 1e-9:
        raise ValueError("El perfil es mas grueso que el bruto")
    return d


def prims_del_perfil(per):
    prims = []
    for a, b in zip(per, per[1:]):
        arco = b.get("arco")
        if arco:
            prims.append(Prim((a["x"], a["z"]), (b["x"], b["z"]), float(arco["r"]), arco["g"]))
        else:
            prims.append(Prim((a["x"], a["z"]), (b["x"], b["z"])))
    return prims


# -------------------------------------------------------------- planificacion
def zona_base(per, largo):
    """Si el perfil termina en un cilindro mas fino que algo anterior, hay zona de base
    que solo se puede limpiar desde el lado de la base (G94 con la herramienta ancha)."""
    x_fin = per[-1]["x"]
    k = None
    for i in range(len(per) - 1, -1, -1):
        if per[i]["x"] > x_fin + 0.01:
            k = i
            break
    if k is None or k == len(per) - 1:
        return None
    zf = per[k + 1]["z"]       # donde termina la bajada hacia el cilindro final
    if abs(zf + largo) < 1e-6:  # no hay cilindro final con largo
        return None
    return {"x": x_fin, "z": zf}


VC_PIEZA = {}  # Vc (m/min) por herramienta, leída del JSON de la pieza


def generar(d, avisos):
    VC_PIEZA.clear()
    VC_PIEZA.update({int(k): float(v) for k, v in d.get("vc", {}).items()})
    bd, bl = float(d["bruto"]["d"]), float(d["bruto"]["l"])
    largo = float(d["largo"])
    per = d["perfil"]
    z_parte = -(largo + ANCHO_T5)   # regla: -(largo + ancho de la herramienta)
    xseg = bd + 3.0

    prims0 = prims_del_perfil(per)
    mapa = Mapa(6.0, -(largo + 14.0), bd / 2, bl - (bl - 1.0))   # cara del bruto en Z=+1
    pmax, pmin = perfil_en_mapa(mapa, prims0)
    mapa_final = (pmax, pmin)

    # piezas monotonas
    segs = []
    for p in prims0:
        if abs(p.dx) < 1e-9 and abs(p.dz) < 1e-9:
            continue
        segs += partir_en_apice(p)

    base = zona_base(per, largo)
    z_base = base["z"] if base else None
    for s in segs:
        s.herr = None
        s.rev = False
        s.en_base = bool(base and s.p1[1] < z_base - 1e-9 + 1e-9 and s.p0[1] <= z_base + 1e-9
                         and s.p1[1] <= z_base + 1e-9)
        if s.en_base:
            s.herr = "base"
        else:
            s.herr = 9     # T0909 neutro termina todo el perfil
            # flanco que baja de diametro y es mas empinado que el limite: se corta
            # desde la base (hacia +Z), donde el porta neutro tiene holgura
            if s.dx < -1e-9 and abs(s.dz) > 1e-9 and s.angulo_bajada() > LIM_FLANCO:
                s.rev = True

    P = Prog(mapa, xseg, bd, avisos)
    P.linea("%")
    P.linea("O2222")
    P.linea("G54")

    # ------------------------------------------------ T0101 frenteado y G90
    P.herramienta(1, 150)
    P.g00(xseg, 5.0)
    P.g00(z=0.0)
    P.g01(0.0, feed=".3")
    for i in mapa.celdas(0.0 + DZ, mapa.ztop):
        mapa.R[i] = 0.0
    P.g00(z=5.0)
    P.g00(xseg)
    D = bd - 1.0
    pasadas = []
    while D > 1.0:
        zl = None
        for i, z in enumerate(mapa.z):
            if z > 0:
                continue
            if z < -(largo + 1e-9):
                break
            if pmax[i] + SOBRE_DESB > D / 2 + 1e-9:
                zl = z
                break
        z_fin = z_parte if zl is None else max(zl + MARGEN_Z, z_parte)
        if z_fin > -0.3:
            break
        pasadas.append((D, z_fin))
        D -= PASO_G90
    zant, primero = None, True
    for D, zf in pasadas:
        mapa.corte_recta(5.0, D / 2, zf, D / 2)
        txt = ""
        if primero:
            txt = "G90 X%s Z%s F.3" % (fmt(D), fmt(zf))
            primero = False
        elif zant is not None and abs(zf - zant) < 1e-9:
            txt = "X%s" % fmt(D)
        else:
            txt = "X%s Z%s" % (fmt(D), fmt(zf))
        P.linea(txt)
        P.camino.append(("F", 1, [(5.0, D / 2), (zf, D / 2)]))
        zant = zf
    P.f = ".3"
    P.x, P.z = xseg, 5.0
    P.fin_herramienta()

    # ------------------------------------------------ T0505 canales (valles)
    sem_r = SOBRE_SEMI / 2
    valles = []
    en = None
    tg3 = math.tan(math.radians(ANG_PORTA[3]))
    alc = 0.0
    for i, z in enumerate(mapa.z):
        if z > 0 or z < -largo:
            continue
        # radio hasta donde llega una herramienta que baja con pendiente limitada
        alc = max(pmax[i] + sem_r, alc - tg3 * DZ) if z < 0 else pmax[i] + sem_r
        if base and z < z_base - 1e-9:
            continue
        exceso = mapa.R[i] - alc
        if exceso > UMBRAL_VALLE:
            if en is None:
                en = [z, z]
            en[1] = z
        elif en is not None:
            valles.append(en)
            en = None
    if en is not None:
        valles.append(en)
    valles = [v for v in valles if v[0] - v[1] > 0.4]
    if valles or base:
        P.herramienta(5, 120, ANCHO_T5)
        for za, zb in valles:
            zr = []
            z0 = za - ANCHO_T5
            if zb > z0:
                zr = [round(z0, 3)]
            else:
                n = max(1, int(math.ceil((z0 - zb) / 2.5)))
                paso = (z0 - zb) / n
                zr = [round(z0 - k * paso, 3) for k in range(n + 1)]
            xret = min(2 * mapa.maximo(zr[-1], zr[0] + ANCHO_T5) + 1.0, xseg)
            primera = True
            for z in zr:
                prof = max(pmax[i] for i in mapa.celdas(z, z + ANCHO_T5)) + sem_r
                xd = round(2 * prof + 1e-9, 3)
                if 2 * mapa.maximo(z, z + ANCHO_T5) - xd < 0.5:
                    continue
                if primera:
                    P.g00(xseg, z)
                    if xret < xseg - 0.01:
                        P.g00(xret)
                    primera = False
                else:
                    P.g00(z=z)
                P.g01(xd, feed=".1")
                P.g01(xret)
            if not primera:
                P.g00(xseg)
        # zona de base con G94 (T0505, pasos de PASO_T5)
        if base:
            zs = base["z"] - ANCHO_T5
            P.g00(xseg, zs)
            zc = zs - PASO_T5
            primero = True
            while True:
                zc = max(zc, z_parte)
                mapa.corte_ancho(zc, base["z"], base["x"] / 2)
                P.linea(("G94 X%s Z%s F.1" if primero else "Z%s") %
                        ((fmt(base["x"]), fmt(zc)) if primero else (fmt(zc),)))
                P.camino.append(("F", 5, [(zs, xseg / 2), (zs, base["x"] / 2),
                                          (zc, base["x"] / 2), (zc, xseg / 2)]))
                primero = False
                if zc <= z_parte + 1e-9:
                    break
                zc -= PASO_T5
            P.f = ".1"
        P.fin_herramienta()

    # ------------------------------------------------ rutina de contorno
    def grupos(pred):
        res, act = [], []
        for s in segs:
            if pred(s):
                act.append(s)
            elif act:
                res.append(act)
                act = []
        if act:
            res.append(act)
        return res

    def recortar_inicio(grupo, tang, dx_off, hacia_mas_z, tol_p=0.4):
        """Si el porta choca al iniciar el grupo, avanza el inicio por el primer tramo."""
        s = grupo[0].trasladado(dx_off) if dx_off else grupo[0]
        L = s.largo()
        paso = 0.1
        t_m = 0.0
        while True:
            q = s.pt(t_m)
            if mapa.porta_libre(q[1], q[0] / 2, hacia_mas_z, tang, tol_p):
                return t_m
            t_m += paso / max(L, 1e-9)
            if t_m >= 0.999 or t_m * L > 6.0:
                return None

    def recorrer(grupo, dx_off, feed, invertir, num):
        """Genera el pasada de un grupo de tramos. grupo en orden de perfil."""
        orden = [s.invertido() for s in reversed(grupo)] if invertir else list(grupo)
        fus = []
        for q in orden:
            a = fus[-1] if fus else None
            if (a is not None and a.R and q.R and a.g == q.g and abs(a.R - q.R) < 1e-6
                    and abs(a.zc - q.zc) < 0.01 and abs(a.rc - q.rc) < 0.01):
                fus[-1] = Prim(a.p0, q.p1, a.R, a.g)
            else:
                fus.append(q)
        orden = fus
        if dx_off:
            orden = [s.trasladado(dx_off) for s in orden]
        a = orden[0].p0
        P.aproximar(a[0], a[1], feed)
        for s in orden:
            if s.R:
                P.arco(s, feed)
            else:
                P.g01(None if abs(s.dx) < 1e-9 else s.p1[0],
                      None if abs(s.dz) < 1e-9 else s.p1[1], feed)
        P.salir()

    # ------------------------------------------------ T0303 semiacabado
    tang3 = math.tan(math.radians(ANG_PORTA[3]))

    def ok3(s):
        # T0303 corta lo que sube de diametro y las bajadas que su porta aguanta
        return s.herr == 9 and (s.dx > -1e-9 or s.angulo_bajada() <= ANG_PORTA[3] + 1e-6)

    g3 = grupos(ok3)
    if g3:
        P.herramienta(3, 200, 0.0, ANG_PORTA[3])
        for g in g3:
            tm = recortar_inicio(g, tang3, SOBRE_SEMI, True, TOL_PORTA[3])
            if tm is None:
                aviso(avisos, "T0303 no puede iniciar en X%s Z%s: se omite ese tramo del semiacabado"
                      % (fmt(g[0].p0[0]), fmt(g[0].p0[1])))
                continue
            g = list(g)
            if tm > 0:
                g = [g[0].cortar(tm)[1]] + g[1:]
            recorrer(g, SOBRE_SEMI, ".2", False, 3)
        P.fin_herramienta()

    # ------------------------------------------------ T0909 acabado neutro (todo el perfil)
    P.herramienta(9, 200, 0.0, ANG_PORTA[9])
    # primero los flancos empinados que bajan de diametro: desde la base hacia +Z
    for g in reversed(grupos(lambda s: s.herr == 9 and s.rev)):
        recorrer(g, 0.0, ".2", True, 9)
    # despues el resto de la punta hacia la base, en pasadas continuas
    for g in grupos(lambda s: s.herr == 9 and not s.rev):
        if g[0].p0[1] >= -1e-6 and abs(g[0].p0[0]) < 1e-6:
            P.aproximar(0.0, 5.0, ".2")
            P.x, P.z = 0.0, 5.0
        recorrer(g, 0.0, ".2", False, 9)
    P.fin_herramienta()

    # ------------------------------------------------ T0505 tronzado
    P.herramienta(5, 120, ANCHO_T5)
    P.g00(xseg, z_parte)
    P.g01(-1.0, feed=".08")
    mapa.corte_ancho(z_parte, z_parte + ANCHO_T5, 0.0)
    P.g01(xseg)
    P.fin_herramienta()
    P.linea("M30")
    P.linea("%")

    sin = [s for s in segs if s.herr == "sin"]
    for s in sin:
        aviso(avisos, "Tramo sin herramienta que lo alcance: X%s Z%s -> X%s Z%s"
              % (fmt(s.p0[0]), fmt(s.p0[1]), fmt(s.p1[0]), fmt(s.p1[1])))
    return P, mapa, mapa_final, segs


# --------------------------------------------------------- verificador del texto .nc
def interpretar_nc(lineas, mapa, bruto_d, largo):
    """Lee el texto del .nc y vuelve a simular el material (independiente del generador).
    Devuelve (mapa, errores, camino)."""
    err, camino = [], []
    st = {"x": 100.0, "z": 100.0, "tool": None, "modo": None, "cx": None, "cz": None,
          "ancho": 0.0}
    ancho_de = {5: ANCHO_T5}

    def corte(x0, z0, x1, z1, rapido, n):
        r0, r1 = x0 / 2, x1 / 2
        w = st["ancho"]
        pasos = max(2, int(math.hypot(abs(r1 - r0), abs(z1 - z0)) / 0.1))
        for k in range(pasos + 1):
            t = k / pasos
            z, r = z0 + t * (z1 - z0), r0 + t * (r1 - r0)
            if rapido:
                zb = z + w
                if z <= mapa.ztop and r < mapa.maximo(z, zb) - 0.02:
                    err.append((n, "G00 dentro del material en X%s Z%s" % (fmt(2 * r), fmt(z))))
                    return
            elif w:
                mapa.corte_ancho(z, z + w, r)
            else:
                mapa.corte_recta(z, r, z, r)
        if not rapido and not w:
            mapa.corte_recta(z0, r0, z1, r1)
            # frenteado en la punta: la herramienta de derecha se lleva todo lo que esta en Z>z
            if abs(z1 - z0) < 1e-9 and z0 >= -1e-6 and x1 < x0 and st["tool"] in (1, 3, 9):
                for i in mapa.celdas(z0 + DZ, mapa.ztop):
                    mapa.R[i] = min(mapa.R[i], r1)

    for n, tx in enumerate(lineas, 1):
        t = tx.strip()
        if not t or t in ("%",) or re.fullmatch(r"O\d+", t):
            continue
        pal = re.findall(r"([A-Z])\s*(-?(?:\d+\.?\d*|\.\d+))", t)
        v, gs = {}, []
        for l, val in pal:
            f = float(val)
            if l == "G":
                gs.append(int(f))
            elif l == "T":
                num = int(f) // 100 if f >= 100 else int(f)
                st["tool"] = num
                st["ancho"] = ancho_de.get(num, 0.0)
            elif l in "XZR":
                v[l] = f
        for g in gs:
            if g in (0, 1, 2, 3, 90, 94):
                st["modo"] = g
                if g in (90, 94):
                    st["cx"] = st["cz"] = None
        if "X" not in v and "Z" not in v:
            continue
        x0, z0 = st["x"], st["z"]
        x = v.get("X", x0)
        z = v.get("Z", z0)
        m = st["modo"]
        if m in (0, 1):
            corte(x0, z0, x, z, m == 0, n)
            camino.append(("R" if m == 0 else "F", st["tool"], [(z0, x0 / 2), (z, x / 2)]))
            st["x"], st["z"] = x, z
        elif m in (2, 3):
            R = v.get("R")
            if R is None:
                err.append((n, "Arco sin R"))
                continue
            try:
                pr = Prim((x0, z0), (x, z), R, "G02" if m == 2 else "G03")
            except ValueError as e:
                err.append((n, str(e)))
                continue
            pts = pr.muestras(0.2)
            for a, b in zip(pts, pts[1:]):
                corte(a[0], a[1], b[0], b[1], False, n)
            camino.append(("F", st["tool"], [(q[1], q[0] / 2) for q in pts]))
            st["x"], st["z"] = x, z
        else:
            if "X" in v:
                st["cx"] = v["X"]
            if "Z" in v:
                st["cz"] = v["Z"]
            cx, cz = st["cx"], st["cz"]
            if cx is None or cz is None:
                err.append((n, "Ciclo incompleto"))
                continue
            if m == 90:
                mapa.corte_recta(z0, cx / 2, cz, cx / 2)
                camino.append(("F", st["tool"], [(z0, cx / 2), (cz, cx / 2)]))
            else:
                mapa.corte_ancho(cz, z0 + st["ancho"], cx / 2)
                camino.append(("F", st["tool"], [(z0, x0 / 2), (z0, cx / 2),
                                                 (cz, cx / 2), (cz, x0 / 2)]))
        if z < -(largo - 30 + 1e-9) - 0 and False:
            pass
    return mapa, err, camino


def comparar(mapa, pmax, pmin, largo, tol=0.03):
    """Devuelve (sobrante_max, z_sobrante, exceso_max, z_exceso) entre el material y la pieza."""
    sob, zs, exc, ze = 0.0, None, 0.0, None
    for i, z in enumerate(mapa.z):
        if z > -1e-9 or z <= -largo + 1e-9:
            continue
        r = mapa.R[i]
        if r - pmax[i] > sob:
            sob, zs = r - pmax[i], z
        if pmin[i] - r > exc:
            exc, ze = pmin[i] - r, z
    return sob, zs, exc, ze


# ------------------------------------------------------------------ dibujo PNG
def dibujar_png(ruta, camino, prims, bruto_d, largo, ancho=1200, alto=560):
    """PNG sencillo (solo libreria estandar): perfil negro, avance de colores, G00 punteado rojo."""
    zmin, zmax = -(largo + 12.0), 10.0
    rmax = bruto_d / 2 + 6.0
    esc = min((ancho - 60) / (zmax - zmin), (alto - 60) / (rmax + 2))
    px = [[(255, 255, 255)] * ancho for _ in range(alto)]

    def a_px(z, r):
        return int(30 + (z - zmin) * esc), int(alto - 30 - (r + 1) * esc)

    def punto(x, y, c):
        if 0 <= x < ancho and 0 <= y < alto:
            px[y][x] = c

    def linea(p, q, c, punteada=False):
        (x0, y0), (x1, y1) = p, q
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for k in range(n + 1):
            if punteada and (k // 4) % 2:
                continue
            punto(int(round(x0 + (x1 - x0) * k / n)), int(round(y0 + (y1 - y0) * k / n)), c)

    paleta = {1: (31, 119, 180), 3: (44, 160, 44), 5: (148, 103, 189), 9: (255, 127, 14),
              10: (214, 39, 40)}
    # bruto
    for a, b in (((zmin + 12.0 - 0, 0), (zmin + 12.0, 0)),):
        pass
    c = (170, 170, 170)
    linea(a_px(1, 0), a_px(1, bruto_d / 2), c)
    linea(a_px(1, bruto_d / 2), a_px(-largo - 10, bruto_d / 2), c)
    linea(a_px(-largo - 10, bruto_d / 2), a_px(-largo - 10, 0), c)
    linea(a_px(zmin, 0), a_px(zmax, 0), (200, 200, 200), True)
    for tipo, t, pts in camino:
        if tipo == "R":
            col = (255, 150, 150)
            for p, q in zip(pts, pts[1:]):
                if p[0] > zmax or q[0] > zmax or p[1] > rmax or q[1] > rmax:
                    continue
                linea(a_px(*p), a_px(*q), col, True)
        else:
            col = paleta.get(t, (0, 0, 0))
            for p, q in zip(pts, pts[1:]):
                linea(a_px(*p), a_px(*q), col)
    # perfil teorico encima (negro)
    for pr in prims:
        pts = pr.muestras(0.1)
        for p, q in zip(pts, pts[1:]):
            linea(a_px(p[1], p[0] / 2), a_px(q[1], q[0] / 2), (0, 0, 0))
    raw = b"".join(b"\x00" + bytes(v for c3 in fila for v in c3) for fila in px)

    def chunk(tag, data):
        c4 = struct.pack(">I", len(data)) + tag + data
        return c4 + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)

    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", ancho, alto, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    with open(ruta, "wb") as f:
        f.write(png)


# ------------------------------------------------------------------ proyecto
def _campo(l, nombre, valor):
    """Cambia un campo 'nombre=valor' de una linea Tool= (separado por espacios)."""
    n = len(re.findall(rb"(?:(?<= )|^)" + re.escape(nombre) + rb"=", l))
    assert n == 1, (nombre, n)
    return re.sub(rb"((?:(?<= )|^)" + re.escape(nombre) + rb"=)[^ ]*",
                  lambda m: m.group(1) + valor, l)


def herramientas_nuevas(l):
    """T5 pasa a canales y tronzado (A4SM ... GMN); T9 pasa a porta neutro DVVNN."""
    if l.startswith(b"Tool=T5^"):
        return l.replace(b"A4SM^R/L^2016K0317", b"A4SM^R/L^2016K0317^GMN")
    if l.startswith(b"Tool=T9^"):
        l = re.sub(rb"^Tool=T9\^9:\^\S*", b"Tool=T9^9:^DVVNN^2020K16KC04", l)
        for k, v in ((b"_Descrip", b"DVVNN^2020K16KC04"), (b"Quadrant", b"1"),
                     (b"Orient.", b"72.50000"), (b"_Orient.", b"107.50000"),
                     (b"IC", b"9.53000"), (b"_IC", b"9.53000"), (b"Alpha", b"35.00000"),
                     (b"r", b"0.40000"), (b"_CodForma", b"8"), (b"H_Width", b"20.00000"),
                     (b"H_Hght", b"125.00000"), (b"H_Clr_X", b"8.00000"),
                     (b"H_Clr_Z", b"2.50000"), (b"H_Ang", b"72.50000")):
            l = _campo(l, k, v)
    return l


def escribir_prj(plantilla, destino, bruto_d, bruto_l):
    with open(plantilla, "rb") as f:
        datos = f.read()
    lineas = datos.split(b"\r\n")
    sec = b""
    for i, l in enumerate(lineas):
        if l.startswith(b"[") and l.endswith(b"]"):
            sec = l
            continue
        if sec == b"[TOOLS]":
            lineas[i] = herramientas_nuevas(l)
        elif sec == b"[BRUTO]":
            if l.startswith(b"ZMax/DExt="):
                lineas[i] = b"ZMax/DExt=" + fmt(bruto_d).encode()
            elif l.startswith(b"YMax/ZMax="):
                lineas[i] = b"YMax/ZMax=" + fmt(bruto_l).encode()
        elif sec == b"[ORIGEN]" and l.startswith(b"G54="):
            lineas[i] = b"G54=0.00,0.00," + fmt(bruto_l - 1).encode()
    with open(destino, "wb") as f:
        f.write(b"\r\n".join(lineas))


def main():
    ap = argparse.ArgumentParser(description="Genera un proyecto WinUnisoft desde una pieza .json")
    ap.add_argument("pieza", help="archivo .json de la pieza")
    ap.add_argument("salida", help="carpeta de salida")
    ap.add_argument("--plantilla", help="carpeta con 'Peon TP.*' (por defecto ../WinUnisoft/originales)")
    ap.add_argument("--base", default="Peon TP", help="nombre de la plantilla (sin extension)")
    args = ap.parse_args()

    aqui = os.path.dirname(os.path.abspath(__file__))
    plant = args.plantilla or os.path.join(aqui, "..", "WinUnisoft", "originales")
    try:
        d = leer_pieza(args.pieza)
    except (ValueError, OSError, KeyError) as e:
        print("ERROR en la pieza: %s" % e)
        return 2
    nombre = d["nombre"].strip().capitalize() + " TP"
    os.makedirs(args.salida, exist_ok=True)

    avisos = []
    try:
        P, mapa, (pmax, pmin), segs = generar(d, avisos)
    except ValueError as e:
        print("ERROR en el perfil: %s" % e)
        return 2

    texto = "\r\n".join(P.l) + "\r\n"
    ruta_nc = os.path.join(args.salida, nombre + ".nc")
    with open(ruta_nc, "wb") as f:
        f.write(texto.encode("ascii"))
    escribir_prj(os.path.join(plant, args.base + ".prj"), os.path.join(args.salida, nombre + ".prj"),
                 float(d["bruto"]["d"]), float(d["bruto"]["l"]))
    for ext in (".txt", ".wmf"):
        with open(os.path.join(plant, args.base + ext), "rb") as f:
            datos = f.read()
        with open(os.path.join(args.salida, nombre + ext), "wb") as f:
            f.write(datos)

    # verificacion independiente: se vuelve a leer el .nc escrito
    largo = float(d["largo"])
    bd, bl = float(d["bruto"]["d"]), float(d["bruto"]["l"])
    m2 = Mapa(6.0, -(largo + 14.0), bd / 2, 1.0)
    with open(ruta_nc, encoding="ascii", newline="") as f:
        lin = f.read().split("\r\n")
    m2, errores, camino = interpretar_nc(lin, m2, bd, largo)
    sob, zs, exc, ze = comparar(m2, pmax, pmin, largo)
    ruta_png = os.path.join(args.salida, nombre + " trayectoria.png")
    dibujar_png(ruta_png, camino, prims_del_perfil(d["perfil"]), bd, largo)

    print("Proyecto generado en: %s" % args.salida)
    print("  %s.nc  (%d lineas)" % (nombre, len(P.l)))
    print("Verificacion del perfil final:")
    print("  sobrante maximo: %.3f mm de radio%s" % (sob, "" if zs is None else " en Z%s" % fmt(zs)))
    print("  exceso (pieza pasada): %.3f mm de radio%s" % (exc, "" if ze is None else " en Z%s" % fmt(ze)))
    for n, e in errores:
        print("  ERROR linea %d: %s" % (n, e))
    choques = [a for a in avisos if a.startswith("Posible choque")]
    for a in avisos:
        if not a.startswith("Posible choque"):
            print("  AVISO: %s" % a)
    if choques:
        print("  AVISO: %d puntos con posible choque del porta (modelo aproximado); primero: %s"
              % (len(choques), choques[0]))
    simu = os.path.join(aqui, "simular_nc.py")
    if os.path.exists(simu):
        r = subprocess.run([sys.executable, simu, ruta_nc, "--prj",
                            os.path.join(args.salida, nombre + ".prj")],
                           capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode:
            print(r.stderr.strip())
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
