import math, numpy as np, cv2
from PIL import ImageDraw
from icons import leer, fertig, schrift, D

C = D / 2

def werkstatt():
    """W aus einem gefalteten Papierstreifen: vier Flächen, abwechselnd Vorder-/Rückseite."""
    a, b = leer(), leer(); da, db = ImageDraw.Draw(a), ImageDraw.Draw(b)
    P = [(330, 520), (700, 1530), (1024, 820), (1348, 1530), (1718, 520)]
    w = 300
    for i in range(4):
        (x0, y0), (x1, y1) = P[i], P[i + 1]
        poly = [(x0 - w / 2, y0), (x0 + w / 2, y0), (x1 + w / 2, y1), (x1 - w / 2, y1)]
        (da if i % 2 == 0 else db).polygon(poly, fill=255)
    return {'a': fertig(a), 'b': fertig(b)}

def setzkasten():
    """Werkstatt-Alternative: Setzkasten 3×3 mit Mini-Zeichen der Apps."""
    a, b = leer(), leer(); da, db = ImageDraw.Draw(a), ImageDraw.Draw(b)
    x0, y0, n, s, g = 300, 300, 3, 1448 / 3, 46
    da.rounded_rectangle([x0, y0, x0 + 1448, y0 + 1448], 70, fill=255)
    for r in range(n):
        for c in range(n):
            xa, ya = x0 + c * s + g / 2 + 18, y0 + r * s + g / 2 + 18
            da.rounded_rectangle([xa, ya, xa + s - g - 36, ya + s - g - 36], 34, fill=0)
    f = schrift(250)
    zeichen = ['◩', 'Aa', '+', '◎', '✶', '♥', '△', '1', '✉']
    zeichen = ['A', 'a', '+', 'O', '*', 'W', 'M', '1', '=']
    for i, z in enumerate(zeichen):
        r, c = divmod(i, 3)
        cx, cy = x0 + c * s + s / 2, y0 + r * s + s / 2
        if i == 4:
            db.rounded_rectangle([cx - 150, cy - 150, cx + 150, cy + 150], 40, fill=255)
        else:
            db.text((cx, cy + 10), z, font=f, fill=255, anchor='mm')
    return {'a': fertig(a), 'b': fertig(b)}

