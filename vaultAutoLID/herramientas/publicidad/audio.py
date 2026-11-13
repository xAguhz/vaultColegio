"""Sintetiza música, efectos y mezcla con el relator según schedule.json.
Uso: python3 audio.py <dir_voz> <salida.wav>"""
import json, sys, wave, os
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
SCH = json.load(open(os.path.join(HERE, "schedule.json")))
DUR = SCH["duration"]
N = int(DUR * SR)
rng = np.random.default_rng(7)


def t_arr(d):
    return np.arange(int(d * SR)) / SR


def nf(name):
    """'A4' -> Hz"""
    notes = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    n, o = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((notes[n] + (o - 4) * 12) / 12)


def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if hi:
        m *= 1 / np.sqrt(1 + (f / hi) ** 4)
    if lo:
        m *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** 4)
    return np.fft.irfft(X * m, len(x))


def tv_band(x, centers, q=1.5, block=2048):
    """Filtro pasabanda que varía en el tiempo (overlap-add)."""
    hop = block // 2
    win = np.hanning(block)
    out = np.zeros(len(x) + block)
    xp = np.concatenate([x, np.zeros(block)])
    f = np.fft.rfftfreq(block, 1 / SR)
    for i, s in enumerate(range(0, len(x), hop)):
        c = centers[min(s, len(centers) - 1)]
        bw = c / q
        m = np.exp(-0.5 * ((f - c) / bw) ** 2)
        seg = np.fft.irfft(np.fft.rfft(xp[s:s + block] * win) * m, block)
        out[s:s + block] += seg
    return out[:len(x)]


def env_adsr(n, a=0.01, d=0.1, s=0.7, r=0.2):
    t = np.arange(n) / SR
    T = n / SR
    e = np.where(t < a, t / max(a, 1e-6), np.where(t < a + d, 1 - (1 - s) * (t - a) / max(d, 1e-6), s))
    rel = np.clip((T - t) / max(r, 1e-6), 0, 1)
    return e * rel


def place(buf, sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    sig = sig[: len(buf) - i]
    l = np.cos((pan + 1) * np.pi / 4)
    r = np.sin((pan + 1) * np.pi / 4)
    if sig.ndim == 1:
        buf[i:i + len(sig), 0] += sig * gain * l * 1.414
        buf[i:i + len(sig), 1] += sig * gain * r * 1.414
    else:
        buf[i:i + len(sig)] += sig * gain


def saw(f, t):
    return 2 * ((f * t) % 1) - 1


# ───────────────────────── Música ─────────────────────────
def pad(notes, dur, vol=0.12):
    t = t_arr(dur)
    s = np.zeros_like(t)
    for n in notes:
        f = nf(n)
        for det in (-0.004, 0, 0.004):
            s += saw(f * (1 + det), t + rng.random())
    s = fft_filter(s, hi=1400) * env_adsr(len(t), a=0.9, d=0.5, s=0.9, r=0.9)
    return s * vol / len(notes)


def piano(note, dur=2.2, vol=0.18):
    t = t_arr(dur)
    f = nf(note)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 2.6)
         + 0.45 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 4)
         + 0.2 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 6)
         + 0.08 * np.sin(2 * np.pi * 4.01 * f * t) * np.exp(-t * 9))
    s *= np.minimum(1, t / 0.004)
    return s * vol


def pluck(note, vol=0.1):
    t = t_arr(0.5)
    f = nf(note)
    s = (np.sin(2 * np.pi * f * t) + 0.5 * np.sign(np.sin(2 * np.pi * f * t)) * 0.3) * np.exp(-t * 9)
    return fft_filter(s, hi=3500) * vol


def kick(vol=0.55):
    t = t_arr(0.45)
    f = 45 + 80 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t * 7) + 0.1 * rng.standard_normal(len(t)) * np.exp(-t * 120)) * vol


def clap(vol=0.18):
    t = t_arr(0.25)
    n = rng.standard_normal(len(t))
    e = np.zeros_like(t)
    for d in (0, 0.011, 0.022):
        e += np.exp(-np.clip(t - d, 0, None) * 60) * (t >= d)
    e += 0.6 * np.exp(-t * 18)
    return fft_filter(n * e, lo=900, hi=6000) * vol


