"""Base converter + ASCII table, bilingual UI."""
import os
import sys
import tkinter as tk
from tkinter import ttk

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
FT_ML  = ("Consolas", 18, "bold")
FT_MS  = ("Consolas", 13)
FT_CD  = ("Consolas", 11)
FT_CB  = ("Consolas", 11, "bold")

BASES = (2, 8, 10, 16)
DIGITS = {2: "01", 8: "01234567", 10: "0123456789", 16: "0123456789abcdef"}
DIGSET = {2: "0-1", 8: "0-7", 10: "0-9", 16: "0-9 A-F"}
PREFIX = {2: "0b", 8: "0o", 10: "", 16: "0x"}

MAX_DISP  = 32        # longest value shown per row; copying still yields the full string
MAX_INPUT = 10_000    # input length cap, also lifts int()'s decimal conversion limit
WIN_W, WIN_H = 720, 800


def _mk_ascii():
    tbl = []
    # control-char labels: ce = mnemonic, cz = Chinese name
    ce = {0:"NUL",1:"SOH",2:"STX",3:"ETX",4:"EOT",5:"ENQ",6:"ACK",7:"BEL",
          8:"BS",9:"HT",10:"LF",11:"VT",12:"FF",13:"CR",14:"SO",15:"SI",
          16:"DLE",17:"DC1",18:"DC2",19:"DC3",20:"DC4",21:"NAK",22:"SYN",
          23:"ETB",24:"CAN",25:"EM",26:"SUB",27:"ESC",28:"FS",29:"GS",30:"RS",31:"US"}
    cz = {0:"空字符",1:"标题开始",2:"正文开始",3:"正文结束",4:"传输结束",
          5:"请求",6:"确认",7:"响铃",8:"退格",9:"水平制表",10:"换行",
          11:"垂直制表",12:"换页",13:"回车",14:"移出",15:"移入",
          16:"数据链路转义",17:"设备控制1",18:"设备控制2",19:"设备控制3",
          20:"设备控制4",21:"否定确认",22:"同步空闲",23:"传输块结束",
          24:"取消",25:"介质结束",26:"替换",27:"转义",
          28:"文件分隔符",29:"组分隔符",30:"记录分隔符",31:"单元分隔符"}
    for i in range(32): tbl.append((i, ce.get(i,"?"), cz.get(i,""), "c"))
    tbl.append((32, "SP", "空格", "p"))
    for i in range(33, 127): tbl.append((i, chr(i), "", "p"))
    tbl.append((127, "DEL", "删除", "c"))
    return tbl

ADATA = _mk_ascii()
ADJ = {"zh": {2:"二进制", 8:"八进制", 10:"十进制", 16:"十六进制"},
       "en": {2:"binary", 8:"octal", 10:"decimal", 16:"hexadecimal"}}

TR = {
  "zh": {
    "title":"进制转换器 + ASCII 码表",
    "sub":"输入任意进制 · 实时转换 · 一键复制",
    "src":"输入进制：",
    "bases":["二进制","八进制","十进制","十六进制"],
    "res":"转换结果", "err":"输入格式错误",
    "tab1":"  进制转换  ", "tab2":"  ASCII 码表  ",
    "sph":"搜索字符或编码 (如 A, 65, 0x41) ...",
    "atl":"ASCII 码表 (0 — 127)", "conv":"字符 ↔ 编码 互查",
    "clbl":"输入字符：", "dlbl":"输入编码 (DEC)：", "all":"显示全部",
    "DEC":"十进制", "HEX":"十六进制", "OCT":"八进制", "BIN":"二进制",
    "Char":"字符", "Desc":"说明",
    "nors":"没有匹配的结果", "trunc":" … 共 {n} 位", "chars":"共 {n} 个字符",
    "neg":"负数按 符号 + 绝对值 显示",
    "hint":"可用字符 {d}{p}，支持负号",
    "badchar":"「{c}」不是有效的{adj}字符",
    "toolong":"输入过长，最多 {n} 个字符",
    "neednum":"请输入数字",
    "hits":"命中 {n} / {total}",
    "copied":"已复制 {name}",
    "nonascii":"非 ASCII", "oor":"超出范围 (0-127)",
  },
  "en": {
    "title":"Base Converter + ASCII Table",
    "sub":"Input any base · Real-time convert · One-click copy",
    "src":"Input base:",
    "bases":["Binary","Octal","Decimal","Hexadecimal"],
    "res":"Results", "err":"Invalid input format",
    "tab1":"  Base Converter  ", "tab2":"  ASCII Table  ",
    "sph":"Search char or code (e.g. A, 65, 0x41) ...",
    "atl":"ASCII Table (0 — 127)", "conv":"Char ↔ Code Lookup",
    "clbl":"Enter char:", "dlbl":"Enter code (DEC):", "all":"Show All",
    "DEC":"DEC", "HEX":"HEX", "OCT":"OCT", "BIN":"BIN",
    "Char":"Char", "Desc":"Description",
    "nors":"No matching results", "trunc":" … {n} total", "chars":"{n} chars",
    "neg":"Negatives shown as sign + magnitude",
    "hint":"Allowed {d}{p}, use - for negatives",
    "badchar":"\"{c}\" is not a valid {adj} digit",
    "toolong":"Input too long, max {n} characters",
    "neednum":"Enter a number",
    "hits":"{n} / {total} hits",
    "copied":"Copied {name}",
    "nonascii":"non-ASCII", "oor":"Out of range (0-127)",
  },
}

