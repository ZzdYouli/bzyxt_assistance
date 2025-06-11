import logging
import random
from threading import Thread

from action_engine import adb_click, smart_click_and_scroll_loop, detect_image
from arts_switch import arts_switch
from arts_to_practice.bhg.lqz import lqz
from arts_to_practice.cxg.xd import xd
from arts_to_practice.mj.hfh import hfh
from arts_to_practice.xyd.tqgs import tqgs
from basic_features.bed_to_post import bed_to_post
from basic_features.pair import pair
from basic_features.reset import reset
from basic_features.to_bed import to_bed
from cleanup import cleanup_screenshots
from image_handler import extract_progress_data, extract_countdown_timer
from path_pick import path_pick
from screenShot import capture_screenshot
from sleep_utils import interruptible_sleep
from utils_path import resource_path


def cleanup_task(folder_path, stop_event):
    cleanup_screenshots(folder_path, stop_event)


def practice(folder_path, speed, art_name, discount, stop_event, performance, update_ui, check):
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

                art = art_name.get() if hasattr(art_name, "get") else art_name
                perf = performance.get() if hasattr(performance, "get") else performance
                path = path_pick(art)
                if check.get():
                    interval = ((float(factor * total - current)) / speed)
                    if ratio >= factor:
                        update_ui(mode="running")

                        adb_click(40, 40, stop_event)
                        interruptible_sleep(0.8, stop_event)
                        adb_click(40, 40, stop_event)
                        interruptible_sleep(0.8, stop_event)
                        bed_to_post(performance, stop_event)

                        if path == "xd":
                            xd(art, perf, stop_event)
                        elif path == "lqz":
                            lqz(art, perf, stop_event)
                        elif path == "tqgs":
                            tqgs(art, perf, stop_event)
                        elif path == "hfh":
                            hfh(art, perf, stop_event)
                        else:
                            raise ValueError(f"未知武学路径: {art} => {path}")

                        to_bed(perf, stop_event)

                        if smart_click_and_scroll_loop(art, stop_event=stop_event) is not True:
                            pair(art, perf, stop_event)
                else:
                    interval = ((float(total - current)) / speed)
                    if detect_image(resource_path("assets", "button", "find_pair.png"), stop_event=stop_event) is True:
                        pair(art, perf, stop_event)
                update_ui(
                    progress=[current, total],
                    level=level,
                    remaining_time=interval * 60,

                    mode="practice"
                )
            elif countdown is not None:
                update_ui(countdown=countdown, mode="retreat")

            else:
                reset(performance, stop_event)
                to_bed(performance, stop_event)
                if smart_click_and_scroll_loop(art_name, stop_event=stop_event) is not True:
                    pair(art_name, performance, stop_event)

        except Exception as e:
            logging.error(f"处理截图时发生错误: {e}")
            interruptible_sleep(30, stop_event)

        interruptible_sleep(random.uniform(3, 5), stop_event)


def start_practice(folder_path, speed, art_name, discount, performance, stop_event, update_ui, check):
    cleanup_thread = Thread(target=cleanup_task, args=(folder_path, stop_event))
    cleanup_thread.daemon = True
    cleanup_thread.start()

    process_thread = Thread(target=practice,
                            args=(
                                folder_path, speed, art_name, discount, stop_event, performance,
                                update_ui, check))
    process_thread.daemon = True
    process_thread.start()

    while not stop_event.is_set():
        interruptible_sleep(0.2, stop_event)
