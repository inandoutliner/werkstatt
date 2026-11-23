# App-Icons (Stil A „Stempel“)

Erzeugt die Icons der Werkstatt-Familie: cremefarbenes Papier mit Knick, gesprenkelte Druckfarbe, Jost Bold – passend zu Fernbedienung, Weiter Writer und Begegnungs Beleg.

- Farben nach Gruppe: Plotten blau, Kinder rot, Fest grün, Werkstatt schwarz (+ alle drei im Dach).
- Werkstatt-Icon: `halle()` in `motive.py` (Werkhalle mit Sägezahndach, Option W1).
- App-Motive: `MOTIVE` in `motive.py`, gerendert mit `stempel()` aus `render.py`.

Neues Projekt: Motiv-Funktion in `motive.py` ergänzen (Lagen `a` = volle Farbe, `b` = heller Ton), in `MOTIVE` und `GRUPPE` (render.py) eintragen, dann:

```
python3 render2.py
```

Ergebnis liegt in `out/` (1024 px). Für Web-Apps auf 180 px verkleinern und als `apple-touch-icon.png` neben die `index.html` legen, zusätzlich nach `werkstatt/icons/<repo>.png` für die Startseite.

Benötigt: Python 3 mit numpy, opencv-python, Pillow; Schrift Jost-Bold.ttf (Pfad über `JOST=…`).