# column widths are set in pixels in _build_table
_COLS = ("DEC", "HEX", "OCT", "BIN", "Char")

# label on the language toggle: the language you would switch to
LANG_LABEL = {"zh": "EN", "en": "中"}


def system_lang():
    """UI language from the system: "zh" on Chinese systems, "en" everywhere else."""
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


def enable_dpi_awareness():
    """Render at the real DPI on Windows, so HiDPI screens stay sharp."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
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
        self._scale = self._init_scale()
        if hasattr(sys, "set_int_max_str_digits"):   # 3.11+ rejects >4300 decimal digits
            try: sys.set_int_max_str_digits(MAX_INPUT)
            except Exception: pass
        self.title(self.t("title"))
        self.configure(bg=BG)
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

    def _init_scale(self):
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

    def _ui(self):
        hf = tk.Frame(self, bg=BG)
        hf.pack(fill=tk.X, padx=30, pady=(20, 0))
        tk.Label(hf, textvariable=self.V("title"), font=FT_TTL, bg=BG, fg=ACCENT
                 ).pack(side=tk.LEFT)
        self._btn_lang = tk.Button(hf, text=LANG_LABEL[self.lang], font=FT_SM,
                                   bg=SURFACE2, fg=TEXT2,
                                   relief=tk.FLAT, bd=0, padx=14, pady=4,
                                   cursor="hand2", command=self._switch_lang)
        self._btn_lang.pack(side=tk.RIGHT)
        tk.Label(self, textvariable=self.V("sub"), font=FT_SM, bg=BG, fg=TEXT2
                 ).pack(pady=(4, 14))

        sty = ttk.Style(); sty.theme_use("default")
        sty.configure("TNotebook", background=BG, borderwidth=0)
        sty.configure("TNotebook.Tab", background=SURFACE, foreground=TEXT2,
                      font=FT_BB, padding=[22,9], borderwidth=0)
        sty.map("TNotebook.Tab", background=[("selected", SURFACE2)],
                foreground=[("selected", ACCENT)])
        self._nb = ttk.Notebook(self)
        self._nb.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0,10))
        self._tab1 = tk.Frame(self._nb, bg=BG)
        self._tab2 = tk.Frame(self._nb, bg=BG)
        self._nb.add(self._tab1, text=self.t("tab1"))
        self._nb.add(self._tab2, text=self.t("tab2"))
        self._mk_tab1()
        self._mk_tab2()

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

        tr = tk.Frame(p, bg=BG)
        tr.pack(fill=tk.X, padx=40, pady=(0, 12))
        tk.Label(tr, textvariable=self.V("res"), font=FT_H2, bg=BG, fg=TEXT
                 ).pack(side=tk.LEFT)
        self._lbl_status = tk.Label(tr, text="", font=FT_SM, bg=BG, fg=SUCCESS)
        self._lbl_status.pack(side=tk.RIGHT)

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
                         justify=tk.LEFT, wraplength=int(430 * self._scale), cursor="hand2")
            v.pack(side=tk.LEFT, padx=(16,8), pady=14)
            v.bind("<Button-1>", lambda e, b=base, l=v: self._copy(b, l))
            cb = tk.Button(c, text="📋", font=("",13), bg=SURFACE2, fg=TEXT2,
                           relief=tk.FLAT, bd=0, padx=12, pady=6, cursor="hand2",
                           command=lambda b=base, l=v: self._copy(b, l))
            cb.pack(side=tk.RIGHT, padx=(0,12), pady=10)
            self._rw[base] = v
            self._cbtn[base] = cb
            self._vals[base] = ""

    def _mk_tab2(self):
        p = self._tab2

        cv = tk.Frame(p, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        cv.pack(fill=tk.X, padx=14, pady=(14, 8))
        tk.Label(cv, textvariable=self.V("conv"), font=FT_H2, bg=SURFACE, fg=TEXT
                 ).pack(anchor="w", padx=18, pady=(14, 8))

        r1 = tk.Frame(cv, bg=SURFACE)
        r1.pack(fill=tk.X, padx=18, pady=(0, 4))
        tk.Label(r1, textvariable=self.V("clbl"), font=FT_BD, bg=SURFACE, fg=TEXT2
                 ).pack(side=tk.LEFT)
        self._ent_ch = tk.Entry(r1, font=FT_MS, width=10, bg=SURFACE2, fg=TEXT,
                                insertbackground=ACCENT, relief=tk.FLAT, justify=tk.CENTER,
                                highlightthickness=1, highlightcolor=ACCENT,
                                highlightbackground=BORDER)
        self._ent_ch.pack(side=tk.LEFT, padx=(8,10), ipady=3)
        self._ent_ch.bind("<KeyRelease>", lambda e: self._c2d())
        self._lbl_co = tk.Label(r1, text="", font=FT_CD, bg=SURFACE, fg=ACCENT, anchor="w")
        self._lbl_co.pack(side=tk.LEFT, fill=tk.X, expand=True)

        r2 = tk.Frame(cv, bg=SURFACE)
        r2.pack(fill=tk.X, padx=18, pady=(4, 16))
        tk.Label(r2, textvariable=self.V("dlbl"), font=FT_BD, bg=SURFACE, fg=TEXT2
                 ).pack(side=tk.LEFT)
        self._ent_cd = tk.Entry(r2, font=FT_MS, width=10, bg=SURFACE2, fg=TEXT,
                                insertbackground=ACCENT, relief=tk.FLAT, justify=tk.CENTER,
                                highlightthickness=1, highlightcolor=ACCENT,
                                highlightbackground=BORDER)
        self._ent_cd.pack(side=tk.LEFT, padx=(8,10), ipady=3)
        self._ent_cd.bind("<KeyRelease>", lambda e: self._d2c())
        self._lbl_do = tk.Label(r2, text="", font=FT_CD, bg=SURFACE, fg=ACCENT, anchor="w")
        self._lbl_do.pack(side=tk.LEFT, fill=tk.X, expand=True)

        sf = tk.Frame(p, bg=BG)
        sf.pack(fill=tk.X, padx=14, pady=(4, 4))
        self._ent_s = tk.Entry(sf, font=FT_BD, bg=SURFACE, fg=TEXT,
                               insertbackground=ACCENT, relief=tk.FLAT,
                               highlightthickness=1, highlightcolor=ACCENT,
                               highlightbackground=BORDER)
        self._ent_s.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0,8))
        self._is_ph = True; self._set_ph()
        self._ent_s.bind("<FocusIn>", self._ph_in)
        self._ent_s.bind("<FocusOut>", self._ph_out)
        self._ent_s.bind("<KeyRelease>", lambda e: self._search())
        self._ent_s.bind("<Escape>", self._clear_search)
        self._count = tk.Label(sf, text="", font=FT_SM, bg=BG, fg=TEXT2, width=14)
        self._count.pack(side=tk.LEFT)
        tk.Button(sf, textvariable=self.V("all"), font=FT_SM, bg=SURFACE2, fg=TEXT2,
                  relief=tk.FLAT, bd=0, padx=12, pady=6, cursor="hand2",
                  command=self._show_all).pack(side=tk.RIGHT)

        tk.Label(p, textvariable=self.V("atl"), font=FT_H2, bg=BG, fg=TEXT
                 ).pack(anchor="w", padx=18, pady=(6, 4))

        # table body is drawn as canvas text items: toggling their visibility skips
        # the geometry manager entirely, so switching 128 rows stays instant
        outer = tk.Frame(p, bg=BG)
        outer.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))
        vsb = ttk.Scrollbar(outer, orient=tk.VERTICAL)
        self._cv = tk.Canvas(outer, bg=BG, highlightthickness=0, yscrollcommand=vsb.set)
        vsb.config(command=self._cv.yview)
        self._head_h = int(29 * self._scale)
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
        x = 8 * s
        self._colx = []
        for w in (62, 62, 62, 92, 62):
            self._colx.append(int(x + w * s / 2))
            x += w * s
        self._desc_x = int(x)

        for c, key in enumerate(_COLS):
            lb = tk.Label(self._hf, textvariable=self.V(key), font=FT_SMB, bg=SURFACE2,
                          fg=ACCENT)
            lb.place(x=self._colx[c], y=self._head_h // 2, anchor="center")
            self._bind_wheel(lb)
        dlb = tk.Label(self._hf, textvariable=self.V("Desc"), font=FT_SMB, bg=SURFACE2,
                       fg=ACCENT)
        dlb.place(x=self._desc_x, y=self._head_h // 2, anchor="w")
        self._bind_wheel(dlb)

        for i in range(len(ADATA)):
            y = i * self._row_h + self._row_h // 2
            zebra = None
            if i % 2 == 0:
                zebra = self._cv.create_rectangle(0, 0, 0, 0, fill=SURFACE,
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

    def _on_canvas_resize(self, e):
        W, rh = e.width, self._row_h
        for i, row in enumerate(self._pool):
            if row["zebra"] is not None:
                self._cv.coords(row["zebra"], 0, i*rh, W, (i+1)*rh)
        self._cv.coords(self._nors, W // 2, rh)
        self._set_scrollregion(W)

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
            target = (str(code), f"{code:02X}", f"{code:03o}", f"{code:08b}",
                      abbr if ctrl else ("SP" if code == 32 else chr(code)),
                      (dz if zh else abbr) if ctrl else "")
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
        q = self._ent_s.get().strip().lower()
        if not q:
            self._render_all(); return
        # a prefixed query matches that base's column only, anything else matches every field
        pre = ""
        for p in ("0x","0b","0o","#"):
            if q.startswith(p) and len(q) > len(p):
                pre, q = p, q[len(p):]
                break
        col = {"0x":1, "#":1, "0b":3, "0o":2}.get(pre)
        out = []
        for c, a, d, cat in ADATA:
            fields = (str(c), hex(c)[2:].zfill(2).lower(), oct(c)[2:].zfill(3).lower(),
                      f"{c:08b}",
                      chr(c).lower() if cat=="p" and c!=32 else "", a.lower(), d.lower())
            if col is not None:
                hit = q in fields[col]
            else:
                hit = any(q in f for f in fields)
            if hit: out.append((c,a,d,cat))
        self._fill(out)
        self._count.config(text=self.t("hits").format(n=len(out), total=len(ADATA)))
    def _render_all(self):
        self._fill(ADATA)
        self._count.config(text="")
    def _show_all(self):
        self._set_ph(); self._render_all()

    def _c2d(self):
        t = self._ent_ch.get()
        if not t: self._lbl_co.config(text=""); return
        if len(t) == 1:
            c = ord(t)
            if c <= 127:
                self._lbl_co.config(
                    text=f"  {self.t('DEC')} {c}   {self.t('HEX')} {hex(c)[2:].upper()}   "
                         f"{self.t('OCT')} {oct(c)[2:]}   {self.t('BIN')} {format(c, '08b')}")
            else:
                self._lbl_co.config(text=f"  U+{c:04X}  ({self.t('nonascii')})")
            return
        parts = [f"{self.t('DEC')} {ord(ch)}" if ord(ch) <= 127 else f"U+{ord(ch):04X}"
                 for ch in t[:8]]
        tail = "…  " if len(t) > 8 else "  "
        self._lbl_co.config(text="  " + "   ".join(parts) + tail + self.t("chars").format(n=len(t)))

    def _d2c(self):
        t = self._ent_cd.get().strip()
        if not t: self._lbl_do.config(text=""); return
        try:
            c = int(t)
            if 0 <= c <= 127:
                r = repr(chr(c)) if c < 32 or c == 127 else f"'{chr(c)}'"
                self._lbl_do.config(text=f"  →  {r}")
            else:
                self._lbl_do.config(text="  " + self.t("oor"))
        except ValueError:
            self._lbl_do.config(text="  " + self.t("neednum"))

    def _switch_lang(self):
        self.lang = "en" if self.lang=="zh" else "zh"
        self._btn_lang.config(text=LANG_LABEL[self.lang])
        self._refresh()

    def _refresh(self):
        self.title(self.t("title"))
        for ck, v in self._vars.items():
            self._set_var(ck, v)
        self._nb.tab(0, text=self.t("tab1"))
        self._nb.tab(1, text=self.t("tab2"))
        if self._is_ph:
            self._set_ph(); self._render_all()
        else:
            self._search()
        self._c2d(); self._d2c(); self._convert()
        self._status("")

    def _set_base(self, b):
        self.src.set(b)
        for k, btn in self._sbtn.items():
            btn.config(bg=BASE_ACCENT[k] if k==b else SURFACE2, fg="#fff" if k==b else TEXT2)
        self._convert()

    def _clear_input(self, e=None):
        self._entry.delete(0, tk.END); self._convert(); return "break"

    def _parse(self, base):
        """Return (value, error text); an empty box gives (None, None)."""
        raw = self._entry.get().strip()
        if not raw: return None, None
        s = raw.replace("_", "").replace(" ", "")     # tolerate 1_000 and "1111 1111"
        sign = ""
        if s[:1] in "+-": sign, s = s[0], s[1:]
        low = s.lower()
        p = PREFIX[base]
        if p and low.startswith(p): s, low = s[2:], low[2:]
        if not s: return None, self.t("neednum")
        if len(s) > MAX_INPUT: return None, self.t("toolong").format(n=MAX_INPUT)
        for ch in s:                      # name the character as typed, without lowercasing
            if ch.lower() not in DIGITS[base]:
                return None, self.t("badchar").format(c=ch, adj=ADJ[self.lang][base])
        try:
            return int(sign + low, base), None
        except ValueError:
            return None, self.t("err")

    def _base_hint(self, base):
        p = PREFIX[base]
        return self.t("hint").format(d=DIGSET[base], p=f" ({p})" if p else "")

    def _msg(self, text, color=TEXT2):
        self._lbl_err.config(text=text, fg=color)

    def _convert(self):
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
        for b in BASES:
            self._rw[b].config(text=self._clip(self._vals[b]))
        self._msg(self.t("neg") if v < 0 else self._base_hint(base))

    @staticmethod
    def _fmt(v, base):
        """Keep the sign on negatives rather than using two's complement."""
        sign = "-" if v < 0 else ""
        n = abs(v)
        if base == 2:
            digits = f"{n:b}"
            groups = []
            for i, ch in enumerate(reversed(digits)):
                if i and i % 4 == 0: groups.append(" ")
                groups.append(ch)
            digits = "".join(reversed(groups))
        elif base == 8:  digits = f"{n:o}"
        elif base == 10: digits = str(n)
        else:            digits = f"{n:X}"
        return sign + digits

    def _clip(self, s):
        if len(s) <= MAX_DISP: return s
        return s[:MAX_DISP] + self.t("trunc").format(n=len(s))

    def _status(self, text):
        if self._status_job is not None:
            try: self.after_cancel(self._status_job)
            except Exception: pass
            self._status_job = None
        self._lbl_status.config(text=text)
        if text:
            self._status_job = self.after(1400, lambda: self._status(""))

    def _copy(self, base, lbl):
        t = self._vals.get(base, "")
        if not t: return
        self.clipboard_clear(); self.clipboard_append(t)
        self._status(self.t("copied").format(name=self.t("bases")[BASES.index(base)]))
        o = lbl.cget("fg"); lbl.config(fg=ACCENT)
        btn, ob = self._cbtn[base], self._cbtn[base].cget("text")
        btn.config(text="✓", fg=SUCCESS)
        def restore():
            try:
                lbl.config(fg=o)
                btn.config(text=ob, fg=TEXT2)
            except tk.TclError:
                pass
        self.after(700, restore)


if __name__ == "__main__":
    enable_dpi_awareness()
    App().mainloop()
