"""Corta la narración de ElevenLabs en las 11 líneas del guion y las ajusta a su ventana de tiempo.
Uso: python3 split_vo.py <entrada.mp3> <dir_salida> <schedule.json>"""
import json, subprocess, sys, wave, os
import numpy as np

SRC, OUT, SCHF = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
SR = 44100
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768

# Tramos de voz (de silencedetect, -38 dB): (inicio, fin)
S = [(0.00, 3.545), (3.938, 5.078), (5.615, 9.037), (9.524, 12.354), (12.783, 16.674), (17.224, 17.750),
     (18.124, 20.645), (20.930, 22.965), (23.460, 24.850), (25.270, 27.008), (27.410, 29.484), (29.850, 30.475),
     (30.731, 31.584), (31.937, 32.371), (32.687, 33.314), (33.727, 34.325), (34.651, 37.280)]
# Línea -> (tramos, inicio en el video, fin máximo, pausa interna máxima)
LINES = {
    "vo1": ([0, 1], 0.50, 5.62, None),
    "vo2a": ([2], 6.38, 9.86, None),
    "vo2b": ([3], 9.90, 12.80, None),
    "vo2c": ([4], 12.85, 16.72, None),
    "vo3": ([5, 6, 7], 17.25, 22.65, 0.22),
    "vo4a": ([8], 23.30, 25.30, None),
    "vo4b": ([9], 25.40, 27.80, None),
    "vo4c": ([10], 28.00, 30.70, None),
    "vo4d": ([11, 12], 30.80, 32.80, None),
    "vo4e": ([13, 14], 32.90, 35.20, None),
    "vo5": ([15, 16], 36.60, 40.60, None),
}
PRE, POST = 0.04, 0.10


def seg(a, b):
    return x[max(0, int((a - PRE) * SR)): min(len(x), int((b + POST) * SR))]


sch = json.load(open(SCHF))
rep = []
for name, (idx, start, end_max, max_gap) in LINES.items():
    parts = []
    for k, i in enumerate(idx):
        a, b = S[i]
        if k > 0:
            gap = a - S[idx[k - 1]][1]
            keep = min(gap, max_gap) if max_gap else gap
            parts.append(np.zeros(int(max(0.0, keep - PRE - POST) * SR)))
        parts.append(seg(a, b))
    y = np.concatenate(parts)
    tmp = os.path.join(OUT, name + "_raw.wav")
    with wave.open(tmp, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    dur = len(y) / SR
    tempo = max(1.0, dur / (end_max - start))
    dst = os.path.join(OUT, name + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"atempo={tempo:.4f}", dst], check=True)
    os.remove(tmp)
    sch["vo"][name] = start
    rep.append(f"{name}: {dur:.2f}s -> {dur / tempo:.2f}s (x{tempo:.3f}) en {start:.2f}-{start + dur / tempo:.2f}")
json.dump(sch, open(SCHF, "w"), indent=2, ensure_ascii=False)
print("\n".join(rep))
