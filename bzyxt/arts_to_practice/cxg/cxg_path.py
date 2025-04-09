from action_engine import adb_click
import time


def cxg_path():
    adb_click(440, 260)
    time.sleep(1.5)

    adb_click(360, 160)
    time.sleep(1.5)

    adb_click(360, 500)
    time.sleep(2)

    adb_click(600, 1200)
    time.sleep(1)
