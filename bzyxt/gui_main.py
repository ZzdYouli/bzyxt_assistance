import sys
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
import json
import os
import threading

# === 导入后台逻辑与停止事件 ===
from function.auto_practice import start_practice
from stop_event import stop_event

# === 本地存储 JSON 文件路径 ===
data_file = 'settings.json'

# === 创建主窗口 ===
root = tk.Tk()
root.title("睡觉也修炼")
root.geometry("700x450")

# === 创建绑定变量 ===
speed = tk.DoubleVar(value=100000)  # 修炼速度默认值
art_name = tk.StringVar(value="玉女剑法")  # 默认功法名
target_level = tk.StringVar()  # 目标等级
discount = tk.DoubleVar()

# === 控制按钮状态 ===
is_running = False  # 标记程序是否在运行
start_button = None  # 用于后面引用“启动/停止”按钮
task_thread = None  # 后台线程引用


def update_ui(progress=None, level=None, remaining_time=None, target_level=None, mode="",
              countdown=None):
    if mode == "practice":
        info_text = (
            f"正在修炼：{art_name.get()}\n"
            f"当前等级：{level}\n"
            f"进度：[ {progress[0]} / {progress[1]} ]\n"
            f"预计剩余时间：{remaining_time:.1f} 分钟"
        )
    elif mode == "retreat":
        info_text = (
            f"闭关中：{art_name.get()}\n"
            f"剩余倒计时：{countdown}\n"
        )
    elif mode == "running":
        info_text = (
            "正在前往师傅处"
        )
    else:
        info_text = "正在初始化化"

    info_label.config(text=info_text)


# === 读取本地存储数据 ===
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            speed.set(data.get('speed', 100000))
            art_name.set(data.get('art_name', "玉女剑法"))
            target_level.set(data.get('target_level', ''))
            discount.set(data.get('discount', 0.0))


# === 保存数据到本地 ===
def save_data():
    data = {
        'speed': speed.get(),
        'art_name': art_name.get(),
        'target_level': target_level.get(),
        'discount': discount.get()
    }
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# === 启动函数：调用后台任务 ===
def start_button_click():
    global is_running, task_thread, info_label
    if not is_running:  # 如果当前不是运行状态
        stop_event.clear()  # 清除停止事件，准备开始任务

        # 从输入框中获取用户配置
        folder_path = "../screen_temp"
        speed_value = speed.get()
        art_name_value = art_name.get()
        target_level_value = target_level.get()
        discount_value = discount.get()

        # 启动后台线程处理修炼任务，并传入回调函数
        task_thread = threading.Thread(
            target=start_practice,
            args=(folder_path, speed_value, art_name_value, target_level_value, discount_value, stop_event, update_ui)
        )
        task_thread.daemon = True  # 设置为守护线程
        task_thread.start()

        # 更改按钮文本为“停止”
        start_button.config(text="停止", command=stop_button_click)
        is_running = True
    else:
        # 如果已经在运行，则调用停止函数
        stop_button_click()


# === 停止修炼任务 ===
def stop_button_click():
    global is_running, task_thread, info_label
    stop_event.set()  # 设置停止事件，通知后台线程退出
    print("停止修炼任务")

    # 等待后台线程安全结束
    if task_thread is not None and task_thread.is_alive():
        task_thread.join()

    # 恢复按钮文本为“启动”
    start_button.config(text="启动", command=start_button_click)
    is_running = False

    # 恢复信息显示为“当前暂无可修炼功法”
    if info_label:
        info_label.config(text="当前没有正在的修炼功法")  # 恢复显示文本


