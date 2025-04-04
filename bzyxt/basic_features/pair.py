from basic_features.reset import reset
from action_engine import adb_click, smart_click_and_scroll_loop
import time


def pair(art_name):
    reset()
    adb_click(520, 400)
    time.sleep(1)
    adb_click(450, 1200)
    time.sleep(1)
    smart_click_and_scroll_loop(art_name)
