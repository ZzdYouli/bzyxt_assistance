import logging
import subprocess
import time
import cv2
import pytesseract
import os
from screenShot import capture_screenshot  # 假设你已经实现了capture_screenshot函数
import numpy as np
from stop_event import stop_event  # 引入 stop_event 用于检查停止信号

# 可选：修改为你的 Tesseract 安装路径
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def adb_click(x, y):
    """通过 ADB 模拟点击操作"""
    if stop_event.is_set():
        return False

    result = subprocess.run(
        ["adb", "shell", "input", "tap", str(x), str(y)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        logging.info(f"❌ ADB 命令执行失败：{result.stderr}")
        return False

    return True


def detect_image(image_path, confidence=0.5, folder_path="../screen_temp"):
    """识别图像是否出现在当前截图中"""
    if stop_event.is_set():
        return False

    screenshot_path = capture_screenshot(folder_path)

    if not os.path.exists(screenshot_path):
        logging.info(f"❌ 无法找到截图文件 {screenshot_path}")
        return False

    screenshot = cv2.imread(screenshot_path)
    target_image = cv2.imread(image_path)

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(screenshot_gray, target_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= confidence)
    return loc[0].size > 0


def click_image(image_path, confidence=0.9, folder_path="../screen_temp"):
    """点击图像，点击前先进行截图"""
    if stop_event.is_set():
        return False

    screenshot_path = capture_screenshot(folder_path)  # 每次调用 capture_screenshot() 都传递文件夹路径

    if not os.path.exists(screenshot_path):
        logging.info(f"❌ 无法找到截图文件 {screenshot_path}")
        return False

    screenshot = cv2.imread(screenshot_path)
    target_image = cv2.imread(image_path)

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(screenshot_gray, target_gray, cv2.TM_CCOEFF_NORMED)
    threshold = confidence  # 设定匹配阈值
    loc = np.where(res >= threshold)

    if loc[0].size > 0:
        # 获取匹配到的位置
        top_left = (loc[1][0], loc[0][0])
        center_x = top_left[0] + target_image.shape[1] // 2
        center_y = top_left[1] + target_image.shape[0] // 2

        # 使用 ADB 执行点击
        adb_click(center_x, center_y)
        return True
    else:
        logging.info(f"❌ 未找到图像 [{image_path}]")
        return False


# --- 智能封装：点击前自动截图 ---
def smart_click_image(image_path, confidence, folder_path="../screen_temp"):
    if stop_event.is_set():
        return False

    capture_screenshot(folder_path)  # 每次点击前都截图
    result = click_image(image_path, confidence, folder_path)
    return result


def smart_scroll(folder_path="../screen_temp"):
    if stop_event.is_set():
        return False

    capture_screenshot(folder_path)  # 每次滚动前都截图

    # 滑动起点和终点
    start_x, start_y = 460, 800  # 滑动起点
    end_x, end_y = 460, 500  # 滑动终点
    duration = 1000  # 滑动时间（毫秒）

    try:
        result = subprocess.run(
            ["adb", "shell", "input", "swipe", str(start_x), str(start_y), str(end_x), str(end_y), str(duration)],
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            logging.info(f"❌ ADB 命令执行失败，错误信息：{result.stderr}")

    except Exception as e:
        logging.info(f"❌ 错误：{str(e)}")


def smart_click_and_scroll_loop(art_name, max_iterations=5,
                                folder_path="../screen_temp"):
    for i in range(max_iterations):
        if stop_event.is_set():
            return False

        if smart_click_image(f"../assets/Martial arts/{art_name}1.png", confidence=0.8):
            if detect_image("../assets/main_if/find_pair.png"):
                return False
            return True
        smart_scroll(folder_path)
        time.sleep(1.5)
    return False
