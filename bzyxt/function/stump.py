import logging
import time
from threading import Thread

from action_engine import adb_click
from basic_features.reset import reset
from basic_features.to_stump import to_stump
from image_handler import extract_timer
from screenShot import capture_screenshot
from sleep_utils import interruptible_sleep


def time_str_to_seconds(time_str):
    try:
        h, m, s = map(int, time_str.strip().split(":"))
        return h * 3600 + m * 60 + s
    except Exception as e:
        logging.error(f"❌ 时间字符串解析失败: {time_str} - 错误: {e}")
        return None


def stump(folder_path, stop_event, update_ui, performance):
    while not stop_event.is_set():
        try:
            latest_screenshot = capture_screenshot(folder_path)
            time_str = extract_timer(latest_screenshot)

            if time_str:
                seconds = time_str_to_seconds(time_str)
                update_ui(mode="stump", time=time_str)

                if seconds > 7205:
                    adb_click(40, 40, stop_event)
                    interruptible_sleep(0.8, stop_event)
                    adb_click(260, 770, stop_event)
                    interruptible_sleep(0.8, stop_event)
                    adb_click(360, 1200, stop_event)
                    interruptible_sleep(0.8, stop_event)
                    reset(performance, stop_event)
                    to_stump(performance, stop_event)

            else:
                reset(performance, stop_event)
                to_stump(performance, stop_event)
                interruptible_sleep(0.8, stop_event)

        except Exception as e:
            logging.error(f"❌ 打桩出错: {e}")

        time.sleep(2)


def start_stump(folder_path, stop_event, update_ui, performance):
    process_thread = Thread(target=stump,
                            args=(
                                folder_path, stop_event, update_ui, performance))
    process_thread.daemon = True
    process_thread.start()

    while not stop_event.is_set():
        interruptible_sleep(0.2, stop_event)
