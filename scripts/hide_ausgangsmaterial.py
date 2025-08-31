import os
import platform
import subprocess
from pathlib import Path


def hide_path(path: Path) -> Path:
    """Hide the given path and restrict permissions."""
    system = platform.system()
    if system == "Windows":
        subprocess.run(["attrib", "+h", str(path)], check=True)
        subprocess.run(["icacls", str(path), "/inheritance:r"], check=True)
        subprocess.run(
            ["icacls", str(path), "/grant:r", f"{os.getlogin()}:F"], check=True
        )
    elif system == "Darwin":
        subprocess.run(["chflags", "hidden", str(path)], check=True)
        path.chmod(0o700)
    else:  # Linux and other Unix
        path.chmod(0o700)
        if not path.name.startswith("."):
            hidden = path.with_name("." + path.name)
            path.rename(hidden)
            path = hidden
    return path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / "Ausgangsmaterial"
    if not target.exists():
        print("No Ausgangsmaterial directory found; nothing to hide.")
        return
    new_path = hide_path(target)
    print(f"Ausgangsmaterial hidden at {new_path}")


if __name__ == "__main__":
    main()
