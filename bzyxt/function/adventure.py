from threading import Thread

from action_engine import adb_click, smart_click_image, detect_image
from adventure_switch import adventure_switch
from basic_features.reset import reset
from basic_features.to_post import to_post
from sleep_utils import interruptible_sleep

count = 1
adventure_thread = None
is_running = False


def adventure(adventure_name, performance, stop_event, on_finish_callback=None):
    global count

    while not stop_event.is_set():
        a = 1.5 if performance == '低性能模式' else 1
        reset(performance, stop_event)
        # 待测试
        # smart_click_image("../assets/button/task.png", confidence=0.9, stop_event=stop_event)
        # interruptible_sleep(0.2 * a, stop_event)
        # adb_click(445, 1010, stop_event)
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
            if on_finish_callback:
                on_finish_callback()
            stop_event.set()
            break

        count += 1


def start_adventure(adventure_name, folder_path, performance, stop_event):
    from function.auto_practice import cleanup_task
    from utils import global_state as g
    from logic.control import start_button_click

    def on_adventure_finished():
        if g.start_button and g.running_label:
            g.start_button.config(text="启动", command=lambda: start_button_click(adventure_name))
            g.running_label.config(text="请选择")
            g.info_label.config(text="已遇到目标奇遇，任务结束")
        g.is_running = False

    global is_running, adventure_thread

    if is_running:
        stop_event.set()
        if adventure_thread is not None and adventure_thread.is_alive():
            adventure_thread.join(timeout=2)

    is_running = True

    cleanup_thread = Thread(target=cleanup_task, args=(folder_path, stop_event))
    cleanup_thread.daemon = True
    cleanup_thread.start()

    adventure_thread = Thread(target=adventure, args=(adventure_name, performance, stop_event, on_adventure_finished))
    adventure_thread.daemon = True
    adventure_thread.start()
