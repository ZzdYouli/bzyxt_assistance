from action_engine import adb_click
import time


def to_bed(performance):
    a = 1.5 if performance == '低性能模式' else 1
    adb_click(170, 400)
    time.sleep(1.5 * a)

    adb_click(150, 1200)
    time.sleep(0.8 * a)

    adb_click(600, 910)
    time.sleep(0.8 * a)
