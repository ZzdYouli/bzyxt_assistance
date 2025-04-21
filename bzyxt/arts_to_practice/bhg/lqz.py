from action_engine import adb_click, smart_click_image, smart_click_and_scroll_loop_learn
import time
from arts_to_practice.bhg.bhg_path import bhg_path
from basic_features.reset import reset
from sleep_utils import interruptible_sleep


def lqz(art_name, performance, stop_event):
    smart_click_image("../assets/post/bhg.png", confidence=0.8, stop_event=stop_event)

    interruptible_sleep(1.5, stop_event)

    bhg_path(performance, stop_event)
    smart_click_and_scroll_loop_learn(art_name, stop_event)
    interruptible_sleep(1, stop_event)

    smart_click_image("../assets/button/learn.png", confidence=0.5, stop_event=stop_event)
    interruptible_sleep(3.5, stop_event)

    adb_click(250, 820, stop_event)
    interruptible_sleep(1, stop_event)

    reset(performance, stop_event)
