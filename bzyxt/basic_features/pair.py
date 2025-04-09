from basic_features.reset import reset
from action_engine import adb_click, smart_click_and_scroll_loop
import time


def pair(art_name, performance):
    a = 1.5 if performance == '低性能模式' else 1
    reset(performance)
    adb_click(520, 400)
    time.sleep(1 * a)
    adb_click(450, 1200)
    time.sleep(1 * a)
    smart_click_and_scroll_loop(art_name)
