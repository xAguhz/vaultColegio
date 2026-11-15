"""Generador mínimo de QR versión 4, modo byte. Nivel M (hasta 62 bytes) o L (hasta 78). Solo usa PIL.
Uso: python3 qr_v4m.py <texto> <salida.png> [escala] [color_oscuro] [color_claro] [M|L]
"""
import sys
from PIL import Image

SIZE = 33  # versión 4
NIVELES = {"M": (18, 2, 64, 0b00), "L": (20, 1, 80, 0b01)}  # ecc por bloque, bloques, datos, bits de formato
ECC_LEN, NUM_BLOCKS, DATA_CW, ECL_BITS = NIVELES["M"]


def nivel(n):
    global ECC_LEN, NUM_BLOCKS, DATA_CW, ECL_BITS
    ECC_LEN, NUM_BLOCKS, DATA_CW, ECL_BITS = NIVELES[n]


def gf_mul(x, y):
    z = 0
    for i in reversed(range(8)):
        z = (z << 1) ^ ((z >> 7) * 0x11D)
        z ^= ((y >> i) & 1) * x
    return z


def rs_divisor(degree):
    res = [0] * (degree - 1) + [1]
    root = 1
    for _ in range(degree):
        for j in range(len(res)):
            res[j] = gf_mul(res[j], root)
            if j + 1 < len(res):
                res[j] ^= res[j + 1]
        root = gf_mul(root, 2)
    return res


def rs_remainder(data, div):
    res = [0] * len(div)
    for b in data:
        f = b ^ res.pop(0)
        res.append(0)
        for i, c in enumerate(div):
            res[i] ^= gf_mul(c, f)
    return res


def encode_data(text):
    data = text.encode("utf-8")
    assert len(data) <= DATA_CW - 2, "demasiado largo para la versión 4"
    bits = []
    def put(v, n):
        bits.extend((v >> i) & 1 for i in reversed(range(n)))
    put(0b0100, 4)
    put(len(data), 8)
    for b in data:
        put(b, 8)
    cap = DATA_CW * 8
    put(0, min(4, cap - len(bits)))
    put(0, (8 - len(bits) % 8) % 8)
    pad = 0xEC
    while len(bits) < cap:
        put(pad, 8)
        pad ^= 0xEC ^ 0x11
    cws = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, cap, 8)]
    div = rs_divisor(ECC_LEN)
    per = DATA_CW // NUM_BLOCKS
    blocks = [cws[i * per:(i + 1) * per] for i in range(NUM_BLOCKS)]
    eccs = [rs_remainder(b, div) for b in blocks]
    out = []
    for i in range(per):
        for b in blocks:
            out.append(b[i])
    for i in range(ECC_LEN):
        for e in eccs:
            out.append(e[i])
    return out


