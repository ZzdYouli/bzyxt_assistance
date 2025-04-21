from action_engine import adb_click
import time

from sleep_utils import interruptible_sleep


def to_bed(performance, stop_event):
    a = 1.5 if performance == '低性能模式' else 1
    adb_click(170, 400, stop_event)
    interruptible_sleep(1.5 * a, stop_event)

    adb_click(150, 1200, stop_event)
    interruptible_sleep(0.8 * a, stop_event)

    adb_click(600, 910, stop_event)
    interruptible_sleep(0.8 * a, stop_event)
