from action_engine import adb_click
import time


def to_post():
    adb_click(630, 960)
    time.sleep(0.2)

    adb_click(500, 750)
    time.sleep(0.5)

    adb_click(365, 1140)
    time.sleep(1)

    adb_click(140, 540)
    time.sleep(0.5)
