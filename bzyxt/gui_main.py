import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
import json
import os
import threading

from function.adventure import start_adventure
# === 导入后台逻辑与停止事件 ===
from function.auto_practice import start_practice
from stop_event import stop_event
from task_switch import task_switch

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
adventure_name = tk.StringVar(value="赌场")
count_max = tk.DoubleVar(value=0)
task = tk.StringVar(value="躺床")
# === 控制按钮状态 ===
is_running = False  # 标记程序是否在运行
start_button = None  # 用于后面引用“启动/停止”按钮
task_thread = None  # 后台线程引用
adventure_thread = None
info_label = None
running_label = None


def show_tooltip(event, text):
    """显示气泡提示"""
    tooltip = tk.Label(root, text=text, font=("微软雅黑", 10), bg="lightyellow", relief="solid", bd=1)
    tooltip.place(x=300, y=100)  # 在鼠标下方显示气泡


def hide_tooltip(event):
    """隐藏气泡提示"""
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("bg") == "lightyellow":
            widget.destroy()  # 删除气泡提示


def update_ui(progress=None, level=None, remaining_time=None, target_level=None, mode="",
              countdown=None):
    if progress is None:
        progress = [0, 0]  # 设置默认值，避免访问 NoneType

    # 如果 remaining_time 是 None，使用默认值 0
    if remaining_time is None:
        remaining_time = 0

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
            f"闭关倒计时：{countdown}\n"
        )
    elif mode == "running":
        info_text = (
            "正在前往师傅处"
        )
    elif mode == "adventure":
        info_text = (
            "刷奇遇中......"
        )
    else:
        info_text = "正在初始化"

    info_label.config(text=info_text)


# === 读取本地存储数据 ===
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # 加载睡觉页面的数据
            sleep_data = data.get('sleep_data', {})
            speed.set(sleep_data.get('speed', 100000))
            art_name.set(sleep_data.get('art_name', "玉女剑法"))
            target_level.set(sleep_data.get('target_level', ''))
            discount.set(sleep_data.get('discount', 0.0))

            # 加载奇遇页面的数据
            adventure_data = data.get('adventure_data', {})
            adventure_name.set(adventure_data.get('adventure_name', '赌场'))  # 默认奇遇为 赌场
            count_max.set(adventure_data.get('count_max', 0))  # 默认奇遇为 赌场

            task_data = data.get('task_data', {})
            task.set(task_data.get('task', '躺床'))


# === 保存数据到本地 ===
def save_data():
    # 睡觉页面数据
    sleep_data = {
        'speed': speed.get(),
        'art_name': art_name.get(),
        'target_level': target_level.get(),
        'discount': discount.get()
    }

    # 奇遇页面数据
    adventure_data = {
        'adventure_name': adventure_name.get(),  # 获取当前选择的奇遇
        'count_max_data': count_max.get()
    }

    task_data = {
        'task': task.get()

    }

    # 保存数据到 JSON 文件
    data = {
        'sleep_data': sleep_data,
        'adventure_data': adventure_data,
        'task_data': task_data
    }

    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# === 启动函数：调用后台任务 ===
def start_button_click(task):
    global is_running, task_thread, adventure_thread, info_label
    if not is_running:  # 如果当前不是运行状态
        stop_event.clear()  # 清除停止事件，准备开始任务

        # 从输入框中获取用户配置
        folder_path = "../screen_temp"
        speed_value = speed.get()
        art_name_value = art_name.get()
        target_level_value = target_level.get()
        discount_value = discount.get()

        if task_switch(task) == "practice":
            # 启动修炼任务的线程
            task_thread = threading.Thread(
                target=start_practice,
                args=(folder_path, speed_value, art_name_value, target_level_value, discount_value, stop_event, update_ui)
            )
            task_thread.daemon = True  # 设置为守护线程
            task_thread.start()
            update_ui(mode="practice", progress=[0, 100])  # 确保传递有效的 progress

        elif task_switch(task) == "adventure":
            # 启动冒险任务的线程
            adventure_thread = threading.Thread(
                target=start_adventure,
                args=(adventure_name.get(), folder_path, count_max.get())  # Pass count_max value
            )
            adventure_thread.daemon = True  # 设置为守护线程
            adventure_thread.start()
            update_ui(mode="adventure", progress=[0, 100])  # 确保传递有效的 progress

        # 更改按钮文本为“停止”
        start_button.config(text="停止", command=lambda: stop_button_click(task))
        running_label.config(text="正在运行")

        is_running = True
    else:
        # 如果已经在运行，则调用停止函数
        stop_button_click(task)


