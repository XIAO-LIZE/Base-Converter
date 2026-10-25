"""IPv4 parsing and subnet arithmetic shared by both UI versions.

Errors are returned as ``(code, params)`` tuples so that each UI can show
localized text.  The module intentionally uses integer arithmetic instead of
the ipaddress module, so results and validation do not change between Python
releases.
"""
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

Error = Tuple[str, Dict[str, object]]

# First match wins. Values are network address, prefix length and scope key.
IP_SCOPES = (
    (0xFFFFFFFF, 32, "ipScopeLimitedBroadcast"),
    (0x00000000, 8, "ipScopeUnspecified"),
    (0x0A000000, 8, "ipScopePrivate"),
    (0x64400000, 10, "ipScopeCgnat"),
    (0x7F000000, 8, "ipScopeLoopback"),
    (0xA9FE0000, 16, "ipScopeLinkLocal"),
    (0xAC100000, 12, "ipScopePrivate"),
    (0xC0A80000, 16, "ipScopePrivate"),
    (0xC0000000, 24, "ipScopeProtocol"),
    (0xC0000200, 24, "ipScopeDoc"),
    (0xC6336400, 24, "ipScopeDoc"),
    (0xCB007100, 24, "ipScopeDoc"),
    (0xC6120000, 15, "ipScopeBench"),
    (0xE0000000, 4, "ipScopeMulticast"),
    (0xF0000000, 4, "ipScopeReserved"),
)


def dotted(value: int) -> str:
    return ".".join(str((value >> shift) & 0xFF) for shift in (24, 16, 8, 0))


def scope_key(ip: int) -> str:
    """Return the i18n key for the address classification."""
    for base, prefix, key in IP_SCOPES:
        mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
        if ip & mask == base:
            return key
    return "ipScopePublic"


@dataclass(frozen=True)
class Subnet:
    mask: int
    network: int
    broadcast: int
    first: int
    last: int
    hosts: int
    total: int
    note: Optional[str] = None  # "rfc3021" for /31 links


@dataclass(frozen=True)
class Ipv4Result:
    ip: int
    prefix: Optional[int] = None

    @property
    def decimal(self) -> str:
        return str(self.ip)

    @property
    def hex(self) -> str:
        return f"0x{self.ip:08X}"

    @property
    def binary(self) -> str:
        bits = f"{self.ip:032b}"
        return ".".join(bits[i:i + 8] for i in range(0, 32, 8))

    @property
    def dotted(self) -> str:
        return dotted(self.ip)

    @property
    def scope(self) -> str:
        return scope_key(self.ip)

    def subnet(self) -> Optional[Subnet]:
        if self.prefix is None:
            return None
        mask = (0xFFFFFFFF << (32 - self.prefix)) & 0xFFFFFFFF
        network = self.ip & mask
        broadcast = network | (~mask & 0xFFFFFFFF)
        total = 1 << (32 - self.prefix)
        if self.prefix == 32:
            first = last = self.ip
            hosts, note = 1, None
        elif self.prefix == 31:  # RFC 3021 point-to-point link
            first, last = network, broadcast
            hosts, note = 2, "rfc3021"
        else:
            first, last = network + 1, broadcast - 1
            hosts, note = total - 2, None
        return Subnet(mask, network, broadcast, first, last, hosts, total, note)


def _looks_like_mask(tok: str) -> bool:
    if tok.isdigit():
        return len(tok) <= 2 and int(tok) <= 32
    return tok.count(".") == 3


def _parse_ipv4(s: str) -> Tuple[Optional[int], Optional[Error]]:
    if "." in s:
        segs = s.split(".")
        if len(segs) != 4:
            return None, ("addr", {})
        values = []
        for i, seg in enumerate(segs, 1):
            if len(seg) == 8 and all(ch in "01" for ch in seg):
                value = int(seg, 2)  # dotted binary octet
            elif seg.isdigit() and len(seg) <= 3:
                value = int(seg)
            else:
                return None, ("seg", {"n": i, "s": seg})
            if value > 255:
                return None, ("seg_range", {"n": i, "v": value})
            values.append(value)
        return (values[0] << 24) | (values[1] << 16) | (values[2] << 8) | values[3], None

    low = s.lower()
    if low.startswith("0x"):
        try:
            value = int(s[2:], 16)
        except ValueError:
            return None, ("hex", {"s": s})
    elif low.startswith("0b"):
        try:
            value = int(s[2:], 2)
        except ValueError:
            return None, ("bin", {"s": s})
    elif s.isdigit():
        if len(s) == 32 and all(ch in "01" for ch in s):
            value = int(s, 2)  # 32 raw bits
        else:
            value = int(s)
    else:
        return None, ("addr", {})
    if not 0 <= value <= 0xFFFFFFFF:
        return None, ("int", {})
    return value, None


def _parse_mask(tok: str) -> Tuple[Optional[int], Optional[Error]]:
    tok = tok.strip()
    if tok.startswith("/"):
        tok = tok[1:]
    if tok.isdigit():
        prefix = int(tok)
        if 0 <= prefix <= 32:
            return prefix, None
        return None, ("prefix", {})
    if tok.count(".") == 3:
        mask, err = _parse_ipv4(tok)
        if err is None:
            inverse = ~mask & 0xFFFFFFFF
            if (inverse & (inverse + 1)) == 0:  # low-order ones only
                return 32 - bin(inverse).count("1"), None
    return None, ("mask", {"s": tok})


def parse(raw: str) -> Tuple[Optional[Ipv4Result], Optional[Error]]:
    """Parse an address with optional prefix or mask. Empty input gives (None, None)."""
    if not raw:
        return None, None
    if len(raw) > 64:
        return None, ("long", {})
    s = raw.replace("_", "")
    mask_tok = None
    if "/" in s:
        s, mask_tok = s.rsplit("/", 1)
        s = s.strip()
    else:
        tokens = s.split()
        if len(tokens) > 1 and _looks_like_mask(tokens[-1]):
            s, mask_tok = tokens[0], tokens[-1]
        else:
            s = "".join(tokens)  # grouped binary: 11000000 10101000 ...
    ip, err = _parse_ipv4(s)
    if err:
        return None, err
    if mask_tok is None:
        return Ipv4Result(ip), None
    prefix, err = _parse_mask(mask_tok)
    if err:
        return None, err
    return Ipv4Result(ip, prefix), None
