Aufgabenliste (maximale Detailtiefe, in sinnvoller Reihenfolge)

Epic A – Dezimaldarstellung & Runden korrekt (kaufmännisch)

A1. Decimal-basierte Formatierung einführen ✅

Änderungen

Neue Helfer: _quantize(x, nd) -> Decimal, de_format(x, nd=2, thousand=False) -> str.

fmt(...) als Alias auf de_format(...) belassen (Kompatibilität).

fmt_int_or_dec(...) auf Decimal umstellen (Integer-Erkennung mit ROUND_HALF_UP).


Ziel

Komma als Dezimaltrennzeichen, optionaler Tausenderpunkt, keine E-Notation.


Akzeptanzkriterien

fmt(1234.5, 2, thousand=True) == "1.234,50".

fmt_int_or_dec(12.0) == "12", fmt_int_or_dec(12.1) == "12,10".

Im gesamten erzeugten Test/ Lösungen taucht niemals ein . als Dezimaltrennzeichen auf; e+/e- kommt nicht vor.



A2. Stellenrunden mit ROUND_HALF_UP vereinheitlichen ✅

Änderungen

MathSolver.round_to_place(value, place):

Für t/h/z/E: über _quantize(value, k) (k = 3/2/1/0).

Für Z/H/T/…: skalieren, auf ganze Zahl quantizen, zurückskalieren (auch Decimal).



Akzeptanzkriterien

round_to_place(2.5, "E") == 3.0 (kaufmännisch, nicht Bankers).

round_to_place(1499.5, "Z") == 1500.0.

Keine Float-Artefakte (z. B. 1,999999).




---

Epic B – Mathematische Konsistenz & Gleichungen

B1. solve_linear_equation Typenbereinigung ✅

Änderungen

Signatur: -> float | None.

Falls a == c: None zurück (keine/∞ Lösungen).


Akzeptanzkriterien

Keine gemischten Rückgabe-Typen in Downstream-Code; Lösungen werden korrekt formatiert oder „keine eindeutige Lösung“ im Erklärungstext vermerkt (wie schon implementiert).



B2. Variable für Unbekannte parametrisierbar ✅

Änderungen

generate_gleichung(schwer=False, var="x").

Alle Gleichungstemplates verwenden var anstelle festem x.


Akzeptanzkriterien

In der Aufgaben- und Lösungsdarstellung steht konsequent dasselbe Variable-Symbol (z. B. n = ...), ohne den Aufgabentyp zu verändern.




---

Epic C – Tabellen & „Zahlenraum“ korrekt rendern

C1. Stellenwerttabelle mit 11 Spalten korrekt füllen ✅

Änderungen

Lösungsteil: Kopf mit | Nr | HT | ZT | T | H | Z | E | , | z | h | t |.

Zeilen parserseitig aus Tags ("3E 2z 1h 5t") in genau diese 11 Spalten mappen (Leerspalt nach E für Komma).


Akzeptanzkriterien

Jede Lösungszeile hat genau 12 Trennstriche | (11 Spalten + 2 Rand-Pipes).

Word-/LaTeX-Export erzeugt eine 11-spaltige Tabelle ohne verrutschte Spalten.



C2. Markdown→Word Tabellenabschluss robust ✅

Änderungen

In _parse_markdown_to_word: Bei nicht tabellarischen Zeilen current_table = None setzen (sicherstellen).


Akzeptanzkriterien

Nach einer Tabelle beginnende Absätze landen nicht versehentlich als weitere Tabellenzeilen.




---

Epic D – „No-Touch“ für Skizzen/ASCII, Parser-Stabilität

D1. Codeblöcke / ASCII-Skizzen unverändert durchleiten ✅

Änderungen

Parser ignoriert Zeilen zwischen … (keine Formatierung, keine Substitution).

Keine post-processing „Smart“-Ersetzung von Linien-/Blockzeichen.


Akzeptanzkriterien

Die ASCII-Bilder (3-Ansichten, Körpernetz) sind bytegenau ident zwischen test_content und erwarteter Vorlage.




---

Epic E – Einheitenumwandlung & sehr kleine/große Werte

