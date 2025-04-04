from action_engine import adb_click
import time


def to_bed():
    adb_click(170, 400)
    time.sleep(1.5)

    adb_click(150, 1200)
    time.sleep(0.8)

    adb_click(600, 910)
    time.sleep(0.8)
