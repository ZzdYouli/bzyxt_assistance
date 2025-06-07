# ui/home.py
import tkinter as tk
from tkinter import ttk
from utils import global_state as g


def home_page(mid_frame, right_frame, save_data, start_button_click, stop_button_click):
    # 清空中间区
    for widget in mid_frame.winfo_children():
        widget.pack_forget()

    # 调度器区
    separator = tk.Frame(mid_frame, bg="gray", height=2)
    separator.pack(fill="x", padx=5, pady=5)

    scheduler_frame = tk.Frame(mid_frame)
    scheduler_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(scheduler_frame, text="调度器", font=("微软雅黑", 12, "bold")).pack(side="left")

    # 启动/停止按钮
    if g.is_running:
        g.start_button = tk.Button(scheduler_frame, text="停止", font=("微软雅黑", 10), width=8,
                                   command=lambda: stop_button_click(g.task.get()))
    else:
        g.start_button = tk.Button(scheduler_frame, text="启动", font=("微软雅黑", 10), width=8,
                                   command=lambda: start_button_click(g.task.get()))

    g.start_button.pack(side="right", padx=10)

    separator = tk.Frame(mid_frame, bg="gray", height=2)
    separator.pack(fill="x", padx=5, pady=10)

    # 正在运行区
    running_frame = tk.Frame(mid_frame)
    running_frame.pack(fill="x", padx=10)

    g.running_label = tk.Label(running_frame, text="想做什么：", font=("微软雅黑", 12, "bold"))
    g.running_label.pack(side="left")

    top_frame = tk.Frame(mid_frame)
    top_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

    task_combobox = ttk.Combobox(top_frame, values=["躺床", "刷奇遇"], textvariable=g.task)
    task_combobox.grid(row=0, column=1, sticky="w", padx=5)

    task_combobox.bind("<<ComboboxSelected>>", lambda event: save_data())

    # 右侧状态区
    right_frame.pack(side="right", fill="both", expand=True)
    if g.info_label is None:
        g.info_label = tk.Label(right_frame, text="找点事情做吧", font=("微软雅黑", 12, "bold"), bg="#ffffff")
        g.info_label.pack(pady=20)
    else:
        g.info_label.config(text="找点事情做吧")

    save_data()
