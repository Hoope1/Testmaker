import subprocess
import sys

FORBIDDEN = {"Ausgangsmaterial", "Ausgangsmaterial/AGENTS.py"}


def staged_files() -> set[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--cached", "--diff-filter=AM"],
        capture_output=True,
        text=True,
        check=True,
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def main() -> int:
    staged = staged_files()
    conflicts = [f for f in staged if any(f.startswith(p) for p in FORBIDDEN)]
    if conflicts:
        sys.stderr.write(
            "Ausgangsmaterial contains sensitive data and must not be committed.\n"
        )
        for c in conflicts:
            sys.stderr.write(f" - {c}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
