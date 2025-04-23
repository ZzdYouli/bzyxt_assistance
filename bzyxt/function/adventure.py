import time
from action_engine import adb_click, smart_click_image, detect_image
from adventure_switch import adventure_switch
import logging
from basic_features.to_post import to_post
from basic_features.reset import reset
from threading import Thread

from sleep_utils import interruptible_sleep

count = 1
adventure_thread = None  # 用于保存线程对象
is_running = False  # 用于标识冒险是否正在运行


def adventure(adventure_name, count_max, performance, stop_event):
    global count

    while not stop_event.is_set():
        if 0 < count_max <= count:
            print(f"共刷新{count_max}次，未遇到{adventure_name}奇遇")
            break
        a = 1.5 if performance == '低性能模式' else 1
        reset(performance, stop_event)
        smart_click_image("../assets/button/task.png", confidence=0.9, stop_event=stop_event)
        interruptible_sleep(0.2 * a, stop_event)
        adb_click(445, 1010, stop_event)
        interruptible_sleep(0.5 * a, stop_event)
        to_post(performance, stop_event)
        smart_click_image("../assets/post/tjs.png", confidence=0.9, stop_event=stop_event)
        interruptible_sleep(0.5 * a, stop_event)
        adb_click(445, 1010, stop_event)
        interruptible_sleep(0.5 * a, stop_event)
        adb_click(0, 720, stop_event)
        interruptible_sleep(1.5 * a, stop_event)
        print(f"已刷新{count}次奇遇")
        if detect_image(f"../assets/adventure/{adventure_switch(adventure_name)}.png", confidence=0.7,
                        stop_event=stop_event):
            print(f"已遇到{adventure_name}奇遇")
            print(f"共遇到{count}次奇遇")
            break

        count += 1


def start_adventure(adventure_name, folder_path, count_max, performance, stop_event):
    global is_running, adventure_thread
    from function.auto_practice import cleanup_task

    if is_running:
        stop_event.set()
        if adventure_thread is not None and adventure_thread.is_alive():
            adventure_thread.join(timeout=2)

    is_running = True
    count = 1

    cleanup_thread = Thread(target=cleanup_task, args=(folder_path, stop_event))
    cleanup_thread.daemon = True
    cleanup_thread.start()

    adventure_thread = Thread(target=adventure, args=(adventure_name, count_max, performance, stop_event))
    adventure_thread.daemon = True
    adventure_thread.start()
