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
from Create import MathSolver, Schwierigkeit, TestGenerator, fmt

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
    ok &= assert_true(
        "fmt(1234.5, 2, thousand=True) == '1.234,50'",
        fmt(1234.5, 2, True) == "1.234,50",
    )
    ok &= assert_true("fmt(0.125, 3) == '0,125'", fmt(0.125, 3) == "0,125")
    # Keine E-Notation im Format
    samples = [0.00000123, 123456789.0, 12.0, 12.3456]
    for s in samples:
        out = fmt(s, 6)
        ok &= assert_true(f"Keine E-Notation ({s})", "e" not in out.lower(), out)
        ok &= assert_true(
            f"Komma als Dezimaltrennzeichen ({s})", "," in out or out.isdigit(), out
        )
    return ok


def check_rounding_places():
    print("\n[Check] Kaufmännisches Runden & Stellen")
    ok = True
    # Kaufmännisch: 2.5 -> 3.0
    ok &= assert_true(
        "ROUND_HALF_UP bei Einer", MathSolver.round_to_place(2.5, "E") == 3.0
    )
    # Zehner/Hunderter
    ok &= assert_true(
        "Zehner-Rundung 1499.5 -> 1500",
        MathSolver.round_to_place(1499.5, "Z") == 1500.0,
    )
    ok &= assert_true(
        "Hundertstel 1.005 -> 1.01", MathSolver.round_to_place(1.005, "h") == 1.01
    )
    return ok


def check_complete_generation(seed: int, var_symbol: str = "x"):
    print(f"\n[Check] Komplette Generation (Seed={seed}, var='{var_symbol}')")
    gen = TestGenerator(Schwierigkeit.MITTEL, seed=seed, var_symbol=var_symbol)
    test_md, sol_md, details = gen.generate_complete_test()

    ok = True

    # 1) Kein Punkt als Dezimaltrenner innerhalb von Zahlen (Ausnahme: Tausenderpunkt)
    # Heuristik: verbiete Muster \d+\.\d+ (Punkt zwischen Ziffern), erlaube 1.234,56 aber das matchen wir nicht
    bad_decimal_point = re.search(r"\d+\.\d+", test_md + sol_md)
    ok &= assert_true(
        "Kein '.' als Dezimaltrenner",
        bad_decimal_point is None,
        bad_decimal_point.group(0) if bad_decimal_point else "",
    )

    # 2) Keine E-Notation
    ok &= assert_true(
        "Keine E-Notation insgesamt",
        "e+" not in (test_md + sol_md).lower()
        and "e-" not in (test_md + sol_md).lower(),
    )

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
        ok &= assert_true(
            "Tabellenkopf korrekt",
            "| Nr | HT | ZT | T | H | Z | E | , | z | h | t |" in block[0],
        )
        # Datenzeilen prüfen
        data_lines = [
            ln
            for ln in block[1:]
            if not set(ln.strip("|").replace("-", "").split()) <= {""}
        ]
        expected_pipes = 12
        for dl in data_lines:
            count = dl.count("|")
            ok &= assert_true(
                "Zeilenpipe-Anzahl == 12",
                count == expected_pipes,
                f"{dl} -> pipes={count}",
            )

    # 4) Gleichungen: Variable konsistent
    if var_symbol != "x":
        eq_lines_sol = [
            ln
            for ln in sol_md.splitlines()
            if "b.1)" in ln or "b.2)" in ln or ("=" in ln and var_symbol in ln)
        ]
        # Minimalprüfung: Lösungszeilen enthalten var_symbol = ...
        joined_sol = "\n".join(eq_lines_sol)
        ok &= assert_true(
            f"Gleichungs-Lösung nutzt '{var_symbol} = ...'",
            re.search(rf"{re.escape(var_symbol)}\s*=", joined_sol) is not None,
            joined_sol[:120],
        )

    # 5) ASCII/Codeblöcke: bleiben unverändert (strukturcheck)
    # Prüfe, dass Linienzeichen vorkommen und dreifache Backticks Blöcke einschließen
    codeblocks = re.findall(r"```(.*?)```", test_md, flags=re.S)
    ok &= assert_true(
        "Mindestens ein Codeblock vorhanden (ASCII/Skizzen)", len(codeblocks) >= 1
    )
    for cb in codeblocks:
        ok &= assert_true(
            "ASCII-Block enthält Linienzeichen",
            any(ch in cb for ch in ["┌", "┐", "└", "┘", "─", "│", "▲", "◼"]),
        )

    # 6) Einheiten: Stichprobenhaft auf , als Dezimaltrennzeichen prüfen
    unit_samples = re.findall(
        r"\b\d[\d\.\,]*\s?(?:m²|m³|dm³|cm²|cm³|km²|ha|l|ml|cl|dl|kg|g|mg|s|min|h)\b",
        sol_md,
    )
    for us in unit_samples[:10]:
        # wenn Dezimal vorhanden, dann muss ein Komma enthalten sein
        if re.search(r"\d[\,]\d", us) or us.isdigit():
            ok &= True
        else:
            # Fälle wie '10 cm' sind okay; Fälle '10.5 cm' wären falsch
            ok &= assert_true(
                "Einheiten ohne '.' als Dezimaltrenner", "." not in us, us
            )

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

    print("\n" + ("=" * 60))
    if overall_ok:
        print(f"{OK} ALLE SMOKE-CHECKS BESTANDEN")
        sys.exit(0)
    else:
        print(f"{FAIL} SMOKE-CHECKS FEHLER – BITTE LOGS PRÜFEN")
        sys.exit(1)


if __name__ == "__main__":
    main()
