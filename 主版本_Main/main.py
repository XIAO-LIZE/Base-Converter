"""Main visual edition entry point: PySide6 + QML, Liquid-Glass-inspired UI."""
import base64
import ctypes
import importlib.util
import sys
import tempfile
import traceback
from ctypes import wintypes
from pathlib import Path

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QGuiApplication, QIcon, QPixmap
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import Backend  # noqa: E402

LOG_FILE = Path(tempfile.gettempdir()) / "BaseConverter-Glass.log"


def _log(message: str) -> None:
    try:
        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(message.rstrip() + "\n")
    except OSError:
        pass


def _qml_entry() -> Path:
    """Works from source, PyInstaller onedir and onefile layouts."""
    candidates = []
    if getattr(sys, "frozen", False):
        bundle = Path(getattr(sys, "_MEIPASS", HERE))
        candidates.extend([
            bundle / "glass" / "qml" / "Main.qml",
            bundle / "qml" / "Main.qml",
        ])
    candidates.append(HERE / "qml" / "Main.qml")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _excepthook(kind, value, tb) -> None:
    _log("".join(traceback.format_exception(kind, value, tb)))
    sys.__excepthook__(kind, value, tb)


sys.excepthook = _excepthook



def _dark_titlebar(window_id: int) -> None:
    """Match the Qt main window to the dark glass content on Windows 11."""
    try:
        dwm = ctypes.windll.dwmapi
        dwm.DwmSetWindowAttribute.argtypes = [
            wintypes.HWND, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD]
        dwm.DwmSetWindowAttribute.restype = ctypes.c_long

        def set_attr(attr: int, value: int) -> None:
            v = ctypes.c_int(value)
            dwm.DwmSetWindowAttribute(window_id, attr, ctypes.byref(v),
                                      ctypes.sizeof(v))

        set_attr(20, 1)  # DWMWA_USE_IMMERSIVE_DARK_MODE
        set_attr(19, 1)  # pre-20H1 fallback
        set_attr(33, 2)  # DWMWA_WINDOW_CORNER_PREFERENCE: round corners
    except Exception:
        pass


def _app_icon() -> QIcon:
    local = HERE / "icon.png"
    if local.exists():
        return QIcon(str(local))
    try:
        spec = importlib.util.spec_from_file_location(
            "bc_main", ROOT / "单文件版本_SingleFile" / "main.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(module.ICON_PNG))
        return QIcon(pixmap)
    except Exception:
        return QIcon()


def main() -> int:
    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "XiaoLize.BaseConverter")
        except Exception:
            pass

    app = QGuiApplication(sys.argv)
    app.setApplicationName("BaseConverter")
    app.setOrganizationName("XiaoLize")
    app.setWindowIcon(_app_icon())
    QQuickStyle.setStyle("Basic")

    engine = QQmlApplicationEngine()
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)
    engine.warnings.connect(
        lambda warnings: _log("QML: " + "; ".join(w.toString() for w in warnings)))
    qml = _qml_entry()
    _log(f"---- start frozen={getattr(sys, 'frozen', False)} qml={qml}")
    engine.load(QUrl.fromLocalFile(str(qml)))
    _log(f"root objects: {len(engine.rootObjects())}")
    if not engine.rootObjects():
        return 1

    window = engine.rootObjects()[0]
    if sys.platform == "win32":
        def apply_titlebar() -> None:
            try:
                hwnd = int(window.winId())
                _dark_titlebar(hwnd)
                user32 = ctypes.windll.user32
                user32.GetParent.argtypes = [wintypes.HWND]
                user32.GetParent.restype = wintypes.HWND
                parent = user32.GetParent(hwnd)
                if parent:
                    _dark_titlebar(parent)
            except Exception:
                pass
        QTimer.singleShot(0, apply_titlebar)
        QTimer.singleShot(250, apply_titlebar)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
