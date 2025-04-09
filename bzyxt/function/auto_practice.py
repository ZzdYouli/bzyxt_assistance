import random

from basic_features.bed_to_post import bed_to_post
from basic_features.reset import reset
from basic_features.to_bed import to_bed
from action_engine import adb_click, smart_click_and_scroll_loop, smart_click_and_scroll_loop_learn
from arts_to_practice.bhg.lqz import lqz
from arts_to_practice.mj.hfh import hfh
from arts_to_practice.cxg.xd import xd
from arts_to_practice.xyd.tqgs import tqgs
from path_pick import path_pick
from image_handler import extract_progress_data, extract_countdown_timer
from basic_features.pair import pair
from cleanup import cleanup_screenshots
from screenShot import capture_screenshot
from threading import Thread
from arts_switch import arts_switch
import time
import logging


def interruptible_sleep(seconds, stop_event, interval=0.2):
    """将长 sleep 拆成小段，便于及时响应 stop_event"""
    slept = 0
    while slept < seconds:
        if stop_event.is_set():
            break
        time.sleep(interval)
        slept += interval


def cleanup_task(folder_path, stop_event):
    cleanup_screenshots(folder_path, stop_event)


def process_screenshot(folder_path, speed, art_name, target_level, discount, stop_event, performance, update_ui):
    while not stop_event.is_set():
        try:

            latest_screenshot = capture_screenshot(folder_path)
            current, total, level = extract_progress_data(latest_screenshot)
            countdown = extract_countdown_timer(latest_screenshot)
            art_name = arts_switch(art_name)

            if total is not None:
                ratio = current / total
                need = 1 - (discount / 100)
                factor = need + 0.05
                interval = ((float(factor * total - current)) / speed)

                # 调用回调函数更新 UI
                # 调用回调函数更新 UI
                if ratio >= factor:
                    update_ui(mode="running")

                    adb_click(40, 40)
                    interruptible_sleep(0.8, stop_event)
                    adb_click(40, 40)
                    interruptible_sleep(0.8, stop_event)
                    bed_to_post(performance)

                    # === 正确转换绑定变量为字符串 ===
                    art = art_name.get() if hasattr(art_name, "get") else art_name
                    perf = performance.get() if hasattr(performance, "get") else performance
                    path = path_pick(art)

                    print(f"当前功法: {art}, 选择路径: {path}")  # 可选：用于调试

                    # === 路径判断并调用对应函数 ===
                    if path == "xd":
                        xd(art, perf)
                    elif path == "lqz":
                        lqz(art, perf)
                    elif path == "tqgs":
                        tqgs(art, perf)
                    elif path == "hfh":
                        hfh(art, perf)
                    else:
                        print(f"[警告] 未知功法路径: {art} => {path}")

                    to_bed(perf)

                    if smart_click_and_scroll_loop(art) is not True:
                        pair(art, perf)

                else:

                    # 调用回调函数更新 UI
                    update_ui(
                        progress=[current, total],
                        level=level,
                        remaining_time=interval * 60,

                        target_level=target_level,
                        mode="practice"
                    )
            elif countdown is not None:

                update_ui(

                    countdown=countdown,
                    mode="retreat"
                )

            else:
                reset(performance)
                to_bed(performance)
                if smart_click_and_scroll_loop(art_name) is not True:
                    pair(art_name, performance)

        except Exception as e:
            logging.error(f"处理截图时发生错误: {e}")
            interruptible_sleep(60, stop_event)

        interruptible_sleep(random.uniform(3, 5), stop_event)


def start_practice(folder_path, speed, art_name, target_level, discount, performance, stop_event, update_ui):
    # 启动清理线程
    cleanup_thread = Thread(target=cleanup_task, args=(folder_path, stop_event))
    cleanup_thread.daemon = True
    cleanup_thread.start()

    # 启动截图处理线程，并传入回调函数
    process_thread = Thread(target=process_screenshot,
                            args=(
                                folder_path, speed, art_name, target_level, discount, stop_event, performance,
                                update_ui))
    process_thread.daemon = True
    process_thread.start()

    # 主线程阻塞，直到 stop_event 被设置
    while not stop_event.is_set():
        time.sleep(0.2)
