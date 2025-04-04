from action_engine import adb_click
import time


def bhg_path():
    adb_click(440, 300)
    time.sleep(1.5)

    adb_click(360, 10)
    time.sleep(2.5)

    adb_click(360, 350)
    time.sleep(2)

    adb_click(360, 10)
    time.sleep(2)

    adb_click(210, 680)
    time.sleep(2)

    adb_click(600, 1200)
    time.sleep(1)
