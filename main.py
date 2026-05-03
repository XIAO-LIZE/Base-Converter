"""
进制转换器 — 中英双语 · 实时转换
"""
import tkinter as tk
from tkinter import ttk

# ─── Colors ───
BG = "#060b14"
SURFACE = "#0f1623"
SURFACE2 = "#192235"
ACCENT = "#4da6ff"
SUCCESS = "#10b981"
WARNING = "#f59e0b"
DANGER = "#ef4444"
TEXT = "#e2e8f0"
TEXT2 = "#8899aa"
BORDER = "#1e3048"

FONT_TITLE = ("Microsoft YaHei UI", 20, "bold")
FONT_H2 = ("Microsoft YaHei UI", 14, "bold")
FONT_BODY = ("Microsoft YaHei UI", 11)
FONT_SMALL = ("Microsoft YaHei UI", 10)
FONT_MONO = ("Consolas", 18, "bold")
FONT_MONO_MD = ("Consolas", 14)

# 多语言文案
TEXT_MAP = {
    "zh": {
        "title": "进制转换器",
        "subtitle": "输入任意进制 · 实时转换 · 一键复制",
        "src_label": "输入进制:",
        "entry_placeholder": "",
        "bases": ["二进制", "八进制", "十进制", "十六进制"],
        "base_abbr": ["BIN", "OCT", "DEC", "HEX"],
        "result_title": "转换结果",
        "format_error": "输入格式错误",
    },
    "en": {
        "title": "Base Converter",
        "subtitle": "Input any base · Real-time convert · One-click copy",
        "src_label": "Input base:",
        "entry_placeholder": "",
        "bases": ["Binary", "Octal", "Decimal", "Hexadecimal"],
        "base_abbr": ["BIN", "OCT", "DEC", "HEX"],
        "result_title": "Results",
        "format_error": "Invalid input format",
    },
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("进制转换器 — Base Converter")
        # 高清窗口 (HiDPI aware)
        self.geometry("620x680")
        self.minsize(520, 600)
        self.configure(bg=BG)

        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 620) // 2
        y = (sh - 680) // 2
        self.geometry(f"+{x}+{y}")

        self.lang = "zh"
        self._build_ui()

    # ─── Lang helper ───
    def t(self, key):
        return TEXT_MAP[self.lang].get(key, key)

    # ─── Build ───
    def _build_ui(self):
        # Header row: title + lang toggle
        header = tk.Frame(self, bg=BG)
        header.pack(fill=tk.X, padx=28, pady=(24, 4))

        self.lbl_title = tk.Label(header, text=self.t("title"), font=FONT_TITLE, bg=BG, fg=ACCENT)
        self.lbl_title.pack(side=tk.LEFT)

        self.btn_lang = tk.Button(header, text="EN", font=FONT_SMALL,
                                   bg=SURFACE2, fg=TEXT2, relief=tk.FLAT, bd=0,
                                   padx=14, pady=4, cursor="hand2",
                                   command=self._toggle_lang)
        self.btn_lang.pack(side=tk.RIGHT)

        self.lbl_subtitle = tk.Label(self, text=self.t("subtitle"), font=FONT_SMALL, bg=BG, fg=TEXT2)
        self.lbl_subtitle.pack(pady=(0, 24))

        # ─── Source base selector ───
        sel_frame = tk.Frame(self, bg=BG)
        sel_frame.pack(pady=(0, 10))

        self.lbl_src = tk.Label(sel_frame, text=self.t("src_label"), font=FONT_BODY, bg=BG, fg=TEXT2)
        self.lbl_src.pack(side=tk.LEFT, padx=(0, 10))

        self.src_base = tk.IntVar(value=10)
        self.src_buttons = {}
        bases = self.t("bases")
        colors = [SUCCESS, ACCENT, TEXT, WARNING]
        for i, (base, label) in enumerate(zip([2, 8, 10, 16], bases)):
            btn = tk.Button(sel_frame, text=label, font=FONT_BODY,
                           bg=SURFACE2, fg=TEXT2, relief=tk.FLAT, bd=0,
                           padx=18, pady=7, cursor="hand2",
                           command=lambda b=base: self._set_src_base(b))
            btn.pack(side=tk.LEFT, padx=3)
            self.src_buttons[base] = (btn, colors[i])

        # ─── Input ───
        input_frame = tk.Frame(self, bg=BG)
        input_frame.pack(pady=(12, 6))

        self.entry = tk.Entry(input_frame, font=("Consolas", 24, "bold"), width=22,
                              bg=SURFACE, fg=TEXT, insertbackground=ACCENT,
                              relief=tk.FLAT, bd=0, justify=tk.CENTER,
                              highlightthickness=2, highlightcolor=ACCENT,
                              highlightbackground=BORDER)
        self.entry.pack(ipady=12)
        self.entry.bind("<KeyRelease>", lambda e: self._convert())
        self.entry.focus_set()

        self.lbl_error = tk.Label(self, text="", font=FONT_SMALL, bg=BG, fg=DANGER)
        self.lbl_error.pack(pady=(2, 8))

        # ─── Separator ───
        sep_frame = tk.Frame(self, bg=BG)
        sep_frame.pack(fill=tk.X, padx=40, pady=(4, 16))
        tk.Frame(sep_frame, bg=BORDER, height=1).pack(fill=tk.X)

        # ─── Results ───
        self.lbl_result_title = tk.Label(self, text=self.t("result_title"), font=FONT_H2, bg=BG, fg=TEXT)
        self.lbl_result_title.pack(anchor=tk.W, padx=40, pady=(0, 12))

        self.result_frame = tk.Frame(self, bg=BG)
        self.result_frame.pack(fill=tk.X, padx=28)

        self.result_widgets = {}
        bases = self.t("bases")
        base_vals = [2, 8, 10, 16]
        # 高辨识度配色：背景色 + 文字色
        tag_styles = [
            ("#059669", "#ffffff"),   # 二进制 — 深绿底白字
            ("#2563eb", "#ffffff"),   # 八进制 — 蓝底白字
            ("#cbd5e1", "#0f172a"),   # 十进制 — 浅灰底深色字
            ("#d97706", "#ffffff"),   # 十六进制 — 琥珀底白字
        ]

        for base, name, (tag_bg, tag_fg) in zip(base_vals, bases, tag_styles):
            card = tk.Frame(self.result_frame, bg=SURFACE, bd=0,
                           highlightthickness=1, highlightbackground=BORDER)
            card.pack(fill=tk.X, pady=3)

            # Color tag — larger, bolder, high contrast
            tag = tk.Label(card, text=name, font=("Microsoft YaHei UI", 11, "bold"),
                          bg=tag_bg, fg=tag_fg, width=9, padx=12, pady=10)
            tag.pack(side=tk.LEFT)

            # Value
            value_label = tk.Label(card, text="—", font=FONT_MONO, bg=SURFACE, fg=TEXT)
            value_label.pack(side=tk.LEFT, padx=(16, 8), pady=14)

            # Copy button
            copy_btn = tk.Button(card, text="📋", font=("", 14), bg=SURFACE2, fg=TEXT2,
                                relief=tk.FLAT, bd=0, padx=12, pady=6, cursor="hand2",
                                command=lambda v=value_label: self._copy_value(v))
            copy_btn.pack(side=tk.RIGHT, padx=(0, 12), pady=10)

            self.result_widgets[base] = (value_label, copy_btn)

        # Init
        self._set_src_base(10, init=True)

    # ─── Language Toggle ───
    def _toggle_lang(self):
        self.lang = "en" if self.lang == "zh" else "zh"
        self.btn_lang.config(text="中" if self.lang == "en" else "EN")
        self._refresh_labels()

    def _refresh_labels(self):
        self.lbl_title.config(text=self.t("title"))
        self.title(self.t("title") + " — Base Converter")
        self.lbl_subtitle.config(text=self.t("subtitle"))
        self.lbl_src.config(text=self.t("src_label"))
        self.lbl_result_title.config(text=self.t("result_title"))

        # Refresh base button labels
        bases = self.t("bases")
        for base, name in zip([2, 8, 10, 16], bases):
            btn, color = self.src_buttons[base]
            btn.config(text=name)

        # Refresh result card tags
        for base, name in zip([2, 8, 10, 16], bases):
            card = self.result_widgets[base][0].master
            tag = card.winfo_children()[0]
            tag.config(text=name)

        # Refresh error text
        val = self._parse_input()
        if val is None and self.entry.get().strip():
            self.lbl_error.config(text=self.t("format_error"))

        self._convert()

    # ─── Source Base ───
    def _set_src_base(self, base, init=False):
        self.src_base.set(base)
        # 高辨识度激活色
        active_colors = {2: "#059669", 8: "#2563eb", 10: "#475569", 16: "#d97706"}
        for b, (btn, _) in self.src_buttons.items():
            if b == base:
                btn.config(bg=active_colors[b], fg="#ffffff")
            else:
                btn.config(bg=SURFACE2, fg=TEXT2)
        if not init:
            self._convert()

    # ─── Parse ───
    def _parse_input(self):
        text = self.entry.get().strip()
        if not text:
            return None
        src = self.src_base.get()
        try:
            return int(text, src)
        except ValueError:
            return None

    # ─── Convert ───
    def _convert(self):
        val = self._parse_input()

        if val is None:
            has_text = bool(self.entry.get().strip())
            self.lbl_error.config(text=self.t("format_error") if has_text else "")
            for base in [2, 8, 10, 16]:
                self.result_widgets[base][0].config(text="—")
            return

        self.lbl_error.config(text="")

        results = {
            2:  self._fmt_bin(val),
            8:  oct(val)[2:],
            10: str(val),
            16: hex(val)[2:].upper(),
        }

        for base, text in results.items():
            lbl, _ = self.result_widgets[base]
            lbl.config(text=text)

    def _fmt_bin(self, val):
        s = bin(val)[2:]
        parts = []
        for i, ch in enumerate(reversed(s)):
            if i > 0 and i % 4 == 0:
                parts.append(" ")
            parts.append(ch)
        return "".join(reversed(parts))

    # ─── Copy ───
    def _copy_value(self, label):
        text = label.cget("text")
        if text and text != "—":
            self.clipboard_clear()
            self.clipboard_append(text)
            orig = label.cget("fg")
            label.config(fg=ACCENT)
            self.after(500, lambda: label.config(fg=orig))


if __name__ == "__main__":
    app = App()
    app.mainloop()
