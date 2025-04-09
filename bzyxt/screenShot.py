import subprocess
import os
import sys
from datetime import datetime


def resource_path(relative_path):
    """
    获取资源文件路径，适配 PyInstaller 打包路径（运行时自动解压到临时目录）
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller运行时临时路径
    except Exception:
        base_path = os.path.abspath(".")  # 普通调试运行时路径
    return os.path.join(base_path, relative_path)


def capture_screenshot(folder_path="../screen_temp"):
    # 确保目标文件夹存在
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 获取 adb.exe 的完整路径（tools 目录下）
    adb_path = resource_path("tools/adb.exe")

    # 执行 adb 截图命令
    subprocess.run([adb_path, "shell", "screencap", "-p", "/sdcard/screenshot.png"])

    # 保存截图到本地
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(folder_path, f"screenshot_{timestamp}.png")

    # 执行 adb pull 命令拉取截图
    subprocess.run(
        [adb_path, "pull", "/sdcard/screenshot.png", screenshot_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return screenshot_path


# 测试运行
capture_screenshot()
