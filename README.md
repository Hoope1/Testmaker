Hier sind die wichtigsten Punkte:

## Sensible Daten
Der Ordner `Ausgangsmaterial` enthält vertrauliche Dokumente und wird nicht versioniert.
Lokale Kopien sollten verschlüsselt und mit minimalen Rechten betrieben werden.
- Nutze `scripts/hide_ausgangsmaterial.py`, um den Ordner zu verbergen und Rechte auf den Besitzer zu beschränken.
- Die Datei `AGENTS.py` gehört ausschließlich in diesen Ordner und bleibt unversioniert.
- Ein Pre-Commit-Hook (`.pre-commit-config.yaml`) verhindert versehentliche Commits.


Ausgangsmaterial:
- 13 verschiedene Überstiegstests (A, B, C, D, E, F, G, H, I, J, K, L, M) für die technische Basisausbildung
- Diese Tests waren in deutscher Sprache und deckten verschiedene mathematische Bereiche ab
- Tests hatten unterschiedliche Strukturen und Schwerpunkte
- Originaltest-Dokumente waren Word-Dateien mit Bildern und Formeln

Anforderungen:
- 5 Hauptkategorien mit je 20 Punkten (total 100 Punkte)
- Jede Kategorie soll leichte, mittlere und schwere Aufgaben enthalten
- Spezifische Anforderungen für Brüche (gemeinsame Nenner unter 100, nie von Anfang an gemeinsame Nenner)
- Spezifische Anforderungen für Gleichungen (mittlere: 3 Klammern ohne Brüche, schwere: mit Brüchen und Dezimalzahlen)
- Handwerk/Technik-Fokus bei Textaufgaben
- Realistische, aktuelle Preise
- Fallstrick-Detektor gegen ähnliche Aufgaben
- Ausgabe in 3 Formaten: Konsole, Markdown, Word
- Automatische Lösungsberechnung
 
Der Generator integriert mehrere technische Komponenten zur Aufgabenerstellung. Ein Template-System ermöglicht die flexible Generierung von Aufgaben mit unterschiedlichen Schwierigkeitsgraden. Der mathematische Lösungsrechner gewährleistet präzise Berechnungen für jede Aufgabe. Ein Qualitätskontrollmechanismus verhindert Redundanzen und stellt die Einzigartigkeit der Aufgaben sicher.

## Vollständige Spezifikation des Überstiegstest-Generators

### Ausgangsmaterial
Das Tool basiert auf der Analyse von **13 authentischen Überstiegstests** (Versionen A-M) für die österreichische technische Basisausbildung. Diese Word-Dokumente enthielten unterschiedliche mathematische Aufgabentypen mit variierenden Strukturen, Punkteverteilungen und Schwierigkeitsgraden. Die Originaltests deckten Bereiche von Grundrechenarten über Bruchrechnung bis hin zu Geometrie und technischen Textaufgaben ab.

### Zielstruktur des generierten Tests

**Gesamtkonzept:** Exakt 100 Punkte verteilt auf 5 Hauptkategorien à 20 Punkte

#### 1. Grundrechenarten (20 Punkte)
- **Leichte Aufgaben:** 2 Aufgaben à 2 Punkte (einfache Addition, Subtraktion, Multiplikation, Division)
- **Mittlere Aufgaben:** 2 Aufgaben à 3 Punkte (Klammern mit Punkt-vor-Strich-Regel)
- **Schwere Aufgaben:** 2 Aufgaben à 5 Punkte (verschachtelte eckige Klammern, negative Zahlen, komplexe KlaPuStri-Fallen)
- **Besonderheit:** Bewusste Einbindung von mathematischen Fallen zur Prüfung der Rechenregeln

#### 2. Zahlenraum (20 Punkte)
- **Zahlenstrahl:** 5 Punkte - Eintragung von Dezimalzahlen, Brüchen und negativen Zahlen
- **Bruch-Dezimal-Umwandlung:** 3 Punkte - Bidirektionale Konvertierung
- **Kopfrechnen:** 3 Punkte - Multiplikation mit Zehnerpotenzen, Prozentrechnung
- **Einheitenumwandlungen:** 9 Punkte (3+3+3)
  - Leicht: Grundeinheiten (m→cm, kg→g)
  - Mittel: Flächen und Volumen (m²→cm², dm³→L)
  - Schwer: Wissenschaftliche Umwandlungen (cm³→m³, min→h)

#### 3. Textaufgaben (20 Punkte)
- **Mittlere Aufgabe:** 10 Punkte - Fokus auf Handwerk/Technik (Elektriker, Mechaniker, CNC-Maschinen)
- **Schwere Aufgabe:** 10 Punkte - Mehrstufige Industrieprobleme (Pumpsysteme, Personalplanung, Produktionslogistik)
- **Realitätsbezug:** Aktuelle österreichische Gehälter (Elektriker 2000-2600€), realistische Arbeitszeiten und Produktionsparameter