def hat(vol=0.05):
    t = t_arr(0.06)
    return fft_filter(rng.standard_normal(len(t)), lo=7000) * np.exp(-t * 70) * vol


def bass(note, dur, vol=0.22):
    t = t_arr(dur)
    f = nf(note)
    s = np.tanh(1.6 * np.sin(2 * np.pi * f * t)) * env_adsr(len(t), a=0.005, d=0.08, s=0.6, r=0.05)
    return s * vol


music = np.zeros((N, 2))
# A: 0-16 melancólico
for i, ch in enumerate([["A3", "C4", "E4"], ["F3", "A3", "C4"], ["C4", "E4", "G4"], ["G3", "B3", "D4"]]):
    place(music, pad(ch, 4.6, 0.10), i * 4.0)
    arp = [ch[0][:-1] + "4", ch[1][:-1] + "4", ch[2][:-1] + "5", ch[1][:-1] + "5"]
    for k in range(8):
        place(music, piano(arp[k % 4], vol=0.09 if k % 2 else 0.12), i * 4.0 + 0.25 + k * 0.5, pan=(-0.3 if k % 2 else 0.3))
# B: 16-23 tensión
place(music, pad(["D4", "F4", "A4"], 3.9, 0.11), 16.0)
place(music, pad(["E3", "G#3", "B3"], 3.9, 0.12), 19.5)
for k in range(int(7.0 / 0.3)):
    tt = 16.0 + k * 0.3
    v = 0.08 + 0.14 * (k / 23)
    place(music, bass("D2" if tt < 19.5 else "E2", 0.25, v), tt)
riser = rng.standard_normal(int(2.0 * SR))
riser = tv_band(riser, np.geomspace(400, 6000, len(riser)), q=2.5) * np.linspace(0, 1, len(riser)) ** 2 * 0.12
place(music, riser, 21.0)
# C: 23-37.4 optimista
prog = [("C", ["C4", "E4", "G4"]), ("G", ["G3", "B3", "D4"]), ("A", ["A3", "C4", "E4"]), ("F", ["F3", "A3", "C4"]),
        ("C", ["C4", "E4", "G4"]), ("G", ["G3", "B3", "D4"])]
beat = 0.6
for i, (root, ch) in enumerate(prog):
    t0 = 23.0 + i * 2.4
    place(music, pad(ch, 2.6, 0.08), t0)
    for b in range(4):
        tb = t0 + b * beat
        place(music, kick(0.42), tb)
        if b % 2 == 1:
            place(music, clap(), tb, pan=0.05)
        for h in range(2):
            place(music, hat(), tb + h * beat / 2, pan=0.4)
            place(music, bass(root + "2", 0.26, 0.2), tb + h * beat / 2)
        tones = [ch[0][:-1] + "5", ch[1][:-1] + "5", ch[2][:-1] + "5", ch[1][:-1] + "6"]
        for h in range(2):
            place(music, pluck(tones[(b * 2 + h) % 4], 0.07), tb + h * beat / 2 + 0.02, pan=(0.35 if h else -0.35))
# D: final
place(music, pad(["C4", "E4", "G4", "C5"], 4.6, 0.12), 37.4)
for k, n in enumerate(["C4", "E4", "G4", "C5"]):
    place(music, piano(n, 3.5, 0.10), 37.4 + k * 0.06)
place(music, kick(0.5), 37.4)
fade = np.ones(N)
fi = int(0.8 * SR)
fade[:fi] = np.linspace(0, 1, fi)
fo0 = int(40.2 * SR)
fade[fo0:] = np.linspace(1, 0, N - fo0)
music *= fade[:, None]