E1. Einheitenergebnisse konsistent formatiert ✅

Änderungen

In generate_einheiten: Ausgabe konsequent via de_format(val, nd) (Heuristik: ≥10000 → 0; ≥1 → 2; ≥0,01 → 4; sonst 6).


Akzeptanzkriterien

Keine wissenschaftliche Notation; dezimale Kommas; sinnvolle Nachkommastellen.

Für Volumina/Fläche (m³/m²) keine Rundungsfehler sichtbar.




---

Epic F – QualityControl robust

F1. „Numbers“ als Floats akzeptieren ✅

Änderungen

Typen der Methoden auf Sequence[float].

Intern map(float, numbers); try/except-Fallback auf [].


Akzeptanzkriterien

Register- und Vergleichsfunktionen funktionieren auch mit gemischten Ganzzahlen/Dezimalen.




---

Epic G – Geometrie-/Volumentasks transparenter

G1. (Optional) zusätzliche Klarheit in Erklärtexten ✅

Änderungen

In generate_geometrie(zeichnen=False): Erklärung ergänzt (z. B. beide Volumen-Einheiten zeigen: dm³ und m³, abhängig vom Preismaß).


Akzeptanzkriterien

Didaktisch klarer, ohne Task-Logik zu verändern.




---

Epic H – CLI-vermeidend, aber kompatibel

H1. CLI bleibt optional, Default „MITTEL“

Änderungen

Wenn keine --stufe übergeben wird und stdin nicht TTY: still „MITTEL“ (so wie jetzt); interaktive Abfrage nur im TTY-Fall – bereits vorhanden, also unverändert lassen.


Akzeptanzkriterien

Script ist ohne Benutzerinteraktion lauffähig (CI/Smoke-Check-tauglich).




---

Epic I – Export-Stabilität

I1. Markdown→LaTeX Escape & Mathe

Änderungen

Bestehende _markdown_to_latex behalten; keine Mathe-Inhalte ändern.


Akzeptanzkriterien

PDFs (falls LaTeX vorhanden) bauen durch, Tabellen/Listen lesbar.




---

Empfohlene Commit-Reihenfolge (atomar, review-freundlich)

1. feat(decimal): _quantize, de_format, fmt/fmt_int_or_dec Migration (Epic A1). ✅


2. feat(rounding): round_to_place (Epic A2) + spez. Tests im Smoke-Check. ✅


3. fix(eq-types): solve_linear_equation Rückgabe vereinheitlichen (Epic B1). ✅


4. feat(eq-var): generate_gleichung(..., var="x") (Epic B2). ✅


5. fix(placevalue): Stellenwerttabelle 11-Spalten-Mapping (Epic C1). ✅


6. fix(word-parser): Tabellenabschluss (Epic C2). ✅


7. fix(units): generate_einheiten → de_format (Epic E1). ✅


8. fix(qc): QualityControl Typ-Robustheit (Epic F1). ✅


9. docs(geo): Erklärtexte Geometrie (Epic G1). ✅


10. chore(smoke): smoke_check.py hinzufügen (siehe unten). ✅




---

Smoke-Check Skript

Fügt eine schnelle, nicht-interaktive Prüfung hinzu. Es baut 5 Varianten mit unterschiedlichen Seeds, schreibt nichts auf Platte, sondern wertet Strings und Kernfunktionen aus.

> Datei: smoke_check.py



#!/usr/bin/env python3
"""
Smoke-Check für Überstiegstest Generator v2.0
- Kein CLI, keine Netzwerkkonnektivität
- Prüft nur oberflächlich, aber gezielt die heiklen Punkte:
  * Dezimalformatierung (Komma, Tausenderpunkt optional, keine E-Notation)
  * Kaufmännisches Runden (ROUND_HALF_UP) inkl. Stellen (E/z/h/t/Z/H/…)
  * Stellenwerttabelle: 11 Spalten im Lösungs-Table, konsistente Pipes
  * Gleichungen: variables Symbol konsistent in Aufgabe & Lösung
  * ASCII/Codeblöcke: bleiben unverändert, keine „Beautify“-Artefakte
  * Einheiten: sinnvolle Nachkommastellen, keine E-Notation
"""

