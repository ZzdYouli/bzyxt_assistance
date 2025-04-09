from action_engine import adb_click, detect_image, smart_click_image
import time


def to_post(performance):
    a = 1.5 if performance == '低性能模式' else 1
    if detect_image("../assets/button/running.png") is False:
        adb_click(630, 960)
        time.sleep(0.2 * a)

    adb_click(500, 750)
    time.sleep(0.7 * a)

    adb_click(365, 1140)
    time.sleep(1 * a)

    smart_click_image("../assets/button/post.png")
    time.sleep(0.8 * a)