def abwickler():
    """Versetztes Würfelnetz – Falzlinien bleiben als Papier stehen, Klebelaschen in Farbe 2."""
    a, b = leer(), leer(); da, db = ImageDraw.Draw(a), ImageDraw.Draw(b)
    s, g = 400, 30
    ox, oy = C - 2 * s, C - 1.5 * s
    felder = [(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (2, 2)]
    for dx, dy in felder:
        x, y = ox + dx * s, oy + dy * s
        da.rounded_rectangle([x + g / 2, y + g / 2, x + s - g / 2, y + s - g / 2], 18, fill=255)
    t = 100; e = 18
    def lasche(dx, dy, seite):
        x, y = ox + dx * s + g / 2, oy + dy * s + g / 2; k = s - g
        q = k * 0.2
        if seite == 'l':
            db.polygon([(x - e, y), (x - e - t, y + q), (x - e - t, y + k - q), (x - e, y + k)], fill=255)
        if seite == 'r':
            db.polygon([(x + k + e, y), (x + k + e + t, y + q), (x + k + e + t, y + k - q), (x + k + e, y + k)], fill=255)
        if seite == 'o':
            db.polygon([(x, y - e), (x + q, y - e - t), (x + k - q, y - e - t), (x + k, y - e)], fill=255)
        if seite == 'u':
            db.polygon([(x, y + k + e), (x + q, y + k + e + t), (x + k - q, y + k + e + t), (x + k, y + k + e)], fill=255)
    return {'a': fertig(a), 'b': fertig(b)}

def modellgenerator():
    """Isometrischer Körper: drei Flächen, oben Farbe 2."""
    a, b, c = leer(), leer(), leer()
    r = 760; cx, cy = C, C + 40
    def pt(ang, rr=r):
        return (cx + rr * math.cos(math.radians(ang)), cy + rr * math.sin(math.radians(ang)))
    top = [pt(-90), pt(-30), (cx, cy), pt(-150)]
    links = [pt(-150), (cx, cy), pt(90), pt(150)]
    rechts = [(cx, cy), pt(-30), pt(30), pt(90)]
    g = 22
    def schrumpf(poly):
        mx = sum(p[0] for p in poly) / 4; my = sum(p[1] for p in poly) / 4
        return [(mx + (x - mx) * (1 - g / 380), my + (y - my) * (1 - g / 380)) for x, y in poly]
    ImageDraw.Draw(b).polygon(schrumpf(top), fill=255)
    ImageDraw.Draw(a).polygon(schrumpf(links), fill=255)
    ImageDraw.Draw(c).polygon(schrumpf(rechts), fill=255)
    return {'a': fertig(a), 'b': fertig(b), 'a2': fertig(c)}

def outliner():
    """Dreiliniger Halbkreis über einer dreisträngigen Linie."""
    a, b = leer(), leer()
    st, lu = 74, 58            # Strichstärke, Lücke
    cx, cy = C, 1150           # Mittelpunkt des Bogens
    R = 760
    am = np.zeros((D, D), np.float32)
    for i in range(3):
        r = R - i * (st + lu)
        cv2.ellipse(am, (int(cx), int(cy)), (int(r - st / 2), int(r - st / 2)), 0, 180, 360, 1.0, int(st), cv2.LINE_AA)
    # Enden gerade abschneiden auf Höhe cy
    am[int(cy):, :] = 0
    bm = np.zeros((D, D), np.float32)
    y0 = cy + 150
    for i in range(3):
        y = int(y0 + i * (st + lu) + st / 2)
        cv2.line(bm, (int(cx - R), y), (int(cx + R), y), 1.0, int(st), cv2.LINE_AA)
    return {'a': am, 'b': bm}

def herz(d, cx, cy, s, fill):
    # Herz aus zwei Kreisen + Dreieck
    r = s * 0.3
    d.ellipse([cx - 2 * r, cy - r * 1.4, cx, cy + r * 0.6], fill=fill)
    d.ellipse([cx, cy - r * 1.4, cx + 2 * r, cy + r * 0.6], fill=fill)
    d.polygon([(cx - 1.93 * r, cy - 0.1 * r), (cx + 1.93 * r, cy - 0.1 * r), (cx, cy + 1.9 * r)], fill=fill)

def hochzeitskarten():
    """Leicht aufgeklapptes Heft: Rückseite schaut rechts heraus, Herz auf dem Deckblatt."""
    a, b = leer(), leer(); da, db = ImageDraw.Draw(a), ImageDraw.Draw(b)
    x0, y0, x1, y1 = 470, 300, 1600, 1750          # Rückseite / Seiten
    db.rounded_rectangle([x0, y0, x1, y1], 26, fill=255)
    # Deckblatt um den Rücken links gedreht: rechte Kante kommt näher -> etwas höher, etwas nach links
    xr = x1 - 150; dy = 55
    da.polygon([(x0, y0), (xr, y0 - dy), (xr, y1 + dy), (x0, y1)], fill=255)
    # Spalt zwischen Deckblatt und Seiten als Papierlinie
    da.line([(xr + 4, y0 - dy), (xr + 4, y1 + dy)], fill=0, width=0)
    herz(da, (x0 + xr) / 2, (y0 + y1) / 2 - 40, 560, 0)
    am, bm = fertig(a), fertig(b)
    bm = np.clip(bm - cv2.dilate(am, np.ones((41, 41), np.uint8)), 0, 1)
    return {'a': am, 'b': bm}

def rechtschreib():
    """„Aa" in Jost, darunter die rote Schlängellinie der Rechtschreibprüfung."""
    a, b = leer(), leer(); da, db = ImageDraw.Draw(a), ImageDraw.Draw(b)
    da.text((C, C - 120), 'Aa', font=schrift(1080), fill=255, anchor='mm')
    pts = []
    for i in range(0, 1301, 6):
        x = 374 + i; y = 1560 + math.sin(i / 1300 * math.pi * 6) * 70
        pts.append((x, y))
    db.line(pts, fill=255, width=78, joint='curve')
    for p in (pts[0], pts[-1]):
        db.ellipse([p[0] - 39, p[1] - 39, p[0] + 39, p[1] + 39], fill=255)
    return {'a': fertig(a), 'b': fertig(b)}

def rechnen():
    """Vier Rechenzeichen im Quadrat, diagonal in zwei Farben."""
    a, b = leer(), leer(); da, db = ImageDraw.Draw(a), ImageDraw.Draw(b)
    off, L, st = 440, 520, 150
    def plus(d, cx, cy, rot=False):
        if not rot:
            d.rounded_rectangle([cx - L / 2, cy - st / 2, cx + L / 2, cy + st / 2], 40, fill=255)
            d.rounded_rectangle([cx - st / 2, cy - L / 2, cx + st / 2, cy + L / 2], 40, fill=255)
        else:
            for ang in (45, -45):
                ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
                hw, hh = L / 2, st / 2
                pts = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]]
                d.polygon(pts, fill=255)
    plus(da, C - off, C - off)                                   # +
    db.rounded_rectangle([C + off - L / 2, C - off - st / 2, C + off + L / 2, C - off + st / 2], 40, fill=255)  # −
    plus(db, C - off, C + off, rot=True)                         # ×
    for dy in (-125, 125):                                       # =
        da.rounded_rectangle([C + off - L / 2, C + off + dy - st / 2, C + off + L / 2, C + off + dy + st / 2], 40, fill=255)
    return {'a': fertig(a), 'b': fertig(b)}