class QR:
    def __init__(self):
        self.m = [[False] * SIZE for _ in range(SIZE)]
        self.f = [[False] * SIZE for _ in range(SIZE)]

    def setf(self, x, y, dark):
        self.m[y][x] = dark
        self.f[y][x] = True

    def function_patterns(self):
        for i in range(SIZE):
            self.setf(6, i, i % 2 == 0)
            self.setf(i, 6, i % 2 == 0)
        for cx, cy in ((3, 3), (SIZE - 4, 3), (3, SIZE - 4)):
            for dy in range(-4, 5):
                for dx in range(-4, 5):
                    x, y = cx + dx, cy + dy
                    if 0 <= x < SIZE and 0 <= y < SIZE:
                        d = max(abs(dx), abs(dy))
                        self.setf(x, y, d not in (2, 4))
        cx = cy = 26  # única alineación de la versión 4
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                self.setf(cx + dx, cy + dy, max(abs(dx), abs(dy)) != 1)
        self.format_bits(0)

    def format_bits(self, mask):
        data = (ECL_BITS << 3) | mask
        rem = data
        for _ in range(10):
            rem = (rem << 1) ^ ((rem >> 9) * 0x537)
        bits = ((data << 10) | rem) ^ 0x5412
        g = lambda i: ((bits >> i) & 1) != 0
        for i in range(6):
            self.setf(8, i, g(i))
        self.setf(8, 7, g(6))
        self.setf(8, 8, g(7))
        self.setf(7, 8, g(8))
        for i in range(9, 15):
            self.setf(14 - i, 8, g(i))
        for i in range(8):
            self.setf(SIZE - 1 - i, 8, g(i))
        for i in range(8, 15):
            self.setf(8, SIZE - 15 + i, g(i))
        self.setf(8, SIZE - 8, True)  # módulo oscuro

    def place(self, cws):
        i, total = 0, len(cws) * 8
        right = SIZE - 1
        while right >= 1:
            if right == 6:
                right = 5
            for vert in range(SIZE):
                for j in range(2):
                    x = right - j
                    up = ((right + 1) & 2) == 0
                    y = SIZE - 1 - vert if up else vert
                    if not self.f[y][x] and i < total:
                        self.m[y][x] = ((cws[i >> 3] >> (7 - (i & 7))) & 1) != 0
                        i += 1
            right -= 2
        assert i == total

    def apply_mask(self, k):
        fn = [lambda x, y: (x + y) % 2 == 0, lambda x, y: y % 2 == 0, lambda x, y: x % 3 == 0,
              lambda x, y: (x + y) % 3 == 0, lambda x, y: (x // 3 + y // 2) % 2 == 0,
              lambda x, y: x * y % 2 + x * y % 3 == 0, lambda x, y: (x * y % 2 + x * y % 3) % 2 == 0,
              lambda x, y: ((x + y) % 2 + x * y % 3) % 2 == 0][k]
        for y in range(SIZE):
            for x in range(SIZE):
                if not self.f[y][x] and fn(x, y):
                    self.m[y][x] = not self.m[y][x]

    def penalty(self):
        p, m = 0, self.m
        for lines in (m, list(map(list, zip(*m)))):
            for row in lines:
                run, prev = 0, None
                for v in row:
                    if v == prev:
                        run += 1
                    else:
                        if run >= 5:
                            p += run - 2
                        run, prev = 1, v
                if run >= 5:
                    p += run - 2
                s = "".join("1" if v else "0" for v in row)
                p += 40 * (s.count("1011101" + "0000") + s.count("0000" + "1011101"))
        for y in range(SIZE - 1):
            for x in range(SIZE - 1):
                if m[y][x] == m[y][x + 1] == m[y + 1][x] == m[y + 1][x + 1]:
                    p += 3
        dark = sum(map(sum, m))
        p += 10 * (abs(dark * 20 - SIZE * SIZE * 10) // (SIZE * SIZE))
        return p


def make(text):
    cws = encode_data(text)
    best = None
    for k in range(8):
        q = QR()
        q.function_patterns()
        q.place(cws)
        q.apply_mask(k)
        q.format_bits(k)
        pen = q.penalty()
        if best is None or pen < best[0]:
            best = (pen, q)
    return best[1]


def render(q, path, scale=20, dark="#000000", light="#FFFFFF", border=4):
    n = (SIZE + 2 * border) * scale
    img = Image.new("RGB", (n, n), light)
    px = img.load()
    dc = tuple(int(dark[i:i + 2], 16) for i in (1, 3, 5))
    for y in range(SIZE):
        for x in range(SIZE):
            if q.m[y][x]:
                for yy in range((y + border) * scale, (y + border + 1) * scale):
                    for xx in range((x + border) * scale, (x + border + 1) * scale):
                        px[xx, yy] = dc
    img.save(path)


if __name__ == "__main__":
    a = sys.argv
    nivel(a[6] if len(a) > 6 else "M")
    render(make(a[1]), a[2], int(a[3]) if len(a) > 3 else 20,
           a[4] if len(a) > 4 else "#000000", a[5] if len(a) > 5 else "#FFFFFF")
