"""BaseConverter single-file edition -- tkinter interface.

The parsing and formatting logic lives in :mod:`core` at the repository root
and is shared with the PySide6 visual edition (``主版本/``).  The interface is
bilingual (Simplified Chinese / English) and uses only the Python standard
library.
"""
import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import font as tkfont, ttk
from typing import Dict, List, Optional, Tuple

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.bases import (BASE_NAMES, BASES, DIGSET, MAX_INPUT, PREFIX,
                        format_value, parse_number)
from core.ascii_data import ADATA, EN_CTRL_NAMES, search as search_ascii
from core.ipv4 import dotted as dotted_ip, parse as parse_ip_input

APP_NAME = "BaseConverter"
APP_ID = "XiaoLize.BaseConverter"

# 64x64 PNG application icon generated from vector shapes; inlined so that the
# program stays a single, portable file.
ICON_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAACFklEQVR42u2bvS8EQRjGLwqiIkQh"
    "EY3oJER1iUYtCo1SFBpRXqEmIdGdqK6TqEUo6GQbhUKiUUj4D5DzGVww8hQrMWbn9gvv7DyTvMXN"
    "zcy+z2/na+ejVGJgiBXauodGukYXl/omdoOBmcv64NyVkmTwCb7BR/iam/D23rFxFCxNcDODz/A9"
    "tfCW1o7OnvJK1TXhukEDtCQW3z8VnLouPjRoiQ2haOITQyhCtbc1h6YdXlHFh2btGF3s7dOMDpHj"
    "fNHFh2acJ2AC4QsAaPWy+lubgcTp7W9Om38A8EV8aARAAI4AOD5vKD0gjgAkARheuFaz6/dqdedZ"
    "bR01VHDx8WX4jXj8j3SFAgBBlc1HtX/2/k10lCEd0icBIRbA5PKt2j55iyVcN+RDfmcBoDqnEa4b"
    "ynEOQF7i40IQBaBcuYls74hHZ6dXbfxGvC0fynUCQO3w1SgC8TYRITxbfvEA8CZNzuPtJnkw0pvK"
    "ieoUxQCoHrwYe/OkYzvSm0YPlC8agOmtTa/dpXo48pnKEwvAVP3xFrM4YKoFpmYgAsB87SFz24/T"
    "F+A5IgFg+qo7i7gsDsQtkwDYBNgJchjkRIhTYX4M8XOYCyK+LomJ3Rj5q0VR0TtDeS+Lb+w9qbQB"
    "eZ3fGHEWQF5GAL4D4PY4AfwjAO8PSXl/TM77g5LeH5X1/rA0j8vzwgSvzPDSFK/N8eIkr84y+BY+"
    "ATKkofRfSsn/AAAAAElFTkSuQmCC"
)


def _fail_missing_tk(exc: BaseException) -> None:
    """Report a missing Tk toolkit and abort; no GUI can be created."""
    message = (
        f"{APP_NAME} requires Python 3.8 or newer with the Tk GUI toolkit.\n"
        f"Importing tkinter failed: {exc}\n\n"
        "Windows: re-run the Python installer and enable \"tcl/tk and IDLE\".\n"
        "Debian/Ubuntu: sudo apt install python3-tk\n"
        "Fedora: sudo dnf install python3-tkinter\n"
        "Arch: sudo pacman -S tk\n"
        "macOS: install Python from python.org, or run: brew install python-tk"
    )
    try:
        if sys.platform == "win32":
            import ctypes
            user32 = ctypes.windll.user32
            user32.MessageBoxW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p,
                                           ctypes.c_wchar_p, ctypes.c_uint]
            user32.MessageBoxW(None, message, APP_NAME, 0x10)
        else:
            print(message, file=sys.stderr)
    except Exception:
        print(message, file=sys.stderr)
    raise SystemExit(1)


try:
    import tkinter as tk
    from tkinter import font as tkfont, ttk
except ImportError as exc:              # tkinter or the Tcl/Tk runtime is missing
    _fail_missing_tk(exc)


BG       = "#060b14"
SURFACE  = "#0f1623"
SURFACE2 = "#192235"
ACCENT   = "#4da6ff"
SUCCESS  = "#10b981"
WARNING  = "#f59e0b"
DANGER   = "#ef4444"
TEXT     = "#e2e8f0"
TEXT2    = "#8899aa"
BORDER   = "#1e3048"
BASE_ACCENT = {2: SUCCESS, 8: "#3b82f6", 10: "#475569", 16: WARNING}

FT_TTL = ("Microsoft YaHei UI", 20, "bold")
FT_H2  = ("Microsoft YaHei UI", 14, "bold")
FT_BD  = ("Microsoft YaHei UI", 11)
FT_BB  = ("Microsoft YaHei UI", 11, "bold")
FT_SM  = ("Microsoft YaHei UI", 10)
FT_SMB = ("Microsoft YaHei UI", 10, "bold")
FT_ML  = ("Consolas", 16, "bold")
FT_MS  = ("Consolas", 13)
FT_CD  = ("Consolas", 11)
FT_CB  = ("Consolas", 11, "bold")

IP_ROWS = ("ipDotted", "ipDecimal", "ipHex", "ipBinary", "ipScope")
IP_SUB_ROWS = ("ipMask", "ipWildcard", "ipNetwork", "ipBroadcast",
               "ipHostRange", "ipHostCount")
IP_ALL_ROWS = IP_ROWS + IP_SUB_ROWS

WIN_W, WIN_H = 760, 800

