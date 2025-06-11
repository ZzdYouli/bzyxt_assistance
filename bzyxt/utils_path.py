import os
import sys


def get_adb_path():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, "tools", "adb.exe")


def get_base_path():
    """获取当前项目的根路径"""
    if getattr(sys, 'frozen', False):
        # 被打包成 exe
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    else:
        # 开发模式
        return os.path.dirname(os.path.abspath(__file__))


def resource_path(*relative_path):
    """获取资源文件的绝对路径"""
    return os.path.join(get_base_path(), *relative_path)
