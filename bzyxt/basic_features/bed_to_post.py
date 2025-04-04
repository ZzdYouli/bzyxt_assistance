from action_engine import adb_click
import time


def bed_to_post():
    adb_click(630, 960)
    time.sleep(1)

    adb_click(580, 810)
    time.sleep(1)

    adb_click(350, 1140)
    time.sleep(1)

    adb_click(140, 550)
    time.sleep(1)
