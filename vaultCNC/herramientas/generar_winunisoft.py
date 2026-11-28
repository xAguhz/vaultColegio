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
PASO_G90 = 2.4       # pasada en diametro (mm): 1,2 por lado. CNMG-RP pide 1,1-6,4 mm por lado (A7)
SOBRE_DESB = 0.6     # sobremetal radial que deja el desbaste (mm): la T0303 corta 0,3 (FP pide 0,3-2,5, A7)
SOBRE_SEMI = 0.6     # sobremetal en diametro que deja el semiacabado (mm)
MARGEN_Z = 0.5       # el desbaste frena antes de las paredes (mm)
UMBRAL_VALLE = 1.6   # sobremetal radial a partir del cual hay un valle que limpiar (mm)
ANCHO_T5 = 3.05      # ancho de T0505: A4G0305M03U02GMN mide W 3,05 (A73)
PASO_T5 = 2.5        # paso de T0505 al limpiar la base (menor que el ancho: solapa)
# angulo libre del porta respecto de Z. T0303: el prj dice 30 pero los originales bajan 45 grados
# con ella. T0909 es neutro (DVVNN, acercamiento 72.5): mismo angulo a los dos lados.
ANG_PORTA = {3: 46.0, 9: 72.5}
TOL_PORTA = {3: 0.8, 9: 0.4}   # holgura del modelo de porta (sobremetal de acabado)
LIM_NEUTRO = 62.0    # pendiente maxima (respecto del eje Z) que sigue el porta neutro sin que el flanco
                     # del inserto de 35 grados (17,5 grados a cada lado de -X) muerda la pieza
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
        # no partir si el apice cae en un extremo (quedaria un tramo de largo cero)
        if t * prim.largo() > 1e-3 and (1 - t) * prim.largo() > 1e-3:
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

    def corte_nariz(self, z0, r0, z1, r1, rn, dzc):
        """Corte de un inserto con radio de punta rn: el centro está en punta + (dzc, rn)."""
        n = max(1, int(math.hypot(z1 - z0, r1 - r0) / 0.05))
        for k in range(n + 1):
            t = k / n
            zc, rc = z0 + t * (z1 - z0) + dzc, r0 + t * (r1 - r0) + rn
            for i in self.celdas(zc - rn, zc + rn):
                d = self.z[i] - zc
                if abs(d) <= rn:
                    rb = max(rc - math.sqrt(rn * rn - d * d), 0.0)
                    if rb < self.R[i]:
                        self.R[i] = rb

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
        self.ap = {}          # herramienta -> maxima profundidad radial cortada (mm)

    # --- texto
    def linea(self, t):
        self.l.append(t)

    def herramienta(self, num, vc, ancho=0.0, porta=None):
        # la Vc del JSON ("vc": {"1": 150, ...}) manda sobre la de por defecto
        vc = VC_PIEZA.get(num, vc)
        self.linea("T%02d%02d" % (num, num))
        self.linea("G96 S%d M3" % vc)
        self.tool, self.ancho, self.porta, self.f = num, ancho, porta, None
        self.nariz = NARIZ.get(num)
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
        # bajar en X con la herramienta ya dentro de la pieza (Z<0): WinUnisoft lo cuenta como
        # colision si el rapido roza material; se baja con avance, como en los programas del curso
        if x is not None and x1 < self.x - 1e-9 and min(self.z, z1) < 0 and self.x <= self.xseg + 1e-6:
            self.g01(x=x, z=z, feed=self.f or (".1" if self.tool == 5 else ".2"))
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
            if max(x / 2, 0.0) < self.m.maximo(za, zb) - 0.02:
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
        if not self.ancho and abs(z1 - z0) > 1e-9:
            for i in self.m.celdas(z0, z1):
                if abs(z1 - z0) < 1e-9:
                    rt = min(r0, r1)
                else:
                    t = min(max((self.m.z[i] - z0) / (z1 - z0), 0.0), 1.0)
                    rt = r0 + t * (r1 - r0)
                # la celda justo en el extremo del tramo puede ser una cara vertical (no es pasada)
                if min(abs(self.m.z[i] - z0), abs(self.m.z[i] - z1)) < DZ * 1.01:
                    continue
                # espesor perpendicular a la pasada (en una pared empinada el radial engaña)
                cos_t = abs(z1 - z0) / max(math.hypot(z1 - z0, r1 - r0), 1e-9)
                e = (self.m.R[i] - rt) * cos_t
                if e > self.ap.get(self.tool, (0.0,))[0] and self.m.z[i] < -1e-6:
                    self.ap[self.tool] = (e, self.m.z[i])
        if self.ancho:
            n = max(2, int(math.hypot(abs(r1 - r0), abs(z1 - z0)) / 0.1))
            for k in range(n + 1):
                t = k / n
                self.m.corte_ancho(z0 + t * (z1 - z0), z0 + t * (z1 - z0) + self.ancho,
                                   r0 + t * (r1 - r0))
        elif getattr(self, "nariz", None):
            rn, dzc = self.nariz
            idx = list(self.m.celdas(min(z0, z1) - rn - DZ, max(z0, z1) + rn + DZ))
            antes = {i: self.m.R[i] for i in idx}
            self.m.corte_nariz(z0, r0, z1, r1, rn, dzc)
            if abs(z1 - z0) > 1e-9:
                cos_t = abs(z1 - z0) / max(math.hypot(z1 - z0, r1 - r0), 1e-9)
                for i in idx:
                    # cerca de los extremos el radio toca de costado una cara (no es profundidad)
                    if min(abs(self.m.z[i] - z0 - dzc), abs(self.m.z[i] - z1 - dzc)) < rn + DZ:
                        continue
                    e = (antes[i] - self.m.R[i]) * cos_t
                    if e > self.ap.get(self.tool, (0.0,))[0] and self.m.z[i] < -1e-6:
                        self.ap[self.tool] = (e, self.m.z[i])
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
            libre = self.m.porta_libre(p[1], p[0] / 2, self.tool in (1, 3), tg, tol)
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
        # con radio de punta, el inserto ocupa rn a cada lado del centro (corrido rn de la punta)
        rn = self.nariz[0] if getattr(self, "nariz", None) else 0.0
        return 2 * self.m.maximo(z - 0.35 - 2 * rn, z + 0.35 + 2 * rn) + 1.0

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
        # sale siempre hacia arriba: si el material de al lado es mas bajo, no se baja hasta el
        xl = max(self.xl_local(self.z), self.x)
        if xl < self.xseg - 0.01:
            if xl > self.x + 1e-6:
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


