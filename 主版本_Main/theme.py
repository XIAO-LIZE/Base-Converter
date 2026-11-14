"""Theme state and palette for the main edition."""
from PySide6.QtCore import Property, QObject, QSettings, Qt, Signal, Slot
from PySide6.QtGui import QGuiApplication


DARK = {
    "window": "#05080e",
    "bgTop": "#04070d",
    "bgMid": "#071120",
    "bgBottom": "#0a1828",
    "glow1": "#662563eb", "glow2": "#242563eb", "glow3": "#002563eb",
    "glow4": "#380ea5e9", "glow5": "#140ea5e9", "glow6": "#000ea5e9",
    "glow7": "#407c3aed", "glow8": "#167c3aed", "glow9": "#007c3aed",
    "glow10": "#1c22d3ee", "glow11": "#0c22d3ee", "glow12": "#0022d3ee",
    "text": "#f2f7ff",
    "textStrong": "#eaf2ff",
    "textSecondary": "#8496ad",
    "textMuted": "#7f91aa",
    "textDim": "#65778f",
    "icon": "#93a4bd",
    "iconActive": "#ffffff",
    "controlHover": "#14ffffff",
    "closeHover": "#e81123",
    "onClose": "#ffffff",
    "buttonTint": "#0dffffff",
    "buttonHover": "#1affffff",
    "buttonBorder": "#21ffffff",
    "buttonText": "#9fb0c8",
    "primaryTint": "#4d4da6ff",
    "primaryBorder": "#734d9aff",
    "primaryText": "#f4f9ff",
    "fieldTint": "#73050a0f",
    "fieldBorder": "#21ffffff",
    "fieldText": "#eef5ff",
    "placeholder": "#64748b",
    "clearTint": "#0affffff",
    "clearHover": "#1affffff",
    "clearText": "#93a4bd",
    "cardTint": "#2e0e1621",
    "cardEdge": "#29c7dbff",
    "cardHighlight": "#47ffffff",
    "shadow": "#000000",
    "shadowOpacity": 0.45,
    "tabBarTint": "#8c0a111a",
    "tabSelection": "#474da6ff",
    "tabSelectionBorder": "#734d9aff",
    "tabText": "#8496ad",
    "tabTextActive": "#f4f9ff",
    "footerTint": "#8c091017",
    "segTint": "#52050a0f",
    "segBorder": "#1cffffff",
    "segSelection": "#524da6ff",
    "segSelectionBorder": "#734d9aff",
    "segText": "#8b9bb4",
    "segTextActive": "#f4f9ff",
    "rowTint": "#66050a0f",
    "rowBorder": "#17ffffff",
    "rowEven": "#06ffffff",
    "rowOdd": "#1a000000",
    "resultTint": "#66050a0f",
    "resultBorder": "#17ffffff",
    "labelTint": "#334d8ce6",
    "textValue": "#eaf2ff",
    "textCode": "#dbe7f7",
    "textDesc": "#8fa2ba",
    "tableMuted": "#9fb0c8",
    "warning": "#f0b429",
    "scrollThumb": "#3b4a60",
    "error": "#ef4444",
    "success": "#10b981",
    "accent": "#4da6ff",
}

