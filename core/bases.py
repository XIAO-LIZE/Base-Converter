"""Numeral-base conversion primitives shared by both UI versions.

The functions here are UI-agnostic and standard-library only.  Errors are
returned as ``(code, params)`` tuples so that each UI can localize them.
"""
from typing import Dict, Optional, Tuple

BASES = (2, 8, 10, 16)
DIGITS = {2: "01", 8: "01234567", 10: "0123456789", 16: "0123456789abcdef"}
DIGSET = {2: "0-1", 8: "0-7", 10: "0-9", 16: "0-9 A-F"}
PREFIX = {2: "0b", 8: "0o", 10: "", 16: "0x"}
BASE_NAMES = {
    "zh": {2: "二进制", 8: "八进制", 10: "十进制", 16: "十六进制"},
    "en": {2: "binary", 8: "octal", 10: "decimal", 16: "hexadecimal"},
}
MAX_INPUT = 10_000

Error = Tuple[str, Dict[str, object]]


def parse_number(raw: str, base: int) -> Tuple[Optional[int], Optional[Error]]:
    """Parse one numeric input; return (value, error) with an empty box as (None, None)."""
    if not raw:
        return None, None
    s = raw.replace("_", "").replace(" ", "")
    sign = ""
    if s[:1] in "+-":
        sign, s = s[0], s[1:]
    low = s.lower()
    prefix = PREFIX[base]
    if prefix and low.startswith(prefix):
        s, low = s[2:], low[2:]
    if not s:
        return None, ("neednum", {})
    if len(s) > MAX_INPUT:
        return None, ("toolong", {"n": MAX_INPUT})
    for ch in s:
        if ch.lower() not in DIGITS[base]:
            return None, ("badchar", {"c": ch, "base": base})
    try:
        return int(sign + low, base), None
    except ValueError:
        return None, ("err", {})


def format_value(value: int, base: int) -> str:
    """Format a value for display; negatives keep their sign (no two's complement)."""
    sign = "-" if value < 0 else ""
    n = abs(value)
    if base == 2:
        digits = f"{n:b}"
        groups = []
        for i, ch in enumerate(reversed(digits)):
            if i and i % 4 == 0:
                groups.append(" ")
            groups.append(ch)
        digits = "".join(reversed(groups))
    elif base == 8:
        digits = f"{n:o}"
    elif base == 10:
        digits = str(n)
    else:
        digits = f"{n:X}"
    return sign + digits


def digit_count(text: str) -> int:
    """Count numeric digits, ignoring sign and binary group separators."""
    return len(text.replace(" ", "").replace("-", ""))
