"""
进制转换器 + ASCII码查询 — 中英双语 · 实时转换
"""
import tkinter as tk
from tkinter import ttk

# ─── Theme ───
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

# ─── ASCII data ───
def _mk_ascii():
    tbl = []
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

# ─── i18n ───
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
  },
}

# Column keys in order: (i18n_key, zh_width, en_width)
_COLS = [("DEC",8,7), ("HEX",10,7), ("OCT",8,7), ("BIN",11,11), ("Char",7,7), ("Desc",22,22)]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = "zh"
        self.title(self.t("title"))
        self.configure(bg=BG)
        gw, gh = 720, 800
        self.geometry(f"{gw}x{gh}")
        self.minsize(620, 680)
        self.update_idletasks()
        x = (self.winfo_screenwidth() - gw) // 2
        y = (self.winfo_screenheight() - gh) // 2
        self.geometry(f"+{x}+{y}")
        self._ui()
        self._set_base(10, init=True)

    def t(self, k):
        return TR[self.lang].get(k, k)

    # ══════════════════ UI ══════════════════
    def _ui(self):
        # ── Header ──
        hf = tk.Frame(self, bg=BG)
        hf.pack(fill=tk.X, padx=30, pady=(20, 0))
        tk.Label(hf, text=self.t("title"), font=FT_TTL, bg=BG, fg=ACCENT
                 ).pack(side=tk.LEFT)
        self._btn_lang = tk.Button(hf, text="EN", font=FT_SM, bg=SURFACE2, fg=TEXT2,
                                   relief=tk.FLAT, bd=0, padx=14, pady=4,
                                   cursor="hand2", command=self._switch_lang)
        self._btn_lang.pack(side=tk.RIGHT)
        self._lbl_sub = tk.Label(self, text=self.t("sub"), font=FT_SM, bg=BG, fg=TEXT2)
        self._lbl_sub.pack(pady=(4, 14))

        # ── Notebook ──
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

    # ═══════════════ TAB 1: Base Converter ═══════════════
    def _mk_tab1(self):
        p = self._tab1

        # Base selector: label above, buttons below — both centered
        self._lbl_src = tk.Label(p, text=self.t("src"), font=FT_BD, bg=BG, fg=TEXT2)
        self._lbl_src.pack(pady=(24, 6))

        btn_row = tk.Frame(p, bg=BG)
        btn_row.pack(pady=(0, 10))

        self.src = tk.IntVar(value=10)
        self._sbtn = {}
        actv = {2: SUCCESS, 8: "#3b82f6", 10: "#475569", 16: WARNING}
        for base, name in zip([2,8,10,16], self.t("bases")):
            b = tk.Button(btn_row, text=name, font=FT_BD, bg=SURFACE2, fg=TEXT2,
                          relief=tk.FLAT, bd=0, padx=18, pady=7, cursor="hand2",
                          command=lambda x=base: self._set_base(x))
            b.pack(side=tk.LEFT, padx=3)
            self._sbtn[base] = (b, actv[base])

        # Input (centered)
        ef = tk.Frame(p, bg=BG)
        ef.pack(pady=(12, 6))
        self._entry = tk.Entry(ef, font=("Consolas", 24, "bold"), width=22,
                               bg=SURFACE, fg=TEXT, insertbackground=ACCENT,
                               relief=tk.FLAT, justify=tk.CENTER,
                               highlightthickness=2, highlightcolor=ACCENT,
                               highlightbackground=BORDER)
        self._entry.pack(ipady=12)
        self._entry.bind("<KeyRelease>", lambda e: self._convert())
        self._entry.focus_set()

        self._lbl_err = tk.Label(p, text="", font=FT_SM, bg=BG, fg=DANGER)
        self._lbl_err.pack(pady=(2, 6))

        # Divider
        tk.Frame(p, bg=BORDER, height=1).pack(fill=tk.X, padx=50, pady=(4, 16))

        # Result title
        self._lbl_res = tk.Label(p, text=self.t("res"), font=FT_H2, bg=BG, fg=TEXT)
        self._lbl_res.pack(anchor="w", padx=40, pady=(0, 12))

        # Result cards
        rf = tk.Frame(p, bg=BG)
        rf.pack(fill=tk.X, padx=28)
        self._rw = {}
        tstyles = [("#059669","#fff"),("#2563eb","#fff"),
                   ("#cbd5e1","#0f172a"),("#d97706","#fff")]
        for base, name, (tg,tf) in zip([2,8,10,16], self.t("bases"), tstyles):
            c = tk.Frame(rf, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
            c.pack(fill=tk.X, pady=3)
            tk.Label(c, text=name, font=("Microsoft YaHei UI",11,"bold"),
                     bg=tg, fg=tf, width=10, padx=12, pady=10).pack(side=tk.LEFT)
            v = tk.Label(c, text="—", font=FT_ML, bg=SURFACE, fg=TEXT)
            v.pack(side=tk.LEFT, padx=(16,8), pady=14)
            tk.Button(c, text="📋", font=("",13), bg=SURFACE2, fg=TEXT2,
                      relief=tk.FLAT, bd=0, padx=12, pady=6, cursor="hand2",
                      command=lambda l=v: self._copy(l)
                      ).pack(side=tk.RIGHT, padx=(0,12), pady=10)
            self._rw[base] = v

    # ═══════════════ TAB 2: ASCII ═══════════════
    def _mk_tab2(self):
        p = self._tab2

        # ── Converter card ──
        cv = tk.Frame(p, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        cv.pack(fill=tk.X, padx=14, pady=(14, 8))
        self._lbl_conv = tk.Label(cv, text=self.t("conv"), font=FT_H2, bg=SURFACE, fg=TEXT)
        self._lbl_conv.pack(anchor="w", padx=18, pady=(14, 8))

        # Row 1: char → codes
        r1 = tk.Frame(cv, bg=SURFACE)
        r1.pack(fill=tk.X, padx=18, pady=(0, 4))
        self._lbl_cl = tk.Label(r1, text=self.t("clbl"), font=FT_BD, bg=SURFACE, fg=TEXT2)
        self._lbl_cl.pack(side=tk.LEFT)
        self._ent_ch = tk.Entry(r1, font=FT_MS, width=5, bg=SURFACE2, fg=TEXT,
                                insertbackground=ACCENT, relief=tk.FLAT, justify=tk.CENTER,
                                highlightthickness=1, highlightcolor=ACCENT,
                                highlightbackground=BORDER)
        self._ent_ch.pack(side=tk.LEFT, padx=(8,10), ipady=3)
        self._ent_ch.bind("<KeyRelease>", lambda e: self._c2d())
        self._lbl_co = tk.Label(r1, text="", font=FT_CD, bg=SURFACE, fg=ACCENT, anchor="w")
        self._lbl_co.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Row 2: code → char
        r2 = tk.Frame(cv, bg=SURFACE)
        r2.pack(fill=tk.X, padx=18, pady=(4, 16))
        self._lbl_dl = tk.Label(r2, text=self.t("dlbl"), font=FT_BD, bg=SURFACE, fg=TEXT2)
        self._lbl_dl.pack(side=tk.LEFT)
        self._ent_cd = tk.Entry(r2, font=FT_MS, width=5, bg=SURFACE2, fg=TEXT,
                                insertbackground=ACCENT, relief=tk.FLAT, justify=tk.CENTER,
                                highlightthickness=1, highlightcolor=ACCENT,
                                highlightbackground=BORDER)
        self._ent_cd.pack(side=tk.LEFT, padx=(8,10), ipady=3)
        self._ent_cd.bind("<KeyRelease>", lambda e: self._d2c())
        self._lbl_do = tk.Label(r2, text="", font=FT_CD, bg=SURFACE, fg=ACCENT, anchor="w")
        self._lbl_do.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # ── Search ──
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
        tk.Button(sf, text=self.t("all"), font=FT_SM, bg=SURFACE2, fg=TEXT2,
                  relief=tk.FLAT, bd=0, padx=12, pady=6, cursor="hand2",
                  command=self._show_all).pack(side=tk.RIGHT)

        # ── Table title ──
        self._lbl_atl = tk.Label(p, text=self.t("atl"), font=FT_H2, bg=BG, fg=TEXT)
        self._lbl_atl.pack(anchor="w", padx=18, pady=(6, 4))

        # ── Scrollable table ──
        outer = tk.Frame(p, bg=BG)
        outer.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))
        self._cv = tk.Canvas(outer, bg=BG, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient=tk.VERTICAL, command=self._cv.yview)
        self._tfr = tk.Frame(self._cv, bg=BG)
        self._tfr.bind("<Configure>",
                       lambda e: self._cv.configure(scrollregion=self._cv.bbox("all")))
        self._cwin = self._cv.create_window((0,0), window=self._tfr, anchor="nw")
        self._cv.configure(yscrollcommand=vsb.set)
        self._cv.bind("<Configure>",
                      lambda e: self._cv.itemconfig(self._cwin, width=e.width))
        self._cv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._cv.bind_all("<MouseWheel>",
                          lambda e: self._cv.yview_scroll(int(-1*(e.delta/120)),"units"))
        self._fill(ADATA)

    def _fill(self, data):
        for w in self._tfr.winfo_children(): w.destroy()
        # Header
        for col, (key, zw, ew) in enumerate(_COLS):
            w = zw if self.lang == "zh" else ew
            tk.Label(self._tfr, text=self.t(key), font=FT_SMB,
                     bg=SURFACE2, fg=ACCENT, width=w, anchor="center"
                     ).grid(row=0, column=col, padx=1, pady=7, sticky="w")
        self._tfr.columnconfigure(5, weight=1)
        # Rows
        for idx, (code, abbr, dz, cat) in enumerate(data):
            bg = SURFACE if idx%2==0 else BG
            r = idx + 1
            for c, v in enumerate([str(code), hex(code)[2:].upper().zfill(2),
                                    oct(code)[2:].zfill(3), format(code,"08b")]):
                tk.Label(self._tfr, text=v, font=FT_CD, bg=bg, fg=TEXT,
                         width=7, anchor="center"
                         ).grid(row=r, column=c, padx=1, pady=3, sticky="w")
            if cat == "c":
                ct, cf, dt = abbr, WARNING, (dz if self.lang=="zh" else abbr)
            else:
                ct, cf = (chr(code) if code!=32 else "SP"), SUCCESS
                dt = ""
            tk.Label(self._tfr, text=ct, font=FT_CB, bg=bg, fg=cf,
                     width=7, anchor="center").grid(row=r, column=4, padx=1, pady=3, sticky="w")
            tk.Label(self._tfr, text=dt, font=FT_SM, bg=bg, fg=TEXT2,
                     anchor="w").grid(row=r, column=5, padx=1, pady=3, sticky="we")

    # ── Search ──
    def _set_ph(self):
        self._ent_s.delete(0, tk.END); self._ent_s.insert(0, self.t("sph"))
        self._ent_s.config(fg=TEXT2); self._is_ph = True
    def _ph_in(self, e=None):
        if self._is_ph: self._ent_s.delete(0, tk.END); self._ent_s.config(fg=TEXT); self._is_ph = False
    def _ph_out(self, e=None):
        if not self._ent_s.get().strip(): self._set_ph()
    def _search(self):
        if self._is_ph: return
        q = self._ent_s.get().strip().lower()
        if not q: self._fill(ADATA); return
        out = []
        for c, a, d, cat in ADATA:
            ch = chr(c) if cat=="p" and c!=32 else ""
            if any(q in s for s in [str(c),hex(c)[2:],oct(c)[2:],format(c,"08b"),
                                     ch.lower(),a.lower(),d.lower()]):
                out.append((c,a,d,cat))
        self._fill(out if out else [])
    def _show_all(self): self._set_ph(); self._fill(ADATA)

    # Char ↔ Code 互查
    def _c2d(self):
        t = self._ent_ch.get()
        if not t: self._lbl_co.config(text=""); return
        c = ord(t[0])
        if c <= 127:
            self._lbl_co.config(
                text=f"  {self.t('DEC')} {c}   {self.t('HEX')} {hex(c)[2:].upper()}   "
                     f"{self.t('OCT')} {oct(c)[2:]}   {self.t('BIN')} {format(c, '08b')}")
        else:
            self._lbl_co.config(text=f"  U+{c:04X}  ({'非 ASCII' if self.lang=='zh' else 'non-ASCII'})")

    def _d2c(self):
        t = self._ent_cd.get().strip()
        if not t: self._lbl_do.config(text=""); return
        try:
            c = int(t)
            if 0 <= c <= 127:
                r = repr(chr(c)) if c < 32 or c == 127 else f"'{chr(c)}'"
                self._lbl_do.config(text=f"  →  {r}")
            else:
                self._lbl_do.config(
                    text="  超出范围 (0-127)" if self.lang=="zh" else "  Out of range (0-127)")
        except ValueError:
            self._lbl_do.config(
                text="  请输入数字" if self.lang=="zh" else "  Enter a number")

    # ── Language ──
    def _switch_lang(self):
        self.lang = "en" if self.lang=="zh" else "zh"
        self._btn_lang.config(text="中" if self.lang=="en" else "EN")
        self._refresh()

    def _refresh(self):
        # Title bar
        self.title(self.t("title"))
        for c in self.winfo_children():
            if isinstance(c, tk.Frame) and c != self._tab1 and c != self._tab2 \
               and not hasattr(c, 'master_frame'):
                for w in c.winfo_children():
                    if isinstance(w, tk.Label) and w.cget("font") == str(FT_TTL):
                        w.config(text=self.t("title"))
                    elif isinstance(w, tk.Label) and w.cget("font") == str(FT_SM):
                        w.config(text=self.t("sub"))

        self._lbl_sub.config(text=self.t("sub"))
        self._lbl_src.config(text=self.t("src"))
        self._lbl_res.config(text=self.t("res"))
        self._nb.tab(0, text=self.t("tab1"))
        self._nb.tab(1, text=self.t("tab2"))

        # Base buttons
        for base, name in zip([2,8,10,16], self.t("bases")):
            self._sbtn[base][0].config(text=name)
            self._rw[base].master.winfo_children()[0].config(text=name)

        # ASCII
        self._lbl_conv.config(text=self.t("conv"))
        self._lbl_cl.config(text=self.t("clbl"))
        self._lbl_dl.config(text=self.t("dlbl"))
        self._lbl_atl.config(text=self.t("atl"))
        if self._is_ph: self._set_ph()
        self._fill(ADATA)
        self._c2d(); self._d2c()

        v = self._parse()
        if v is None and self._entry.get().strip():
            self._lbl_err.config(text=self.t("err"))
        self._convert()

    # ── Base conv logic ──
    def _set_base(self, b, init=False):
        self.src.set(b)
        act = {2: SUCCESS, 8: "#3b82f6", 10: "#475569", 16: WARNING}
        for k, (btn, _) in self._sbtn.items():
            btn.config(bg=act[k] if k==b else SURFACE2, fg="#fff" if k==b else TEXT2)
        if not init: self._convert()

    def _parse(self):
        t = self._entry.get().strip()
        if not t: return None
        try: return int(t, self.src.get())
        except ValueError: return None

    def _convert(self):
        v = self._parse()
        if v is None:
            self._lbl_err.config(text=self.t("err") if self._entry.get().strip() else "")
            for b in [2,8,10,16]: self._rw[b].config(text="—")
            return
        self._lbl_err.config(text="")
        for b,s in {2:self._bin(v), 8:oct(v)[2:], 10:str(v), 16:hex(v)[2:].upper()}.items():
            self._rw[b].config(text=s)

    def _bin(self, v):
        s = bin(v)[2:]; p = []
        for i, c in enumerate(reversed(s)):
            if i and i % 4 == 0:
                p.append(" ")
            p.append(c)
        return "".join(reversed(p))

    def _copy(self, lbl):
        t = lbl.cget("text")
        if t and t!="—":
            self.clipboard_clear(); self.clipboard_append(t)
            o = lbl.cget("fg"); lbl.config(fg=ACCENT)
            self.after(500, lambda: lbl.config(fg=o))


if __name__ == "__main__":
    App().mainloop()
