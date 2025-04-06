from action_engine import adb_click, detect_image, smart_click_image
import time


def bed_to_post():
    if detect_image("../assets/button/running.png") is False:
        adb_click(630, 960)
        time.sleep(0.2)

    adb_click(580, 810)
    time.sleep(1)

    adb_click(350, 1140)
    time.sleep(1)

    smart_click_image("../assets/button/post.png")
    time.sleep(0.8)
