"""ASCII table data and search, shared by both UI versions."""
from typing import Dict, List, Tuple

AsciiEntry = Tuple[int, str, str, str]  # (code, mnemonic, Chinese name, category)


def _build() -> List[AsciiEntry]:
    """Build the ASCII table: (code, mnemonic, Chinese name, category)."""
    table: List[AsciiEntry] = []
    ce = {0: "NUL", 1: "SOH", 2: "STX", 3: "ETX", 4: "EOT", 5: "ENQ", 6: "ACK", 7: "BEL",
          8: "BS", 9: "HT", 10: "LF", 11: "VT", 12: "FF", 13: "CR", 14: "SO", 15: "SI",
          16: "DLE", 17: "DC1", 18: "DC2", 19: "DC3", 20: "DC4", 21: "NAK", 22: "SYN",
          23: "ETB", 24: "CAN", 25: "EM", 26: "SUB", 27: "ESC", 28: "FS", 29: "GS",
          30: "RS", 31: "US"}
    cz = {0: "空字符", 1: "标题开始", 2: "正文开始", 3: "正文结束", 4: "传输结束",
          5: "请求", 6: "确认", 7: "响铃", 8: "退格", 9: "水平制表", 10: "换行",
          11: "垂直制表", 12: "换页", 13: "回车", 14: "移出", 15: "移入",
          16: "数据链路转义", 17: "设备控制1", 18: "设备控制2", 19: "设备控制3",
          20: "设备控制4", 21: "否定确认", 22: "同步空闲", 23: "传输块结束",
          24: "取消", 25: "介质结束", 26: "替换", 27: "转义",
          28: "文件分隔符", 29: "组分隔符", 30: "记录分隔符", 31: "单元分隔符"}
    for i in range(32):
        table.append((i, ce.get(i, "?"), cz.get(i, ""), "c"))
    table.append((32, "SP", "空格", "p"))
    for i in range(33, 127):
        table.append((i, chr(i), "", "p"))
    table.append((127, "DEL", "删除", "c"))
    return table


ADATA = _build()

EN_CTRL_NAMES: Dict[int, str] = {
    0: "Null", 1: "Start of Heading", 2: "Start of Text", 3: "End of Text",
    4: "End of Transmission", 5: "Enquiry", 6: "Acknowledge", 7: "Bell",
    8: "Backspace", 9: "Horizontal Tab", 10: "Line Feed", 11: "Vertical Tab",
    12: "Form Feed", 13: "Carriage Return", 14: "Shift Out", 15: "Shift In",
    16: "Data Link Escape", 17: "Device Control 1", 18: "Device Control 2",
    19: "Device Control 3", 20: "Device Control 4", 21: "Negative Acknowledge",
    22: "Synchronous Idle", 23: "End of Transmission Block", 24: "Cancel",
    25: "End of Medium", 26: "Substitute", 27: "Escape", 28: "File Separator",
    29: "Group Separator", 30: "Record Separator", 31: "Unit Separator",
    32: "Space", 127: "Delete",
}

_PREFIX_COLUMNS = {"0x": 1, "#": 1, "0b": 3, "0o": 2}


def search(entries: List[AsciiEntry], query: str) -> List[AsciiEntry]:
    """Filter the table; a 0x/0b/0o/# prefix restricts the match to one column."""
    q = query.strip().lower()
    if not q:
        return list(entries)
    prefix = ""
    for candidate in _PREFIX_COLUMNS:
        if q.startswith(candidate) and len(q) > len(candidate):
            prefix, q = candidate, q[len(candidate):]
            break
    column = _PREFIX_COLUMNS.get(prefix)
    out = []
    for code, abbr, zh_name, category in entries:
        fields = (
            str(code),
            f"{code:02x}",
            f"{code:03o}",
            f"{code:08b}",
            chr(code).lower() if category == "p" and code != 32 else "",
            abbr.lower(),
            zh_name.lower(),
            EN_CTRL_NAMES.get(code, "").lower(),
        )
        hit = (q in fields[column]) if column is not None else any(q in f for f in fields)
        if hit:
            out.append((code, abbr, zh_name, category))
    return out
