"""QML backend for the visual (PySide6) edition.

The backend is deliberately thin: parsing and formatting live in ``core`` so
that both the Qt and the Tk editions stay in sync.
"""
import json
import sys
from pathlib import Path

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core import ascii_data, bases, ipv4  # noqa: E402


STRINGS = {
    "zh": {
        "appTitle": "BaseConverter",
        "appSub": "进制转换 · 字符编码 · IPv4 地址",
        "tabs": ["进制转换", "ASCII 码表", "IPv4 地址"],
        "bases": ["二进制", "八进制", "十进制", "十六进制"],
        "inputBase": "输入进制",
        "inputHint": "输入数值",
        "resultTitle": "转换结果",
        "hint": "允许字符：{d}{p}；支持负号",
        "prefixnote": "（前缀 {p}）",
        "badchar": "“{c}”不是有效的{adj}字符",
        "toolong": "输入长度超出上限（{n} 个字符）",
        "needvalue": "请输入数值",
        "neg": "负数按符号与绝对值显示",
        "copy": "复制", "copied": "已复制",
        "asciiLookup": "字符与编码查询",
        "char": "字符", "decCode": "十进制编码",
        "clear": "清空", "all": "显示全部",
        "searchPh": "搜索字符或编码，例如 A、65、0x41",
        "hits": "匹配 {n} / {total} 项",
        "nors": "未找到匹配项",
        "asciiTitle": "ASCII 码表 · 0–127",
        "colDec": "十进制", "colHex": "十六进制", "colOct": "八进制",
        "colBin": "二进制", "colChar": "字符", "colDesc": "说明",
        "nonascii": "非 ASCII 字符", "chars": "共 {n} 个字符",
        "neednum": "请输入十进制编码", "oor": "编码超出 0–127",
        "ipTitle": "IPv4 地址",
        "ipInput": "IPv4 地址或 CIDR",
        "ipHint": "输入地址、CIDR，或附加点分掩码",
        "ipTotal": "共 {n} 个地址",
        "ipP2P": "（RFC 3021 点对点）",
        "addressRep": "地址表示", "subnetInfo": "子网信息",
        "ipDotted": "点分十进制", "ipDecimal": "十进制整数",
        "ipHex": "十六进制", "ipBinary": "二进制", "ipScope": "地址类型",
        "ipMask": "子网掩码", "ipWildcard": "通配符掩码",
        "ipNetwork": "网络地址", "ipBroadcast": "广播地址",
        "ipHostRange": "可用地址范围", "ipHostCount": "可用地址数",
        "ipScopeLimitedBroadcast": "受限广播地址",
        "ipScopeUnspecified": "本网络 / 未指定（RFC 1122）",
        "ipScopePrivate": "私有地址（RFC 1918）",
        "ipScopeCgnat": "运营商级 NAT（RFC 6598）",
        "ipScopeLoopback": "回环地址（RFC 1122）",
        "ipScopeLinkLocal": "链路本地地址（RFC 3927）",
        "ipScopeProtocol": "IETF 协议保留（RFC 6890）",
        "ipScopeDoc": "文档示例地址（RFC 5737）",
        "ipScopeBench": "基准测试地址（RFC 2544）",
        "ipScopeMulticast": "组播地址（RFC 5771）",
        "ipScopeReserved": "保留地址（RFC 1112）",
        "ipScopePublic": "公网地址",
        "iperrAddr": "无法识别的地址格式",
        "iperrSeg": "第 {n} 段“{s}”无效，应为 0–255 或 8 位二进制",
        "iperrSegRange": "第 {n} 段数值 {v} 超出 0–255",
        "iperrHex": "十六进制数值“{s}”无效",
        "iperrBin": "二进制数值“{s}”无效",
        "iperrPrefix": "前缀长度应为 0–32 的整数",
        "iperrMask": "子网掩码“{s}”无效，需为连续的 1",
        "iperrInt": "IPv4 数值应在 0–4294967295 之间",
        "iperrLong": "输入过长",
        "status": "就绪", "version": "Python 3 · PySide6 · Qt 6",
    },
    "en": {
        "appTitle": "BaseConverter",
        "appSub": "Numeral conversion · Character encoding · IPv4 addressing",
        "tabs": ["Converter", "ASCII Table", "IPv4"],
        "bases": ["Binary", "Octal", "Decimal", "Hexadecimal"],
        "inputBase": "Input base",
        "inputHint": "Enter a value",
        "resultTitle": "Conversion result",
        "hint": "Allowed digits: {d}{p}; a leading minus sign is accepted",
        "prefixnote": " (prefix {p})",
        "badchar": "\"{c}\" is not a valid {adj} digit",
        "toolong": "Input exceeds the {n}-character limit",
        "needvalue": "Enter a numeric value",
        "neg": "Negative values use sign and magnitude",
        "copy": "Copy", "copied": "Copied",
        "asciiLookup": "Character and code lookup",
        "char": "Character", "decCode": "Decimal code",
        "clear": "Clear", "all": "Show all",
        "searchPh": "Search a character or code, e.g. A, 65, 0x41",
        "hits": "{n} of {total} entries",
        "nors": "No matching entries",
        "asciiTitle": "ASCII Table · 0–127",
        "colDec": "DEC", "colHex": "HEX", "colOct": "OCT",
        "colBin": "BIN", "colChar": "Char", "colDesc": "Description",
        "nonascii": "non-ASCII character", "chars": "{n} characters",
        "neednum": "Enter a decimal code", "oor": "Code out of range 0–127",
        "ipTitle": "IPv4 address",
        "ipInput": "IPv4 address or CIDR",
        "ipHint": "Enter an address, CIDR, or a dotted mask",
        "ipTotal": "{n} addresses in total",
        "ipP2P": " (RFC 3021 point-to-point)",
        "addressRep": "Address representation", "subnetInfo": "Subnet information",
        "ipDotted": "Dotted decimal", "ipDecimal": "Decimal integer",
        "ipHex": "Hexadecimal", "ipBinary": "Binary", "ipScope": "Address type",
        "ipMask": "Subnet mask", "ipWildcard": "Wildcard mask",
        "ipNetwork": "Network address", "ipBroadcast": "Broadcast address",
        "ipHostRange": "Usable address range", "ipHostCount": "Usable addresses",
        "ipScopeLimitedBroadcast": "Limited broadcast",
        "ipScopeUnspecified": "This network / unspecified (RFC 1122)",
        "ipScopePrivate": "Private (RFC 1918)",
        "ipScopeCgnat": "Carrier-grade NAT (RFC 6598)",
        "ipScopeLoopback": "Loopback (RFC 1122)",
        "ipScopeLinkLocal": "Link-local (RFC 3927)",
        "ipScopeProtocol": "IETF protocol assignments (RFC 6890)",
        "ipScopeDoc": "Documentation (RFC 5737)",
        "ipScopeBench": "Benchmarking (RFC 2544)",
        "ipScopeMulticast": "Multicast (RFC 5771)",
        "ipScopeReserved": "Reserved (RFC 1112)",
        "ipScopePublic": "Public",
        "iperrAddr": "Unrecognised address format",
        "iperrSeg": "Segment {n} is invalid: {s} (0-255 or 8 binary bits)",
        "iperrSegRange": "Segment {n} value {v} is outside 0-255",
        "iperrHex": "Invalid hexadecimal value: {s}",
        "iperrBin": "Invalid binary value: {s}",
        "iperrPrefix": "Prefix length must be an integer from 0 to 32",
        "iperrMask": "Invalid subnet mask: {s} (must be contiguous ones)",
        "iperrInt": "IPv4 value must be between 0 and 4294967295",
        "iperrLong": "Input is too long",
        "status": "Ready", "version": "Python 3 · PySide6 · Qt 6",
    },
}


