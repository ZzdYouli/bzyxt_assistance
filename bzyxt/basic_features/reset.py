from action_engine import adb_click
import time


def reset(performance):
    a = 1.5 if performance == '低性能模式' else 1
    adb_click(0, 200)
    time.sleep(0.5 * a)

    adb_click(190, 190)
    time.sleep(0.5 * a)

    adb_click(250, 650)
    time.sleep(0.5 * a)

    adb_click(350, 550)
    time.sleep(1.5 * a)

    adb_click(610, 260)
    time.sleep(0.8 * a)

    adb_click(350, 585)
    time.sleep(1 * a)
