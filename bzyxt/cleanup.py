import os
import time
from sleep_utils import interruptible_sleep


def cleanup_screenshots(folder_path, stop_event, interval=60, max_age_minutes=1):
    while not stop_event.is_set():
        current_time = time.time()

        # 遍历文件夹中的图片文件
        screenshots = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

        for screenshot in screenshots:
            screenshot_path = os.path.join(folder_path, screenshot)
            try:
                modified_time = os.path.getmtime(screenshot_path)
                file_age_minutes = (current_time - modified_time) / 60

                if file_age_minutes > max_age_minutes:
                    os.remove(screenshot_path)

            except Exception as e:
                print(f"删除文件时出错：{screenshot_path}，原因：{e}")

        interruptible_sleep(interval, stop_event)
