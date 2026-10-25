"""Build a portable one-file executable for the tkinter single-file edition.

Run from the repository root:

    python -m pip install pyinstaller
    python tools/build_light.py
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller is not installed. Run:")
        print("  python -m pip install pyinstaller")
        return 1

    core_dir = ROOT / "core"
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean", "--windowed", "--onefile",
        "--name", "BaseConverter-SingleFile",
        "--icon", str(ROOT / "单文件版本_SingleFile" / "icon.ico"),
        "--paths", str(ROOT),
        "--add-data", f"{core_dir}{os.pathsep}core",
        str(ROOT / "单文件版本_SingleFile" / "main.py"),
    ]
    print(" ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode:
        return result.returncode
    print()
    print("Portable build ready:")
    print(f"  {ROOT / 'dist' / 'BaseConverter-SingleFile.exe'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
