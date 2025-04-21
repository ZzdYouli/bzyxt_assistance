from action_engine import adb_click
import time
from sleep_utils import interruptible_sleep

def cxg_path(performance, stop_event):
    a = 1.5 if performance == '低性能模式' else 1
    adb_click(440, 260, stop_event)

    interruptible_sleep(1.5 * a, stop_event)

    adb_click(360, 160, stop_event)
    interruptible_sleep(1.5 * a, stop_event)

    adb_click(360, 500, stop_event)
    interruptible_sleep(2 * a, stop_event)

    adb_click(600, 1200, stop_event)
    interruptible_sleep(1 * a, stop_event)
