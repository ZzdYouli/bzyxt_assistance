import time
from action_engine import adb_click, smart_click_image, detect_image
from adventure_switch import adventure_switch
import logging
from basic_features.to_post import to_post
from basic_features.reset import reset
from threading import Thread

count = 1
adventure_thread = None  # 用于保存线程对象
is_running = False  # 用于标识冒险是否正在运行


def adventure(adventure_name, count_max, performance):
    global count
    from stop_event import stop_event

    while not stop_event.is_set():
        if 0 < count_max <= count:
            print(f"共刷新{count_max}次，未遇到{adventure_name}奇遇")
            break
        a = 1.5 if performance == '低性能模式' else 1
        reset(performance)
        smart_click_image("../assets/button/task.png")
        time.sleep(0.2 * a)
        adb_click(445, 1010)
        time.sleep(0.5 * a)
        to_post(performance)
        smart_click_image("../assets/post/tjs.png")
        time.sleep(0.5 * a)
        adb_click(445, 1010)
        time.sleep(0.5 * a)
        adb_click(0, 720)
        time.sleep(1.5 * a)
        print(f"已刷新{count}次奇遇")
        if detect_image(f"../assets/adventure/{adventure_switch(adventure_name)}.png", confidence=0.7):
            print(f"已遇到{adventure_name}奇遇")
            print(f"共遇到{count}次奇遇")
            break

        count += 1


# 用于启动线程的函数
def start_adventure(adventure_name, folder_path, count_max, performance):
    global is_running, adventure_thread
    from function.auto_practice import cleanup_task
    from stop_event import stop_event

    # 如果任务已经在运行，停止并清理旧的线程
    if is_running:
        stop_event.set()  # 通知停止当前线程
        if adventure_thread is not None and adventure_thread.is_alive():
            adventure_thread.join()  # 等待线程安全退出

    # 重置全局变量，准备启动新任务
    is_running = True
    count = 1  # 重置计数器

    # 启动清理线程
    cleanup_thread = Thread(target=cleanup_task, args=(folder_path, stop_event))
    cleanup_thread.daemon = True
    cleanup_thread.start()

    # 启动新的冒险任务线程
    adventure_thread = Thread(target=adventure, args=(adventure_name, count_max, performance))  # 传递 count_max
    adventure_thread.daemon = True
    adventure_thread.start()