def cleanup_screenshots(folder_path, stop_event):
    # 确保传递的是正确的字符串路径
    if not isinstance(folder_path, str):
        print("路径应为字符串类型，当前类型：", type(folder_path))
        return
    screenshots = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    # 其他清理逻辑...


# === 停止修炼任务 ===
def stop_button_click(task):
    global is_running, adventure_thread, count, info_label
    stop_event.set()  # 设置停止事件，通知后台线程退出
    print(f"停止{task}任务")

    # 等待后台线程安全结束
    if adventure_thread is not None and adventure_thread.is_alive():
        adventure_thread.join()  # 等待线程安全退出

    # 重置状态，准备启动新任务
    is_running = False
    count = 1  # 重置计数器

    # 恢复按钮文本为“启动”
    start_button.config(text="启动", command=lambda: start_button_click(task))

    # 恢复“运行中”标签为“请选择”
    running_label.config(text="请选择")

    # 恢复信息文本为“找点事情做吧”
    if info_label is None:
        info_label = tk.Label(right_frame, text="找点事情做吧", font=("微软雅黑", 12, "bold"), bg="#ffffff")
        info_label.pack(pady=20)
    else:
        info_label.config(text="找点事情做吧")  # 恢复显示文本


# === 界面逻辑：总览页 ===
def show_overview():
    global info_label, running_label, start_button  # 声明为全局变量

    for widget in mid_frame.winfo_children():
        widget.pack_forget()  # 隐藏所有控件

    # 中间显示区域
    separator = tk.Frame(mid_frame, bg="gray", height=2)
    separator.pack(fill="x", padx=5, pady=10)

    separator.pack(fill="x", padx=5, pady=5)
    scheduler_frame = tk.Frame(mid_frame)
    scheduler_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(scheduler_frame, text="调度器", font=("微软雅黑", 12, "bold")).pack(side="left")

    # 确保 start_button 已初始化
    if is_running:
        start_button = tk.Button(scheduler_frame, text="停止", font=("微软雅黑", 10), width=8,
                                 command=stop_button_click(task))
    else:
        start_button = tk.Button(scheduler_frame, text="启动", font=("微软雅黑", 10), width=8,
                                 command=lambda: start_button_click(task.get()))  # 传递task.get()

    start_button.pack(side="right", padx=10)

    separator = tk.Frame(mid_frame, bg="gray", height=2)
    separator.pack(fill="x", padx=5, pady=5)

    separator = tk.Frame(mid_frame, bg="gray", height=2)
    separator.pack(fill="x", padx=5, pady=20)
    # 第二部分：运行中
    running_frame = tk.Frame(mid_frame)
    running_frame.pack(fill="x", padx=10)

    # 初始化 running_label，并设置为“请选择”
    running_label = tk.Label(running_frame, text="想做什么：", font=("微软雅黑", 12, "bold"))
    running_label.pack(side="left")

    top_frame = tk.Frame(mid_frame)
    top_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

    method_combobox = ttk.Combobox(top_frame, values=["躺床", "刷奇遇"], textvariable=task)
    method_combobox.grid(row=0, column=1, sticky="w", padx=5)

    # 绑定 Combobox 事件，选择后保存
    method_combobox.bind("<<ComboboxSelected>>", lambda event: save_data())

    # 右侧显示区域
    right_frame.pack(side="right", fill="both", expand=True)
    if info_label is None:
        info_label = tk.Label(right_frame, text="找点事情做吧", font=("微软雅黑", 12, "bold"), bg="#ffffff")
        info_label.pack(pady=20)
    else:
        info_label.config(text="找点事情做吧")  # 恢复显示文本

    save_data()  # 每次切换界面时，保存一下数据


