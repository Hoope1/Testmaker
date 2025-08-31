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
