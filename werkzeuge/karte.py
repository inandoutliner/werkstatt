#!/usr/bin/env python3
"""Erzeugt KARTE.md für eine große Einzeldatei-App (index.html).

Aufruf:  python3 karte.py <repo-ordner> [weitere html-dateien relativ zum repo]
Ergebnis: <repo-ordner>/KARTE.md

Die Karte listet Abschnitte (Kommentar-Überschriften im Code), die Funktionen darin,
die Bedien-Bereiche im HTML und Zeilen mit eingebetteten Daten (Schriften, Bilder),
die man nie komplett lesen sollte. Zeilennummern gelten für den Stand beim Erzeugen;
zum Finden besser nach dem Abschnittstitel suchen (grep -n).
"""
import re, sys, os, subprocess

LANG = 3000  # ab so vielen Zeichen gilt eine Zeile als Datenblock

SEC = [
    re.compile(r'^\s*/\*\s*[-=]{2,}\s*(.+?)\s*[-=]{2,}\s*\*/'),   # /* ---- Titel ---- */
    re.compile(r'^\s*/\*\s*-{2,}\s*(.+?)\s*-{2,}'),                # /* --- Titel ---  (offen)
    re.compile(r'^\s*/\*\s*={2,}\s*(.+?)\s*(?:={2,}|\*/|$)'),      # /* ===== Titel
    re.compile(r'^\s*//\s*[-=]{3,}\s*(.+?)\s*[-=]{3,}\s*$'),       # // ---- Titel ----
]
FN = [
    re.compile(r'^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)'),
    re.compile(r'^\s*(?:const|let)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>'),
]
HTML = re.compile(r'<(section|dialog|nav|header|footer|aside)\b([^>]*)>')
ATTR = re.compile(r'(id|aria-label|data-panel|class)="([^"]+)"')


def kurz(s, n=70):
    s = re.sub(r'\s+', ' ', s).strip()
    return s if len(s) <= n else s[:n - 1] + '…'


def karte(pfad, name):
    zeilen = open(pfad, encoding='utf-8', errors='replace').read().split('\n')
    abschnitte, aktuell, html, daten = [], None, [], []
    for i, z in enumerate(zeilen, 1):
        if len(z) > LANG:
            daten.append((i, len(z), kurz(z, 60)))
            continue
        for r in SEC:
            m = r.match(z)
            if m:
                aktuell = [i, kurz(m.group(1).rstrip('*/ -=')), []]
                abschnitte.append(aktuell)
                break
        else:
            for r in FN:
                m = r.match(z)
                if m and aktuell is not None:
                    aktuell[2].append((i, m.group(1), len(z) - len(z.lstrip())))
                    break
            m = HTML.search(z)
            if m and len(html) < 40:
                a = dict(ATTR.findall(m.group(2)))
                label = a.get('id') or a.get('data-panel') or a.get('aria-label')
                if label:
                    html.append((i, m.group(1), label, a.get('aria-label', '')))
    titel = re.search(r'<title>([^<]*)', '\n'.join(zeilen[:40]))
    out = [f'## `{name}` – {titel.group(1) if titel else ""}'.rstrip(' –'),
           f'{len(zeilen)} Zeilen, {os.path.getsize(pfad) // 1024} KB.', '']
    if daten:
        out += ['**Datenblöcke – nie komplett ausgeben** (z. B. `cut -c1-200` oder `awk \'length<3000\'`):', '']
        out += [f'- Zeile {i}: {n // 1024} KB – `{t}`' for i, n, t in daten[:15]]
        out.append('')
    if html:
        out += ['**Bedien-Bereiche (HTML)**', '']
        out += [f'- {i}: `<{tag}>` {lab}' + (f' – {al}' if al and al != lab else '') for i, tag, lab, al in html]
        out.append('')
    if abschnitte:
        out += ['**Abschnitte im Code** (Suchbegriff = Titel)', '', '| Zeile | Abschnitt | Funktionen |', '|---|---|---|']
        grenzen = [a[0] for a in abschnitte[1:]] + [len(zeilen)]
        for (i, t, f), ende in zip(abschnitte, grenzen):
            if f:
                tief = min(e for _, _, e in f)
                f = [x for x in f if x[2] == tief]
            lang = ende - i > 300
            namen = [f'{n} ({z})' if lang else n for z, n, _ in f[:18 if lang else 12]]
            mehr = f' … +{len(f) - len(namen)}' if len(f) > len(namen) else ''
            out.append(f'| {i}–{ende} | {t.replace("|", "/")} | {", ".join(namen)}{mehr} |')
        out.append('')
    return '\n'.join(out)


def main():
    repo = sys.argv[1]
    dateien = ['index.html'] + sys.argv[2:]
    try:
        stand = subprocess.run(['git', '-C', repo, 'log', '-1', '--format=%h, %cd: %s', '--date=short'],
                               capture_output=True, text=True).stdout.strip()
    except Exception:
        stand = ''
    teile = ['# Inhaltskarte', '',
             f'Automatisch erzeugt mit `werkstatt/werkzeuge/karte.py`. Stand: {stand}', '',
             'Vorgehen: Abschnitt hier finden → `grep -n "<Titel>" index.html` → nur diesen Bereich lesen.', '']
    for d in dateien:
        teile.append(karte(os.path.join(repo, d), d))
    open(os.path.join(repo, 'KARTE.md'), 'w', encoding='utf-8').write('\n'.join(teile))


if __name__ == '__main__':
    main()