class Backend(QObject):
    langChanged = Signal()
    stringsChanged = Signal()
    convChanged = Signal()
    lookupChanged = Signal()
    asciiResult = Signal(str)
    asciiCountChanged = Signal()
    ipChanged = Signal()
    statusChanged = Signal()

    def __init__(self):
        super().__init__()
        self._lang = "zh"
        self._binary = self._octal = self._decimal = self._hex = ""
        self._conv_message = ""
        self._conv_error = False
        self._char_result = ""
        self._char_tone = "ok"
        self._code_result = ""
        self._code_tone = "ok"
        self._ascii_count = ""
        self._ip_rows = []
        self._ip_subnet_rows = []
        self._ip_message = ""
        self._ip_error = False
        self._ip_has_subnet = False
        self._status = STRINGS["zh"]["status"]

    # ---- language ---------------------------------------------------
    @Property(str, notify=langChanged)
    def lang(self):
        return self._lang

    @Property("QVariantMap", notify=stringsChanged)
    def strings(self):
        return STRINGS[self._lang]

    @Slot()
    def toggleLang(self):
        self._lang = "en" if self._lang == "zh" else "zh"
        self._status = STRINGS[self._lang]["status"]
        self.langChanged.emit()
        self.stringsChanged.emit()
        self.statusChanged.emit()

    # ---- converter --------------------------------------------------
    @Property(str, notify=convChanged)
    def binary(self):
        return self._binary

    @Property(str, notify=convChanged)
    def octal(self):
        return self._octal

    @Property(str, notify=convChanged)
    def decimal(self):
        return self._decimal

    @Property(str, notify=convChanged)
    def hexValue(self):
        return self._hex

    @Property(str, notify=convChanged)
    def convMessage(self):
        return self._conv_message

    @Property(bool, notify=convChanged)
    def convError(self):
        return self._conv_error

    def _hint(self, base: int) -> str:
        s = STRINGS[self._lang]
        prefix = bases.PREFIX[base]
        note = s["prefixnote"].format(p=prefix) if prefix else ""
        return s["hint"].format(d=bases.DIGSET[base], p=note)

    @Slot(str, int)
    def convert(self, text: str, base_index: int):
        base = bases.BASES[max(0, min(3, base_index))]
        value, err = bases.parse_number((text or "").strip(), base)
        self._conv_error = bool(err)
        if err:
            code, params = err
            s = STRINGS[self._lang]
            if code == "badchar":
                msg = s["badchar"].format(
                    c=params["c"], adj=bases.BASE_NAMES[self._lang][base])
            elif code == "toolong":
                msg = s["toolong"].format(n=params["n"])
            elif code == "neednum":
                msg = s["needvalue"]
            else:
                msg = s["hint"]
            self._binary = self._octal = self._decimal = self._hex = ""
            self._conv_message = msg
        elif value is None:
            self._binary = self._octal = self._decimal = self._hex = ""
            self._conv_message = self._hint(base)
        else:
            self._binary = bases.format_value(value, 2)
            self._octal = bases.format_value(value, 8)
            self._decimal = bases.format_value(value, 10)
            self._hex = bases.format_value(value, 16)
            s = STRINGS[self._lang]
            self._conv_message = s["neg"] if value < 0 else self._hint(base)
        self.convChanged.emit()

    # ---- ASCII ------------------------------------------------------
    @Property(str, notify=lookupChanged)
    def charResult(self):
        return self._char_result

    @Property(str, notify=lookupChanged)
    def charTone(self):
        return self._char_tone

    @Property(str, notify=lookupChanged)
    def codeResult(self):
        return self._code_result

    @Property(str, notify=lookupChanged)
    def codeTone(self):
        return self._code_tone

    @Property(str, notify=asciiCountChanged)
    def asciiCount(self):
        return self._ascii_count

    def _ascii_json(self, entries) -> str:
        s = STRINGS[self._lang]
        rows = []
        for code, abbr, zh_name, category in entries:
            if self._lang == "zh":
                desc = zh_name if zh_name else (chr(code) if 33 <= code < 127 else "")
            else:
                desc = ascii_data.EN_CTRL_NAMES.get(
                    code, chr(code) if 33 <= code < 127 else "")
            rows.append({
                "code": str(code),
                "hex": f"{code:02X}",
                "oct": f"{code:03o}",
                "bin": f"{code:08b}",
                "char": abbr,
                "desc": desc,
            })
        return json.dumps(rows, ensure_ascii=False)

    @Slot(str)
    def searchAscii(self, query: str):
        entries = ascii_data.search(ascii_data.ADATA, query or "")
        s = STRINGS[self._lang]
        self._ascii_count = s["hits"].format(n=len(entries), total=len(ascii_data.ADATA))
        self.asciiCountChanged.emit()
        self.asciiResult.emit(self._ascii_json(entries))

    @Slot(str)
    def lookupChar(self, text: str):
        s = STRINGS[self._lang]
        text = text or ""
        if not text:
            self._char_result = ""
            self._char_tone = "ok"
        elif len(text) == 1:
            c = ord(text)
            if c <= 127:
                self._char_result = (f"DEC {c} · HEX {c:02X} · OCT {c:03o} · "
                                     f"BIN {c:08b}")
                self._char_tone = "ok"
            else:
                self._char_result = f"U+{c:04X} · {s['nonascii']}"
                self._char_tone = "warn"
        else:
            parts = [f"{ch} → {ord(ch)}" if ord(ch) <= 127 else
                     f"{ch} → U+{ord(ch):04X}" for ch in text[:8]]
            tail = " …" if len(text) > 8 else ""
            self._char_result = (" · ".join(parts) + tail + "   " +
                                 s["chars"].format(n=len(text)))
            self._char_tone = "ok"
        self.lookupChanged.emit()

    @Slot(str)
    def lookupCode(self, text: str):
        s = STRINGS[self._lang]
        text = (text or "").strip()
        if not text:
            self._code_result = ""
            self._code_tone = "ok"
        else:
            try:
                c = int(text)
            except ValueError:
                self._code_result = s["neednum"]
                self._code_tone = "error"
            else:
                if not 0 <= c <= 127:
                    self._code_result = s["oor"]
                    self._code_tone = "error"
                else:
                    rep = repr(chr(c)) if c < 32 or c == 127 else f"'{chr(c)}'"
                    self._code_result = f"{rep} · HEX {c:02X} · BIN {c:08b}"
                    self._code_tone = "ok"
        self.lookupChanged.emit()

    # ---- IPv4 -------------------------------------------------------
    @Property("QVariantList", notify=ipChanged)
    def ipRows(self):
        return self._ip_rows

    @Property("QVariantList", notify=ipChanged)
    def ipSubnetRows(self):
        return self._ip_subnet_rows

    @Property(str, notify=ipChanged)
    def ipMessage(self):
        return self._ip_message

    @Property(bool, notify=ipChanged)
    def ipError(self):
        return self._ip_error

    @Property(bool, notify=ipChanged)
    def ipHasSubnet(self):
        return self._ip_has_subnet

    def _ip_error(self, err) -> str:
        s = STRINGS[self._lang]
        code, params = err
        if code == "seg":
            return s["iperrSeg"].format(n=params["n"], s=params["s"])
        if code == "seg_range":
            return s["iperrSegRange"].format(n=params["n"], v=params["v"])
        if code == "hex":
            return s["iperrHex"].format(s=params["s"])
        if code == "bin":
            return s["iperrBin"].format(s=params["s"])
        if code == "prefix":
            return s["iperrPrefix"]
        if code == "mask":
            return s["iperrMask"].format(s=params["s"])
        if code == "int":
            return s["iperrInt"]
        if code == "long":
            return s["iperrLong"]
        return s["iperrAddr"]

    @Slot(str)
    def parseIp(self, text: str):
        s = STRINGS[self._lang]
        result, err = ipv4.parse((text or "").strip())
        if err:
            self._ip_rows = []
            self._ip_subnet_rows = []
            self._ip_message = self._ip_error(err)
            self._ip_error = True
            self._ip_has_subnet = False
        elif result is None:
            self._ip_rows = []
            self._ip_subnet_rows = []
            self._ip_message = s["ipHint"]
            self._ip_error = False
            self._ip_has_subnet = False
        else:
            self._ip_rows = [
                {"label": s["ipDotted"], "value": result.dotted},
                {"label": s["ipDecimal"], "value": result.decimal},
                {"label": s["ipHex"], "value": result.hex},
                {"label": s["ipBinary"], "value": result.binary},
                {"label": s["ipScope"], "value": s[result.scope]},
            ]
            subnet = result.subnet()
            if subnet:
                host_range = (ipv4.dotted(subnet.first) if subnet.first == subnet.last
                              else f"{ipv4.dotted(subnet.first)} – "
                                   f"{ipv4.dotted(subnet.last)}")
                note = s["ipP2P"] if subnet.note == "rfc3021" else ""
                self._ip_subnet_rows = [
                    {"label": s["ipMask"], "value": ipv4.dotted(subnet.mask)},
                    {"label": s["ipWildcard"], "value": ipv4.dotted(~subnet.mask & 0xFFFFFFFF)},
                    {"label": s["ipNetwork"], "value": ipv4.dotted(subnet.network)},
                    {"label": s["ipBroadcast"], "value": ipv4.dotted(subnet.broadcast)},
                    {"label": s["ipHostRange"], "value": host_range},
                    {"label": s["ipHostCount"], "value": f"{subnet.hosts:,}{note}"},
                ]
                self._ip_message = s["ipTotal"].format(n=f"{subnet.total:,}")
                self._ip_has_subnet = True
            else:
                self._ip_subnet_rows = []
                self._ip_message = s["ipHint"]
                self._ip_has_subnet = False
            self._ip_error = False
        self.ipChanged.emit()

    # ---- misc -------------------------------------------------------
    @Property(str, notify=statusChanged)
    def statusText(self):
        return self._status

    @Slot(str)
    def copy(self, text: str):
        if not text:
            return
        QGuiApplication.clipboard().setText(text)
        self._status = STRINGS[self._lang]["copied"]
        self.statusChanged.emit()