import re
import sys
import traceback

# Importiere Deinen Generator – passe ggf. den Modulnamen an
from Create import TestGenerator, Schwierigkeit, MathSolver, fmt, de_format

OK = "✓"
FAIL = "✗"

def assert_true(name, cond, msg=""):
    if cond:
        print(f"{OK} {name}")
        return True
    else:
        print(f"{FAIL} {name}: {msg}")
        return False

def check_decimal_formatting():
    print("\n[Check] Dezimalformatierung & E-Notation")
    ok = True
    # Basisfälle
    ok &= assert_true("fmt(1234.5, 2, thousand=True) == '1.234,50'",
                      fmt(1234.5, 2, True) == "1.234,50")
    ok &= assert_true("fmt(0.125, 3) == '0,125'", fmt(0.125, 3) == "0,125")
    # Keine E-Notation im Format
    samples = [0.00000123, 123456789.0, 12.0, 12.3456]
    for s in samples:
        out = fmt(s, 6)
        ok &= assert_true(f"Keine E-Notation ({s})", "e" not in out.lower(), out)
        ok &= assert_true(f"Komma als Dezimaltrennzeichen ({s})", "," in out or out.isdigit(), out)
    return ok

def check_rounding_places():
    print("\n[Check] Kaufmännisches Runden & Stellen")
    ok = True
    # Kaufmännisch: 2.5 -> 3.0
    ok &= assert_true("ROUND_HALF_UP bei Einer", MathSolver.round_to_place(2.5, "E") == 3.0)
    # Zehner/Hunderter
    ok &= assert_true("Zehner-Rundung 1499.5 -> 1500",
                      MathSolver.round_to_place(1499.5, "Z") == 1500.0)
    ok &= assert_true("Hundertstel 1.005 -> 1.01",
                      MathSolver.round_to_place(1.005, "h") == 1.01)
    return ok