def weihnachten():
    """Faltstern aus zwei gedrehten Quadraten, Mitte als Kreis in Farbe 2."""
    a, b = leer(), leer(); da, db = ImageDraw.Draw(a), ImageDraw.Draw(b)
    r = 800
    for rot in (0, 45):
        pts = [(C + r * math.cos(math.radians(rot + 45 + 90 * i)), C + r * math.sin(math.radians(rot + 45 + 90 * i))) for i in range(4)]
        da.polygon(pts, fill=255)
    m = np.asarray(a, np.float32) / 255
    # Falzlinien: Strahlen aus der Mitte zu den 8 Spitzen und Einbuchtungen als Papierlinien
    fl = np.zeros((D, D), np.uint8)
    for i in range(16):
        rr = r * 1.42 if i % 2 == 0 else r * 1.42
        ang = math.radians(i * 22.5 + (0 if True else 0))
        cv2.line(fl, (int(C), int(C)), (int(C + rr * math.cos(ang)), int(C + rr * math.sin(ang))), 255, 34, cv2.LINE_AA)
    m = m * (1 - fl / 255)
    db.ellipse([C - 230, C - 230, C + 230, C + 230], fill=255)
    m = m * (1 - np.asarray(b, np.float32) / 255 * 0)  # Kreis liegt drüber
    return {'a': m.astype(np.float32), 'b': fertig(b)}

def zuzweit():
    """Zwei Häkchen hintereinander: eins voll, eins im hellen Ton – erledigt, zu zweit."""
    a, b = leer(), leer(); da, db = ImageDraw.Draw(a), ImageDraw.Draw(b)
    def haken(d, dx, dy):
        pts = [(470 + dx, 1050 + dy), (790 + dx, 1370 + dy), (1420 + dx, 740 + dy)]
        d.line(pts, fill=255, width=210, joint='curve')
        for x, y in (pts[0], pts[2]):
            d.ellipse([x - 105, y - 105, x + 105, y + 105], fill=255)
    haken(db, 230, -330)
    haken(da, -40, 200)
    am, bm = fertig(a), fertig(b)
    bm = np.clip(bm - cv2.dilate(am, np.ones((45, 45), np.uint8)), 0, 1)
    return {'a': am, 'b': bm}

MOTIVE = [
    ('Werkstatt', werkstatt, 'WERKSTATT'),
    ('Abwickler', abwickler, 'FALTEN'),
    ('Modellgenerator', modellgenerator, 'MODELL'),
    ('In And Out Liner', outliner, 'LINER'),
    ('Hochzeitskarten', hochzeitskarten, 'KARTEN'),
    ('Rechtschreibfreunde', rechtschreib, 'WÖRTER'),
    ('Rechenfreunde', rechnen, 'RECHNEN'),
    ('Weihnachten', weihnachten, 'FEST'),
    ('Zu zweit', zuzweit, 'ZWEIT'),
]


# ---------- Werkstatt-Optionen (mehrfarbig: Liste aus (Maske, Farbe, Ton)) ----------
def _knock(m, k):
    return np.clip(m - cv2.dilate(k, np.ones((3, 3), np.uint8)), 0, 1)

def halle():
    """Werkhalle mit Sägezahndach: drei Dachzähne = drei Gruppen (Plotten, Kinder, Fest)."""
    x0, x1, yb, yt, yd = 280, 1768, 1010, 470, 1740
    w = (x1 - x0) / 3; g = 30
    zaehne = []
    for i, f in enumerate(('blau', 'rot', 'gruen')):
        im = leer(); d = ImageDraw.Draw(im)
        xl, xr = x0 + i * w, x0 + (i + 1) * w
        d.polygon([(xl + g / 2, yb - g / 2), (xl + g / 2, yt), (xr - g / 2, yb - g / 2)], fill=255)
        zaehne.append((fertig(im), f, 1.0))
    body = leer(); d = ImageDraw.Draw(body)
    d.rectangle([x0 + g / 2, yb + g / 2, x1 - g / 2, yd], fill=255)
    # Tor in der Mitte, Fenster links und rechts
    d.rounded_rectangle([C - 190, 1280, C + 190, yd + 10], 30, fill=0)
    for cx in (x0 + w / 2, x1 - w / 2):
        for j in range(2):
            for k in range(2):
                xa = cx - 150 + k * 165; ya = 1170 + j * 220
                d.rounded_rectangle([xa, ya, xa + 135, ya + 190], 16, fill=0)
    return zaehne + [(fertig(body), 'schwarz', 1.0)]

