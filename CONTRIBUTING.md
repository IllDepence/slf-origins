# Mitmachen

## Nur darauf hinweisen

Erstelle ein [Issue](https://github.com/IllDepence/slf-origins/issues) und beschreibe Dein Anliegen.

## Selbst Hand anlegen

Erstelle einen [Pull request](https://github.com/IllDepence/slf-origins/pulls) mit vorgeschlagenen Änderungen.

### Artikel-Text

Einfach [docs/index.html](docs/index.html) bearbeiten.

### Artikel-Layout o.Ä.

Bitte die Änderungen auf Desktop und Mobil-Endgerät im Light- und Dark-Mode überprüfen.

### Neue Literaturquelle

1. JSON-Datei in [data/](data) anlegen
    * Datei-Name
        * `yyyy_name_des_werkes.json` wenn nur Publikationsjahr bekannt
        * `yyyy-mm-dd_name_des_werkes.json` wenn Publikationtag bekannt
    * Inhalt
        * die grundlegenden Felder sind hoffentlich selbsterklärend
        * `page`: wenn angegeben die gedruckte Seitennummer im Werk angeben, nicht z.B. um die wievielte Seite einer PDF es sich handelt
        * `slf-kategorien.text-marker`: wird als Regex auf den text angewandt, um die Stelle die, welche Kategorie benennt, zu unterstreichen
        * `slf-antwortform`: werden Antworten nur gesprochen (→ "verbal") oder erstmal aufgeschrieben (→ "schriftlich")?
        * `slf-antwortzeitstruktur`: wird nacheinander geantwortet (→ "sequenziell") oder zeitgleich (→ "zeitgleich")?
        * weitere `slf-`-Felder werden derzeit nicht verwendet und können weggelassen werden
2. Übertragung in den Artikel
    * Abbildungen
        * `$ ./make_js.sh` fasst alle Quellen zusammen und kopiert sie in `docs/js/data.js`
    * Literaturverzeichnis
        * `$ python generate_sources.py` generiert die `<li>`-Einträge für das Literaturverzeichnis
    * Text
        * manuell editieren
        * es bietet sich wahrscheinlich an, eine Sektion für Aktualisierungen anzulegen, sodass die notwendigen Änderungen im Haupttext minimal gehalten werden
