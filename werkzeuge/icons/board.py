import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
from icons import JOST
from motive import MOTIVE
from render import RICHTUNGEN, OUT

def squircle(n):
    # iOS-ähnliche Superellipse
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    u = np.abs((xx + 0.5) / n * 2 - 1); v = np.abs((yy + 0.5) / n * 2 - 1)
    m = (u ** 5 + v ** 5) <= 1
    return Image.fromarray((m * 255).astype(np.uint8))

def board(pfad, icon=190, gap=34, texte=None):
    bg = (250, 248, 243)
    links = 250
    W = links + len(MOTIVE) * (icon + gap) + 40
    H = 170 + len(RICHTUNGEN) * (icon + 110) + 20
    im = Image.new('RGB', (W, H), bg); d = ImageDraw.Draw(im)
    fT = ImageFont.truetype(JOST, 46); fR = ImageFont.truetype(JOST, 34); fS = ImageFont.truetype(JOST, 19)
    fK = ImageFont.truetype(JOST, 20)
    d.text((40, 50), 'Werkstatt – Icon-Familie', font=fT, fill=(30, 28, 26))
    mask = squircle(icon)
    for r, (kz, rname, _) in enumerate(RICHTUNGEN):
        y = 150 + r * (icon + 110)
        d.text((40, y + 40), f'{kz}', font=ImageFont.truetype(JOST, 64), fill=(30, 28, 26))
        d.text((40, y + 115), rname, font=fR, fill=(30, 28, 26))
        if texte:
            d.text((40, y + 158), texte[kz], font=fK, fill=(120, 114, 104))
        for i, (name, _, _) in enumerate(MOTIVE):
            x = links + i * (icon + gap)
            ic = Image.open(f'{OUT}/{kz}_{name.replace(" ", "")}.png').convert('RGB').resize((icon, icon), Image.LANCZOS)
            # leichter Schatten
            sh = Image.new('L', (icon, icon), 0)
            im.paste((225, 221, 212), (x + 2, y + 5), mask)
            im.paste(ic, (x, y), mask)
            d.text((x + icon / 2, y + icon + 22), name, font=fS, fill=(60, 56, 50), anchor='mm')
    im.save(pfad)

if __name__ == '__main__':
    board(sys.argv[1] if len(sys.argv) > 1 else 'board.png')