# ---------------------------------------------- compensación del radio de punta (sin G41/G42)
# El programa da la posición de la punta teórica (la que define el código de forma). El centro
# del radio de punta tiene que recorrer el perfil corrido "r" hacia afuera; la punta teórica está
# a (-r, -r) del centro con código de forma 3 (herramienta derecha) y a (+r, -r) con el 4 (izquierda).
R_PUNTA = {1: 0.8, 3: 0.4, 4: 0.4}     # CNMG120408 y VNMG160404 (catálogo A10 y A14)


def _tangente(s, t):
    """Tangente unitaria (z, r) del tramo en t, recorriéndolo de p0 a p1."""
    if not s.R:
        dz, dr = s.dz, s.dx / 2
        L = math.hypot(dz, dr) or 1.0
        return dz / L, dr / L
    a = s.a0 + t * s.sweep
    sg = 1 if s.sweep >= 0 else -1
    return -math.sin(a) * sg, math.cos(a) * sg


def _corrido(s, d):
    """Tramo del perfil corrido d hacia afuera. Elementos en (z, r): dict tipo/p0/p1/R/g/c."""
    z0, r0, z1, r1 = s.p0[1], s.p0[0] / 2, s.p1[1], s.p1[0] / 2
    tz, tr = _tangente(s, 0.0)
    nz, nr = tr, -tz
    if not s.R:
        return {"tipo": "L", "p0": (z0 + d * nz, r0 + d * nr), "p1": (z1 + d * nz, r1 + d * nr)}
    uz, ur = (z0 - s.zc) / s.R, (r0 - s.rc) / s.R
    vz, vr = (z1 - s.zc) / s.R, (r1 - s.rc) / s.R
    Rn = s.R + d if uz * nz + ur * nr > 0 else s.R - d
    if Rn <= 1e-3:
        return None
    return {"tipo": "A", "p0": (s.zc + uz * Rn, s.rc + ur * Rn), "p1": (s.zc + vz * Rn, s.rc + vr * Rn),
            "R": Rn, "g": s.g, "c": (s.zc, s.rc)}


def _cortes(a, b):
    """Intersecciones de las curvas completas (recta o círculo) de dos elementos."""
    def recta(e):
        (z0, r0), (z1, r1) = e["p0"], e["p1"]
        return (z0, r0), (z1 - z0, r1 - r0)
    def rc(p, v, c, R):
        fz, fr = p[0] - c[0], p[1] - c[1]
        A = v[0] ** 2 + v[1] ** 2
        B = 2 * (fz * v[0] + fr * v[1])
        C = fz * fz + fr * fr - R * R
        disc = B * B - 4 * A * C
        if A < 1e-12 or disc < 0:
            return []
        return [(p[0] + t * v[0], p[1] + t * v[1]) for t in ((-B + math.sqrt(disc)) / (2 * A), (-B - math.sqrt(disc)) / (2 * A))]
    if a["tipo"] == "L" and b["tipo"] == "L":
        (p, v), (q, w) = recta(a), recta(b)
        den = v[0] * w[1] - v[1] * w[0]
        if abs(den) < 1e-12:
            return []
        t = ((q[0] - p[0]) * w[1] - (q[1] - p[1]) * w[0]) / den
        return [(p[0] + t * v[0], p[1] + t * v[1])]
    if a["tipo"] == "L" or b["tipo"] == "L":
        l, c = (a, b) if a["tipo"] == "L" else (b, a)
        p, v = recta(l)
        return rc(p, v, c["c"], c["R"])
    (c1, R1), (c2, R2) = (a["c"], a["R"]), (b["c"], b["R"])
    dz, dr = c2[0] - c1[0], c2[1] - c1[1]
    D = math.hypot(dz, dr)
    if D < 1e-12 or D > R1 + R2 or D < abs(R1 - R2):
        return []
    x = (D * D + R1 * R1 - R2 * R2) / (2 * D)
    h = math.sqrt(max(R1 * R1 - x * x, 0.0))
    mz, mr = c1[0] + x * dz / D, c1[1] + x * dr / D
    return [(mz - h * dr / D, mr + h * dz / D), (mz + h * dr / D, mr - h * dz / D)]


