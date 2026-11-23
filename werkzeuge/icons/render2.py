import numpy as np
from PIL import Image, ImageDraw, ImageFont
from icons import papier, rau, tinte, drucken, platziere, JOST, S
from motive import MOTIVE, WERKSTATT_OPTIONEN
from render import stempel, SCHWARZ, BLAU_FB, ROT, GRUEN, OUT
from board import squircle

FARBE = {'schwarz': SCHWARZ, 'blau': BLAU_FB, 'rot': ROT, 'gruen': GRUEN}

def mehrfarbig(lagen, seed, skala=0.80):
    img = papier(seed)
    for i, (m, f, t) in enumerate(lagen):
        mm = platziere(m, skala, S / 2, S / 2)
        img = drucken(img, tinte(rau(mm, seed + i), seed + 31 * i, t), FARBE[f])
    return img

def speichern(img, pfad):
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(pfad)

if __name__ == '__main__':
    for i, (name, fn, _) in enumerate(MOTIVE):
        if name == 'Werkstatt':
            continue
        speichern(stempel(name, fn(), 11 + i * 7), f'{OUT}/A_{name.replace(" ", "")}.png')
    for j, (name, fn) in enumerate(WERKSTATT_OPTIONEN):
        speichern(mehrfarbig(fn(), 5 + j * 13), f'{OUT}/W{j + 1}.png')

    # Board
    bg = (250, 248, 243); ink = (30, 28, 26); grau = (120, 114, 104)
    big, small = 300, 170
    W = 1900; H = 1260
    im = Image.new('RGB', (W, H), bg); d = ImageDraw.Draw(im)
    f = lambda px: ImageFont.truetype(JOST, px)
    d.text((60, 50), 'Werkstatt – Runde 2 (Richtung A)', font=f(46), fill=ink)
    d.text((60, 140), 'Werkstatt-Icon: drei neue Ideen', font=f(32), fill=ink)
    texte = ['Werkhalle mit Sägezahndach:\ndrei Dachzähne = drei Gruppen',
             'Setzkasten: jedes Fach\nein Stück aus der Werkstatt',
             'Himmel und Hölle: Faltspiel,\nvier Klappen in den Gruppenfarben']
    m = squircle(big); sm = squircle(76)
    for j, (name, _) in enumerate(WERKSTATT_OPTIONEN):
        x = 60 + j * 600; y = 210
        ic = Image.open(f'{OUT}/W{j + 1}.png').convert('RGB').resize((big, big), Image.LANCZOS)
        im.paste((225, 221, 212), (x + 3, y + 7), m); im.paste(ic, (x, y), m)
        ic2 = ic.resize((76, 76), Image.LANCZOS)
        im.paste(ic2, (x + big + 40, y + big - 76), sm)
        d.text((x + big + 40 + 38, y + big + 18), 'echte Größe', font=f(16), fill=grau, anchor='mm')
        d.text((x, y + big + 40), f'W{j + 1}  {name}', font=f(30), fill=ink)
        d.multiline_text((x, y + big + 86), texte[j], font=f(21), fill=grau, spacing=8)
    d.text((60, 780), 'Apps', font=f(32), fill=ink)
    m = squircle(small)
    apps = [n for n, _, _ in MOTIVE if n != 'Werkstatt']
    for i, name in enumerate(apps):
        x = 60 + i * (small + 90); y = 850
        ic = Image.open(f'{OUT}/A_{name.replace(" ", "")}.png').convert('RGB').resize((small, small), Image.LANCZOS)
        im.paste((225, 221, 212), (x + 2, y + 5), m); im.paste(ic, (x, y), m)
        d.text((x + small / 2, y + small + 26), name, font=f(19), fill=(60, 56, 50), anchor='mm')
    im.save('board2.png')