# ───────────────────────── Efectos ─────────────────────────
def whoosh():
    d = 0.9
    n = rng.standard_normal(int(d * SR))
    c = 300 + 3000 * np.sin(np.linspace(0, np.pi, len(n))) ** 2
    s = tv_band(n, c, q=1.2) * np.sin(np.linspace(0, np.pi, len(n))) ** 1.5
    pan = np.linspace(-0.8, 0.8, len(s))
    out = np.stack([s * np.cos((pan + 1) * np.pi / 4), s * np.sin((pan + 1) * np.pi / 4)], 1) * 1.4
    return out * 0.35


def clack():
    t = t_arr(0.12)
    s = (fft_filter(rng.standard_normal(len(t)), lo=2000) * np.exp(-t * 90) * 0.5
         + np.sin(2 * np.pi * 1850 * t) * np.exp(-t * 45) * 0.4 + np.sin(2 * np.pi * 2930 * t) * np.exp(-t * 60) * 0.25)
    return s * 0.5


def pop(f0=880):
    t = t_arr(0.5)
    f = f0 * (1 - 0.3 * np.exp(-t * 40))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 14) + 0.35 * np.sin(2 * np.pi * f0 * 1.5 * t) * np.exp(-t * 6)
    return s * 0.28


def tick():
    t = t_arr(0.03)
    return fft_filter(rng.standard_normal(len(t)), lo=3000) * np.exp(-t * 300) * 0.25


def flush():
    d = 2.4
    t = t_arr(d)
    n = rng.standard_normal(len(t))
    body = fft_filter(n, hi=900) * (0.6 + 0.4 * np.sin(2 * np.pi * (5 + 3 * np.sin(2 * np.pi * 0.7 * t)) * t))
    hiss = fft_filter(rng.standard_normal(len(t)), lo=2500, hi=7000) * 0.12
    e = np.minimum(1, t / 0.35) * np.exp(-np.clip(t - 0.8, 0, None) * 1.6)
    return (body + hiss) * e * 0.45


def sparkle():
    out = np.zeros(int(1.2 * SR))
    for _ in range(28):
        at = rng.random() * 0.9
        f = 2800 + rng.random() * 3500
        t = t_arr(0.12)
        s = np.sin(2 * np.pi * f * t) * np.exp(-t * 40) * (0.04 + 0.05 * rng.random())
        i = int(at * SR)
        out[i:i + len(s)] += s
    return out


def impact():
    t = t_arr(1.6)
    f = 35 + 45 * np.exp(-t * 6)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 2.5) * 0.7 + fft_filter(rng.standard_normal(len(t)), hi=500) * np.exp(-t * 9) * 0.4
    shimmer = fft_filter(rng.standard_normal(len(t)), lo=5000) * np.exp(-t * 3) * 0.06
    return s * 0.6 + shimmer


def bell(f, d=1.6, v=0.15):
    t = t_arr(d)
    s = np.zeros_like(t)
    for ratio, amp, dec in ((1, 1, 2.5), (2.76, 0.4, 4), (5.4, 0.2, 6), (8.93, 0.1, 9)):
        s += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t * dec)
    return s * v * np.minimum(1, t / 0.003)


def ping():
    t = t_arr(0.25)
    s = np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 35) * 0.18
    s[int(0.09 * SR):] += s[: len(s) - int(0.09 * SR)] * 0.3
    return s


def servo(d):
    t = t_arr(d)
    f = 120 + 45 * np.sin(np.pi * t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = (2 * ((ph / (2 * np.pi)) % 1) - 1) * (0.65 + 0.35 * np.sin(2 * np.pi * 34 * t))
    gears = np.zeros_like(t)
    gears[:: int(SR / 48)] = 1
    gears = fft_filter(gears, lo=1500, hi=5000) * 0.6
    s = fft_filter(s, hi=2200) + gears
    e = np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.12)
    return s * e * 0.13


