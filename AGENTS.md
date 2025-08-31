Es muss mit black formatiert werden.
Der Ordner "Ausgangsmaterial" und seine Datei "AGENTS.py" sind hochsensibel und dürfen nicht in das Repository gelangen.
Nutze das Skript scripts/hide_ausgangsmaterial.py zum Verbergen und setze die pre-commit Hooks über `.pre-commit-config.yaml`, um versehentliche Commits zu verhindern.

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix, --unsafe-fixes]
      - id: ruff-format
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/asottile/pyupgrade
    rev: v3.19.0
    hooks:
      - id: pyupgrade
        args: [--py312-plus]
  - repo: https://github.com/PyCQA/autoflake
    rev: v2.3.1
    hooks:
      - id: autoflake
        args: [--in-place, --remove-all-unused-imports, --remove-unused-variables]
  - repo: https://github.com/PyCQA/docformatter
    rev: v1.7.5
    hooks:
      - id: docformatter
        args: [--in-place, --wrap-summaries=88, --wrap-descriptions=88]
  - repo: https://github.com/PyCQA/eradicate
    rev: v2.3.0
    hooks:
      - id: eradicate
        args: [--in-place]

---

AGENTS.md — Code-Qualität & Auto-Modernisierung (Windows 11, Python)

Zweck

Dieser Agent verbessert Python-Code vollautomatisch, ohne CLI-Aufrufe, durch:

Formatierung, Import-Normalisierung, Aufräumen

Syntax-Modernisierung, strukturierte Refactorings

Docstring-Korrekturen

Typ-Annotationen (halbautomatisch, wenn Laufzeitdaten vorliegen)

Wartbarkeits-Metriken & Vorschläge


Explizit ausgeschlossen: Security-/Vulnerability-Themen (z. B. bandit).
Zielumgebung: Windows 11, Python ≥ 3.10 (empfohlen 3.11/3.12).


---

Pipeline (Reihenfolge ist bindend)

1. Parsing & Kontext

Dateien sammeln (.py, optional: aus Notebooks extrahierte Codezellen).

Dateiende/Encoding erkennen (UTF-8 erzwingen, \n normalisieren).



2. Syntax-Modernisierung (verlustfrei)

LibCST-basierte Codemods (z. B. .format/% → f-Strings, pathlib-Ersetzungen, Literale, Walrus-Operator, Pattern-Matching wo sinnvoll). 



3. Formatierung & Importe

Black für konsistente Formatierung. 

isort für deterministische Import-Blöcke (Black-Profil). 



4. Aufräumen (totes/ungenutztes)

autoflake: ungenutzte Variablen/Imports entfernen. 

Optional: pycln/unimport (feiner bei Imports). 

eradicate-Logik gegen auskommentierten Altcode (oder äquivalente Regel). 

Vulture für Vorschlagsliste toter Codepfade (keine Auto-Löschung). 



5. Docstrings

docformatter (PEP-257-konform). 



6. Typing (optional, halb-auto)

MonkeyType/PyAnnotate: aus Laufzeit-Traces Stubs/Annotations generieren; Agent bietet Patches an, die der Nutzer akzeptiert. 



7. Qualitätsbericht & Metriken

Radon: Cyclomatic/Halstead/MI erfassen, Hotspots benennen. 

(Optional) Wily: historische Trend-Analyse (nur Vorschläge). 



> Hinweis zu Ruff: Ruff vereint Lint + Formatter + zahlreiche Auto-Fixes; als Bibliothek ist es v. a. konfigurierbar/skriptbar und dient hier als Zusatz-Validierung (ohne CLI), nicht als Primary-Formatter. 



---

Verhaltensregeln (LLM-Agent)

Kein CLI. Nur Python-APIs importieren und auf Strings/Dateiinhalte anwenden.

Idempotenz. Mehrfaches Ausführen darf keinen neuen Diff erzeugen.

Kleine, sichere Schritte. Erst rewrite-to-buffer, dann syntaktisch validieren, dann speichern.

Konfliktlösung. Bei kollidierenden Format-Entscheidungen gilt: LibCST-Rewrite → Black → isort → autoflake → docformatter.

Notebooks. Codezellen via nbformat extrahieren, Pipeline auf Zell-Quelltext anwenden, danach zurückschreiben (Outputs unverändert lassen).

Bericht. Am Ende je Datei: angewandte Schritte, Statistiken, Breaking-Change-Risiken, empfohlene manuelle Nacharbeiten.



---

Referenz-Implementierung (API-Skizzen)

> Alle Snippets arbeiten in-memory auf Strings und schreiben nur bei Erfolg zurück. Pfadnormalisierung: pathlib.Path.



0) Utilities

from pathlib import Path
def read_text(p: Path) -> str:
    data = p.read_bytes()
    try: return data.decode("utf-8")
    except UnicodeDecodeError: return data.decode("utf-8", errors="replace")

def write_text_atomic(p: Path, s: str) -> None:
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(s, encoding="utf-8", newline="\n")
    tmp.replace(p)

1) LibCST-Transform (Beispiel: .format → f-Strings)

import libcst as cst
from libcst import matchers as m

class FormatToF(cst.CSTTransformer):
    def leave_Attribute(self, o, u):
        # Minimalbeispiel: "'.{x}'.format(x=val)" → f"…{val}…"
        return o  # In der echten Implementierung mit parse/Template-Builder

def libcst_apply(code: str) -> str:
    m = cst.MetadataWrapper(cst.parse_module(code))
    new = m.module.visit(FormatToF())
    return new.code