TR = {
  "zh": {
    "sub":"进制转换 · 字符编码 · IPv4 地址",
    "src":"输入进制",
    "bases":["二进制","八进制","十进制","十六进制"],
    "res":"转换结果", "err":"输入格式错误",
    "tab1":"进制转换", "tab2":"ASCII 码表", "tab3":"IPv4 地址",
    "sph":"搜索字符或编码，例如 A、65、0x41",
    "atl":"ASCII 码表 · 0–127", "conv":"字符与编码查询",
    "clbl":"字符", "dlbl":"十进制编码", "all":"显示全部", "clear":"清空",
    "DEC":"十进制", "HEX":"十六进制", "OCT":"八进制", "BIN":"二进制",
    "Char":"字符", "Desc":"说明",
    "nors":"未找到匹配项", "trunc":" … {n} 位", "chars":"共 {n} 个字符",
    "neg":"负数按符号与绝对值显示",
    "hint":"允许字符：{d}{p}；支持负号",
    "prefixnote":"（前缀 {p}）",
    "badchar":"“{c}”不是有效的{adj}字符",
    "toolong":"输入长度超出上限（{n} 个字符）",
    "neednum":"请输入十进制编码",
    "needvalue":"请输入数值",
    "hits":"匹配 {n} / {total} 项",
    "copied":"已复制",
    "copy":"复制",
    "nonascii":"非 ASCII 字符", "oor":"编码超出 0–127",
    "iplbl":"IPv4 地址",
    "iphint":"输入地址、CIDR，或附加点分掩码",
    "ipsec1":"地址表示", "ipsec2":"子网信息",
    "ipsubhint":"输入地址、CIDR，或附加点分掩码",
    "ipDotted":"点分十进制", "ipDecimal":"十进制整数", "ipHex":"十六进制",
    "ipBinary":"二进制", "ipScope":"地址类型",
    "ipMask":"子网掩码", "ipWildcard":"通配符掩码",
    "ipNetwork":"网络地址", "ipBroadcast":"广播地址",
    "ipHostRange":"可用地址范围", "ipHostCount":"可用地址数",
    "ipTotal":"共 {n} 个地址", "ipP2P":"（RFC 3021 点对点）",
    "iperrAddr":"无法识别的地址格式",
    "iperrSeg":"第 {n} 段“{s}”无效，应为 0–255 或 8 位二进制",
    "iperrSegRange":"第 {n} 段数值 {v} 超出 0–255",
    "iperrHex":"十六进制数值“{s}”无效",
    "iperrBin":"二进制数值“{s}”无效",
    "iperrInt":"IPv4 数值应在 0–4294967295 之间",
    "iperrPrefix":"前缀长度应为 0–32 的整数",
    "iperrMask":"子网掩码“{s}”无效，需为连续的 1",
    "iperrLong":"输入过长",
    "ipScopeUnspecified":"本网络 / 未指定（RFC 1122）",
    "ipScopePrivate":"私有地址（RFC 1918）",
    "ipScopeCgnat":"运营商级 NAT（RFC 6598）",
    "ipScopeLoopback":"回环地址（RFC 1122）",
    "ipScopeLinkLocal":"链路本地地址（RFC 3927）",
    "ipScopeProtocol":"IETF 协议保留（RFC 6890）",
    "ipScopeDoc":"文档示例地址（RFC 5737）",
    "ipScopeBench":"基准测试地址（RFC 2544）",
    "ipScopeMulticast":"组播地址（RFC 5771）",
    "ipScopeReserved":"保留地址（RFC 1112）",
    "ipScopeLimitedBroadcast":"受限广播地址",
    "ipScopePublic":"公网地址",
  },
  "en": {
    "sub":"Numeral conversion · Character encoding · IPv4 addressing",
    "src":"Input base",
    "bases":["Binary","Octal","Decimal","Hexadecimal"],
    "res":"Conversion result", "err":"Invalid input",
    "tab1":"Converter", "tab2":"ASCII Table", "tab3":"IPv4",
    "sph":"Search a character or code, e.g. A, 65, 0x41",
    "atl":"ASCII Table · 0–127", "conv":"Character and code lookup",
    "clbl":"Character", "dlbl":"Decimal code", "all":"Show all", "clear":"Clear",
    "DEC":"DEC", "HEX":"HEX", "OCT":"OCT", "BIN":"BIN",
    "Char":"Char", "Desc":"Description",
    "nors":"No matching entries", "trunc":" … {n} digits", "chars":"{n} characters",
    "neg":"Negative values use sign and magnitude",
    "hint":"Allowed digits: {d}{p}; a leading minus sign is accepted",
    "prefixnote":" (prefix {p})",
    "badchar":"\"{c}\" is not a valid {adj} digit",
    "toolong":"Input exceeds the {n}-character limit",
    "neednum":"Enter a decimal code",
    "needvalue":"Enter a numeric value",
    "hits":"{n} of {total} entries",
    "copied":"Copied",
    "copy":"Copy",
    "nonascii":"non-ASCII character", "oor":"Code out of range 0–127",
    "iplbl":"IPv4 address",
    "iphint":"Enter an address, CIDR, or a dotted mask",
    "ipsec1":"Address representation", "ipsec2":"Subnet information",
    "ipsubhint":"Enter an address, CIDR, or a dotted mask",
    "ipDotted":"Dotted decimal", "ipDecimal":"Decimal integer", "ipHex":"Hexadecimal",
    "ipBinary":"Binary", "ipScope":"Address type",
    "ipMask":"Subnet mask", "ipWildcard":"Wildcard mask",
    "ipNetwork":"Network address", "ipBroadcast":"Broadcast address",
    "ipHostRange":"Usable address range", "ipHostCount":"Usable addresses",
    "ipTotal":"{n} addresses in total", "ipP2P":" (RFC 3021 point-to-point)",
    "iperrAddr":"Unrecognised address format",
    "iperrSeg":"Segment {n} is invalid: {s} (0-255 or 8 binary bits)",
    "iperrSegRange":"Segment {n} value {v} is outside 0-255",
    "iperrHex":"Invalid hexadecimal value: {s}",
    "iperrBin":"Invalid binary value: {s}",
    "iperrInt":"IPv4 value must be between 0 and 4294967295",
    "iperrPrefix":"Prefix length must be an integer from 0 to 32",
    "iperrMask":"Invalid subnet mask: {s} (must be contiguous ones)",
    "iperrLong":"Input is too long",
    "ipScopeUnspecified":"This network / unspecified (RFC 1122)",
    "ipScopePrivate":"Private (RFC 1918)",
    "ipScopeCgnat":"Carrier-grade NAT (RFC 6598)",
    "ipScopeLoopback":"Loopback (RFC 1122)",
    "ipScopeLinkLocal":"Link-local (RFC 3927)",
    "ipScopeProtocol":"IETF protocol assignments (RFC 6890)",
    "ipScopeDoc":"Documentation (RFC 5737)",
    "ipScopeBench":"Benchmarking (RFC 2544)",
    "ipScopeMulticast":"Multicast (RFC 5771)",
    "ipScopeReserved":"Reserved (RFC 1112)",
    "ipScopeLimitedBroadcast":"Limited broadcast",
    "ipScopePublic":"Public",
  },
}

# column widths are set in pixels in _build_table
_COLS = ("DEC", "HEX", "OCT", "BIN", "Char")

# label on the language toggle: the language you would switch to
LANG_LABEL = {"zh": "EN", "en": "中"}


def system_lang() -> str:
    """Return "zh" on Chinese systems and "en" everywhere else."""
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        v = os.environ.get(var, "").lower()
        if v and v not in ("c", "posix"):
            return "zh" if v.startswith("zh") else "en"
    if sys.platform == "win32":
        try:
            import ctypes
            lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            return "zh" if (lcid & 0x3ff) == 0x04 else "en"
        except Exception:
            pass
    try:
        import locale
        code = (locale.getlocale()[0] or "").lower()
    except Exception:
        code = ""
    return "zh" if code.startswith("zh") else "en"


