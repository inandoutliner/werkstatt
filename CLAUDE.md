# Arbeitsweise für Claude

Einstieg ist immer `README.md` in diesem Repo. Sie listet alle Projekte, Repos und Online-Adressen.

## Bei Arbeit an einem Projekt

1. Nur das betroffene Repo klonen (`--depth 1`), nicht alle.
2. Erst die README des Repos lesen, dann gezielt suchen (`grep -n`), statt die ganze `index.html` zu lesen. Die Dateien sind groß (bis ca. 700 KB, alles in einer Datei).
3. Änderung machen, Versionsnummer/Titel im Commit nennen (z. B. „Abwickler 3030: …“).
4. Pushen → GitHub Pages aktualisiert die Online-Version.
5. Bei Bedarf das passende Claude-Artefakt mit derselben Datei neu veröffentlichen.
6. Wenn sich Zweck, Adresse oder Stand ändern: README des Repos und die Tabelle hier anpassen.

## Grundsätze

- Ein Repo pro Projekt; dieses Repo enthält keinen Code.
- Alle Repos sind öffentlich: keine personenbezogenen Daten, Passwörter oder geheimen Schlüssel einchecken. Öffentliche Schlüssel (z. B. Supabase Publishable Key) sind ok, dann aber Zugriffsregeln in der Datenbank prüfen.
- Native Apps (Xcode, Android Studio) liegen lokal im Ordner `APPs` auf dem Mac.
