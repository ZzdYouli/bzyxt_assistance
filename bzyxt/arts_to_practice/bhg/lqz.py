from action_engine import adb_click, smart_click_image, smart_click_and_scroll_loop_learn
import time
from arts_to_practice.bhg.bhg_path import bhg_path
from basic_features.reset import reset


def lqz(art_name, performance):
    smart_click_image("../assets/post/bhg.png", confidence=0.8)
    time.sleep(1.5)

    bhg_path()
    smart_click_and_scroll_loop_learn(art_name)
    time.sleep(1)

    smart_click_image("../assets/button/learn.png", confidence=0.5)
    time.sleep(3.5)

    adb_click(250, 820)
    time.sleep(1)

    reset(performance)
