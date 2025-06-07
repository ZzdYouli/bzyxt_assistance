from threading import Thread
from basic_features.weeding import weeding
from cleanup import cleanup_screenshots
from sleep_utils import interruptible_sleep
import random
import logging


def cleanup_task(folder_path, stop_event):
    cleanup_screenshots(folder_path, stop_event)


def process_weeding(performance, stop_event, update_ui):
    while not stop_event.is_set():
        try:
            # 执行一次除草操作
            perf = performance.get() if hasattr(performance, "get") else performance
            weeding(perf, stop_event)

            # 可选：更新界面，显示除草状态

            update_ui(mode="weeding")  # 你也可以在update_ui()中添加"weeding"模式显示

        except Exception as e:
            logging.error(f"[除草模块] 发生异常: {e}")
            interruptible_sleep(30, stop_event)

        # 正常每次除草后，随机休息一段时间，模拟真人操作
        interruptible_sleep(random.uniform(3, 5), stop_event)


def start_weeding(folder_path, performance, stop_event, update_ui):
    # 启动清理临时文件夹的线程
    cleanup_thread = Thread(target=cleanup_task, args=(folder_path, stop_event))
    cleanup_thread.daemon = True
    cleanup_thread.start()

    # 启动 weeding 处理线程
    weeding_thread = Thread(target=process_weeding, args=(performance, stop_event, update_ui))
    weeding_thread.daemon = True
    weeding_thread.start()

    # 主循环，持续轻量检测停止信号
    while not stop_event.is_set():
        interruptible_sleep(0.2, stop_event)
