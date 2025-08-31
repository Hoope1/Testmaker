# AGENTS Guidelines — Code-Qualität & Auto-Modernisierung

## Ziel
Automatisierte Verbesserung von Python-Code (Windows 11, Python ≥3.10; empfohlen 3.11/3.12).
Security-Tools (z.B. bandit) sind explizit ausgeschlossen.

## Sensible Daten
- Der Ordner `Ausgangsmaterial` und die Datei `AGENTS.py` dürfen nie im Repo erscheinen.
- Verstecke sie mit `python scripts/hide_ausgangsmaterial.py`.
- Ein Pre-Commit-Hook (`scripts/prevent_ausgangsmaterial_commit.py`) verhindert versehentliche Commits.

## Pre-Commit
Installiere die Hooks aus `.pre-commit-config.yaml` und führe vor jedem Commit
`pre-commit run --all-files` aus.

```yaml
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
  - repo: local
    hooks:
      - id: forbid-ausgangsmaterial
        name: forbid committing Ausgangsmaterial
        entry: python scripts/prevent_ausgangsmaterial_commit.py
        language: system
        pass_filenames: false
```

## Pipeline (Reihenfolge bindend)
1. **Parsing & Kontext** – Dateien sammeln, UTF-8, `\n`-Normalisierung.
2. **Syntax-Modernisierung** – LibCST-Codemods (f-Strings, pathlib, Literale…).
3. **Formatierung & Importe** – Black, isort (Profil *black*).
4. **Aufräumen** – autoflake, eradicate; optional `pycln/unimport`.
5. **Docstrings** – docformatter (PEP 257).
6. **Typing (optional)** – MonkeyType/PyAnnotate aus Laufzeit-Traces.
7. **Qualität** – Radon-Metriken, Vulture-Vorschläge.

## Qualitätsbericht
Pro Datei: Änderungen (Formatierung, Importe, Entferntes, Docstrings) und
Radon-Metriken (CC/Halstead/MI). Refactor-Backlog: Vulture-Funde und Codemod-Vorschläge.

## Erweiterungen (optional)
Rope/Bowler/RedBaron für größere Refactorings, mdformat für Markdown,
pyproject-fmt & toml-sort für TOML.

## Qualitätsgarantien
- `ast.parse` nach jedem Schritt.
- Deterministische Reihenfolge der Tools.
- Trailing Commas optional.

## Änderungsprotokoll
- v1.0 (31-Aug-2025): Erstausgabe, reine API-Variante ohne Shell/CLI.