# === 界面逻辑：睡觉页 ===
def show_sleep_page():
    for widget in mid_frame.winfo_children():
        widget.pack_forget()  # 隐藏所有控件

    # 隐藏右侧框架
    right_frame.pack_forget()

    container = tk.Frame(mid_frame)
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

    previous_discount = discount_entry.get()

    def validate_discount(event=None):
        global previous_discount
        value = discount_entry.get()
        try:
            num = float(value)
            if not 0 <= num <= 100:
                raise ValueError
        except ValueError:
            # 输入无效，恢复到上一个有效值
            msgbox.showerror("输入错误", "请输入0到100之间的整数")
            discount.set(float(previous_discount))  # 恢复为上一个有效值
            discount_entry.focus_set()  # 重新聚焦到输入框

    discount_entry.bind("<Return>", validate_discount)
    discount_entry.bind("<FocusOut>", validate_discount)

    save_data()  # 每次切换界面时，保存一下数据


# === 界面逻辑：奇遇页 ===
def show_adventure_page():
    for widget in mid_frame.winfo_children():
        widget.pack_forget()  # 隐藏所有控件

    # 隐藏右侧框架
    right_frame.pack_forget()

    container = tk.Frame(mid_frame)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="奇遇", font=("微软雅黑", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=10)
    adventure_combobox = ttk.Combobox(container, values=["赌场", "家", "残破的小镇", "竹林", "小池塘"],
                                      textvariable=adventure_name)
    adventure_combobox.grid(row=0, column=1, sticky="w", padx=5, pady=10)

    tk.Label(container, text="最大刷新次数", font=("微软雅黑", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=10)
    count_max_entry = tk.Entry(container, textvariable=count_max)
    count_max_entry.grid(row=1, column=1, sticky="w", padx=5)
    tip_text = "这里设置最大刷新次数，\n数值为0~100，\n0为持续刷新直到出现对应奇遇。"
    count_max_entry.bind("<Enter>", lambda event: show_tooltip(event, tip_text))  # 鼠标进入时显示气泡提示
    count_max_entry.bind("<Leave>", hide_tooltip)  # 鼠标离开时隐藏气泡提示

    previous_count_max = count_max.get()

    def validate_count_max(event=None):
        global previous_count_max
        value = count_max_entry.get()
        try:
            num = int(value)  # 尝试将输入转为整数
            if not 0 <= num <= 100:  # 检查是否在有效范围内
                raise ValueError
            else:
                # 如果验证通过，更新上一个有效值
                previous_count_max = num
        except ValueError:
            # 输入无效，恢复到上一个有效值
            msgbox.showerror("输入错误", "请输入0到100之间的整数")
            count_max.set(previous_count_max)  # 恢复为上一个有效值
            count_max_entry.focus_set()  # 重新聚焦到输入框

    count_max_entry.bind("<Return>", validate_count_max)
    count_max_entry.bind("<FocusOut>", validate_count_max)

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
tk.Button(left_frame, text="奇遇", font=("微软雅黑", 12), width=12, command=show_adventure_page).pack(pady=10)

# 右侧显示区
mid_frame = tk.Frame(main_frame, bg="#f8f8f8", bd=1, relief="solid")
mid_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), ipadx=10, ipady=10)

right_frame = tk.Frame(main_frame, bg="#f8f8f8", bd=1, relief="solid")
# right_frame.pack(side="left", fill="both", expand=True)
# 默认先显示“总览”页面
show_overview()

# 窗口关闭时，先保存数据再关闭
root.protocol("WM_DELETE_WINDOW", lambda: (save_data(), root.destroy()))

# 进入主循环
root.mainloop()