def compensar(grupo, extra, rn, codigo, antes=None, despues=None):
    """Trayectoria de la punta teórica para seguir el grupo (en orden de perfil) con un inserto de
    radio rn, dejando 'extra' mm de sobremetal (normal al perfil). antes/despues: tramos vecinos
    del perfil que hace otra herramienta; si el rincón con ellos es cóncavo, se recorta contra
    ellos para que el radio de punta no muerda la pieza."""
    d = extra + rn
    els, esquinas = [], []
    for s in [antes] + list(grupo) + [despues]:
        e = _corrido(s, d) if s is not None else None
        if e is not None:
            e["vecino"] = s is antes or s is despues
            els.append(e)
            esquinas.append((s.p0[1], s.p0[0] / 2))
    out = []
    for k, e in enumerate(els):
        if out:
            prev = out[-1]
            q = esquinas[k]
            if math.hypot(prev["p1"][0] - e["p0"][0], prev["p1"][1] - e["p0"][1]) > 1e-6:
                t1 = prev["p1"][0] - prev["p0"][0], prev["p1"][1] - prev["p0"][1]
                t2 = e["p1"][0] - e["p0"][0], e["p1"][1] - e["p0"][1]
                if prev["tipo"] == "A":
                    a = math.atan2(prev["p1"][1] - prev["c"][1], prev["p1"][0] - prev["c"][0])
                    sg = -1 if prev["g"] == "G02" else 1
                    t1 = (-math.sin(a) * sg, math.cos(a) * sg)
                if e["tipo"] == "A":
                    a = math.atan2(e["p0"][1] - e["c"][1], e["p0"][0] - e["c"][0])
                    sg = -1 if e["g"] == "G02" else 1
                    t2 = (-math.sin(a) * sg, math.cos(a) * sg)
                cruz = t1[0] * t2[1] - t1[1] * t2[0]
                if cruz > 0:      # esquina convexa: el centro del radio la rodea con un arco
                    a0 = math.atan2(prev["p1"][1] - q[1], prev["p1"][0] - q[0])
                    a1 = math.atan2(e["p0"][1] - q[1], e["p0"][0] - q[0])
                    da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
                    out.append({"tipo": "A", "p0": prev["p1"], "p1": e["p0"], "R": d,
                                "g": "G02" if da < 0 else "G03", "c": q})
                else:             # esquina cóncava: se cortan los dos tramos corridos
                    cand = _cortes(prev, e)
                    if cand:
                        I = min(cand, key=lambda p: math.hypot(p[0] - q[0], p[1] - q[1]))
                        prev["p1"] = I
                        e = dict(e)
                        e["p0"] = I
        out.append(e)
    # los vecinos solo sirvieron para recortar: no se recorren (ni el arco de esquina hacia ellos)
    while out and (out[0].get("vecino") or (len(out) > 1 and out[1].get("vecino") is False and False)):
        out.pop(0)
        if out and out[0]["tipo"] == "A" and out[0].get("c") and out[0]["R"] == d and "vecino" not in out[0]:
            out.pop(0)
    while out and out[-1].get("vecino"):
        out.pop()
        if out and out[-1]["tipo"] == "A" and out[-1]["R"] == d and "vecino" not in out[-1]:
            out.pop()
    dz = -rn if codigo == 3 else rn
    res = []
    for e in out:
        p0 = (round(2 * (e["p0"][1] - rn), 3), round(e["p0"][0] + dz, 3))
        p1 = (round(2 * (e["p1"][1] - rn), 3), round(e["p1"][0] + dz, 3))
        if math.hypot((p1[0] - p0[0]) / 2, p1[1] - p0[1]) < 1e-3:
            continue
        if e["tipo"] == "L":
            res.append(Prim(p0, p1))
        else:
            c = math.hypot((p1[0] - p0[0]) / 2, p1[1] - p0[1])
            res.append(Prim(p0, p1, round(max(e["R"], c / 2 + 1e-4), 3), e["g"]))
    return res


VC_PIEZA = {}  # Vc (m/min) por herramienta, leída del JSON de la pieza
NARIZ = {}     # herramienta -> (radio de punta, corrimiento Z del centro); solo con compensación

# ------------------------------------------------------------------ estrategia "par"
# TP con herramientas derecha e izquierda (como T0909/T1010 de los TP originales):
#   T0101 DCLN R + CNMG120408RP: refrentado, G90 con pasadas grandes y una pasada de contorno
#   T0505 A4SM 2020K0317 + A4G0305M03U02GMN: ranuras rectas a medida, valles (G90) y tronzado
#   T0303 DVJN R + VNMG160404FP: acabado de lo que se corta hacia -Z
#   T0404 DVJN L (misma herramienta invertida: Quadrant 2, codigo de forma 4): acabado de
#         las paredes que bajan de diametro hacia la base, cortando hacia +Z
# Datos del catalogo Kennametal (A7): RP ap 1,1-6,4 mm y f 0,2-0,6; FP ap 0,3-2,5 y f 0,1-0,3.
PAR = {
    "paso1": 6.0,      # G90 de la T0101: 3 mm por lado (RP admite hasta 6,4)
    "f1": ".4",        # avance de desbaste (RP 0,2-0,6)
    "fc": ".3",        # avance de la pasada de contorno de la T0101
    "sobre_g90": 0.6,  # sobremetal radial que deja el G90
    "sobre_c": 0.6,    # sobremetal en diametro que deja el contorno (0,3 por lado: FP pide >= 0,3)
    "paso5": 3.2,      # G90 de la T0505 en valles: 1,6 por lado (grafico A70)
    "f5p": ".12",      # avance de entrada de la T0505 (ejemplo A71: 0,14 ranurado)
    "f5": ".2",        # avance de torneado de la T0505 (ejemplo A71: 0,25 torneado)
    "ff": ".2",        # avance de acabado T0303/T0404 (FP 0,1-0,3)
}
ANG_PORTA.setdefault(1, 5.0)     # DCLN: filo secundario a 5 grados de Z (95 + 80)
ANG_PORTA.setdefault(4, ANG_PORTA[3])
TOL_PORTA.setdefault(1, 0.3)
TOL_PORTA.setdefault(4, TOL_PORTA[3])


def ranuras_rectas(per):
    """Ranuras rectangulares del perfil (pared, fondo plano, pared) de ancho >= T0505."""
    out = []
    for i in range(len(per) - 3):
        a, b, c, e = per[i:i + 4]
        if (abs(a["z"] - b["z"]) < 1e-9 and b["x"] < a["x"] - 1e-9 and abs(b["x"] - c["x"]) < 1e-9
                and c["z"] < b["z"] - 1e-9 and abs(c["z"] - e["z"]) < 1e-9 and e["x"] > c["x"] + 1e-9
                and not c.get("arco") and b["z"] - c["z"] >= ANCHO_T5 - 1e-9):
            out.append({"x": b["x"], "za": b["z"], "zb": c["z"], "xa": a["x"], "xe": e["x"]})
    return out


