from action_engine import adb_click, detect_image,smart_click_image
import time


def to_post():
    if detect_image("../assets/button/running.png") is False:
        adb_click(630, 960)
        time.sleep(0.2)

    adb_click(500, 750)
    time.sleep(0.7)

    adb_click(365, 1140)
    time.sleep(1)

    smart_click_image("../assets/button/post.png")
    time.sleep(0.8)
