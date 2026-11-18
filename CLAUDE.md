# Arbeitsweise für Claude

Einstieg ist immer `README.md` in diesem Repo. Sie listet alle Projekte, Repos und Online-Adressen.

## Bei Arbeit an einem Projekt

1. Nur das betroffene Repo klonen (`--depth 1`), nicht alle.
2. Erst README und `KARTE.md` des Repos lesen, dann den Abschnitt per `grep -n` finden und nur diesen Bereich lesen. Nie die ganze `index.html` lesen (bis ca. 700 KB); Datenblöcke aus der Karte nie ausgeben.
3. Änderung machen, Versionsnummer/Titel im Commit nennen (z. B. „Abwickler 3030: …“).
4. Pushen → GitHub Pages aktualisiert die Online-Version.
5. Bei Bedarf das passende Claude-Artefakt mit derselben Datei neu veröffentlichen.
6. Nach größeren Änderungen die Karte neu erzeugen: `python3 werkstatt/werkzeuge/karte.py <repo>` (Rechtschreibfreunde: zusätzlich `mathe/index.html` anhängen).
7. Wenn sich Zweck, Adresse oder Stand ändern: README des Repos und die Tabelle hier anpassen.
8. Die aktuelle Datei zusätzlich in den Ordner `APPs` auf dem Mac legen (Web-Projekte als `<Name> <Version>.html`).

## Wo ist der aktuelle Stand?

- GitHub ist die Quelle. Zu Beginn wird das Repo gelesen, nicht der APPs-Ordner.
- Ausnahme: Wenn der Nutzer selbst am Mac geändert hat (v. a. Xcode/Android Studio), zuerst mit dem APPs-Ordner abgleichen.

## Grundsätze

- Ein Repo pro Projekt; dieses Repo enthält nur Übersicht und Werkzeuge (`werkzeuge/`).
- Web-Repos sind öffentlich, native Apps privat (z. B. `fernbedienung`). In keinem Repo: keine personenbezogenen Daten, Passwörter oder geheimen Schlüssel einchecken. Öffentliche Schlüssel (z. B. Supabase Publishable Key) sind ok, dann aber Zugriffsregeln in der Datenbank prüfen.
- Native Apps (Xcode, Android Studio) werden lokal im Ordner `APPs` auf dem Mac gebaut; das Repo ist die Sicherung. Signierschlüssel (`*.keystore`) bleiben nur lokal.
