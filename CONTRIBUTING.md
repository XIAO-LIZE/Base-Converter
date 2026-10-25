# Contributing and releasing

English | [简体中文](CONTRIBUTING.zh-CN.md)

This document is for developers and maintainers. End users do not need anything
on this page: they only need a release asset from the
[Releases](https://github.com/XIAO-LIZE/Base-Converter/releases) page.

## Development setup

- Main visual edition: Python 3.9+, `pip install -r "主版本_Main/requirements.txt"`
- Single-file edition: Python 3.8+ with tkinter
- Shared core: standard library only

Run the editions from the repository root:

```bash
python "主版本_Main/main.py"
python "单文件版本_SingleFile/main.py"
```

Run the shared tests:

```bash
python -m unittest discover -s tests
```

The Windows launchers in each edition folder locate Python and the required
dependencies for source checkouts.

## Portable builds

Install PyInstaller, then build one or both editions:

```bash
python -m pip install pyinstaller
python tools/build_glass.py
python tools/build_light.py
```

Outputs:

- `dist/BaseConverter-Glass/` — onedir build with the Qt runtime; zip the whole
  folder. It is typically 300–450 MB.
- `dist/BaseConverter-SingleFile.exe` — one-file build with the Python runtime.

Neither build requires Python or PySide6 on the target machine.

## Publishing a release

The workflow in `.github/workflows/build-release.yml` builds both editions on
Windows and attaches four assets to a GitHub Release.

Commit and push the workflow before creating the tag:

```bash
git add .
git commit -m "Release v1.0.0"
git tag v1.0.0
git push origin master --tags
```

Release assets created by the workflow:

- `BaseConverter-SingleFile-Windows.exe`
- `BaseConverter-Glass-Windows.zip`
- `BaseConverter-SingleFile-Source.zip`
- `BaseConverter-Main-Source.zip`

To test the build without publishing a release, run the workflow manually from
the Actions tab. The same four files are then available as workflow artifacts;
those artifacts are for verification, not for end-user distribution.

## Contribution notes

Changes to parsing, formatting, validation or IPv4 logic belong in `core/` and
must keep both editions in sync. Add a test under `tests/` for shared logic, run
the test suite, and smoke-test both editions before opening a pull request.
