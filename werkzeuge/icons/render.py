import sys, os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from icons import papier, rau, tinte, drucken, raster, platziere, JOST, S
from motive import MOTIVE

OUT = os.environ.get('OUT', 'out')
os.makedirs(OUT, exist_ok=True)

SCHWARZ = (44, 41, 39)
BLAU_FB = (52, 74, 182)      # Fernbedienung
ROT = (192, 42, 52)
GRUEN = (34, 110, 82)
BLAU_WW = (33, 108, 174)     # Weiter Writer
PINK = (255, 74, 160)

GRUPPE = {'Werkstatt': SCHWARZ, 'Abwickler': BLAU_FB, 'Modellgenerator': BLAU_FB, 'In And Out Liner': BLAU_FB,
          'Hochzeitskarten': BLAU_FB, 'Rechtschreibfreunde': ROT, 'Rechenfreunde': ROT, 'Weihnachten': GRUEN}

def lagen(motiv, skala, cx, cy):
    return {k: platziere(v, skala, cx, cy) for k, v in motiv.items()}

def stempel(name, motiv, seed):
    img = papier(seed)
    L = lagen(motiv, 0.80, S / 2, S / 2)
    farbe = GRUPPE[name]
    ton = {'a': 1.0, 'a2': 0.66, 'b': 0.42}
    if name == 'Werkstatt':
        ton['b'] = 0.5
    if name == 'In And Out Liner':
        ton['b'] = 1.0
    for k in ('b', 'a2', 'a'):
        if k in L:
            img = drucken(img, tinte(rau(L[k], seed + len(k)), seed + ord(k[0]), ton[k]), farbe)
    return img

def riso(name, motiv, seed):
    img = papier(seed)
    yy, xx = np.mgrid[0:S, 0:S]
    kreis = (((xx - S / 2) ** 2 + (yy - S / 2) ** 2) < 345 ** 2).astype(np.float32)
    L = lagen(motiv, 0.56, S / 2, S / 2)
    aus = np.clip(L['a'] + L.get('a2', 0), 0, 1)
    blau = np.clip(kreis - rau(aus, seed, 2), 0, 1)
    img = drucken(img, tinte(rau(blau, seed + 1, 3), seed + 2), BLAU_WW)
    pink = np.roll(np.roll(rau(L['b'], seed + 3), 12, axis=1), 9, axis=0)
    img = drucken(img, tinte(pink, seed + 4, 0.9), PINK)
    return img

def gerastert(name, motiv, seed, label):
    img = papier(seed)
    L = lagen(motiv, 0.60, S / 2, 400)
    alles = np.clip(sum(L.values()), 0, 1)
    echo = cv2.dilate(alles, np.ones((25, 25), np.uint8))
    echo = np.roll(np.roll(echo, -46, axis=1), -34, axis=0)
    r = raster(rau(echo, seed), seed + 3, 18, (1, 0.6))
    img = drucken(img, tinte(r, seed + 5), SCHWARZ)
    ton = {'a': 1.0, 'a2': 0.78, 'b': 0.5}
    for k in ('b', 'a2', 'a'):
        if k in L:
            img = drucken(img, tinte(rau(L[k], seed + 6 + len(k)), seed + 7, ton[k]), SCHWARZ)
    # Wortmarke wie „BELEG"
    t = Image.new('L', (S, S), 0); d = ImageDraw.Draw(t)
    px = 190
    while True:
        f = ImageFont.truetype(JOST, px)
        x0, y0, x1, y1 = d.textbbox((0, 0), label, font=f)
        if x1 - x0 <= 680 or px < 60:
            break
        px -= 4
    # Laufweite wie bei BELEG
    sp = px * 0.12
    breite = sum(d.textlength(c, font=f) for c in label) + sp * (len(label) - 1)
    x = S / 2 - breite / 2
    for c in label:
        d.text((x, 800), c, font=f, fill=255, anchor='lm')
        x += d.textlength(c, font=f) + sp
    m = np.asarray(t, np.float32) / 255
    img = drucken(img, tinte(rau(m, seed + 8, 2), seed + 9), SCHWARZ)
    return img

RICHTUNGEN = [('A', 'Stempel', stempel), ('B', 'Riso-Doppel', riso), ('C', 'Raster', gerastert)]

if __name__ == '__main__':
    nur = sys.argv[1:]  # optional: Motivnamen
    for i, (name, fn, label) in enumerate(MOTIVE):
        if nur and name not in nur:
            continue
        motiv = fn()
        for kz, rname, rf in RICHTUNGEN:
            seed = 11 + i * 7
            img = rf(name, motiv, seed, label) if rf is gerastert else rf(name, motiv, seed)
            out = np.clip(img, 0, 255).astype(np.uint8)
            Image.fromarray(out).save(f'{OUT}/{kz}_{name.replace(" ", "")}.png')
        print('ok', name, flush=True)