def generar_par(d, avisos):
    NARIZ.clear()
    NARIZ.update({1: (R_PUNTA[1], R_PUNTA[1]), 3: (R_PUNTA[3], R_PUNTA[3]), 4: (R_PUNTA[4], -R_PUNTA[4])})
    bd, bl = float(d["bruto"]["d"]), float(d["bruto"]["l"])
    largo = float(d["largo"])
    per = d["perfil"]
    z_parte = -(largo + ANCHO_T5)
    xseg = bd + 3.0
    prims0 = prims_del_perfil(per)
    mapa = Mapa(6.0, -(largo + 14.0), bd / 2, 1.0)
    pmax, pmin = perfil_en_mapa(mapa, prims0)
    segs = []
    for p in prims0:
        if abs(p.dx) < 1e-9 and abs(p.dz) < 1e-9:
            continue
        segs += partir_en_apice(p)
    ranuras = ranuras_rectas(per)
    lim3 = ANG_PORTA[3]
    for s in segs:
        s.rev = False
        zlo, zhi = min(s.p0[1], s.p1[1]), max(s.p0[1], s.p1[1])
        if any(g["zb"] - 1e-9 <= zlo and zhi <= g["za"] + 1e-9 and max(s.p0[0], s.p1[0]) <= max(g["xa"], g["xe"]) + 1e-9
               for g in ranuras):
            s.herr = "ranura"
        elif s.dx < -1e-9 and s.angulo_bajada() > lim3 - 1e-6:
            s.herr, s.rev = 4, True
        else:
            s.herr = 3

    P = Prog(mapa, xseg, bd, avisos)
    for t in ("%", "O2222", "G54"):
        P.linea(t)

    # ------------------------------------------------ T0101: refrentado, G90 y contorno
    P.herramienta(1, 150)
    P.g00(xseg, 5.0)
    P.g00(0.0)
    P.g01(z=0.0, feed=".3")
    P.g01(xseg)
    for i in mapa.celdas(0.0 + DZ, mapa.ztop):
        mapa.R[i] = 0.0
    P.g00(z=5.0)
    P.g00(xseg)
    sg90 = PAR["sobre_g90"]
    rmax = max(pmax[i] for i, z in enumerate(mapa.z) if -largo - 1e-9 <= z <= 0)
    D = round(2 * (rmax + sg90), 3)
    if (bd - D) / 2 < 1.1:          # pasada minima de RP
        D = bd - 2.2
    pasadas = []
    while D > 1.0:
        zl = None
        for i, z in enumerate(mapa.z):
            if z > 0:
                continue
            if z < -(largo + 1e-9):
                break
            if pmax[i] + sg90 > D / 2 + 1e-9:
                zl = z
                break
        # termina contra la pared: si quedara una franja de MARGEN_Z a la altura de la pasada
        # anterior, la pasada de contorno tendria que sacarla entera (mas de 6,4 mm)
        z_fin = z_parte if zl is None else max(zl + DZ, z_parte)
        if z_fin > -0.3:
            break
        pasadas.append((D, round(z_fin, 3)))
        D = round(D - PAR["paso1"], 3)
    zant = None
    for k, (D, zf) in enumerate(pasadas):
        mapa.corte_recta(5.0, D / 2, zf, D / 2)
        if k == 0:
            P.linea("G90 X%s Z%s F%s" % (fmt(D), fmt(zf), PAR["f1"]))
        elif abs(zf - zant) < 1e-9:
            P.linea("X%s" % fmt(D))
        else:
            P.linea("X%s Z%s" % (fmt(D), fmt(zf)))
        P.camino.append(("F", 1, [(5.0, D / 2), (zf, D / 2)]))
        zant = zf
    P.f = PAR["f1"]
    P.x, P.z = xseg, 5.0

    # contorno: tramos que no bajan de diametro y donde el porta (filo secundario a 5 grados)
    # no toca material hacia +Z
    tg1 = math.tan(math.radians(ANG_PORTA[1]))
    oc = PAR["sobre_c"]

    # obstaculo para el porta: donde el contorno pasa, el material queda en perfil + sobremetal
    # (la propia pasada lo saca antes de que llegue el porta); en el resto, lo que dejo el G90
    def obstaculos(tramos):
        sube = [False] * len(mapa.R)
        for s in tramos:
            if s is not None:
                for i in mapa.celdas(s.p0[1], s.p1[1]):
                    sube[i] = True
        return [min(mapa.R[i], pmax[i] + oc / 2) if sube[i] else mapa.R[i] for i in range(len(mapa.R))]

    obst = obstaculos([s for s in segs if s.herr != "ranura" and s.dx >= -1e-9])

    def libre1(q):
        z, r = q[1], (q[0] + oc) / 2
        i0 = mapa.i(z)
        for k in range(1, int(25.0 / DZ)):
            i = i0 - k
            if i < 0:
                break
            if obst[i] > r + tg1 * k * DZ + TOL_PORTA[1]:
                return False
        return True

    for _vuelta in range(6):     # se repite con los tramos que de verdad recorre el contorno
      piezas = []
      for s in segs:
        if s.herr == "ranura" or s.dx < -1e-9:
            piezas.append(None)
            continue
        n = max(4, int(s.largo() / 0.25))
        ts = [k / n for k in range(n + 1)]
        ok = [libre1(s.pt(t)) for t in ts]
        k0 = None
        for k in range(len(ts) - 1, -1, -1):
            if not ok[k]:
                break
            k0 = k
        if k0 is None or ts[k0] > 0.98:
            piezas.append(None)
        elif k0 == 0:
            piezas.append(s)
        else:
            piezas.append(s.cortar(ts[k0])[1])
      nuevo = obstaculos(piezas)
      if nuevo == obst:
          break
      obst = nuevo
    grupos_c, act = [], []
    for s, pz in zip(segs, piezas):
        if pz is not None and (not act or (abs(act[-1].p1[0] - pz.p0[0]) < 1e-6 and abs(act[-1].p1[1] - pz.p0[1]) < 1e-6)):
            act.append(pz)
        else:
            if act:
                grupos_c.append(act)
            act = [pz] if pz is not None else []
    if act:
        grupos_c.append(act)
    P.porta = ANG_PORTA[1]
    def paralelo(s, dd):
        """Tramo corrido dd (en diametro) hacia afuera; los arcos, concentricos."""
        if not s.R:
            return s.trasladado(dd)
        rm = s.pt(0.5)[0] / 2
        k = (s.R + dd / 2) / s.R if rm >= s.rc else (s.R - dd / 2) / s.R
        q = [(2 * (s.rc + (pt[0] / 2 - s.rc) * k), s.zc + (pt[1] - s.zc) * k) for pt in (s.p0, s.p1)]
        q = [(round(max(x, 0.0), 3), round(z, 3)) for x, z in q]
        return Prim(q[0], q[1], round(s.R * k, 3), s.g)

    def sin_gubias(rec, rn, dzc, tol=0.01):
        """Recorta el principio y el final de una pasada compensada donde el radio de punta
        quedaría por debajo de la pieza terminada (gubia)."""
        def ok(q):
            zc, rc = q[1] + dzc, q[0] / 2 + rn
            for i in mapa.celdas(zc - rn, zc + rn):
                dd = mapa.z[i] - zc
                if abs(dd) <= rn and rc - math.sqrt(rn * rn - dd * dd) < pmax[i] - tol and mapa.z[i] <= 0:
                    return False
            return True
        def recorte(rec):
            while rec:
                s0 = rec[0]
                n = max(4, int(s0.largo() / 0.05))
                k = next((k for k in range(n + 1) if ok(s0.pt(k / n))), None)
                if k is None:
                    rec = rec[1:]
                    continue
                if k > 0:
                    rec = [s0.cortar(k / n)[1]] + rec[1:]
                return rec
            return rec
        rec = recorte(rec)
        rec = [x.invertido() for x in reversed(recorte([x.invertido() for x in reversed(rec)]))]
        return rec

    def vecinos(g):
        cerca = lambda p, q: abs(p[0] - q[0]) < 1e-6 and abs(p[1] - q[1]) < 1e-6
        antes = next((s for s in segs if cerca(s.p1, g[0].p0)), None)
        despues = next((s for s in segs if cerca(s.p0, g[-1].p1)), None)
        return antes, despues

    for g in grupos_c:
        orden = sin_gubias(compensar(g, oc / 2, R_PUNTA[1], 3, *vecinos(g)), R_PUNTA[1], R_PUNTA[1])
        if not orden:
            continue
        a = orden[0].p0
        P.aproximar(a[0], a[1], PAR["fc"])
        for s in orden:
            if s.R:
                P.arco(s, PAR["fc"])
            else:
                P.g01(None if abs(s.dx) < 1e-9 else s.p1[0], None if abs(s.dz) < 1e-9 else s.p1[1], PAR["fc"])
        P.salir()
    P.porta = None
    P.fin_herramienta()

    # ------------------------------------------------ T0505: ranuras a medida y valles
    sem_r = oc / 2
    P.herramienta(5, 120, ANCHO_T5)
    for g in ranuras:
        z1 = round(g["za"] - ANCHO_T5, 3)
        xs = round(min(2 * mapa.maximo(g["zb"], g["za"]) + 1.0, xseg), 3)
        P.g00(xseg, z1)
        if xs < xseg - 0.01:
            P.g00(xs)
        P.g01(g["x"], feed=PAR["f5p"])
        if g["zb"] < z1 - 1e-9:
            P.g01(z=g["zb"], feed=PAR["f5"])
        P.g01(xs, feed=PAR["f5"])
        mapa.corte_ancho(g["zb"], g["za"], g["x"] / 2)
        P.g00(xseg)
    # valles: material que el acabado no puede sacar en una pasada (FP <= 2,5 mm)
    valles, en = [], None
    for i, z in enumerate(mapa.z):
        if z > 0 or z < -largo:
            continue
        if mapa.R[i] - (pmax[i] + sem_r) > UMBRAL_VALLE:
            if en is None:
                en = [z, z]
            en[1] = z
        elif en is not None:
            valles.append(en)
            en = None
    if en is not None:
        valles.append(en)
    valles = [v for v in valles if v[0] - v[1] > 0.4]
    w = ANCHO_T5
    mg = DZ          # la cuchilla frena casi contra la pared (sin franja alta para el acabado)

    def prof(z0):          # radio minimo al que puede bajar la cuchilla en [z0, z0 + w]
        return max(pmax[i] for i in mapa.celdas(z0, z0 + w)) + sem_r

    for za, zb in valles:
        # entrada en el punto mas hondo del valle (la cuchilla ocupa [z0, z0 + w])
        lo, hi = max(zb, -largo), za - w
        cand = [round(lo + k * 0.05, 3) for k in range(int(max(0.0, hi - lo) / 0.05) + 1)] or [round(za - w, 3)]
        z0 = min(cand, key=lambda z: (prof(z), -z))
        xd0 = round(2 * prof(z0) + 1e-9, 3)
        xtop = 2 * mapa.maximo(min(zb, z0), max(za, z0 + w))
        xs = round(min(xtop + 1.0, xseg), 3)
        P.g00(xseg, z0)
        if xs < xseg - 0.01:
            P.g00(xs)
        P.g01(xd0, feed=PAR["f5p"])
        mapa.corte_ancho(z0, z0 + w, xd0 / 2)
        P.g01(xs, feed=PAR["f5"])
        P.x, P.z = xs, z0
        for sentido in (-1, 1):          # G90 hacia -Z y despues hacia +Z (el A4 tornea en los dos)
            D = round(xtop - PAR["paso5"], 3)
            primero, zant = True, None
            while True:
                D = max(D, xd0)
                if sentido < 0:          # avanza hacia -Z hasta que la pieza sube
                    zend = zb
                    for k, z in enumerate(mapa.z):
                        if z >= z0 or z < -largo:
                            continue
                        if pmax[k] + sem_r > D / 2 + 1e-9:
                            zend = z + mg
                            break
                    zend = round(max(zend, -largo), 3)
                    ok = zend < z0 - 0.3
                    za_c, zb_c = zend, z0 + w
                else:                    # avanza hacia +Z: el lado derecho de la cuchilla frena antes
                    zr = za
                    for k in range(len(mapa.z) - 1, -1, -1):
                        z = mapa.z[k]
                        if z <= z0 + w or z > 0:
                            continue
                        if pmax[k] + sem_r > D / 2 + 1e-9:
                            zr = z - mg
                            break
                    zend = round(min(zr, 0.0) - w, 3)
                    ok = zend > z0 + 0.3
                    za_c, zb_c = z0, zend + w
                if ok and mapa.maximo(min(za_c, zb_c), max(za_c, zb_c)) > D / 2 + 0.05:
                    mapa.corte_ancho(za_c, zb_c, D / 2)
                    if primero:
                        txt = "G90 X%s Z%s F%s" % (fmt(D), fmt(zend), PAR["f5"])
                    elif zant is not None and abs(zend - zant) < 1e-9:
                        txt = "X%s" % fmt(D)
                    else:
                        txt = "X%s Z%s" % (fmt(D), fmt(zend))
                    P.linea(txt)
                    P.camino.append(("F", 5, [(z0, xs / 2), (z0, D / 2), (zend, D / 2), (zend, xs / 2)]))
                    primero, zant = False, zend
                    P.f = PAR["f5"]
                if D <= xd0 + 1e-9:
                    break
                D = round(D - PAR["paso5"], 3)
        P.g00(xseg)
    P.fin_herramienta()

    # ------------------------------------------------ grupos de acabado
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

    def fusionar(orden):
        fus = []
        for q in orden:
            a = fus[-1] if fus else None
            if (a is not None and a.R and q.R and a.g == q.g and abs(a.R - q.R) < 1e-6
                    and abs(a.zc - q.zc) < 0.01 and abs(a.rc - q.rc) < 0.01):
                fus[-1] = Prim(a.p0, q.p1, a.R, a.g)
            else:
                fus.append(q)
        return fus

    def espesor(orden):
        """Material (radial) que queda sobre los tramos inclinados del grupo."""
        mx = 0.0
        for s in orden:
            if abs(s.dz) < 1e-9:
                continue
            for i in P.m.celdas(s.p0[1], s.p1[1]):
                z = P.m.z[i]
                if min(abs(z - s.p0[1]), abs(z - s.p1[1])) < 1.01 * DZ:
                    continue
                mx = max(mx, P.m.R[i] - pmax[i])
        return mx

    def pasada(orden, feed, codigo=3):
        """orden en sentido del perfil; la T0404 (codigo 4) lo recorre al reves (hacia +Z)."""
        orden = fusionar(orden)
        rn = R_PUNTA.get(4 if codigo == 4 else 3, 0.4)
        recorridos = []
        e = espesor(orden)
        if e > 2.0:        # FP admite hasta 2,5 mm: primero una pasada previa paralela al perfil
            recorridos.append(compensar(orden, round(max(0.3, e - 2.2), 2), rn, codigo, *vecinos(orden)))
        recorridos.append(compensar(orden, 0.0, rn, codigo, *vecinos(orden)))
        for rec in recorridos:
            rec = sin_gubias(rec, rn, rn if codigo == 3 else -rn)
            if not rec:
                continue
            if codigo == 4:
                rec = [s.invertido() for s in reversed(rec)]
            a = rec[0].p0
            P.aproximar(a[0], a[1], feed)
            for s in rec:
                if s.R:
                    P.arco(s, feed)
                else:
                    P.g01(None if abs(s.dx) < 1e-9 else s.p1[0], None if abs(s.dz) < 1e-9 else s.p1[1], feed)
            P.salir()

    def inicio_libre(s, hacia_mas_z, tang, tol):
        """Primer t (0..1) del tramo desde el que el porta no toca la pieza terminada."""
        L = max(s.largo(), 1e-9)
        t = 0.0
        while t < 0.999:
            q = s.pt(t)
            if P.m.porta_libre(q[1], q[0] / 2, hacia_mas_z, tang, tol):
                return t
            t += 0.1 / L
        return None

    ff = PAR["ff"]
    tg3 = math.tan(math.radians(ANG_PORTA[3]))
    # ------------------------------------------------ T0303 acabado hacia -Z
    a_cubrir = {}      # indice de tramo -> t hasta donde lo tiene que hacer la T0404
    P.herramienta(3, 200, 0.0, ANG_PORTA[3])
    for g in grupos(lambda s: s.herr == 3):
        g = list(g)
        t0 = inicio_libre(g[0], True, tg3, TOL_PORTA[3])
        idx = segs.index(g[0])
        if t0 is None:
            a_cubrir[idx] = 1.0
            g = g[1:]
            if not g:
                continue
        elif t0 > 0:
            a_cubrir[idx] = t0
            g[0] = g[0].cortar(t0)[1]
        pasada(g, ff)
    P.fin_herramienta()

    # ------------------------------------------------ T0404 acabado hacia +Z
    tg4 = math.tan(math.radians(ANG_PORTA[4]))
    trabajos = []
    for g in grupos(lambda s: s.herr == 4):
        i_fin = segs.index(g[-1]) + 1
        orden = list(g)          # en orden de perfil; pasada() lo recorre hacia +Z
        if i_fin in a_cubrir:
            s = segs[i_fin]
            t = min(1.0, a_cubrir[i_fin] + 0.5 / max(s.largo(), 1e-9))
            orden.append(s.cortar(t)[0] if t < 1.0 else s)
            del a_cubrir[i_fin]
        trabajos.append(orden)
    for i, t in a_cubrir.items():
        s = segs[i]
        aviso(avisos, "La T0303 no alcanza el comienzo de X%s Z%s y no hay pared para la T0404"
              % (fmt(s.p0[0]), fmt(s.p0[1])))
    if trabajos:
        P.herramienta(4, 200, 0.0, ANG_PORTA[4])
        for orden in reversed(trabajos):
            pasada(orden, ff, 4)
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
    return P, mapa, (pmax, pmin), segs


