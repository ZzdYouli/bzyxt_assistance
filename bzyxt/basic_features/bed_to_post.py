from action_engine import adb_click, detect_image, smart_click_image
import time

from sleep_utils import interruptible_sleep


def bed_to_post(performance, stop_event):
    a = 1.5 if performance == '低性能模式' else 1
    if detect_image("../assets/button/running.png") is False:
        adb_click(630, 960, stop_event)
        interruptible_sleep(0.2 * a, stop_event)

    adb_click(580, 810, stop_event)
    interruptible_sleep(1 * a, stop_event)

    adb_click(350, 1140, stop_event)
    interruptible_sleep(1 * a, stop_event)

    smart_click_image("../assets/button/post.png", confidence=0.9, stop_event=stop_event)
    interruptible_sleep(0.8 * a, stop_event)