#### 4. Brüche und Gleichungen (20 Punkte)
- **3 Bruchrechnungen:** je 4 Punkte
  - Leicht: Grundoperationen ohne gemeinsame Nenner von Anfang an
  - Mittel: Mit Dezimalzahlen und gemischten Zahlen
  - Schwer: Negative Zahlen, Klammern, Dezimalzahlen kombiniert
  - **Constraint:** Gemeinsame Nenner im Lösungsweg müssen unter 100 bleiben
- **2 Gleichungen:** je 4 Punkte
  - Mittel: Mindestens 3 Klammern (eine mit -, eine mit +, eine mit × davor), OHNE Brüche
  - Schwer: Alle Klammer-Varianten PLUS Brüche und Dezimalzahlen

#### 5. Raumvorstellung (20 Punkte)
- **Zeichenaufgabe:** 10 Punkte - Geometrische Figuren mit Maßstab (Rechtecke, L-förmige Werkstücke)
- **Technische Raumaufgabe:** 10 Punkte - Volumen/Gewichtsberechnungen mit praktischen Anwendungen (Stahlträger, Öltanks)

### Technische Implementierung

#### Qualitätskontrolle-System
- **Fallstrick-Detektor:** Verhindert zu ähnliche aufeinanderfolgende Aufgaben durch Zahlenanalyse (>70% identische Zahlen werden abgelehnt)
- **Template-Tracking:** Verwendete Aufgabenvorlagen werden gespeichert um Wiederholungen zu vermeiden
- **Plausibilitätsprüfung:** Validierung realistischer Werte (Gehälter 1000-5000€, Arbeitszeiten 20-50h)
- **Bruch-Optimierung:** Automatische Überprüfung dass gemeinsame Nenner unter 100 bleiben

#### Mathematischer Lösungsrechner
- **Grundrechenarten:** Automatische Auswertung komplexer Ausdrücke mit verschachtelten Klammern
- **Einheitenumwandlungen:** Präzise Konvertierung zwischen metrischen Einheiten
- **Bruchrechnung:** Vereinfachung und Kürzung von Bruchergebnissen
- **Gleichungen:** Schrittweise Lösungshinweise für lineare Gleichungen

#### Realistische Datenbank
- **Handwerksberufe:** Elektriker, Mechaniker, Schweißer, KFZ-Techniker, Maurer, Installateure
- **Österreichische Preise 2025:** Strom 0,22€/kWh, Benzin 1,45€/l, Baustahl 0,85€/kg
- **Durchschnittsgehälter:** Lehrling 1. Jahr 650€ bis Meister 3400€
- **Technische Parameter:** CNC-Maschinen, Druckluftsysteme, Produktionsraten

### Ausgabeformate

#### 1. Konsolen-Preview
Vollständige Darstellung des Tests und der ersten Lösungen zur sofortigen Überprüfung

#### 2. Markdown-Dateien (.md)
- `ueberstiegstest.md` - Der komplette Test in Markdown-Format
- `ueberstiegstest_loesungen.md` - Separater Lösungsbogen für Lehrkräfte

#### 3. Word-Dokumente (.docx)
- `ueberstiegstest.docx` - Professionell formatiertes Test-Dokument mit korrekten Überschriften, Einrückungen und Schriftgrößen
- `ueberstiegstest_loesungen.docx` - Formatierter Lösungsschlüssel für Lehrkräfte
- **Formatierungsdetails:** Arial 11pt, Überschriften 14pt fett, Aufgaben eingerückt, Punkteangaben rechtsbündig

### Mathematische Präzision
- **Exakte Punkteverteilung:** 2+2+3+3+5+5+5+3+3+3+3+3+10+10+4+4+4+4+4+10+10 = 100
- **Schwierigkeitsprogression:** Systematische Steigerung innerhalb jeder Kategorie
- **Österreichisches Bewertungssystem:** 90-100 (Sehr gut) bis unter 60 (Nicht genügend)
- **Bearbeitungszeit:** 90 Minuten entsprechend österreichischen Standards

### Template-System
Flexible Aufgabengenerierung mit über 50 verschiedenen Vorlagen, die verschiedene Zahlenbereiche und Schwierigkeitsgrade abdecken. Jede Vorlage enthält definierte Variablenbereiche für realistische und pädagogisch sinnvolle Zahlenwerte.

### Automatisierte Features
- **Ein-Klick-Generierung:** Kompletter Test mit einem Befehl
- **Integrierte Validierung:** Automatische Überprüfung auf Vollständigkeit und Konsistenz
- **Fehlerbehandlung:** Robuste Behandlung von Edge-Cases bei der Lösungsberechnung
- **Wiederholbarkeit:** Verschiedene Tests bei jedem Lauf durch intelligente Randomisierung

Der Generator erfüllt damit alle ursprünglichen Anforderungen und bietet zusätzliche professionelle Features für den Einsatz in der österreichischen technischen Berufsausbildung.
