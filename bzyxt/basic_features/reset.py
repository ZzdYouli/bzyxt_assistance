from action_engine import adb_click
import time

from sleep_utils import interruptible_sleep


def reset(performance, stop_event):
    a = 1.5 if performance == '低性能模式' else 1
    adb_click(0, 200, stop_event)
    interruptible_sleep(0.5 * a, stop_event)

    adb_click(190, 190, stop_event)
    interruptible_sleep(0.5 * a, stop_event)

    adb_click(250, 650, stop_event)
    interruptible_sleep(0.5 * a, stop_event)

    adb_click(350, 550, stop_event)
    interruptible_sleep(1.5 * a, stop_event)

    adb_click(610, 260, stop_event)
    interruptible_sleep(0.8 * a, stop_event)

    adb_click(350, 585, stop_event)
    interruptible_sleep(2 * a, stop_event)
