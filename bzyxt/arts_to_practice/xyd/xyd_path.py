from action_engine import adb_click
import time


def xyd_path():
    adb_click(360, 80)
    time.sleep(1.5)

    adb_click(360, 0)
    time.sleep(1.5)

    adb_click(360, 480)
    time.sleep(2)

    adb_click(600, 1200)
    time.sleep(1)
