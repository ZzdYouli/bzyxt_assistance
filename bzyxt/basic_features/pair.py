from basic_features.reset import reset
from action_engine import adb_click, smart_click_and_scroll_loop
import time
from sleep_utils import interruptible_sleep


def pair(art_name, performance, stop_event):
    a = 1.5 if performance == '低性能模式' else 1
    reset(performance, stop_event)
    adb_click(520, 400, stop_event)

    interruptible_sleep(1 * a, stop_event)
    adb_click(450, 1200, stop_event)
    interruptible_sleep(1 * a, stop_event)
    smart_click_and_scroll_loop(art_name)
