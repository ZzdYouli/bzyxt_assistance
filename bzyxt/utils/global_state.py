# utils/global_state.py

import tkinter as tk

# 主窗口（需在 main.py 中传入）
root = None

# tkinter 变量初始化
speed = None
art_name = None
discount = None
adventure_name = None
task = None
performance = None
emulator = None
weeding = None
check = None

# 控制变量（非tk类型）
is_running = False
start_button = None
task_thread = None
adventure_thread = None
stop_event = None
info_label = None
running_label = None
adb_target_device = None  # 用于 adb -s 连接指定设备
fail_count = 0
saved_task_info = {}


def init_variables(master):
    global root, speed, art_name,  discount
    global adventure_name,  task, performance
    global emulator, weeding, check

    root = master

    # 初始化 tkinter 控件绑定变量
    speed = tk.DoubleVar(master, value=100000)
    art_name = tk.StringVar(master, value="玉女剑法")
    discount = tk.DoubleVar()
    adventure_name = tk.StringVar(master, value="赌场")
    task = tk.StringVar(master, value="躺床")
    performance = tk.StringVar(master, value="高性能模式")
    emulator = tk.StringVar(master, value="雷电")
    weeding = tk.BooleanVar(master, value=True)
    check = tk.BooleanVar(master, value=True)
