import math, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

import os
JOST = os.environ.get('JOST', os.path.expanduser('~/Desktop/APPs/fernbedienung/Fernbedienung/Resources/Jost-Bold.ttf'))
D = 2048          # Zeichenfläche für Motive (Design-Box = ganze Fläche)
S = 1024          # Ausgabegröße

# ---------- Papier ----------
def papier(seed, ton=(236, 232, 221)):
    rng = np.random.default_rng(seed)
    img = np.ones((S, S, 3), np.float32) * np.array(ton, np.float32)
    grob = cv2.GaussianBlur(rng.normal(0, 1, (S, S)).astype(np.float32), (0, 0), 70); grob /= grob.std() + 1e-6
    mittel = cv2.GaussianBlur(rng.normal(0, 1, (S, S)).astype(np.float32), (0, 0), 6); mittel /= mittel.std() + 1e-6
    fein = rng.normal(0, 1, (S, S)).astype(np.float32)
    img -= (grob * 3.2 + mittel * 1.2 + fein * 1.6)[:, :, None]
    # Knick: leicht geschwungene Linie, oben links
    knick = np.zeros((S, S), np.float32)
    x0 = rng.uniform(330, 430); laenge = rng.uniform(0.5, 0.7); dx = rng.uniform(200, 300); bog = rng.uniform(-25, 25)
    pts = []
    for t in np.linspace(0, 1, 60):
        y = t * S * laenge
        x = x0 - t * dx + math.sin(t * math.pi) * bog
        pts.append((x, y))
    pts = np.array(pts, np.int32)
    cv2.polylines(knick, [pts], False, 1.0, 3, cv2.LINE_AA)
    hell = cv2.GaussianBlur(knick, (0, 0), 2.5)
    dunkel = cv2.GaussianBlur(np.roll(knick, 5, axis=1), (0, 0), 5)
    img += (hell * 13)[:, :, None]; img -= (dunkel * 14)[:, :, None]
    return np.clip(img, 0, 255)

# ---------- Druckfarbe ----------
def rau(mask, seed, rund=5):
    """Kanten leicht weich/organisch, Ecken minimal gerundet (wie Jost-Stempel)."""
    rng = np.random.default_rng(seed)
    m = cv2.GaussianBlur(mask, (0, 0), rund)
    n = cv2.GaussianBlur(rng.normal(0, 1, mask.shape).astype(np.float32), (0, 0), 1.5) * 0.06
    return np.clip((m + n - 0.5) * 6 + 0.5, 0, 1)

def tinte(mask, seed, deckung=1.0):
    rng = np.random.default_rng(seed + 99)
    h, w = mask.shape
    fleck = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 18); fleck /= fleck.std() + 1e-6
    a = mask * np.clip(0.9 + fleck * 0.07, 0.72, 1.0) * deckung
    # Sprenkel: kurze helle Striche
    kratz = np.zeros((h, w), np.float32)
    ys, xs = np.nonzero(mask > 0.5)
    if len(xs):
        k = min(len(xs) // 260, 900)
        idx = rng.choice(len(xs), k, replace=False)
        for i in idx:
            L = rng.uniform(2, 9); ang = rng.uniform(0, math.pi)
            x, y = xs[i], ys[i]
            cv2.line(kratz, (int(x), int(y)), (int(x + L * math.cos(ang)), int(y + L * math.sin(ang))), 1.0, 1, cv2.LINE_AA)
    a *= 1 - np.clip(kratz, 0, 1) * 0.75
    return np.clip(a, 0, 1)

def drucken(bild, alpha, farbe):
    f = np.array(farbe, np.float32) / 255
    return bild * (1 - alpha[:, :, None] * (1 - f))

# ---------- Raster (Beleg-Look) ----------
def raster(mask, seed, zelle=22, richtung=(1, 0.35)):
    rng = np.random.default_rng(seed + 7)
    h, w = mask.shape
    weich = cv2.GaussianBlur(mask, (0, 0), 26)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ys, xs = np.nonzero(mask > 0.5)
    if not len(xs):
        return np.zeros_like(mask)
    proj = (xx * richtung[0] + yy * richtung[1])
    p0, p1 = (proj[ys, xs].min(), proj[ys, xs].max())
    verlauf = 1 - np.clip((proj - p0) / max(p1 - p0, 1), 0, 1) * 0.85
    dichte = np.clip(weich * 1.6, 0, 1) * verlauf
    out = np.zeros_like(mask)
    for cy in range(zelle // 2, h, zelle):
        for cx in range(zelle // 2, w, zelle):
            v = dichte[cy, cx]
            if v < 0.04 or rng.random() > v ** 0.6:
                continue
            s = zelle * (0.45 + 0.5 * v) * rng.uniform(0.85, 1.05)
            jx, jy = rng.uniform(-1.5, 1.5, 2)
            x0, y0 = int(cx - s / 2 + jx), int(cy - s / 2 + jy)
            out[y0:y0 + int(s), x0:x0 + int(s)] = 1
    return out

# ---------- Motiv-Helfer ----------
def leer():
    return Image.new('L', (D, D), 0)

def fertig(im):
    return np.asarray(im, np.float32) / 255

def schrift(px):
    return ImageFont.truetype(JOST, px)

def text_mitte(dr, txt, cx, cy, px):
    f = schrift(px)
    dr.text((cx, cy), txt, font=f, fill=255, anchor='mm')

def platziere(m, skala, cx, cy):
    """Motiv (D×D) auf S×S setzen: skala = Anteil der Ausgabebreite, cx/cy in Ausgabe-px."""
    k = S * skala / D
    M = np.array([[k, 0, cx - D * k / 2], [0, k, cy - D * k / 2]], np.float32)
    return cv2.warpAffine(m, M, (S, S), flags=cv2.INTER_AREA)
