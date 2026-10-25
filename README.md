# BaseConverter

A desktop utility for numeral-base conversion, ASCII character lookup and IPv4
subnet calculation. The repository contains two editions that share one logic
core and are stored in separate folders:

| Edition | Look | Entry point |
| ------- | ---- | ----------- |
| **Main visual edition** | Frameless, Liquid-Glass-inspired PySide6/QML interface with live backdrop blur, animated tab indicator, glass cards and a custom title bar | `主版本_Main/main.py` · `主版本_Main/启动_Start.bat` |
| **Single-file edition** | Compact tkinter interface using only the Python standard library | `单文件版本_SingleFile/main.py` · `单文件版本_SingleFile/单文件启动_SingleFileStart.bat` |

English | [简体中文](README.zh-CN.md)

## Downloads

Published builds are attached to the repository's
[Releases](https://github.com/XIAO-LIZE/Base-Converter/releases) page. GitHub's
"Download ZIP" command downloads the complete source, which contains both
editions; use a release asset when only one edition is needed.

| Requirement | Release asset |
| ----------- | ------------- |
| Single-file edition, no Python required | `BaseConverter-SingleFile-Windows.exe` |
| Main visual edition, no Python required | `BaseConverter-Glass-Windows.zip` (extract, then run `BaseConverter-Glass.exe`) |
| Single-file source only | `BaseConverter-SingleFile-Source.zip` |
| Main visual source only | `BaseConverter-Main-Source.zip` |

The `.bat` launchers and source files require Python. The published Windows
assets bundle Python; the visual edition also bundles Qt/PySide6.

Source-only archives include the shared `core/` folder. After extracting one,
install the visual dependencies with
`python -m pip install -r "主版本_Main/requirements.txt"` and run
`python "主版本_Main/main.py"`; the single-file edition runs with
`python "单文件版本_SingleFile/main.py"`.

## Features

Both editions share the same core behaviour:

- Live conversion between binary, octal, decimal and hexadecimal
- ASCII table for codes 0–127 with character/code lookup and column-aware search
- IPv4 address and subnet calculator: dotted, integer, hexadecimal and binary forms, prefix/mask parsing, network, broadcast, host range and address classification
- Runtime language switching between Simplified Chinese and English
- Copy-to-clipboard with status feedback
- Shared parsing, formatting and validation from `core/`, so both editions return identical results; labels, hints and error wording for equivalent actions are kept aligned

Edition-specific:

- **Main visual edition**: live backdrop blur on glass panels, rounded glass cards, frameless custom title bar with drag/resize support, animated tab selection, hover feedback, explicit Clear buttons for ASCII lookups
- **Single-file edition**: compact window, standard-library only, fixed header table with adaptive columns, animated tab underline and startup fade
- Windows integration: application icon and AppUserModelID; the single-file edition additionally requests a dark native title bar and rounded window corners through DWM

## Requirements

| | Main visual edition | Single-file edition |
| --- | --- | --- |
| Python | 3.9 or newer | 3.8 or newer |
| GUI toolkit | PySide6 6.8+ (Qt 6) | tkinter (included with the official Python installers) |
| Third-party packages | `PySide6` | none |
| Operating system | Windows 10/11 recommended; Qt 6 is cross-platform | Windows/macOS/Linux |

The single-file edition has no `pip install` step. The main visual edition needs
the Qt runtime; install it with:

```bash
python -m pip install -r "主版本_Main/requirements.txt"
```

## Running from source

### Single-file edition (tkinter)

```bash
python "单文件版本_SingleFile/main.py"
```

On Windows, double-click `单文件版本_SingleFile/单文件启动_SingleFileStart.bat`. It probes
`py`, `python`, `pyw` and `pythonw` for Python 3.8+ with tkinter and can install
Python through winget when none is usable. Pass `--auto` to skip confirmation
prompts.

### Main visual edition (PySide6 + QML)

```bash
python -m pip install -r "主版本_Main/requirements.txt"
python "主版本_Main/main.py"
```

On Windows, double-click `主版本_Main/启动_Start.bat`. It selects a Python
3.9+ interpreter that already has PySide6; if the dependency is missing, it
offers to run `pip install -r requirements.txt` from the main visual edition
folder. Pass `--auto` to accept the prompt automatically.

Keyboard shortcuts in the visual edition: `Ctrl+L` switches language.

## Interface

### Converter

Select the source base, then type a value. The other three bases update on
every keystroke.

Accepted input:

- Digits valid for the selected base (binary `0-1`, octal `0-7`, decimal `0-9`, hexadecimal `0-9 A-F`)
- Base prefixes: `0b`, `0o`, `0x`
- `_` and spaces as digit separators, e.g. `1_000` or `1111 1111`
- A leading `+` or `-` sign
- Up to 10,000 characters

Negative values are rendered as sign plus magnitude (`-5` → `-101`, `-5`,
`-5`, `-5`); two's complement is not used. Binary results are grouped in
nibbles. Long values wrap to the available width; the complete value is always
kept for copying. In the visual edition each result has its own Copy button.

### ASCII table

The table covers codes 0–127 and keeps its header visible while the body
scrolls.

- **Character**: shows the code values of the entered character. Multiple characters are listed individually (up to eight before the list is abbreviated). A Clear button next to the field empties it.
- **Decimal code**: shows the character for a decimal code in the range 0–127. Control characters are written as mnemonics in the table and as escape sequences in the lookup result. A Clear button next to the field empties it.
- **Search**: matches character, code values and descriptions. A prefixed query is limited to one column: `0x41` matches the hexadecimal column, `0o101` the octal column, `0b1000001` the binary column, and `#41` the hexadecimal column. The match count is shown next to the field; Show all clears the search and restores the table.
- Esc clears the focused field.

### IPv4

Enter an address, optionally followed by a prefix length or subnet mask. The
tab accepts:

| Form | Example |
| ---- | ------- |
| Dotted decimal | `192.168.1.10` |
| CIDR | `192.168.1.10/24` |
| Address and dotted mask | `192.168.1.10 255.255.255.0` |
| Address and dotted mask with slash | `192.168.1.10/255.255.255.0` |
| Dotted binary (8 bits per octet) | `11000000.10101000.00000001.00001010` |
| Grouped binary | `11000000 10101000 00000001 00001010` |
| Decimal integer | `3232235786` |
| Hexadecimal | `0xC0A8010A` |
| Binary | `0b11000000101010000000000100001010` |

The address representation reports dotted decimal, 32-bit unsigned decimal,
hexadecimal, binary and address classification. When a prefix length or mask is
supplied, subnet information additionally reports the subnet mask, wildcard
mask, network address, broadcast address, usable address range, usable address
count and total number of addresses.

Subnet rules:

- Prefix omitted: the address is treated as a single host; subnet fields are not calculated.
- `/31`: both addresses are usable, following RFC 3021 point-to-point links.
- `/32`: a single host route with one usable address.

Address classification follows RFC 1122 (unspecified, loopback), RFC 1918
(private), RFC 6598 (carrier-grade NAT), RFC 3927 (link-local), RFC 6890 (IETF
protocol assignments), RFC 5737 (documentation), RFC 2544 (benchmarking),
RFC 5771 (multicast) and RFC 1112 (reserved). All other addresses are reported
as public.

## Architecture

`core/` contains all UI-independent logic. Both editions import the same
modules, so a feature added there behaves identically in the tkinter and the
Qt interface:

```
core/
├── bases.py         base parsing/formatting, prefixes, error codes
├── ascii_data.py    ASCII table data + column-aware search
└── ipv4.py          IPv4 parsing, subnet arithmetic and scope classification
```

Errors are returned as `(code, params)` tuples rather than localized strings.
Each UI maps them to its own text, which keeps localization in the interface
layer and results in one source of truth. Both editions use the same labels,
hints and error wording for equivalent actions.

The "single-file" name refers to the small tkinter edition. Its source imports
the shared `core/` package, so source distributions contain
`单文件版本_SingleFile/` and `core/`; the packaged Windows executable is a
single file.

### Implementation notes

- **Single-file edition**: the ASCII table is a pool of canvas text items
  toggled during search; result rows measure available width/height and wrap or
  truncate while keeping the complete value for copying. DPI awareness is
  requested per monitor (v2), then system-wide.
- **Main visual edition**: QML renders the UI. Glass panels capture the
  background beneath them with `ShaderEffectSource`, blur it with
  `GaussianBlur`, mask it with `OpacityMask`, and add a translucent tint and
  specular border. The window is frameless with a custom title bar and edge
  resize handles. `QQuickStyle.setStyle("Basic")` keeps the Qt Quick Controls
  styling consistent across platforms.
- Both editions expose the same IPv4 and ASCII behaviour; only the widget
  toolkit and visual treatment differ.

## Project layout

```
单文件版本_SingleFile/                    single-file edition folder
├── main.py                              tkinter entry point
├── icon.ico                             executable icon
└── 单文件启动_SingleFileStart.bat        Windows launcher (Chinese + English label)

主版本_Main/                               main visual edition folder
├── main.py                              PySide6 entry point
├── backend.py                           QObject bridge between QML and core
├── requirements.txt                     PySide6 dependency
├── icon.png / icon.ico                  window and executable icon
├── 启动_Start.bat                        Windows launcher (Chinese + English label)
└── qml/
    ├── Main.qml                         window, background, tabs, footer
    ├── components/                      GlassCard, GlassField, GlassButton, Segmented
    └── pages/                           ConverterPage, AsciiPage, Ipv4Page

core/                                    shared logic (no GUI imports)
tests/test_core.py                       unit tests for the shared core
tools/build_light.py                     PyInstaller build for the single-file edition
tools/build_glass.py                     PyInstaller onedir build for the visual edition
.github/workflows/build-release.yml      CI: build and attach both editions to a release
dist/                                    generated portable builds (ignored by git)
README.md / README.zh-CN.md              user documentation
CONTRIBUTING.md / CONTRIBUTING.zh-CN.md  build and release guide
```

Edition folders and launchers use underscores instead of spaces in their names
so they work more reliably in shells, scripts and CI systems. Chinese
characters remain in the names and are handled as UTF-8 paths on modern
Windows; the `dist/` executable names are ASCII only.

## Compatibility and limitations

- IPv4 only; IPv6 parsing and subnetting are not implemented.
- ASCII covers 7-bit codes 0–127; wider code pages are out of scope.
- Negative numbers are sign plus magnitude, not two's complement.
- The single-file edition opens at 760×800 logical pixels (minimum 620×680).
- The main visual edition opens at 1180×940 logical pixels (minimum 980×820).
- Backdrop blur requires a GPU/compositing environment. If effects are
  unavailable, the translucent cards still render from their tint colour.
- The visual edition depends on PySide6, which is licensed under LGPLv3/GPL.
  When redistributing a bundled build, include the Qt/PySide6 licence notices
  and keep the Qt libraries replaceable as required by the LGPL.
- The visual edition writes a diagnostic startup log to
  `%TEMP%\BaseConverter-Glass.log`. It does not access the network and does not
  write configuration files.

## Troubleshooting

- **Tk is missing**: use `单文件版本_SingleFile/单文件启动_SingleFileStart.bat`, or repair Python:
  on Windows re-run the installer and enable "tcl/tk and IDLE";
  Debian/Ubuntu `python3-tk`; Fedora `python3-tkinter`; Arch `tk`; macOS use
  python.org or `brew install python-tk`.
- **PySide6 is missing**: run
  `python -m pip install -r "主版本_Main/requirements.txt"`, then
  `python "主版本_Main/main.py"`. The visual launcher offers the same installation.
- **QML window is blank or effects are missing**: install the full PySide6
  package (including Qt Quick Effects and Qt5Compat), update the graphics
  driver, and try `set QT_QUICK_BACKEND=software` before launching. Software
  rendering may reduce blur quality.
- **Inspect the single-file runtime**: `python "单文件版本_SingleFile/main.py" --check`
  prints Python, Tk, platform and interpreter details.
- **Launcher cannot find Python**: install Python 3.9+ from python.org and
  enable "Add python.exe to PATH"; the single-file launcher can also install
  Python through winget.

## Extending

1. Add shared logic and tests in `core/` and `tests/`.
2. Wire it into the tkinter UI (`单文件版本_SingleFile/main.py`, `TR` dictionaries).
3. Wire it into the QML UI (`主版本_Main/backend.py` strings/slots and the relevant
   QML page).
4. Run `python -m unittest discover -s tests`, then smoke-test both editions.

- **Add a language**: add a `TR` dictionary in `单文件版本_SingleFile/main.py`; add a
  `STRINGS` dictionary in `主版本_Main/backend.py`; update `core.bases.BASE_NAMES`
  and, for ASCII control names, `core.ascii_data.EN_CTRL_NAMES`.
- **Add a numeral base**: extend `core/bases.py` (`BASES`, `DIGITS`,
  `DIGSET`, `PREFIX`, `BASE_NAMES`) and both UI base selectors.
- **Add an IPv4 special range**: append an entry to `core.ipv4.IP_SCOPES`
  and add the matching translation key to both UI dictionaries.

## Tests

```bash
python -m unittest discover -s tests
```

## Contributing

Bug reports and pull requests are welcome. Please describe the affected
edition and tab, the input used, and the expected/actual result. Changes that
affect parsing or formatting belong in `core/` and must keep both editions in
sync; include a test for the shared logic.

Build, packaging and release instructions are in
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

This repository does not currently include a license file. Add a license before
redistributing or reusing the code. PySide6/Qt have their own LGPLv3/GPL terms;
see the Qt for Python licensing documentation before distributing bundled
builds.
