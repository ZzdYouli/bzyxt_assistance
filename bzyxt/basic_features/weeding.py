from action_engine import adb_click, detect_image, smart_click_image
from basic_features.reset import reset

from sleep_utils import interruptible_sleep

start_x = 50
start_y = 720
step_x = 170
step_y = 120
cols = 5  # 每行点击5次
final_x = 730
final_y = 960


def weeding(performance, stop_event):
    a = 1.5 if performance == '低性能模式' else 1
    reset(performance, stop_event)
    if detect_image("../assets/button/running.png") is False:
        adb_click(630, 960, stop_event)
        interruptible_sleep(0.2 * a, stop_event)

    adb_click(500, 750, stop_event)
    interruptible_sleep(0.7 * a, stop_event)

    adb_click(365, 1140, stop_event)
    interruptible_sleep(1 * a, stop_event)

    adb_click(200, 320, stop_event)
    interruptible_sleep(1 * a, stop_event)

    if smart_click_image("../assets/button/weeding.png", stop_event) is False:
        y = start_y
        while y <= final_y:
            for i in range(cols):
                x = start_x + i * step_x
                adb_click(x, y, stop_event)
                interruptible_sleep(0.5 * a, stop_event)
                adb_click(x, y, stop_event)
                interruptible_sleep(0.5 * a, stop_event)

                # 检查是否点击到最后一个点
                if x == final_x and y == final_y:
                    return
            y += step_y