LIGHT = {
    "window": "#eef4fc",
    "bgTop": "#fbfdff",
    "bgMid": "#edf4fd",
    "bgBottom": "#dbe8f8",
    "glow1": "#1f2563eb", "glow2": "#0d2563eb", "glow3": "#002563eb",
    "glow4": "#1f0ea5e9", "glow5": "#0c0ea5e9", "glow6": "#000ea5e9",
    "glow7": "#1f7c3aed", "glow8": "#0d7c3aed", "glow9": "#007c3aed",
    "glow10": "#1422d3ee", "glow11": "#0822d3ee", "glow12": "#0022d3ee",
    "text": "#142033",
    "textStrong": "#1d2b3f",
    "textSecondary": "#5f7289",
    "textMuted": "#73869c",
    "textDim": "#8799ad",
    "icon": "#5f7289",
    "iconActive": "#1a73e8",
    "controlHover": "#141a73e8",
    "closeHover": "#d92b2b",
    "onClose": "#ffffff",
    "buttonTint": "#0f1a73e8",
    "buttonHover": "#1f1a73e8",
    "buttonBorder": "#2e1a73e8",
    "buttonText": "#3f5f82",
    "primaryTint": "#334da6ff",
    "primaryBorder": "#664da6ff",
    "primaryText": "#0b2b50",
    "fieldTint": "#e6ffffff",
    "fieldBorder": "#331a3a5c",
    "fieldText": "#142033",
    "placeholder": "#8a9aab",
    "clearTint": "#0f1a73e8",
    "clearHover": "#1f1a73e8",
    "clearText": "#5f7289",
    "cardTint": "#ccffffff",
    "cardEdge": "#331a3a5c",
    "cardHighlight": "#b3ffffff",
    "shadow": "#1a2c4a",
    "shadowOpacity": 0.18,
    "tabBarTint": "#b3ffffff",
    "tabSelection": "#334da6ff",
    "tabSelectionBorder": "#664da6ff",
    "tabText": "#5f7289",
    "tabTextActive": "#0f2b4a",
    "footerTint": "#ccffffff",
    "segTint": "#d9ffffff",
    "segBorder": "#2e1a3a5c",
    "segSelection": "#334da6ff",
    "segSelectionBorder": "#664da6ff",
    "segText": "#5f7289",
    "segTextActive": "#0b2b50",
    "rowTint": "#b3ffffff",
    "rowBorder": "#1f1a3a5c",
    "rowEven": "#0d1a73e8",
    "rowOdd": "#141a3a5c",
    "resultTint": "#b3ffffff",
    "resultBorder": "#1f1a3a5c",
    "labelTint": "#264d8ce6",
    "textValue": "#142033",
    "textCode": "#1d2b3f",
    "textDesc": "#5f7289",
    "tableMuted": "#5f7289",
    "warning": "#b45309",
    "scrollThumb": "#9aaec4",
    "error": "#dc2626",
    "success": "#059669",
    "accent": "#1a73e8",
}


class Theme(QObject):
    modeChanged = Signal()
    themeChanged = Signal()

    def __init__(self):
        super().__init__()
        self._settings = QSettings("XiaoLize", "BaseConverter")
        saved = str(self._settings.value("appearance/mode", "dark"))
        self._mode = saved if saved in ("dark", "light", "system") else "dark"
        self._system_dark = self._detect_system()
        hints = QGuiApplication.styleHints()
        if hints is not None:
            hints.colorSchemeChanged.connect(self._on_system_scheme)
        self._dark = self._resolve_dark()

    @staticmethod
    def _detect_system() -> bool:
        try:
            scheme = QGuiApplication.styleHints().colorScheme()
            return scheme != Qt.ColorScheme.Light
        except Exception:
            return True

    def _resolve_dark(self) -> bool:
        if self._mode == "dark":
            return True
        if self._mode == "light":
            return False
        return self._system_dark

    def _on_system_scheme(self, *_args) -> None:
        self._system_dark = self._detect_system()
        if self._mode == "system":
            self._set_dark(self._system_dark)

    def _set_dark(self, dark: bool) -> None:
        if dark != self._dark:
            self._dark = dark
            self.themeChanged.emit()

    @Property(str, notify=modeChanged)
    def mode(self):
        return self._mode

    @Property(bool, notify=themeChanged)
    def dark(self):
        return self._dark

    @Property("QVariantMap", notify=themeChanged)
    def colors(self):
        return dict(DARK if self._dark else LIGHT)

    @Slot(str)
    def setMode(self, mode: str) -> None:
        if mode not in ("dark", "light", "system") or mode == self._mode:
            return
        self._mode = mode
        self._settings.setValue("appearance/mode", mode)
        self.modeChanged.emit()
        self._set_dark(self._resolve_dark())

    @Slot()
    def cycleMode(self) -> None:
        order = ("dark", "light", "system")
        self.setMode(order[(order.index(self._mode) + 1) % len(order)])
