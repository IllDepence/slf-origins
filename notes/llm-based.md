LLM-gestützte Suche nach Literaturquellen zu Stadt, Land, Fluss und etwaigen Vorgängern.

Code: [github.com/IllDepence/slf-origins-llm](https://github.com/IllDepence/slf-origins-llm)

# Quellen

* [Berlin State Library (2023). Fulltexts of the Digitized Collections of the Berlin State Library (SBB)](https://zenodo.org/records/7716098)
    * 4.998.099 Seiten
    * 28.909 Werke
    * `fulltext.sqlite3`

# Vorgehen

* Filter-Kaskade
    1. Stichwort-Filter
    2. LLM-Beurteilung
    3. Manuelle Überprüfung
* LLM-Aspekte
    * Aus Ergebnissen von [manueller Recherche](manual.md) valide und invalide Beispiele als [ICL](https://en.wikipedia.org/wiki/Prompt_engineering#In-context_learning)-Input bereitstellen
    * Detektion auf Stichprobe testen
    * Kosten abschätzen
        * ~5,000 Input-Tokens
        * ~25 Output-Tokens
        * ✕200,000
        * Mistral Medium 3.1
            * `((5000*(0.4/1000000))+(25*(2/1000000)))*200000 = 410`
        * Mistral Small 3.1 24B
            * `((5000*(0.05/1000000))+(25*(0.1/1000000)))*200000 = 50`
        * Mistral Nemo
            * `((5000*(0.02/1000000))+(25*(0.04/1000000)))*200000 = 20`

# Verarbeitungs-Vorbereitung

Daten-Verifikation
* Tabelle "text" hat Spalten "id", "file_name", "ppn", "text"
* Test mit **_Mit gegebenen Anfangsbuchſtaben (1882)_**
    * PPN: 745171761
    * `select count(*) from text where ppn = '745171761';`
        * [x] 783
        * → stimmt mit Seitenzahl überein
    * `select * from text where ppn = '745171761' limit 66;`
        * [x] letztes Ergebnis (Seite 66) enthält Text von **_Mit gegebenen Anfangsbuchſtaben (1882)_**
        * id: 2290531

Vorbereitung Positiv- und Negativbeispiele
* Positiv
    * **_Mit gegebenen Anfangsbuchſtaben (1882)_**
        * id: 2290531
    * **_Reiſeſpiel (1899)_**
        * id: 2429526 + 2429577
            * (über Seitenumbruch)
    * **_Mit gegebenen Anfangsbuchſtaben (1905)_**
        * (id: 3148256)
    * **_Mein Nachbar gefällt mir (1909 a)_**
        * id: 4969308
    * **_Das ABC der Großen oder das Reiſeſpiel (1909)_**
        * id: 1608883
    * **_Schreibspiel (1911)_**
        * id: 1814578
* Negativ
    * [Illustrirtes Spielbuch für Mädchen (1865)](http://resolver.staatsbibliothek-berlin.de/SBB0000D67200000000)
        * id: 3973548
            * „Komplimente nach dem ABC“ involviert nur eine „Kategorie“, daher irrelevant
        * (id: 3973667 „Die Bestimmung nach dem ABC“)
    * [Spiele zur Uebung und Erholung des Körpers und des Geistes (1878)](http://resolver.staatsbibliothek-berlin.de/SBB0000D7C700000000)
        * id: 4191016
            * „Die Bestimmung nach dem ABC“: Buchstabe gegeben durch Gegenstand, gefordert Tätigkeit/Bestimmung. Involviert nur eine „Kategorie“, daher irrelevant
    * [Das Spiel im Zimmer 1887](http://resolver.staatsbibliothek-berlin.de/SBB0000D5E900000000)
        * id: 2110021
            * „Die drei Dinge“: beliebige Wörter (keine Kategorien), daher als irrelevant betrachtet
        * (id: 2109917 „Die Bestimmung nach dem ABC“)
    * [Großes illustriertes Spielbuch für Mädchen : eine Auswahl der schönsten Spiele, anregender und unterhaltender Beschäftigungen und Belustigungen im Freien und im Zimmer (1900)](http://resolver.staatsbibliothek-berlin.de/SBB0000D61800000000)
        * id: 2948770
            * „Das Freundschafts-ABC“ nur eine „Kategorie“, daher als irrelevant betrachtet
* Nicht in DB?
    * **_Mein Nachbar gefällt mir (1836)_**
        * PPN 766629139
    * [Das Buch der Spiele und Kunststücke für die fröhliche Jugend (1846)](https://resolver.staatsbibliothek-berlin.de/SBB00033ADD00000000)
        * PPN 1818359847

Vorfilter-Test
* Spiel
    * `r"(?<!bei)([sſf]\s?p\s?i\s?e\s?l)", re.I`
    * 253,472 Seiten ohne Text
    * 4,562,036 Seiten ohne Treffer
    * 172,591 Seiten mit Treffer
* Spiel / Alphabet / Anfangsbuchstabe
    * `r"(?<!bei)([sſf]\s?p\s?i\s?e\s?l)", re.I`
    * `r"(a\s?l[\s-]?p\s?h\s?a[\s-]?[bß]\s?e\s?t(?!a)|a\s?n[\s-]?[sſf]\s?a\s?n\s?g\s?s[\s-]?[bß]\s?u\s?c\s?h[\s-]?[sſf]\s?t\s?a[\s-]?[bß]\s?e)", re.I`
    * 253,472 Seiten ohne Text
    * 4,532,390 Seiten ohne Treffer
    * 202,237 Seiten mit Treffer
* Spiel / Alphabet / Anfangsbuchstabe optimiert
    * Regex
        ```
        """
        (?<!be[iy])
        (?<!kirch)
        (?<!schau)
        (?<!gl[üu]cks)
        (?<!gl[üu]ck)
        (?<!kost)
        (?<!lust)
        (?<!hazard)
        (?<!karten)
        (?<!sing)
        (?<!ball)
        (?<!vor)
        (?<!gast)
        (?<!orgel)
        (?<!schach)
        (?<!taschen)
        (?<!würfel)
        (?<!marionetten)
        (?<!puppen)
        (?<!fest)
        (?<!licht)
        (?<!aus)
        (?<!rolle\s)
        ([sſf]\s?p\s?i\s?e\s?l)
        (?!zeug)
        (?!war)
        (?!raum)
        (?!kart)
        (?!tisch)
        """, re.I | re.X

        r"""
        (
        a\s?l[\s-]?p\s?h\s?a[\s-]?[bß]\s?e\s?t
        (?!a)
        (?!isch\sge)
        (?!isches\sreg)
        (?!isches\sver)
        (?!ischer\sord)
        |
        a\s?n[\s-]?[sſf]\s?a\s?n\s?g\s?s[\s-]?[bß]\s?u\s?c\s?h[\s-]?[sſf]\s?t\s?a[\s-]?[bß]\s?e
        )
        """, re.I | re.X
        ```
    * 253,472 Seiten ohne Text
    * 4,596,378 Seiten ohne Treffer
    * 138,249 valid Seiten mit Treffer

LLM-Tests
* Mistral Nemo
    * hält sich nicht an Anweisungen
* Mistral Small 3.1 24B
    * scheint zu funktionieren
* Google Gemini 2.5 Flash Lite
    * solala, nennt Antworten als Kategorien
* GPT-4.1 Nano
    * falsch-negative Antwort in erstem Test
* DeepSeek R1 Distill Llama 70B
    * würde Kapazität für Reasoning-Tokens beanspruchen

Ergebnis in Zahlen
* Seiten
    * `fulltext.sqlite3`
        * → 4.998.099
    * Ohne Text: 253.472
        * → 4.734.627
    * Text kürzer als 250 Zeichen: 173.034
        * → 4.561.593
    * Stichwort-Filter Spiel / Alphabet / Anfangsbuchstabe: 4.423.795
        * → 138.249
    * LLM-Kategorisierung
        * → 139
    * Manuelle Überprüfung
        * → 22 (2 ICL, 8 bekannt, 12 neu)
* Klassifikation
    * 2 ICL-Texte ausgeschlossen
    * 20 korrekt-positive (TP)
    * 117 falsch-positive (FP)
    * Genauigkeit (precision)
        * 20/(20+117) = 0.15
    * Trefferquote (recall)
        * Von LLM als nicht relevant klassifizierte 138,110 nicht manuell geprüft, daher keine Zahl für falsch-negative Klassifikationen und somit Trefferquote nicht bestimmbar. Bei niedriger Genauigkeit (0.15), sprich zu freizügiger Klassifikation als relevant, aber vermutlich eher hoch als tief.
* LLM
    * 66.59 $
    * 670M Tokens
        * 667M Prompt
        * 2.65M Completion

Neue Funde (DB ID, PPN, Seite)
* (2109991, 745139965, 00000065.xml)
    * **_Mein Nachbar gefällt mir (1887)_**
* (2109991, 745139965, 00000070.xml)
    * **_Die Poſt (1887)_**
* (1121138, 74518166X, 00000740.xml)
    * **_Mein Nachbar gefällt mir (1911)_**
* (4507196, 74518961X, 00000094.xml)
    * **_Die Poſt (1894)_**
* (1380111, 745280099, 00000110.xml)
    * **_The Holiday ABC (1910)_**
* (908229, 745605478, 00000115.xml)
    * **_Steeple-Chase (1887)_**
* (4800020, 745725198, 00000048.xml)
    * **_Das Handel-Bandel-Spiel (1911)_**
* (4702942, 745861873, 00000732.xml)
    * **_Das ABC-Spiel (1874)_**
* (3696366, 746238983, 00000336.xml)
    * **_Die Handlungsreisenden (1890)_**
* (3696347, 746238983, 00000345.xml)
    * **_Das Fünfminutenſpiel (1890)_**
* (948114, 746636121, 00000309.xml)
    * **_Mein Nachbar gefällt mir (1879)_**
* (2431996, 767214722, 00000203.xml)
    * **_Le Logement (1860)_**