def setzkasten():
    """Setzkasten 3×3: jedes Fach ein Stück aus der Werkstatt, in den Gruppenfarben."""
    x0, n, B, rand, steg = 270, 3, 1508, 64, 44
    rahmen = leer(); d = ImageDraw.Draw(rahmen)
    d.rounded_rectangle([x0, x0, x0 + B, x0 + B], 60, fill=255)
    f = (B - 2 * rand - (n - 1) * steg) / n
    zellen = []
    for r in range(n):
        for c in range(n):
            xa = x0 + rand + c * (f + steg); ya = x0 + rand + r * (f + steg)
            d.rounded_rectangle([xa, ya, xa + f, ya + f], 26, fill=0)
            zellen.append((xa + f / 2, ya + f / 2))
    teile = []
    def neu():
        im = leer(); return im, ImageDraw.Draw(im)
    s = f * 0.30
    plan = [('blau', 'quadrat'), (None, None), ('rot', 'kreis'),
            ('gruen', 'stern'), ('blau', 'herz'), ('rot', 'plus'),
            ('rot', 'dreieck'), ('gruen', 'halb'), ('blau', 'raute')]
    for (cx, cy), (farbe, form) in zip(zellen, plan):
        if not farbe:
            continue
        im, dd = neu()
        if form == 'quadrat': dd.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], 18, fill=255)
        if form == 'kreis': dd.ellipse([cx - s * 1.1, cy - s * 1.1, cx + s * 1.1, cy + s * 1.1], fill=255)
        if form == 'raute': dd.polygon([(cx, cy - s * 1.3), (cx + s * 1.3, cy), (cx, cy + s * 1.3), (cx - s * 1.3, cy)], fill=255)
        if form == 'dreieck': dd.polygon([(cx, cy - s * 1.25), (cx + s * 1.25, cy + s * 0.95), (cx - s * 1.25, cy + s * 0.95)], fill=255)
        if form == 'halb': dd.pieslice([cx - s * 1.3, cy - s * 0.9, cx + s * 1.3, cy + s * 1.7], 180, 360, fill=255)
        if form == 'plus':
            dd.rounded_rectangle([cx - s * 1.2, cy - s * 0.38, cx + s * 1.2, cy + s * 0.38], 14, fill=255)
            dd.rounded_rectangle([cx - s * 0.38, cy - s * 1.2, cx + s * 0.38, cy + s * 1.2], 14, fill=255)
        if form == 'herz': herz(dd, cx, cy - s * 0.15, s * 2.3, 255)
        if form == 'stern':
            pts = []
            for i in range(10):
                rr = s * 1.3 if i % 2 == 0 else s * 0.55
                ang = math.radians(-90 + i * 36)
                pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
            dd.polygon(pts, fill=255)
        teile.append((fertig(im), farbe, 1.0))
    return [(fertig(rahmen), 'schwarz', 1.0)] + teile

def faltspiel():
    """Himmel und Hölle von oben: vier Klappen in den Gruppenfarben, je mit Mittelfalz."""
    R = 760; g = 34
    ecken = [(C - R, C - R), (C + R, C - R), (C + R, C + R), (C - R, C + R)]
    out = []
    farben = ['schwarz', 'blau', 'rot', 'gruen']
    for i in range(4):
        p, q = ecken[i], ecken[(i + 1) % 4]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        for half, ton in ((0, 1.0), (1, 0.62)):
            im = leer(); d = ImageDraw.Draw(im)
            tri = [(C, C), p, (mx, my)] if half == 0 else [(C, C), (mx, my), q]
            d.polygon(tri, fill=255)
            mk = fertig(im)
            out.append([mk, farbe := farben[i], ton])
    # Falzlinien (Diagonalen + Mittelfalze) als Papier
    fl = np.zeros((D, D), np.uint8)
    for p in ecken:
        cv2.line(fl, (int(C), int(C)), (int(p[0]), int(p[1])), 255, g, cv2.LINE_AA)
    for i in range(4):
        p, q = ecken[i], ecken[(i + 1) % 4]
        cv2.line(fl, (int(C), int(C)), (int((p[0] + q[0]) / 2), int((p[1] + q[1]) / 2)), 255, int(g * 0.6), cv2.LINE_AA)
    fl = fl.astype(np.float32) / 255
    rund = leer(); ImageDraw.Draw(rund).rounded_rectangle([C - R, C - R, C + R, C + R], 70, fill=255)
    rund = fertig(rund)
    res = []
    M = cv2.getRotationMatrix2D((C, C), 45, 0.72)
    for mk, f, t in out:
        mm = np.clip(mk * rund - fl, 0, 1)
        res.append((cv2.warpAffine(mm, M, (D, D), flags=cv2.INTER_LINEAR), f, t))
    return res

WERKSTATT_OPTIONEN = [('Werkhalle', halle), ('Setzkasten', setzkasten), ('Himmel und Hölle', faltspiel)]
