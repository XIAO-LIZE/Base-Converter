"""Build a portable onedir folder for the PySide6 visual edition.

Run from the repository root:

    python -m pip install pyinstaller
    python tools/build_glass.py

The result is dist/BaseConverter-Glass/. Zip that folder and it runs on a
Windows machine without Python or PySide6 installed.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _use_utf8_stdio() -> None:
    """Keep console output readable when paths contain non-ASCII characters."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


def _hide_broken_qml_plugin():
    """PyInstaller scans every QML plugin folder; an incomplete PySide6 install
    can contain a qmldir for a plugin whose DLL was never shipped and abort the
    build. Move such a folder aside for the duration of the build."""
    try:
        import PySide6
        folder = Path(PySide6.__file__).resolve().parent / "qml" / "Qt" / "labs" / "assetdownloader"
        if folder.is_dir() and not (folder / "qmlassetdownloaderprivateplugin.dll").exists():
            target = Path(tempfile.mkdtemp()) / "assetdownloader"
            shutil.move(str(folder), str(target))
            print(f"Temporarily excluded incomplete QML plugin: {folder}")
            return folder, target
    except Exception:
        pass
    return None


def main() -> int:
    _use_utf8_stdio()
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller is not installed. Run:")
        print("  python -m pip install pyinstaller")
        return 1

    qml_dir = ROOT / "主版本_Main" / "qml"
    icon = ROOT / "主版本_Main" / "icon.png"
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean", "--windowed", "--onedir",
        "--name", "BaseConverter-Glass",
        "--icon", str(ROOT / "主版本_Main" / "icon.ico"),
        "--paths", str(ROOT),
        "--add-data", f"{qml_dir}{os.pathsep}qml",
        "--add-data", f"{icon}{os.pathsep}.",
        str(ROOT / "主版本_Main" / "main.py"),
    ]
    print(" ".join(cmd))
    moved = _hide_broken_qml_plugin()
    try:
        result = subprocess.run(cmd, cwd=ROOT)
    finally:
        if moved:
            folder, backup = moved
            shutil.move(str(backup), str(folder))
    if result.returncode:
        return result.returncode
    print()
    print("Portable build ready:")
    print(f"  {ROOT / 'dist' / 'BaseConverter-Glass'}")
    print("Zip that folder and distribute the extracted folder.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
