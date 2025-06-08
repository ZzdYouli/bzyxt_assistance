import os
import threading
import time
import tkinter.messagebox as msgbox
from collections import deque

from function.adventure import start_adventure
from function.auto_practice import start_practice
from logic.update_ui import update_ui
from task_switch import task_switch
from utils import global_state as g
from utils.connect_emulator import connect_emulator

error_history = {}


def on_adventure_finished(task_value):
    """用于在遇到目标奇遇后自动重置 UI 状态"""
    if g.start_button and g.running_label:
        g.start_button.config(text="启动", command=lambda: start_button_click(task_value))
        g.running_label.config(text="请选择")
        g.info_label.config(text="已遇到目标奇遇，任务结束")
    g.is_running = False


def start_button_click(task_value):
    if g.task_thread and g.task_thread.is_alive():
        g.stop_event.set()
        g.task_thread.join(timeout=2)
        g.task_thread = None
    if g.adventure_thread and g.adventure_thread.is_alive():
        g.stop_event.set()
        g.adventure_thread.join(timeout=2)
        g.adventure_thread = None

    g.stop_event = threading.Event()

    if not connect_emulator():
        msgbox.showerror("连接失败", "无法连接模拟器")
        return

    folder_path = "../screen_temp"
    os.makedirs(folder_path, exist_ok=True)

    try:
        task_type = task_switch(task_value)

        if task_type == "practice":
            g.task_thread = threading.Thread(
                target=start_practice,
                args=(
                    folder_path,
                    g.speed.get(),
                    g.art_name.get(),
                    g.discount.get(),
                    g.performance.get(),
                    g.stop_event,
                    update_ui,
                    g.check,
                )
            )
            g.task_thread.daemon = True
            g.task_thread.start()
            update_ui(mode="practice", progress=[0, 100])

        elif task_type == "adventure":
            g.adventure_thread = threading.Thread(
                target=start_adventure,
                args=(
                    g.adventure_name.get(),
                    folder_path,
                    g.performance.get(),
                    g.stop_event
                )
            )
            g.adventure_thread.daemon = True
            g.adventure_thread.start()
            update_ui(mode="adventure", progress=[0, 100])

        g.start_button.config(text="停止", command=lambda: stop_button_click(task_value))
        g.running_label.config(text="正在运行")
        g.is_running = True

    except Exception as e:
        error_key = str(e)
        now = time.time()
        dq = error_history.setdefault(error_key, deque())
        dq.append(now)
        while dq and now - dq[0] > 30:
            dq.popleft()

        if len(dq) >= 3:
            stop_button_click(task_value)
            msgbox.showerror("自动停止", f"同一错误30秒内发生3次，任务已停止。\n错误信息：{e}")
        else:
            msgbox.showerror("任务启动错误", f"启动线程时出错：{e}")

        print(f"[ERROR] 启动线程失败: {e}")


def stop_button_click(task_value):
    if g.stop_event:
        g.stop_event.set()

    if g.task_thread and g.task_thread.is_alive():
        g.task_thread.join(timeout=2)
        g.task_thread = None

    if g.adventure_thread and g.adventure_thread.is_alive():
        g.adventure_thread.join(timeout=2)
        g.adventure_thread = None

    g.is_running = False
    g.start_button.config(text="启动", command=lambda: start_button_click(task_value))
    g.running_label.config(text="请选择")
    g.info_label.config(text="找点事情做吧")
