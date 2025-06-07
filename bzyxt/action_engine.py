import logging
import os
import subprocess

import cv2
import numpy as np
import pytesseract

from screenShot import capture_screenshot  # 假设你已经实现了capture_screenshot函数
from sleep_utils import interruptible_sleep
from utils import global_state as g
from utils_path import get_adb_path

# 可选：修改为你的 Tesseract 安装路径
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def adb_click(x, y, stop_event):
    if stop_event and stop_event.is_set():
        return False

    result = subprocess.run(
        [get_adb_path(), "-s", g.adb_target_device, "shell", "input", "tap", str(x), str(y)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        logging.info(f"❌ ADB 命令执行失败：{result.stderr}")
        return False

    return True


def detect_image(image_path, confidence=0.8, folder_path="../screen_temp", stop_event=None):
    if stop_event and stop_event.is_set():
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


def click_image(image_path, confidence=0.8, folder_path="../screen_temp", stop_event=None):
    if stop_event and stop_event.is_set():
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

    if loc[0].size > 0:
        top_left = (loc[1][0], loc[0][0])
        center_x = top_left[0] + target_image.shape[1] // 2
        center_y = top_left[1] + target_image.shape[0] // 2

        adb_click(center_x, center_y, stop_event)
        return True
    else:
        logging.info(f"❌ 未找到图像 [{image_path}]")
        return False


def smart_click_image(image_path, confidence=0.9, folder_path="../screen_temp", stop_event=None, max_retry=5):
    if stop_event and stop_event.is_set():
        return False

    for attempt in range(max_retry):
        if stop_event and stop_event.is_set():
            return False

        logging.info(f"[点击尝试] 第 {attempt + 1} 次尝试点击图像：{image_path}")
        capture_screenshot(folder_path)
        success = click_image(image_path, confidence, folder_path, stop_event)

        if success:
            logging.info("[点击成功]")
            return True
        else:
            logging.info(f"[未匹配到图像] 第 {attempt + 1} 次未命中 {image_path}")

    return False


def smart_scroll(folder_path="../screen_temp", stop_event=None):
    if stop_event and stop_event.is_set():
        return False

    capture_screenshot(folder_path)

    start_x, start_y = 460, 800
    end_x, end_y = 460, 500
    duration = 1000

    try:
        result = subprocess.run(
            [get_adb_path(), "-s", g.adb_target_device, "shell", "input", "swipe", str(start_x), str(start_y),
             str(end_x), str(end_y),
             str(duration)],
            text=True,
            capture_output=True
        )
        if result.returncode != 0:
            logging.info(f"❌ ADB 命令执行失败，错误信息：{result.stderr}")
    except Exception as e:
        logging.info(f"❌ 错误：{str(e)}")


def smart_scroll_learn(folder_path="../screen_temp", stop_event=None):
    if stop_event and stop_event.is_set():
        return False

    capture_screenshot(folder_path)

    start_x, start_y = 350, 1200
    end_x, end_y = 350, 900
    duration = 1000

    try:
        result = subprocess.run(
            [get_adb_path(), "-s", g.adb_target_device, "shell", "input", "swipe", str(start_x), str(start_y),
             str(end_x), str(end_y),
             str(duration)],
            text=True,
            capture_output=True
        )
        if result.returncode != 0:
            logging.info(f"❌ ADB 命令执行失败，错误信息：{result.stderr}")
    except Exception as e:
        logging.info(f"❌ 错误：{str(e)}")


def smart_click_and_scroll_loop(art_name, max_iterations=5, folder_path="../screen_temp", stop_event=None):
    for i in range(max_iterations):
        if stop_event and stop_event.is_set():
            return False

        if smart_click_image(f"../assets/Martial arts/{art_name}.png", confidence=0.9, folder_path=folder_path,
                             stop_event=stop_event):
            if detect_image("../assets/main_if/find_pair.png", stop_event=stop_event):
                return False
            return True

        smart_scroll(folder_path, stop_event)
        interruptible_sleep(1.5, stop_event)
    return False


def smart_click_and_scroll_loop_learn(art_name, max_iterations=5, folder_path="../screen_temp", stop_event=None):
    for i in range(max_iterations):
        if stop_event and stop_event.is_set():
            return False

        if smart_click_image(f"../assets/Martial arts/{art_name}1.png", confidence=0.9, folder_path=folder_path,
                             stop_event=stop_event):
            if detect_image("../assets/main_if/find_pair.png", stop_event=stop_event):
                return False
            return True

        smart_scroll_learn(folder_path, stop_event)
        interruptible_sleep(1.5, stop_event)
    return False