def lock():
    t = t_arr(0.5)
    s = np.zeros_like(t)
    for d in (0, 0.045):
        i = int(d * SR)
        c = fft_filter(rng.standard_normal(int(0.012 * SR)), lo=2500) * 0.6
        s[i:i + len(c)] += c
    s += np.sin(2 * np.pi * 90 * t) * np.exp(-t * 30) * 0.4
    tone = np.zeros_like(t)
    a = t_arr(0.14)
    w = np.sin(2 * np.pi * 660 * a) * np.sin(np.pi * a / 0.14) * 0.12
    i = int(0.12 * SR)
    tone[i:i + len(w)] += w
    b = np.sin(2 * np.pi * 523 * a) * np.sin(np.pi * a / 0.14) * 0.12
    i = int(0.28 * SR)
    tone[i:i + len(b)] += b
    return (s + tone) * 0.6


def step():
    t = t_arr(0.12)
    s = np.sin(2 * np.pi * (85 + 20 * rng.random()) * t) * np.exp(-t * 35) * 0.5
    s += fft_filter(rng.standard_normal(len(t)), lo=1500, hi=5000) * np.exp(-t * 80) * 0.15
    return s * 0.35


sfx = np.zeros((N, 2))
S = SCH["sfx"]
for a in S["whoosh"]:
    place(sfx, whoosh(), a)
for a in S["clack"]:
    place(sfx, clack(), a, pan=0.2)
for i, a in enumerate(S["pop"]):
    place(sfx, pop(880 * 2 ** (i * 4 / 12)), a)
t0, t1 = S["ticks"]
k = 0
tt = t0
while tt < t1:
    place(sfx, tick(), tt, pan=0.1)
    k += 1
    tt += 0.11 - 0.004 * min(k, 15)
for a in S["flush"]:
    place(sfx, flush(), a, gain=0.42)
for a in S["sparkle"]:
    place(sfx, sparkle(), a, pan=-0.2)
for a in S["impact"]:
    place(sfx, impact(), a)
for a in S["ding"]:
    place(sfx, bell(nf("E6"), 1.2, 0.12), a)
for (a, b) in (S["steps_in"], S["steps_out"]):
    x = a
    j = 0
    while x < b:
        place(sfx, step(), x, pan=(0.25 if j % 2 else -0.05))
        x += 0.36
        j += 1
for a in S["ping"]:
    place(sfx, ping(), a, pan=0.15)
for a, b in S["servo"]:
    place(sfx, servo(b - a), a, pan=0.25)
for a in S["lock"]:
    place(sfx, lock(), a)
for a in S["chime"]:
    for j, n in enumerate(["C6", "E6", "G6", "C7"]):
        place(sfx, bell(nf(n), 2.0, 0.11), a + j * 0.11, pan=-0.3 + 0.2 * j)

# ───────────────────────── Relator ─────────────────────────
def read_wav(p):
    with wave.open(p) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(1)
    # re-muestreo lineal a 48 kHz
    tn = np.arange(int(len(x) * SR / sr)) / SR
    return np.interp(tn, np.arange(len(x)) / sr, x)


vdir = sys.argv[1]
vo = np.zeros(N)
for name, at in SCH["vo"].items():
    x = read_wav(os.path.join(vdir, name + ".wav"))
    x = fft_filter(x, lo=80)  # limpia graves
    x = x / (np.abs(x).max() + 1e-9) * 0.75
    i = int(at * SR)
    vo[i:i + len(x)] += x[: N - i]

# Compresión suave del relator
vo = np.tanh(vo * 1.6) / np.tanh(1.6)

# Ducking: baja la música cuando habla el relator
blk = 480
env = np.abs(vo[: N // blk * blk]).reshape(-1, blk).max(1)
act = (env > 0.02).astype(float)
# suaviza: ataque rápido, liberación lenta
sm = np.zeros_like(act)
v = 0
for i, a in enumerate(act):
    v = a if a > v else v * 0.93
    sm[i] = v
duck = 1 - 0.55 * np.repeat(sm, blk)
duck = np.concatenate([duck, np.ones(N - len(duck))])

mix = music * duck[:, None] * 0.9 + sfx * 0.85 + np.stack([vo, vo], 1) * 0.95
peak = np.abs(mix).max()
mix = np.tanh(mix / peak * 1.15) / np.tanh(1.15) * 0.93

out = sys.argv[2]
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
print("OK", out, f"{DUR:.1f}s", "pico previo", round(float(peak), 3))
