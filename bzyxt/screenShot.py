import subprocess
import os
from datetime import datetime
from utils_path import get_adb_path


def capture_screenshot(folder_path="../screen_temp"):
    # 确保目标文件夹存在
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 获取 adb.exe 的完整路径（tools 目录下）

    # 执行 adb 截图命令

    subprocess.run([get_adb_path(), "shell", "screencap", "-p", "/sdcard/screenshot.png"])

    # 保存截图到本地
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(folder_path, f"screenshot_{timestamp}.png")

    # 执行 adb pull 命令拉取截图
    subprocess.run(
        [get_adb_path(), "pull", "/sdcard/screenshot.png", screenshot_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return screenshot_path


# 测试运行
capture_screenshot()