def configure_process() -> None:
    """Apply process-level Windows integration: taskbar identity and DPI awareness."""
    if sys.platform != "win32":
        return
    import ctypes
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
    except Exception:
        pass
    try:  # per-monitor DPI awareness v2 (Windows 10 1703+)
        if ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4)):
            return
    except Exception:
        pass
    try:  # system DPI awareness (Windows 8.1+)
        if ctypes.windll.shcore.SetProcessDpiAwareness(1) == 0:
            return
    except Exception:
        pass
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def apply_dark_titlebar(window: tk.Misc) -> None:
    """Match the native title bar to the dark theme on Windows 10/11."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        user32 = ctypes.windll.user32
        user32.GetParent.restype = ctypes.c_void_p
        user32.GetParent.argtypes = [ctypes.c_void_p]
        hwnd = user32.GetParent(ctypes.c_void_p(window.winfo_id())) or window.winfo_id()
        dwm = ctypes.windll.dwmapi
        dwm.DwmSetWindowAttribute.argtypes = [ctypes.c_void_p, ctypes.c_uint,
                                              ctypes.c_void_p, ctypes.c_uint]
        # DWMWA_USE_IMMERSIVE_DARK_MODE: 20 on Windows 10 20H1+, 19 on earlier builds
        enabled = ctypes.c_int(1)
        for attr in (20, 19):
            if dwm.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(enabled),
                                         ctypes.sizeof(enabled)) == 0:
                break
        # DWMWA_WINDOW_CORNER_PREFERENCE: rounded corners on Windows 11
        rounded = ctypes.c_int(2)  # DWMWCP_ROUND
        dwm.DwmSetWindowAttribute(hwnd, 33, ctypes.byref(rounded),
                                  ctypes.sizeof(rounded))
    except Exception:
        pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = system_lang()
        self._vars = {}          # (i18n_key, index) -> StringVar
        self._pool = []          # canvas text items, one set per table row
        self._shown = 0
        self._status_job = None
        self._result_job = None
        self._result_font = None
        self._result_lines = 0
        self._result_widths: Dict[int, int] = {}
        self._active_tab = 0
        self._tab_anim_job = None
        self._fade_job = None
        self._table_width = 0
        self._table_job = None
        self._scale = self._init_scale()
        if hasattr(sys, "set_int_max_str_digits"):   # 3.11+ rejects >4300 decimal digits
            try: sys.set_int_max_str_digits(MAX_INPUT)
            except Exception: pass
        self.title(APP_NAME)
        self.configure(bg=BG)
        self._load_icon()
        gw, gh = int(WIN_W * self._scale), int(WIN_H * self._scale)
        gw = min(gw, self.winfo_screenwidth() - 40)
        gh = min(gh, self.winfo_screenheight() - 80)
        self.geometry(f"{gw}x{gh}")
        self.minsize(min(int(620 * self._scale), gw), min(int(680 * self._scale), gh))
        self.update_idletasks()
        x = (self.winfo_screenwidth() - gw) // 2
        y = (self.winfo_screenheight() - gh) // 2
        self.geometry(f"+{x}+{y}")
        self._ui()
        self._set_base(10)
        self.after(20, lambda: apply_dark_titlebar(self))
        self.after(10, self._fade_in)

    def _load_icon(self) -> None:
        """Set the window icon; the inline PNG keeps the program single-file."""
        try:
            self._icon = tk.PhotoImage(data=ICON_PNG)
            self.iconphoto(True, self._icon)
            self._logo = self._icon.subsample(2)
        except tk.TclError:
            self._icon = None
            self._logo = None

    def t(self, k):
        return TR[self.lang].get(k, k)

    # register UI strings as StringVars so one language switch updates them all
    def V(self, key, i=None):
        ck = (key, i)
        v = self._vars.get(ck)
        if v is None:
            v = tk.StringVar(master=self)
            self._vars[ck] = v
            self._set_var(ck, v)
        return v

    def _set_var(self, ck, v):
        key, i = ck
        val = self.t(key)
        v.set(val[i] if i is not None else val)

    def _init_scale(self) -> float:
        """Return the DPI scale factor, clamped so the window always fits the screen."""
        try:
            dpi = self.winfo_fpixels("1i")
        except Exception:
            return 1.0
        s = dpi / 96.0
        if not 1.0 < s <= 4.0:
            return 1.0
        try:  # never let the window grow past the screen, content would be clipped
            s = max(1.0, min(s, (self.winfo_screenwidth() - 40) / WIN_W,
                             (self.winfo_screenheight() - 80) / WIN_H))
        except Exception:
            pass
        try:
            self.tk.call("tk", "scaling", 96.0 * s / 72.0)
        except Exception:
            return 1.0
        return s

    def _ui(self) -> None:
        self._build_statusbar()

        hf = tk.Frame(self, bg=BG)
        hf.pack(fill=tk.X, padx=30, pady=(20, 0))
        if self._logo is not None:
            tk.Label(hf, image=self._logo, bg=BG).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(hf, text=APP_NAME, font=FT_TTL, bg=BG, fg=ACCENT
                 ).pack(side=tk.LEFT)
        self._btn_lang = tk.Button(hf, text=LANG_LABEL[self.lang], font=FT_SM,
                                   bg=SURFACE2, fg=TEXT2,
                                   relief=tk.FLAT, bd=0, padx=14, pady=4,
                                   cursor="hand2", command=self._switch_lang)
        self._btn_lang.pack(side=tk.RIGHT)
        self._hoverable(self._btn_lang, SURFACE2, BORDER)
        tk.Label(self, textvariable=self.V("sub"), font=FT_SM, bg=BG, fg=TEXT2
                 ).pack(pady=(4, 16))

        sty = ttk.Style()
        try:
            sty.theme_use("clam")
        except tk.TclError:
            pass
        sty.configure("Dark.Vertical.TScrollbar", background=SURFACE2,
                      troughcolor=BG, bordercolor=BG, arrowcolor=TEXT2,
                      lightcolor=SURFACE2, darkcolor=SURFACE2, relief=tk.FLAT)
        sty.map("Dark.Vertical.TScrollbar", background=[("active", BORDER)])

        # Tab bar is built from plain buttons so the selection indicator can
        # slide between tabs and pages can animate in.
        self._tabbar = tk.Frame(self, bg=BG)
        self._tabbar.pack(fill=tk.X, padx=14, pady=(0, 4))
        self._tab_btns = []
        for i, key in enumerate(("tab1", "tab2", "tab3")):
            btn = tk.Button(self._tabbar, textvariable=self.V(key), font=FT_BB,
                            bg=BG, fg=TEXT2, activebackground=SURFACE,
                            activeforeground=ACCENT, relief=tk.FLAT, bd=0,
                            padx=16, pady=8, cursor="hand2",
                            highlightthickness=0,
                            command=lambda idx=i: self._select_tab(idx))
            btn.pack(side=tk.LEFT, padx=(0, 4))
            btn.bind("<Enter>", lambda e, b=btn: self._hover_tab(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self._hover_tab(b, False))
            self._tab_btns.append(btn)
        self._indicator = tk.Frame(self._tabbar, bg=ACCENT, height=2)
        self._indicator.place(x=0, y=0, width=0)

        tk.Frame(self, bg=BORDER, height=1).pack(fill=tk.X, padx=14, pady=(0, 8))
        self._pages = tk.Frame(self, bg=BG)
        self._pages.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))
        self._tab1 = tk.Frame(self._pages, bg=BG)
        self._tab2 = tk.Frame(self._pages, bg=BG)
        self._tab3 = tk.Frame(self._pages, bg=BG)
        self._page_list = [self._tab1, self._tab2, self._tab3]

        self._mk_tab1()
        self._mk_tab2()
        self._mk_tab3()
        self._select_tab(0, animate=False)
        self.after(60, self._ensure_page_layout)

    def _ensure_page_layout(self) -> None:
        """Re-assert the visible page and indicator after the window is mapped."""
        page = self._page_list[self._active_tab]
        if not page.winfo_ismapped():
            page.pack(fill=tk.BOTH, expand=True)
        self._position_indicator()

    # ---- tab bar and lightweight UI animation ----
    def _select_tab(self, index: int, animate: bool = True) -> None:
        """Switch pages and slide the tab indicator to the new tab."""
        new_page = self._page_list[index]
        if index == self._active_tab and new_page.winfo_ismapped():
            return
        old_page = self._page_list[self._active_tab]
        self._active_tab = index
        self._style_tabs()
        if old_page is not new_page:
            old_page.pack_forget()
        new_page.pack(fill=tk.BOTH, expand=True)
        target_x = self._tab_btns[index].winfo_x()
        target_w = self._tab_btns[index].winfo_width()
        if not animate or target_w < 5:
            self.after(30, self._position_indicator)
        else:
            start_x = self._indicator.winfo_x()
            start_w = self._indicator.winfo_width()
            if start_w <= 1:
                start_x, start_w = target_x, target_w

            def apply(t: float) -> None:
                self._indicator.place(
                    x=int(round(start_x + (target_x - start_x) * t)),
                    y=self._indicator_y(),
                    width=max(2, int(round(start_w + (target_w - start_w) * t))))

            def done() -> None:
                self._indicator.place(x=target_x, y=self._indicator_y(),
                                      width=target_w)

            self._animate("_tab_anim_job", 6, apply, done)
        self._after_tab_shown(index)

    def _style_tabs(self) -> None:
        for i, btn in enumerate(self._tab_btns):
            if i == self._active_tab:
                btn.config(bg=SURFACE2, fg=ACCENT)
            else:
                btn.config(bg=BG, fg=TEXT2)

    def _hover_tab(self, btn: tk.Button, hover: bool) -> None:
        idx = self._tab_btns.index(btn)
        if idx == self._active_tab:
            return
        btn.config(bg=SURFACE if hover else BG,
                   fg=TEXT if hover else TEXT2)

    def _indicator_y(self) -> int:
        return max(0, self._tab_btns[0].winfo_height() - 2)

    def _position_indicator(self) -> None:
        btn = self._tab_btns[self._active_tab]
        if btn.winfo_width() <= 1:          # geometry not ready yet
            self.after(30, self._position_indicator)
            return
        self._indicator.place(x=btn.winfo_x(), y=self._indicator_y(),
                              width=btn.winfo_width())

    def _after_tab_shown(self, index: int) -> None:
        """Refresh content whose layout depends on a mapped page."""
        if index == 0:
            self.after(40, lambda: self._render_results(force=True))
        elif index == 1:
            self.after(40, self._refresh_table_layout)
        elif index == 2:
            self.after(40, self._ip_sync_scroll)

    def _animate(self, job_attr: str, frames: int, apply, done=None) -> None:
        """Run a short ease-out animation using after() frames."""
        old = getattr(self, job_attr, None)
        if old is not None:
            try: self.after_cancel(old)
            except Exception: pass

        def step(i: int = 0) -> None:
            t = (i + 1) / frames
            apply(1.0 - (1.0 - t) ** 3)
            if i + 1 < frames:
                setattr(self, job_attr, self.after(16, step, i + 1))
            else:
                setattr(self, job_attr, None)
                if done is not None:
                    done()
        step(0)

    def _fade_in(self) -> None:
        """Fade the window in once on startup; ignored where unsupported."""
        try:
            self.attributes("-alpha", 0.0)
        except tk.TclError:
            return

        def step(i: int = 0) -> None:
            i += 1
            try:
                self.attributes("-alpha", min(1.0, i / 6))
            except tk.TclError:
                try: self.attributes("-alpha", 1.0)
                except Exception: pass
                return
            if i < 6:
                self._fade_job = self.after(16, step, i)

        step(0)

    def _hoverable(self, widget: tk.Widget, normal: str, hover: str) -> None:
        widget.bind("<Enter>", lambda e: widget.config(bg=hover), add="+")
        widget.bind("<Leave>", lambda e: widget.config(bg=normal), add="+")

    def _hover_base(self, base: int, hover: bool) -> None:
        if base == self.src.get():
            return
        self._sbtn[base].config(bg=SURFACE if hover else SURFACE2)

    def _build_statusbar(self) -> None:
        bar = tk.Frame(self, bg=SURFACE)
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Frame(bar, bg=BORDER, height=1).pack(side=tk.TOP, fill=tk.X)
        inner = tk.Frame(bar, bg=SURFACE)
        inner.pack(fill=tk.X, padx=16, pady=(4, 5))
        self._lbl_status = tk.Label(inner, text="", font=FT_SM, bg=SURFACE,
                                    fg=SUCCESS, anchor="w")
        self._lbl_status.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(inner, text=self._runtime_info(), font=FT_SM, bg=SURFACE,
                 fg=TEXT2).pack(side=tk.RIGHT)

    @staticmethod
    def _runtime_info() -> str:
        return f"Python {sys.version.split()[0]} · Tk {tk.TkVersion}"

    def _mk_tab1(self):
        p = self._tab1

        tk.Label(p, textvariable=self.V("src"), font=FT_BD, bg=BG, fg=TEXT2
                 ).pack(pady=(24, 6))

        btn_row = tk.Frame(p, bg=BG)
        btn_row.pack(pady=(0, 10))

        self.src = tk.IntVar(value=10)
        self._sbtn = {}
        for i, base in enumerate(BASES):
            b = tk.Button(btn_row, textvariable=self.V("bases", i), font=FT_BD,
                          bg=SURFACE2, fg=TEXT2, relief=tk.FLAT, bd=0, padx=18, pady=7,
                          cursor="hand2", command=lambda x=base: self._set_base(x))
            b.pack(side=tk.LEFT, padx=3)
            b.bind("<Enter>", lambda e, x=base: self._hover_base(x, True))
            b.bind("<Leave>", lambda e, x=base: self._hover_base(x, False))
            self._sbtn[base] = b

        ef = tk.Frame(p, bg=BG)
        ef.pack(pady=(12, 6))
        self._entry = tk.Entry(ef, font=("Consolas", 24, "bold"), width=22,
                               bg=SURFACE, fg=TEXT, insertbackground=ACCENT,
                               relief=tk.FLAT, justify=tk.CENTER,
                               highlightthickness=2, highlightcolor=ACCENT,
                               highlightbackground=BORDER)
        self._entry.pack(ipady=12)
        self._entry.bind("<KeyRelease>", lambda e: self._convert())
        self._entry.bind("<Escape>", self._clear_input)
        self._entry.focus_set()

        self._lbl_err = tk.Label(p, text="", font=FT_SM, bg=BG, fg=TEXT2)
        self._lbl_err.pack(pady=(2, 6))

        tk.Frame(p, bg=BORDER, height=1).pack(fill=tk.X, padx=50, pady=(4, 16))

        tk.Label(p, textvariable=self.V("res"), font=FT_H2, bg=BG, fg=TEXT
                 ).pack(anchor="w", padx=40, pady=(0, 12))

        rf = tk.Frame(p, bg=BG)
        rf.pack(fill=tk.X, padx=28)
        self._rw = {}
        self._cbtn = {}
        self._vals = {}
        tstyles = [("#059669","#fff"),("#2563eb","#fff"),
                   ("#cbd5e1","#0f172a"),("#d97706","#fff")]
        for i, (base, (tg, tf)) in enumerate(zip(BASES, tstyles)):
            c = tk.Frame(rf, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
            c.pack(fill=tk.X, pady=3)
            tk.Label(c, textvariable=self.V("bases", i), font=("Microsoft YaHei UI",11,"bold"),
                     bg=tg, fg=tf, width=10, padx=12, pady=10).pack(side=tk.LEFT)
            v = tk.Label(c, text="—", font=FT_ML, bg=SURFACE, fg=TEXT, anchor="w",
                         justify=tk.LEFT, cursor="hand2")
            v.pack(side=tk.LEFT, padx=(12,6), pady=14, fill=tk.X, expand=True)
            v.bind("<Button-1>", lambda e, b=base, l=v: self._copy(b, l))
            c.bind("<Configure>", lambda e: self._schedule_result_render())
            cb = tk.Button(c, textvariable=self.V("copy"), font=FT_SM, width=4,
                           bg=SURFACE2, fg=TEXT2, relief=tk.FLAT, bd=0,
                           padx=8, pady=6, cursor="hand2",
                           command=lambda b=base, l=v: self._copy(b, l))
            cb.pack(side=tk.RIGHT, padx=(0,12), pady=10)
            self._hoverable(cb, SURFACE2, BORDER)
            self._rw[base] = v
            self._cbtn[base] = cb
            self._vals[base] = ""
        self.bind("<Configure>", lambda e: self._schedule_result_render())

    def _mk_tab2(self):
        p = self._tab2

        # Query card, matching the card style used by the other tabs.
        cv = tk.Frame(p, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        cv.pack(fill=tk.X, padx=28, pady=(16, 10))
        tk.Label(cv, textvariable=self.V("conv"), font=FT_H2, bg=SURFACE, fg=TEXT
                 ).pack(anchor="w", padx=18, pady=(14, 10))

        form = tk.Frame(cv, bg=SURFACE)
        form.pack(fill=tk.X, padx=18, pady=(0, 16))
        form.grid_columnconfigure(3, weight=1)

        tk.Label(form, textvariable=self.V("clbl"), font=FT_BD, bg=SURFACE, fg=TEXT2,
                 width=13, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 8))
        self._ent_ch = tk.Entry(form, font=FT_MS, width=12, bg=SURFACE2, fg=TEXT,
                                insertbackground=ACCENT, relief=tk.FLAT, justify=tk.CENTER,
                                highlightthickness=2, highlightcolor=ACCENT,
                                highlightbackground=BORDER)
        self._ent_ch.grid(row=0, column=1, sticky="w", padx=(10, 12), pady=(0, 8), ipady=5)
        self._ent_ch.bind("<KeyRelease>", lambda e: self._c2d())
        self._ent_ch.bind("<Escape>", self._clear_char)
        clear_ch = tk.Button(form, textvariable=self.V("clear"), font=FT_BD,
                             bg=SURFACE2, fg=TEXT2, relief=tk.FLAT, bd=0,
                             padx=12, pady=1, cursor="hand2", command=self._clear_char)
        clear_ch.grid(row=0, column=2, sticky="w", padx=(0, 12), pady=(0, 8))
        self._hoverable(clear_ch, SURFACE2, BORDER)
        self._lbl_co = tk.Label(form, text="", font=FT_CD, bg=SURFACE, fg=ACCENT,
                                anchor="w", justify=tk.LEFT)
        self._lbl_co.grid(row=0, column=3, sticky="ew")
        self._bind_query_wrap(self._lbl_co)

        tk.Label(form, textvariable=self.V("dlbl"), font=FT_BD, bg=SURFACE, fg=TEXT2,
                 width=13, anchor="w").grid(row=1, column=0, sticky="w")
        self._ent_cd = tk.Entry(form, font=FT_MS, width=12, bg=SURFACE2, fg=TEXT,
                                insertbackground=ACCENT, relief=tk.FLAT, justify=tk.CENTER,
                                highlightthickness=2, highlightcolor=ACCENT,
                                highlightbackground=BORDER)
        self._ent_cd.grid(row=1, column=1, sticky="w", padx=(10, 12), ipady=5)
        self._ent_cd.bind("<KeyRelease>", lambda e: self._d2c())
        self._ent_cd.bind("<Escape>", self._clear_code)
        clear_cd = tk.Button(form, textvariable=self.V("clear"), font=FT_BD,
                             bg=SURFACE2, fg=TEXT2, relief=tk.FLAT, bd=0,
                             padx=12, pady=1, cursor="hand2", command=self._clear_code)
        clear_cd.grid(row=1, column=2, sticky="w", padx=(0, 12))
        self._hoverable(clear_cd, SURFACE2, BORDER)
        self._lbl_do = tk.Label(form, text="", font=FT_CD, bg=SURFACE, fg=ACCENT,
                                anchor="w", justify=tk.LEFT)
        self._lbl_do.grid(row=1, column=3, sticky="ew")
        self._bind_query_wrap(self._lbl_do)

        sf = tk.Frame(p, bg=BG)
        sf.pack(fill=tk.X, padx=28, pady=(0, 2))
        self._ent_s = tk.Entry(sf, font=FT_MS, bg=SURFACE2, fg=TEXT,
                               insertbackground=ACCENT, relief=tk.FLAT,
                               highlightthickness=2, highlightcolor=ACCENT,
                               highlightbackground=BORDER)
        self._ent_s.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 10))
        self._is_ph = True; self._set_ph()
        self._ent_s.bind("<FocusIn>", self._ph_in)
        self._ent_s.bind("<FocusOut>", self._ph_out)
        self._ent_s.bind("<KeyRelease>", lambda e: self._search())
        self._ent_s.bind("<Escape>", self._clear_search)
        self._count = tk.Label(sf, text="", font=FT_SM, bg=BG, fg=TEXT2, anchor="w")
        self._count.pack(side=tk.LEFT, padx=(0, 10))
        all_btn = tk.Button(sf, textvariable=self.V("all"), font=FT_BD, bg=SURFACE2,
                            fg=TEXT2, relief=tk.FLAT, bd=0, padx=16, pady=2,
                            cursor="hand2", command=self._show_all)
        all_btn.pack(side=tk.RIGHT)
        self._hoverable(all_btn, SURFACE2, BORDER)

        tk.Label(p, textvariable=self.V("atl"), font=FT_H2, bg=BG, fg=TEXT
                 ).pack(anchor="w", padx=28, pady=(10, 6))

        # table body is drawn as canvas text items: toggling their visibility skips
        # the geometry manager entirely, so switching 128 rows stays instant
        outer = tk.Frame(p, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        outer.pack(fill=tk.BOTH, expand=True, padx=28, pady=(0, 0))
        vsb = ttk.Scrollbar(outer, orient=tk.VERTICAL,
                            style="Dark.Vertical.TScrollbar")
        self._cv = tk.Canvas(outer, bg=SURFACE, highlightthickness=0, yscrollcommand=vsb.set)
        vsb.config(command=self._cv.yview)
        self._head_h = int(30 * self._scale)
        self._hf = tk.Frame(outer, bg=SURFACE2, height=self._head_h)
        self._hf.pack(side=tk.TOP, fill=tk.X, padx=(0, vsb.winfo_reqwidth()))
        self._hf.pack_propagate(False)          # same width as the canvas, so columns line up
        self._cv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._cv.bind("<Configure>", self._on_canvas_resize)
        for w in (self._cv, self._hf):
            self._bind_wheel(w)
        self._build_table()
        self._fill(ADATA)

    def _mk_tab3(self) -> None:
        self._ip_rows = {}
        self._ip_vals = {}

        # The page is scrollable so that the subnet rows stay reachable when the
        # window is reduced to its minimum height.
        outer = tk.Frame(self._tab3, bg=BG)
        outer.pack(fill=tk.BOTH, expand=True)
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)
        self._ip_canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        self._ip_canvas.grid(row=0, column=0, sticky="nsew")
        self._ip_vsb = ttk.Scrollbar(outer, orient=tk.VERTICAL,
                                     command=self._ip_canvas.yview,
                                     style="Dark.Vertical.TScrollbar")
        self._ip_vsb.grid(row=0, column=1, sticky="ns")
        self._ip_vsb.grid_remove()
        self._ip_canvas.configure(yscrollcommand=self._ip_vsb.set)
        p = tk.Frame(self._ip_canvas, bg=BG)
        self._ip_body = self._ip_canvas.create_window((0, 0), window=p, anchor="nw")
        p.bind("<Configure>", self._ip_body_cfg)
        self._ip_canvas.bind("<Configure>", self._ip_canvas_cfg)

        tk.Label(p, textvariable=self.V("iplbl"), font=FT_BD, bg=BG, fg=TEXT2
                 ).pack(pady=(18, 6))
        ef = tk.Frame(p, bg=BG)
        ef.pack()
        self._ip_entry = tk.Entry(ef, font=("Consolas", 20, "bold"), width=26,
                                  bg=SURFACE, fg=TEXT, insertbackground=ACCENT,
                                  relief=tk.FLAT, justify=tk.CENTER,
                                  highlightthickness=2, highlightcolor=ACCENT,
                                  highlightbackground=BORDER)
        self._ip_entry.pack(ipady=8)
        self._ip_entry.bind("<KeyRelease>", lambda e: self._convert_ip())
        self._ip_entry.bind("<Escape>", self._clear_ip)

        self._lbl_ip_err = tk.Label(p, text="", font=FT_SM, bg=BG, fg=TEXT2)
        self._lbl_ip_err.pack(pady=(2, 4))
        tk.Frame(p, bg=BORDER, height=1).pack(fill=tk.X, padx=50, pady=(2, 8))

        tk.Label(p, textvariable=self.V("ipsec1"), font=FT_H2, bg=BG, fg=TEXT
                 ).pack(anchor="w", padx=40, pady=(0, 4))
        body = tk.Frame(p, bg=BG)
        body.pack(fill=tk.X, padx=28)
        for key in IP_ROWS:
            self._ip_row(body, key)

        tk.Label(p, textvariable=self.V("ipsec2"), font=FT_H2, bg=BG, fg=TEXT
                 ).pack(anchor="w", padx=40, pady=(8, 4))
        self._ip_sub = tk.Frame(p, bg=BG)
        self._ip_sub.pack(fill=tk.X, padx=28)
        for key in IP_SUB_ROWS:
            self._ip_row(self._ip_sub, key)
        self._ip_ph = tk.Label(self._ip_sub, textvariable=self.V("ipsubhint"),
                               font=FT_SM, bg=BG, fg=TEXT2, anchor="w")
        self._show_ip_sub(False)
        self._convert_ip()
        self._bind_ip_wheel(p)

    def _ip_canvas_cfg(self, e) -> None:
        self._ip_canvas.itemconfigure(self._ip_body, width=e.width)
        self._ip_sync_scroll()

    def _ip_body_cfg(self, e=None) -> None:
        self._ip_canvas.configure(scrollregion=self._ip_canvas.bbox("all"))
        self._ip_sync_scroll()

    def _ip_sync_scroll(self) -> None:
        """Show the scrollbar only while the content is taller than the viewport."""
        if not self._ip_canvas.winfo_ismapped():
            return
        bbox = self._ip_canvas.bbox("all")
        needed = (bbox[3] - bbox[1]) if bbox else 0
        if needed > self._ip_canvas.winfo_height():
            self._ip_vsb.grid()
        else:
            self._ip_vsb.grid_remove()
            self._ip_canvas.yview_moveto(0)

    def _bind_ip_wheel(self, widget: tk.Misc) -> None:
        widget.bind("<MouseWheel>", self._ip_wheel)
        for child in widget.winfo_children():
            self._bind_ip_wheel(child)

    def _ip_wheel(self, e) -> None:
        if not self._ip_vsb.winfo_ismapped():
            return
        steps = int(-e.delta / 120)
        if steps == 0:
            steps = -1 if e.delta > 0 else 1
        self._ip_canvas.yview_scroll(steps, "units")

    def _ip_row(self, parent: tk.Misc, key: str) -> None:
        row = tk.Frame(parent, bg=SURFACE, highlightthickness=1,
                       highlightbackground=BORDER)
        row.pack(fill=tk.X, pady=1)
        tk.Label(row, textvariable=self.V(key), font=FT_SMB, bg=SURFACE2,
                 fg=TEXT2, width=18, anchor="w", padx=10, pady=4
                 ).pack(side=tk.LEFT, fill=tk.Y)
        val = tk.Label(row, text="—", font=FT_CD, bg=SURFACE, fg=TEXT,
                       anchor="w", justify=tk.LEFT, padx=8, pady=4)
        val.pack(side=tk.LEFT, fill=tk.X, expand=True)
        btn = tk.Button(row, textvariable=self.V("copy"), font=FT_SM, width=4,
                        bg=SURFACE2, fg=TEXT2, relief=tk.FLAT, bd=0,
                        padx=6, pady=2, cursor="hand2")
        btn.pack(side=tk.RIGHT, padx=(6, 8), pady=2)
        self._hoverable(btn, SURFACE2, BORDER)
        btn.config(command=lambda k=key, l=val, b=btn: self._copy_ip(k, l, b))
        val.bind("<Button-1>", lambda e, k=key, l=val, b=btn: self._copy_ip(k, l, b))
        self._ip_rows[key] = (row, val, btn)

    def _show_ip_sub(self, visible: bool) -> None:
        """Only show the subnet rows when a prefix length was supplied."""
        if visible:
            self._ip_ph.pack_forget()
            for key in IP_SUB_ROWS:
                self._ip_rows[key][0].pack(fill=tk.X, pady=1)
        else:
            for key in IP_SUB_ROWS:
                self._ip_rows[key][0].pack_forget()
            self._ip_ph.pack(anchor="w", pady=6)

    def _ip_fill(self, data: Dict[str, str]) -> None:
        for key in IP_ALL_ROWS:
            text = data.get(key, "")
            self._ip_vals[key] = text
            self._ip_rows[key][1].config(text=text or "—")

    def _ip_msg(self, text, color=TEXT2):
        self._lbl_ip_err.config(text=text, fg=color)

    def _clear_ip(self, e=None):
        self._ip_entry.delete(0, tk.END)
        self._convert_ip()
        return "break"

    # ---- IPv4 presentation ----
    def _ip_error(self, err) -> str:
        code, params = err
        if code == "seg":
            return self.t("iperrSeg").format(n=params["n"], s=params["s"])
        if code == "seg_range":
            return self.t("iperrSegRange").format(n=params["n"], v=params["v"])
        if code == "hex":
            return self.t("iperrHex").format(s=params["s"])
        if code == "bin":
            return self.t("iperrBin").format(s=params["s"])
        if code == "prefix":
            return self.t("iperrPrefix")
        if code == "mask":
            return self.t("iperrMask").format(s=params["s"])
        if code == "int":
            return self.t("iperrInt")
        if code == "long":
            return self.t("iperrLong")
        return self.t("iperrAddr")

    def _convert_ip(self) -> None:
        result, err = parse_ip_input(self._ip_entry.get().strip())
        if err:
            self._ip_fill({})
            self._show_ip_sub(False)
            self._ip_msg(self._ip_error(err), DANGER)
            return
        if result is None:
            self._ip_fill({})
            self._show_ip_sub(False)
            self._ip_msg(self.t("iphint"))
            return
        data = {
            "ipDotted": result.dotted,
            "ipDecimal": result.decimal,
            "ipHex": result.hex,
            "ipBinary": result.binary,
            "ipScope": self.t(result.scope),
        }
        subnet = result.subnet()
        if subnet is None:
            self._ip_fill(data)
            self._show_ip_sub(False)
            self._ip_msg(self.t("iphint"))
            return
        host_range = (dotted_ip(subnet.first) if subnet.first == subnet.last
                      else f"{dotted_ip(subnet.first)} – {dotted_ip(subnet.last)}")
        note = self.t("ipP2P") if subnet.note == "rfc3021" else ""
        data.update({
            "ipMask": dotted_ip(subnet.mask),
            "ipWildcard": dotted_ip(~subnet.mask & 0xFFFFFFFF),
            "ipNetwork": dotted_ip(subnet.network),
            "ipBroadcast": dotted_ip(subnet.broadcast),
            "ipHostRange": host_range,
            "ipHostCount": f"{subnet.hosts:,}{note}",
        })
        self._ip_fill(data)
        self._show_ip_sub(True)
        self._ip_msg(self.t("ipTotal").format(n=f"{subnet.total:,}"))

    def _bind_wheel(self, w):
        w.bind("<MouseWheel>", self._wheel_win)
        w.bind("<Button-4>", self._wheel_x11)
        w.bind("<Button-5>", self._wheel_x11)

    def _wheel_win(self, e):
        steps = int(-e.delta / 120)
        if steps == 0:
            steps = -1 if e.delta > 0 else 1
        self._cv.yview_scroll(steps, "units")

    def _wheel_x11(self, e):
        self._cv.yview_scroll(-3 if e.num == 4 else 3, "units")

    def _build_table(self):
        s = self._scale
        self._row_h = int(24 * s)
        self._head_cells = []
        for c, key in enumerate(_COLS):
            lb = tk.Label(self._hf, textvariable=self.V(key), font=FT_SMB,
                          bg=SURFACE2, fg=ACCENT)
            lb.place(x=0, y=self._head_h // 2, anchor="center")
            self._bind_wheel(lb)
            self._head_cells.append(lb)
        self._desc_head = tk.Label(self._hf, textvariable=self.V("Desc"), font=FT_SMB,
                                   bg=SURFACE2, fg=ACCENT)
        self._desc_head.place(x=0, y=self._head_h // 2, anchor="w")
        self._bind_wheel(self._desc_head)
        self._layout_columns(int(620 * s))

        for i in range(len(ADATA)):
            y = i * self._row_h + self._row_h // 2
            zebra = None
            if i % 2 == 0:
                zebra = self._cv.create_rectangle(0, 0, 0, 0, fill=BG,
                                                   outline="", state="hidden")
            cells = [self._cv.create_text(self._colx[c], y, text="", font=FT_CD, fill=TEXT,
                                          anchor="center", state="hidden") for c in range(4)]
            ch = self._cv.create_text(self._colx[4], y, text="", font=FT_CB, fill=SUCCESS,
                                      anchor="center", state="hidden")
            ds = self._cv.create_text(self._desc_x, y, text="", font=FT_SM, fill=TEXT2,
                                      anchor="w", state="hidden")
            self._pool.append({"cells": cells, "char": ch, "desc": ds, "zebra": zebra,
                               "all": cells + [ch, ds], "cur": None, "shown": False})

        self._nors = self._cv.create_text(0, 0, text="", font=FT_BD, fill=TEXT2,
                                          anchor="center", state="hidden")
        self._nors_var = self.V("nors")
        self._nors_var.trace_add("write", lambda *a: self._cv.itemconfigure(
            self._nors, text=self._nors_var.get()))
        self._cv.itemconfigure(self._nors, text=self._nors_var.get())

    def _layout_columns(self, width: int) -> None:
        """Distribute the available width across the table columns."""
        s = self._scale
        pad = int(12 * s)
        avail = max(width - 2 * pad, int(360 * s))
        desc_min = int(150 * s)
        body = max(avail - desc_min, int(avail * 0.56))
        weights = (1.0, 1.0, 1.0, 1.55, 1.2)
        total = sum(weights)
        widths = [max(int(body * w / total), int(46 * s)) for w in weights]
        if sum(widths) > body:
            scale = body / sum(widths)
            widths = [max(int(w * scale), int(40 * s)) for w in widths]
        x = pad
        self._colx = []
        for w in widths:
            self._colx.append(x + w // 2)
            x += w
        self._desc_x = x
        y = self._head_h // 2
        for c, lb in enumerate(getattr(self, "_head_cells", ())):
            lb.place_configure(x=self._colx[c], y=y, anchor="center")
        head = getattr(self, "_desc_head", None)
        if head is not None:
            head.place_configure(x=self._desc_x, y=y, anchor="w")

    def _on_canvas_resize(self, e):
        self._table_width = e.width
        if self._table_job is not None:
            try: self.after_cancel(self._table_job)
            except Exception: pass
        self._table_job = self.after(30, self._apply_table_layout)

    def _refresh_table_layout(self) -> None:
        """Recompute the table layout from the current canvas width."""
        self._table_width = self._cv.winfo_width()
        self._apply_table_layout()

    def _apply_table_layout(self) -> None:
        """Re-position header and row items after a resize."""
        self._table_job = None
        width = self._table_width
        if width < 60:
            return
        self._layout_columns(width)
        rh = self._row_h
        for i, row in enumerate(self._pool):
            y = i * rh + rh // 2
            if row["zebra"] is not None:
                self._cv.coords(row["zebra"], 0, i * rh, width, (i + 1) * rh)
            for c, item in enumerate(row["cells"]):
                self._cv.coords(item, self._colx[c], y)
            self._cv.coords(row["char"], self._colx[4], y)
            self._cv.coords(row["desc"], self._desc_x, y)
        self._cv.coords(self._nors, width // 2, rh)
        self._set_scrollregion(width)

    def _set_scrollregion(self, W=None):
        if W is None:
            W = self._cv.winfo_width()
        self._cv.configure(scrollregion=(0, 0, W, max(self._shown, 1) * self._row_h))

    def _fill(self, data):
        """Lay the result set into the item pool, writing only what changed."""
        cv, n, zh = self._cv, len(data), self.lang == "zh"
        for i, (code, abbr, dz, cat) in enumerate(data):
            row = self._pool[i]
            ctrl = cat == "c"
            if code == 32:
                desc = "空格" if zh else "Space"
            elif ctrl:
                desc = dz if zh else EN_CTRL_NAMES.get(code, abbr)
            else:
                desc = ""
            target = (str(code), f"{code:02X}", f"{code:03o}", f"{code:08b}",
                      abbr if ctrl else ("SP" if code == 32 else chr(code)), desc)
            if row["cur"] != target:          # skip rows whose text did not change
                for it, v in zip(row["all"], target):
                    if cv.itemcget(it, "text") != v:
                        cv.itemconfigure(it, text=v)
                cv.itemconfigure(row["char"], fill=WARNING if ctrl else SUCCESS)
                row["cur"] = target
            if not row["shown"]:
                for it in row["all"]:
                    cv.itemconfigure(it, state="normal")
                if row["zebra"] is not None:
                    cv.itemconfigure(row["zebra"], state="normal")
                row["shown"] = True
        for i in range(n, self._shown):
            row = self._pool[i]
            if row["shown"]:
                for it in row["all"]:
                    cv.itemconfigure(it, state="hidden")
                if row["zebra"] is not None:
                    cv.itemconfigure(row["zebra"], state="hidden")
                row["shown"] = False
        self._shown = n
        cv.itemconfigure(self._nors, state="normal" if not n else "hidden")
        self._set_scrollregion()
        cv.yview_moveto(0)

    def _set_ph(self):
        self._ent_s.delete(0, tk.END); self._ent_s.insert(0, self.t("sph"))
        self._ent_s.config(fg=TEXT2); self._is_ph = True
    def _ph_in(self, e=None):
        if self._is_ph: self._ent_s.delete(0, tk.END); self._ent_s.config(fg=TEXT); self._is_ph = False
    def _ph_out(self, e=None):
        if not self._ent_s.get().strip(): self._set_ph()
    def _clear_search(self, e=None):
        self._is_ph = False; self._set_ph(); self._render_all(); return "break"
    def _search(self):
        if self._is_ph: return
        q = self._ent_s.get().strip()
        if not q:
            self._render_all(); return
        out = search_ascii(ADATA, q)
        self._fill(out)
        self._count.config(text=self.t("hits").format(n=len(out), total=len(ADATA)))
    def _render_all(self):
        self._fill(ADATA)
        self._count.config(text="")
    def _show_all(self):
        self._set_ph(); self._render_all()

    def _bind_query_wrap(self, lbl: tk.Label) -> None:
        """Wrap lookup results inside the result column instead of clipping them."""
        def on_resize(e) -> None:
            width = e.width
            wrap = max(120, width - 4)
            if width > 40 and int(lbl.cget("wraplength")) != wrap:
                lbl.config(wraplength=wrap)
        lbl.bind("<Configure>", on_resize)

    def _clear_char(self, e=None):
        self._ent_ch.delete(0, tk.END)
        self._c2d()
        self._ent_ch.focus_set()
        return "break"

    def _clear_code(self, e=None):
        self._ent_cd.delete(0, tk.END)
        self._d2c()
        self._ent_cd.focus_set()
        return "break"

    def _c2d(self):
        t = self._ent_ch.get()
        if not t:
            self._lbl_co.config(text="", fg=ACCENT)
            return
        if len(t) == 1:
            c = ord(t)
            if c <= 127:
                self._lbl_co.config(
                    fg=ACCENT,
                    text=f"DEC {c} · HEX {c:02X} · OCT {c:03o} · BIN {c:08b}")
            else:
                self._lbl_co.config(fg=WARNING,
                                    text=f"U+{c:04X} · {self.t('nonascii')}")
            return
        parts = [f"{ch} → {ord(ch)}" if ord(ch) <= 127 else f"{ch} → U+{ord(ch):04X}"
                 for ch in t[:8]]
        tail = " …" if len(t) > 8 else ""
        self._lbl_co.config(
            fg=ACCENT,
            text=" · ".join(parts) + tail + "   " + self.t("chars").format(n=len(t)))

    def _d2c(self):
        t = self._ent_cd.get().strip()
        if not t:
            self._lbl_do.config(text="", fg=ACCENT)
            return
        try:
            c = int(t)
        except ValueError:
            self._lbl_do.config(text=self.t("neednum"), fg=DANGER)
            return
        if not 0 <= c <= 127:
            self._lbl_do.config(text=self.t("oor"), fg=DANGER)
            return
        r = repr(chr(c)) if c < 32 or c == 127 else f"'{chr(c)}'"
        self._lbl_do.config(fg=ACCENT,
                            text=f"{r} · HEX {c:02X} · BIN {c:08b}")

    def _switch_lang(self):
        self.lang = "en" if self.lang=="zh" else "zh"
        self._btn_lang.config(text=LANG_LABEL[self.lang])
        self._refresh()

    def _refresh(self) -> None:
        for ck, v in self._vars.items():
            self._set_var(ck, v)
        if self._is_ph:
            self._set_ph(); self._render_all()
        else:
            self._search()
        self._c2d(); self._d2c(); self._convert(); self._convert_ip()
        self._status("")
        self.after(30, self._position_indicator)

    def _set_base(self, b):
        self.src.set(b)
        for k, btn in self._sbtn.items():
            btn.config(bg=BASE_ACCENT[k] if k==b else SURFACE2, fg="#fff" if k==b else TEXT2)
        self._convert()

    def _clear_input(self, e=None):
        self._entry.delete(0, tk.END); self._convert(); return "break"

    def _parse(self, base: int) -> Tuple[Optional[int], Optional[str]]:
        """Return (value, error text); an empty box gives (None, None)."""
        value, err = parse_number(self._entry.get().strip(), base)
        if err is None:
            return value, None
        code, params = err
        if code == "badchar":
            text = self.t("badchar").format(c=params["c"], adj=BASE_NAMES[self.lang][base])
        elif code == "toolong":
            text = self.t("toolong").format(n=params["n"])
        elif code == "neednum":
            text = self.t("needvalue")
        else:
            text = self.t("err")
        return None, text

    def _base_hint(self, base: int) -> str:
        p = PREFIX[base]
        note = self.t("prefixnote").format(p=p) if p else ""
        return self.t("hint").format(d=DIGSET[base], p=note)

    def _msg(self, text, color=TEXT2):
        self._lbl_err.config(text=text, fg=color)

    def _convert(self) -> None:
        base = self.src.get()
        v, err = self._parse(base)
        if v is None:
            for b in BASES:
                self._vals[b] = ""
                self._rw[b].config(text="—")
            self._msg(err if err else self._base_hint(base),
                      DANGER if err else TEXT2)
            return
        self._vals = {2: self._fmt(v,2), 8: self._fmt(v,8),
                      10: self._fmt(v,10), 16: self._fmt(v,16)}
        self._render_results(force=True)
        self._msg(self.t("neg") if v < 0 else self._base_hint(base))

    def _schedule_result_render(self) -> None:
        """Debounce re-rendering while the window is being resized."""
        if self._result_job is None:
            self._result_job = self.after(30, self._render_results)

    def _render_results(self, force: bool = False) -> None:
        """Fit each result to its row width; the stored values stay complete."""
        self._result_job = None
        if self._result_font is None:
            self._result_font = tkfont.Font(font=FT_ML)
        height = self.winfo_height() / self._scale
        max_lines = 3 if height >= 785 else (2 if height >= 700 else 1)
        lines_changed = self._result_lines != max_lines
        self._result_lines = max_lines
        for base in BASES:
            lbl = self._rw[base]
            px = lbl.winfo_width() - 8
            if px < 20:                     # not laid out yet
                continue
            if (not force and not lines_changed
                    and self._result_widths.get(base) == px):
                continue
            self._result_widths[base] = px
            lbl.config(wraplength=px)
            raw = self._vals.get(base, "")
            lbl.config(text=self._fit(raw, base, px, self._result_font, max_lines)
                       if raw else "—")

    def _fit(self, s: str, base: int, px: int, font: tkfont.Font,
             max_lines: int = 1) -> str:
        """Truncate a value to the available space and report its total digit count."""
        sign = "-" if s.startswith("-") else ""
        digits = s[1:] if sign else s
        ch = font.measure("0") or 1
        if len(s) <= 1024 and font.measure(s) <= px * max_lines:
            return s
        total = len(digits.replace(" ", ""))
        tail = self.t("trunc").format(n=total)
        tail_px = font.measure(tail)
        if base == 2:
            group_px = font.measure("0000 ") or 5 * ch
            per_line = max(1, int(px // group_px))
            tail_slots = max(1, (tail_px + group_px - 1) // group_px)
            groups = max(1, per_line * max_lines - tail_slots)
            prefix = digits[:groups * 5 - 1]
        else:
            per_line = max(1, int(px // ch))
            tail_slots = max(1, (tail_px + ch - 1) // ch)
            prefix = digits[:max(1, per_line * max_lines - tail_slots)]
        prefix = prefix.rstrip()
        return sign + prefix + tail if prefix else sign + "…"

    @staticmethod
    def _fmt(v: int, base: int) -> str:
        """Keep the sign on negatives rather than using two's complement."""
        return format_value(v, base)

    def _status(self, text: str) -> None:
        if self._status_job is not None:
            try: self.after_cancel(self._status_job)
            except Exception: pass
            self._status_job = None
        self._lbl_status.config(text=text)
        if text:
            self._status_job = self.after(1400, lambda: self._status(""))

    def _copy(self, base: int, lbl: tk.Label) -> None:
        self._copy_text(self._vals.get(base, ""),
                        self.t("bases")[BASES.index(base)], lbl, self._cbtn[base])

    def _copy_ip(self, key: str, lbl: tk.Label, btn: tk.Button) -> None:
        self._copy_text(self._ip_vals.get(key, ""), self.V(key).get(), lbl, btn)

    def _copy_text(self, text: str, name: str, lbl: tk.Label, btn: tk.Button) -> None:
        if not text:
            return
        try:
            self.clipboard_clear(); self.clipboard_append(text)
        except tk.TclError:
            return
        self._status(self.t("copied").format(name=name))
        old_lbl = lbl.cget("fg"); lbl.config(fg=ACCENT)
        old_btn = btn.cget("fg"); btn.config(fg=SUCCESS)
        def restore() -> None:
            try:
                lbl.config(fg=old_lbl)
                btn.config(fg=old_btn)
            except tk.TclError:
                pass
        self.after(700, restore)


def _print_environment() -> None:
    """Print runtime details for troubleshooting; used by `main.py --check`."""
    print(f"{APP_NAME} environment check")
    print(f"  Python  : {sys.version.split()[0]}")
    print(f"  Tk      : {tk.TkVersion}")
    print(f"  Platform: {sys.platform}")
    print(f"  Executable: {sys.executable}")


if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        _print_environment()
        raise SystemExit(0)
    configure_process()
    App().mainloop()