# === 界面逻辑：睡觉页 ===
def show_sleep_page():
    for widget in right_frame.winfo_children():
        widget.pack_forget()  # 隐藏所有控件

    container = tk.Frame(right_frame)
    container.pack(fill="both", expand=True)

    top_frame = tk.Frame(container)
    top_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

    tk.Label(top_frame, text="需要修炼的功法", font=("微软雅黑", 12)).grid(row=0, column=0, sticky="w")
    method_combobox = ttk.Combobox(top_frame, values=["玉女剑法", "飞蝶舞步", "素心掌"], textvariable=art_name)
    method_combobox.grid(row=0, column=1, sticky="w", padx=5)

    tk.Label(top_frame, text="目标等级：", font=("微软雅黑", 11)).grid(row=1, column=0, sticky="w", pady=10)
    target_level_entry = tk.Entry(top_frame, textvariable=target_level)
    target_level_entry.grid(row=1, column=1, sticky="w")

    separator = tk.Frame(container, bg="gray", height=2)
    separator.pack(fill="x", padx=5)

    bottom_frame = tk.Frame(container)
    bottom_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    tk.Label(bottom_frame, text="修炼速度：", font=("微软雅黑", 11)).grid(row=0, column=0, sticky="w", pady=5)
    speed_entry = tk.Entry(bottom_frame, textvariable=speed)
    speed_entry.grid(row=0, column=1, sticky="w")

    tk.Label(bottom_frame, text="潜能减免：", font=("微软雅黑", 11)).grid(row=1, column=0, sticky="w", pady=5)
    discount_entry = tk.Entry(bottom_frame, textvariable=discount)
    discount_entry.grid(row=1, column=1, sticky="w")
    tk.Label(bottom_frame, text="%", font=("微软雅黑", 10)).grid(row=1, column=2, sticky="w", padx=5)

    # 简单校验 0~100 范围
    def validate_discount(event=None):
        value = discount_entry.get()
        try:
            num = float(value)
            if not 0 <= num <= 100:
                raise ValueError
        except ValueError:
            msgbox.showerror("输入错误", "请输入0~100之间的数值")
            discount_entry.focus_set()

    discount_entry.bind("<Return>", validate_discount)
    discount_entry.bind("<FocusOut>", validate_discount)

    save_data()  # 每次切换界面时，保存一下数据


# === 界面逻辑：总览页 ===
def show_overview():
    global info_label
    for widget in right_frame.winfo_children():
        widget.pack_forget()  # 隐藏所有控件

    top_right = tk.Frame(right_frame, bg="#ffffff", height=100)
    top_right.pack(fill="x", pady=(0, 5))

    tk.Label(top_right, text="睡觉", font=("微软雅黑", 12, "bold"), bg="#ffffff").pack(side="left", padx=10, pady=10)

    global start_button
    if is_running:
        start_button = tk.Button(top_right, text="停止", font=("微软雅黑", 10), width=8, command=stop_button_click)
    else:
        start_button = tk.Button(top_right, text="启动", font=("微软雅黑", 10), width=8, command=start_button_click)
    start_button.pack(side="right", padx=10, pady=10)

    separator = tk.Frame(right_frame, bg="gray", height=2)
    separator.pack(fill="x", padx=5, pady=5)

    bottom_right = tk.Frame(right_frame, bg="#ffffff")
    bottom_right.pack(fill="both", expand=True)

    # 使用一个 Label 变量来显示动态内容
    info_label = tk.Label(bottom_right, text="当前没有正在修炼的功法", font=("微软雅黑", 12, "bold"), bg="#ffffff")
    info_label.pack(pady=20)

    save_data()


# === 读取并初始化数据 ===
load_data()

# === 主体布局 ===
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# 左侧按钮区
left_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
left_frame.pack(side="left", fill="y", padx=(0, 10), ipadx=10, ipady=10)

tk.Button(left_frame, text="总览", font=("微软雅黑", 12), width=12, command=show_overview).pack(pady=10)
tk.Button(left_frame, text="睡觉", font=("微软雅黑", 12), width=12, command=show_sleep_page).pack(pady=10)

# 右侧显示区
right_frame = tk.Frame(main_frame, bg="#f8f8f8", bd=1, relief="solid")
right_frame.pack(side="left", fill="both", expand=True)

# 默认先显示“总览”页面
show_overview()

# 窗口关闭时，先保存数据再关闭
root.protocol("WM_DELETE_WINDOW", lambda: (save_data(), root.destroy()))

# 进入主循环
root.mainloop()
