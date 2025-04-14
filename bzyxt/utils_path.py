import os
import sys


def get_adb_path():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, "tools", "adb.exe")


def get_tesseract_path():
    """
    自动识别 tesseract.exe 路径，兼容 PyInstaller 打包环境
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, "tools", "tesseract-OCR", "tesseract.exe")
