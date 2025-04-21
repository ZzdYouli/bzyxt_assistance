from action_engine import adb_click, detect_image, smart_click_image
import time

from sleep_utils import interruptible_sleep


def to_post(performance, stop_event):
    a = 1.5 if performance == '低性能模式' else 1
    if detect_image("../assets/button/running.png") is False:
        adb_click(630, 960, stop_event)
        interruptible_sleep(0.2 * a, stop_event)

    adb_click(500, 750, stop_event)
    interruptible_sleep(0.7 * a, stop_event)

    adb_click(365, 1140, stop_event)
    interruptible_sleep(1 * a, stop_event)

    smart_click_image("../assets/button/post.png", stop_event)
    interruptible_sleep(0.8 * a, stop_event)