def generar(d, avisos):
    NARIZ.clear()
    if d.get("estrategia") == "par":
        VC_PIEZA.clear()
        VC_PIEZA.update({int(k): float(v) for k, v in d.get("vc", {}).items()})
        return generar_par(d, avisos)
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

    # el porta neutro no puede seguir paredes empinadas (refrentados, paredes de escalones,
    # extremos de arcos con tangente vertical): esos pedazos se sacan de la T0909.
    #  - pared de frente (sube de diametro hacia la base): la termina la T0303 sin sobremetal
    #  - pared de atras (baja de diametro hacia la base): la sigue la T0909 desde la base
    #  - refrentado en Z0: ya lo hizo la T0101
    def pendiente(sg, t):
        a, b = sg.pt(max(0.0, t - 0.004)), sg.pt(min(1.0, t + 0.004))
        dr, dz = (b[0] - a[0]) / 2.0, b[1] - a[1]
        return math.degrees(math.atan2(abs(dr), abs(dz))), dr

    nuevos = []
    for sg in segs:
        if sg.herr != 9:
            nuevos.append(sg)
            continue
        n = 40 if sg.R else 1
        marcas = []
        for k in range(n):
            t = (k + 0.5) / n
            ang, dr = pendiente(sg, t)
            marcas.append(ang > LIM_NEUTRO)
        if not any(marcas):
            nuevos.append(sg)
            continue
        if all(marcas) or not sg.R:
            trozos = [(sg, True)]
        else:
            trozos, resto, t_ant = [], sg, 0.0
            for k in range(1, n):
                if marcas[k] != marcas[k - 1]:
                    t = k / n
                    tl = (t - t_ant) / (1.0 - t_ant)
                    a, b = resto.cortar(tl)
                    trozos.append((a, marcas[k - 1]))
                    resto, t_ant = b, t
            trozos.append((resto, marcas[-1]))
        for tr, emp in trozos:
            tr.herr, tr.rev, tr.en_base = 9, sg.rev, sg.en_base
            if emp:
                _, dr = pendiente(tr, 0.5)
                if abs(tr.dz) < 1e-9 and abs(tr.p0[1]) < 1e-6 and abs(tr.p1[1]) < 1e-6:
                    tr.herr = "frente"          # cara en Z0: la refrentó la T0101
                elif dr > 0:
                    tr.herr = "e3"              # pared de frente: T0303 sin sobremetal
                # pared de atrás: la sigue la T0909 desde la base (s.rev), como antes
            nuevos.append(tr)
    segs = nuevos

    P = Prog(mapa, xseg, bd, avisos)
    P.linea("%")
    P.linea("O2222")
    P.linea("G54")

    # ------------------------------------------------ T0101 frenteado y G90
    P.herramienta(1, 150)
    P.g00(xseg, 5.0)
    # refrentado desde el centro hacia afuera, como en los programas del curso: WinUnisoft
    # marca colision del DCLN si se refrenta hacia el centro (lado que no corta)
    P.g00(0.0)
    P.g01(z=0.0, feed=".3")
    P.g01(xseg)
    for i in mapa.celdas(0.0 + DZ, mapa.ztop):
        mapa.R[i] = 0.0
    P.g00(z=5.0)
    P.g00(xseg)
    D = bd - PASO_G90   # la primera pasada ya saca 1,2 por lado
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
            # consigna del TP: el desbaste se hace con G90; G01 solo para entrar y salir.
            # 1) ranura de entrada con G01 al lado de la pared (la T0505 ocupa [z0, z0+ancho])
            # 2) desde esa ranura, ciclos G90 hacia -Z que vacían el valle por escalones
            z0 = round(za - ANCHO_T5, 3)
            xtop = 2 * mapa.maximo(min(zb, z0), za)
            xs = round(min(xtop + 1.0, xseg), 3)
            prof0 = max(pmax[i] for i in mapa.celdas(z0, z0 + ANCHO_T5)) + sem_r
            xd0 = round(2 * prof0 + 1e-9, 3)
            P.g00(xseg, z0)
            if xs < xseg - 0.01:
                P.g00(xs)
            P.g01(xd0, feed=".1")
            mapa.corte_ancho(z0, z0 + ANCHO_T5, xd0 / 2)
            P.g01(xs)
            if zb < z0 - 0.3:
                D = round(xtop - PASO_G90, 3)
                primero, zant = True, None
                while D > xd0 - 1e-9 or primero:
                    D = max(D, xd0)
                    zend = None
                    for k, z in enumerate(mapa.z):
                        if z > z0 or z < -largo:
                            continue
                        if pmax[k] + sem_r > D / 2 + 1e-9:
                            zend = z + MARGEN_Z * 0.4
                            break
                    if zend is None:
                        zend = zb
                    zend = round(max(zend, zb), 3)
                    if zend < z0 - 0.3:
                        mapa.corte_ancho(zend, z0 + ANCHO_T5, D / 2)
                        if primero:
                            txt = "G90 X%s Z%s F.1" % (fmt(D), fmt(zend))
                        elif zant is not None and abs(zend - zant) < 1e-9:
                            txt = "X%s" % fmt(D)
                        else:
                            txt = "X%s Z%s" % (fmt(D), fmt(zend))
                        P.linea(txt)
                        P.camino.append(("F", 5, [(z0, xs / 2), (z0, D / 2), (zend, D / 2), (zend, xs / 2)]))
                        primero, zant = False, zend
                        P.f = ".1"
                    if D <= xd0 + 1e-9:
                        break
                    D = round(D - PASO_G90, 3)
                P.x, P.z = xs, z0
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
        return s.herr in (9, "e3") and (s.dx > -1e-9 or s.angulo_bajada() <= ANG_PORTA[3] + 1e-6)

    g3 = grupos(ok3)
    if g3 or any(s.herr == "e3" for s in segs):
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
        for g in grupos(lambda s: s.herr == "e3"):
            recorrer(g, 0.0, ".2", False, 3)
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
def interpretar_nc(lineas, mapa, bruto_d, largo, nariz=None):
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
                if z <= mapa.ztop and max(r, 0.0) < mapa.maximo(z, zb) - 0.02:
                    err.append((n, "G00 dentro del material en X%s Z%s" % (fmt(2 * r), fmt(z))))
                    return
            elif w:
                mapa.corte_ancho(z, z + w, r)
            elif not (nariz and st["tool"] in nariz):
                mapa.corte_recta(z, r, z, r)
        if not rapido and not w and nariz and st["tool"] in nariz:
            mapa.corte_nariz(z0, r0, z1, r1, *nariz[st["tool"]])
        elif not rapido and not w:
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
            if m == 90 and st["ancho"]:
                # cuchilla de ranurar: ocupa [z, z + ancho] en todo el recorrido (hacia -Z o hacia +Z)
                mapa.corte_ancho(min(z0, cz), max(z0, cz) + st["ancho"], cx / 2)
                camino.append(("F", st["tool"], [(z0, cx / 2), (cz, cx / 2)]))
            elif m == 90:
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
    """T5 pasa a canales y tronzado (A4SM ... GMN); T9 pasa a porta neutro DVVNN.
    T1 y T3: radio de punta del inserto elegido (CNMG120408 = 0,8; VNMG160404 = 0,4)."""
    if l.startswith(b"Tool=T1^"):
        return _campo(l, b"r", b"0.80000")
    if l.startswith(b"Tool=T3^"):
        return _campo(l, b"r", b"0.40000")
    if l.startswith(b"Tool=T5^"):
        l = l.replace(b"A4SM^R/L^2016K0317", b"A4SM^R/L^2016K0317^GMN")
        for k, v in ((b"IC", b"3.05000"), (b"_IC", b"3.05000"), (b"r", b"0.20000")):
            l = _campo(l, k, v)   # inserto W 3,05 y radio 0,2 (A73)
        return l
    if l.startswith(b"Tool=T9^"):
        l = re.sub(rb"^Tool=T9\^9:\^\S*", b"Tool=T9^9:^DVVNN^2020K16KC04", l)
        for k, v in ((b"_Descrip", b"DVVNN^2020K16KC04"), (b"Quadrant", b"1"),
                     (b"Orient.", b"72.50000"), (b"_Orient.", b"72.50000"),
                     (b"IC", b"9.53000"), (b"_IC", b"9.53000"), (b"Alpha", b"35.00000"),
                     (b"r", b"0.40000"), (b"_CodForma", b"8"), (b"H_Width", b"20.00000"),
                     (b"H_Hght", b"125.00000"), (b"H_Clr_X", b"8.00000"),
                     (b"H_Clr_Z", b"2.50000"), (b"H_Ang", b"72.50000")):
            l = _campo(l, k, v)
    return l