def check_complete_generation(seed: int, var_symbol: str = "x"):
    print(f"\n[Check] Komplette Generation (Seed={seed}, var='{var_symbol}')")
    gen = TestGenerator(Schwierigkeit.MITTEL, seed=seed)
    test_md, sol_md, details = gen.generate_complete_test()

    ok = True

    # 1) Kein Punkt als Dezimaltrenner innerhalb von Zahlen (Ausnahme: Tausenderpunkt)
    # Heuristik: verbiete Muster \d+\.\d+ (Punkt zwischen Ziffern), erlaube 1.234,56 aber das matchen wir nicht
    bad_decimal_point = re.search(r"\d+\.\d+", test_md + sol_md)
    ok &= assert_true("Kein '.' als Dezimaltrenner", bad_decimal_point is None,
                      bad_decimal_point.group(0) if bad_decimal_point else "")

    # 2) Keine E-Notation
    ok &= assert_true("Keine E-Notation insgesamt", "e+" not in (test_md+sol_md).lower() and "e-" not in (test_md+sol_md).lower())

    # 3) Stellenwerttabelle: Kopf korrekt, jede Datenzeile hat 12 '|' (11 Spalten + 2 Ränder)
    tbl_blocks = []
    capture = False
    for line in sol_md.splitlines():
        if line.strip().startswith("| Nr |"):
            capture = True
            tbl_blocks.append([line])
            continue
        if capture:
            if line.strip().startswith("|"):
                tbl_blocks[-1].append(line)
            else:
                capture = False

    has_table = assert_true("Stellenwerttabelle vorhanden", len(tbl_blocks) >= 1)
    ok &= has_table
    if has_table:
        block = tbl_blocks[0]
        # Kopf prüfen
        ok &= assert_true("Tabellenkopf korrekt",
                          "| Nr | HT | ZT | T | H | Z | E | , | z | h | t |" in block[0])
        # Datenzeilen prüfen
        data_lines = [ln for ln in block[1:] if not set(ln.strip("|").replace("-", "").split()) <= {""}]
        expected_pipes = 12
        for dl in data_lines:
            count = dl.count("|")
            ok &= assert_true("Zeilenpipe-Anzahl == 12", count == expected_pipes,
                              f"{dl} -> pipes={count}")

    # 4) Gleichungen: Variable konsistent
    if var_symbol != "x":
        eq_lines_task = [ln for ln in test_md.splitlines() if "Gleichungen" in ln or ("=" in ln and ("(" in ln and ")" in ln))]
        eq_lines_sol = [ln for ln in sol_md.splitlines() if "b.1)" in ln or "b.2)" in ln or ("=" in ln and var_symbol in ln)]
        # Minimalprüfung: Lösungszeilen enthalten var_symbol = ...
        joined_sol = "\n".join(eq_lines_sol)
        ok &= assert_true(f"Gleichungs-Lösung nutzt '{var_symbol} = ...'",
                          re.search(rf"{re.escape(var_symbol)}\s*=", joined_sol) is not None,
                          joined_sol[:120])

    # 5) ASCII/Codeblöcke: bleiben unverändert (strukturcheck)
    # Prüfe, dass Linienzeichen vorkommen und dreifache Backticks Blöcke einschließen
    codeblocks = re.findall(r"```(.*?)```", test_md, flags=re.S)
    ok &= assert_true("Mindestens ein Codeblock vorhanden (ASCII/Skizzen)", len(codeblocks) >= 1)
    for cb in codeblocks:
        ok &= assert_true("ASCII-Block enthält Linienzeichen", any(ch in cb for ch in ["┌", "┐", "└", "┘", "─", "│", "▲", "◼"]))

    # 6) Einheiten: Stichprobenhaft auf , als Dezimaltrennzeichen prüfen
    unit_samples = re.findall(r"\b\d[\d\.\,]*\s?(?:m²|m³|dm³|cm²|cm³|km²|ha|l|ml|cl|dl|kg|g|mg|s|min|h)\b", sol_md)
    for us in unit_samples[:10]:
        # wenn Dezimal vorhanden, dann muss ein Komma enthalten sein
        if re.search(r"\d[\,]\d", us) or us.isdigit():
            ok &= True
        else:
            # Fälle wie '10 cm' sind okay; Fälle '10.5 cm' wären falsch
            ok &= assert_true("Einheiten ohne '.' als Dezimaltrenner", "." not in us, us)

    return ok

def main():
    overall_ok = True
    try:
        overall_ok &= check_decimal_formatting()
        overall_ok &= check_rounding_places()
        # Erzeuge mehrere Varianten; in der Praxis gern mehr Seeds
        for seed in [1, 2, 3, 4, 5]:
            overall_ok &= check_complete_generation(seed, var_symbol="x")
        # Bonus: eine Runde mit alternativem Variablensymbol
        overall_ok &= check_complete_generation(42, var_symbol="n")
    except Exception as e:
        print(f"{FAIL} Smoke-Check Exception: {e}")
        traceback.print_exc()
        overall_ok = False

    print("\n" + ("="*60))
    if overall_ok:
        print(f"{OK} ALLE SMOKE-CHECKS BESTANDEN")
        sys.exit(0)
    else:
        print(f"{FAIL} SMOKE-CHECKS FEHLER – BITTE LOGS PRÜFEN")
        sys.exit(1)

if __name__ == "__main__":
    main()

So nutzt du den Smoke-Check

Datei neben Create.py speichern: smoke_check.py

Ausführen: python smoke_check.py

Exit-Code 0 = alles ok; 1 = ein Check ist fehlgeschlagen (Konsole zeigt, welcher).



---

Akzeptanz-Definition (Definition of Done)

Alle Epics A–I erfüllt; smoke_check.py läuft grün (Exit-Code 0).

Generierte Dateien (Markdown, DOCX, optional PDF) zeigen:

Komma-Dezimaltrennung, keine wissenschaftliche Notation.

Korrekte Stellenwerttabelle (11 Spalten) im Lösungsteil.

Gleichungen zeigen konsistente Variable (x standard; bei Bedarf n).

ASCII-Skizzen/Codeblöcke sind unverändert (kein „Beautify“).

Einheiten sind sinnvoll gerundet und formatiert.

