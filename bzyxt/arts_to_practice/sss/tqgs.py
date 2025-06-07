from action_engine import adb_click, smart_click_image, smart_click_and_scroll_loop_learn
from basic_features.reset import reset
from arts_to_practice.xyd.xyd_path import xyd_path
from sleep_utils import interruptible_sleep


def tqgs(art_name, performance, stop_event):
    a = 1.5 if performance == '低性能模式' else 1
    smart_click_image("../assets/post/xyd.png", confidence=0.8, stop_event=stop_event)
    interruptible_sleep(1.5, stop_event)

    xyd_path(performance, stop_event)
    smart_click_and_scroll_loop_learn(art_name, stop_event)
    interruptible_sleep(1, stop_event)

    smart_click_image("../assets/button/learn.png", confidence=0.5, stop_event=stop_event)
    interruptible_sleep(3.5, stop_event)

    adb_click(250, 820, stop_event)
    interruptible_sleep(1, stop_event)

    reset(performance, stop_event)
