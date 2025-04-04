import subprocess
import os
from datetime import datetime


def capture_screenshot(folder_path="../screen_temp"):
    # 确保目标文件夹存在
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 执行 ADB 命令：截图并保存到模拟器内部
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/screenshot.png"])

    # 将截图文件从模拟器拉取到本地
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(folder_path, f"screenshot_{timestamp}.png")

    subprocess.run(
        ["adb", "pull", "/sdcard/screenshot.png", screenshot_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return screenshot_path


capture_screenshot()