> LibCST bewahrt Whitespaces/Kommentare exakt und eignet sich für sichere Refactorings. 



2) Black (API)

import black
def black_apply(code: str) -> str:
    mode = black.Mode()
    return black.format_str(code, mode=mode)

> „Uncompromising“ Formatter; deterministisch. 



3) isort (API)

import isort
def isort_apply(code: str) -> str:
    return isort.code(code, profile="black")

> Sortiert & gruppiert Imports, Black-kompatibel. 



4) Aufräumen: autoflake (+ optional pycln)

import autoflake
def autoflake_apply(code: str) -> str:
    return autoflake.fix_code(
        code,
        remove_all_unused_imports=True,
        remove_unused_variables=True,
        expand_star_imports=True,
    )

> Entfernt ungenutzte Variablen/Imports. 


(Optional, falls feiner gebraucht): pycln/unimport als Library aufrufen. 

5) Auskommentierten Altcode entfernen (heuristisch)

from eradicate import eradicate
def eradicate_apply(code: str) -> str:
    # entfernt kommentierten Code, belässt echte Kommentare
    return eradicate(code, aggressive=True)

> Entspricht Ruff-Regel ERA001 / commented-out-code. 



6) Docstrings (PEP-257)

from docformatter import format_code
def docformatter_apply(code: str) -> str:
    return format_code(code, description_wrap_length=88, summary_wrap_length=88)

> Formatiert Docstrings gemäß PEP-257. 



7) Typing-Vorschläge (halb-auto)

MonkeyType sammelt zur Laufzeit Typen und erzeugt Stubs / Patch-Vorschläge. Der Agent:

1. zeigt die Diffs an,


2. wendet sie nur nach Zustimmung an. 



---

Notebook-Unterstützung (ohne CLI)

import nbformat
from nbformat import NotebookNode

def process_notebook(path: Path) -> None:
    nb: NotebookNode = nbformat.read(path, as_version=4)
    changed = False
    for cell in nb.cells:
        if cell.get("cell_type") == "code" and isinstance(cell.get("source"), str):
            src = cell["source"]
            new = libcst_apply(src)
            new = black_apply(new)
            new = isort_apply(new)
            new = autoflake_apply(new)
            new = docformatter_apply(new)
            if new != src:
                cell["source"] = new; changed = True
    if changed:
        nbformat.write(nb, path)

> (Alternative/Ergänzung via CLI wäre nbQA; hier nicht verwendet, nur als Referenz erwähnenswert.) 



---

Qualitätsbericht (Auszug)

Nach jedem Lauf pro Datei:

Änderungen: Formatierung, Imports, entfernte Unuseds, Docstring-Wraps

Metriken (Radon): CC/Halstead/MI vor/nachher, neue Hotspots (Funktionen > CC 10). 

Refactor-Backlog: Vulture-Funde, nicht auto-behebbare Muster, empfohlene LibCST-Codemods. 



---

Erweiterungen (optional, nur Suggestions)

Rope/Bowler/RedBaron für größere API-Renames/Extract-Method u. Ä. (programmatische Refactorings). 

mdformat für Markdown-Dateien (README/Docs) via Python-API. 

pyproject-fmt und toml-sort für TOML-Dateien (falls programmatic API genutzt werden kann; sonst weglassen). 



---

Minimaler Orchestrator (alles in-memory, keine CLIs)

from pathlib import Path

TRANSFORMS = [
    libcst_apply,
    black_apply,
    isort_apply,
    autoflake_apply,
    docformatter_apply,
    eradicate_apply,
]

def process_file(p: Path) -> None:
    code = read_text(p)
    new = code
    for step in TRANSFORMS:
        try:
            new = step(new)
        except Exception:
            # defensiv: bei Fehlern Schritt überspringen, aber nichts kaputt schreiben
            pass
    if new != code:
        write_text_atomic(p, new)

def run(root: Path) -> None:
    for p in root.rglob("*.py"):
        process_file(p)
    for p in root.rglob("*.ipynb"):
        process_notebook(p)


---

Paket-Kurzreferenz

Ruff – sehr schneller Linter + Formatter; viele Auto-Fixes. (Referenz/Validierung) 

Black – kompromissloser Formatter (API: format_str). 

isort – Import-Sortierung (API: isort.code). 

autoflake – entfernt ungenutzte Importe/Variablen (API: fix_code). 

pycln / unimport – Import-Cleaner (optional). 

eradicate – kommentierten Altcode entfernen (oder Ruff-Regel ERA001). 

Vulture – findet toten Code (Vorschläge). 

docformatter – PEP-257-Docstrings. 

LibCST – sichere, verlustfreie Codemods. 

Rope/Bowler/RedBaron – Refactoring-Frameworks. 

MonkeyType/PyAnnotate – Typ-Annotationen aus Laufzeitdaten. 

Radon – Komplexitäts-/Wartbarkeits-Metriken. 

Wily – Komplexität über Git-Historie (Trends). 

mdformat – Markdown-Formatter (API verfügbar). 

pyproject-fmt / toml-sort – TOML-Formatierer (optional). 



---

Qualitäts-Garantien

Syntaktische Korrektheit: Nach jedem Schritt per ast.parse validieren; bei Fehlern Schritt zurückrollen.

Determinismus: Black + isort + idempotente Transformationsreihenfolge. 

Minimale Diffs: Trailing-Comma-Einführung ist optional (CLI-Tool; hier bewusst nicht automatisch). 



---

Änderungsprotokoll

v1.0 (31-Aug-2025): Erstausgabe für Windows 11/Python; reine API-Variante ohne Shell/CLI.



---