def escribir_prj(plantilla, destino, bruto_d, bruto_l, par=False):
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
            if par and lineas[i].startswith(b"Tool=T5^"):
                # porta de 20x20 (A75): encaja en la torreta igual que los demas
                lineas[i] = lineas[i].replace(b"2016K0317", b"2020K0317")
        elif sec == b"[BRUTO]":
            if l.startswith(b"ZMax/DExt="):
                lineas[i] = b"ZMax/DExt=" + fmt(bruto_d).encode()
            elif l.startswith(b"YMax/ZMax="):
                lineas[i] = b"YMax/ZMax=" + fmt(bruto_l).encode()
        elif sec == b"[ORIGEN]" and l.startswith(b"G54="):
            lineas[i] = b"G54=0.00,0.00," + fmt(bruto_l - 1).encode()
    if par:
        # T4 = la T3 invertida (DVJN L): igual que T9/T10 de los TP originales,
        # cambia solo Quadrant=2 y el codigo de forma 4
        i3 = next(i for i, l in enumerate(lineas) if l.startswith(b"Tool=T3^"))
        i4 = next(i for i, l in enumerate(lineas) if l.startswith(b"Tool=T4^"))
        l4 = lineas[i3].replace(b"Tool=T3^3:^DVJN^R/L^2020K16KC04", b"Tool=T4^4:^DVJN^R/L^2020K16KC04^(4)")
        for k, v in ((b"_NumHta", b"4"), (b"_Corrector", b"4"), (b"_Descrip", b"DVJN^R/L^2020K16KC04^(4)"),
                     (b"Quadrant", b"2"), (b"_CodForma", b"4")):
            l4 = _campo(l4, k, v)
        lineas[i4] = l4
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
                 float(d["bruto"]["d"]), float(d["bruto"]["l"]), d.get("estrategia") == "par")
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
    m2, errores, camino = interpretar_nc(lin, m2, bd, largo, dict(NARIZ) or None)
    sob, zs, exc, ze = comparar(m2, pmax, pmin, largo)
    ruta_png = os.path.join(args.salida, nombre + " trayectoria.png")
    dibujar_png(ruta_png, camino, prims_del_perfil(d["perfil"]), bd, largo)

    print("Proyecto generado en: %s" % args.salida)
    print("  %s.nc  (%d lineas)" % (nombre, len(P.l)))
    if P.ap:
        print("Profundidad radial maxima por herramienta (contorno): " +
              ", ".join("T%02d%02d %.2f mm (Z%s)" % (t, t, v[0], fmt(v[1])) for t, v in sorted(P.ap.items()) if t))
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
