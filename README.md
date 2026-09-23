# Base Converter / 进制转换器

English | [简体中文](README.zh-CN.md)

A small tkinter tool with two tabs, one for base conversion and one for an ASCII table. Bilingual UI, standard library only.

## Base conversion

Type in the box and the conversion happens as you type. Binary, octal, decimal and hexadecimal results sit side by side.

Copy a result by clicking the button on its row, or by clicking the number itself. On success the button turns into ✓ and the title area shows "Copied Binary".

The input side is forgiving, so a typo is easy to pin down.

- Binary gets a space every four bits, which keeps long values readable
- Negatives are shown as sign + magnitude, so -5 reads -101 / -5 / -5, not two's complement
- An invalid character is named, e.g. "G" is not a valid hexadecimal digit; with an empty box the characters the current base accepts are shown
- The 0x41, 0b1010 and 0o17 prefixes are accepted, as are 1_000 and 1111 1111, so binary copied out of this tool can be pasted straight back in
- Up to 10000 characters, with a message beyond that; a long result is only truncated on screen, copying still yields the full value

## ASCII table

The table covers 0 to 127. The header stays in place while the body scrolls.

- Type a character and its codes appear on the right; several characters are listed one by one
- Type a decimal code and the character appears, control codes written out as NUL, LF and friends
- Characters, code values and the description column are all searchable, and the hit count is shown
- A prefixed query is limited to the matching column: 0x41 only matches the hex column, 0b1010 only the binary one
- Esc clears the search box, and Esc on the converter tab clears the input

## Running

    python main.py

Or double-click `启动 Start.bat`, which tries `pyw -3`, `pythonw`, `py -3` and `python` in turn, and points you back to this file if none of them exists.

Python 3.6+ is required. tkinter ships with Python and there is nothing to install with pip. The whole program is the single file main.py, so it runs wherever you copy it.

## Notes

The UI language follows the system: Chinese on a Chinese system, English anywhere else. The button in the top right switches at any time, and the table's description column follows along. On a HiDPI screen the window and its fonts stay sharp; on a small screen the window shrinks to fit. Searching and switching languages only update the parts of the table that changed instead of rebuilding it.

To add a language, drop another dictionary into `TR` and add that language's base names to `ADJ`.

## Files

    main.py           the program
    启动 Start.bat    launcher
    .gitignore
    README.md         this file
    README.zh-CN.md   Chinese version
