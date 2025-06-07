import tkinter as tk
from tkinter import ttk

from utils import global_state as g


def options_page(mid_frame, right_frame, save_data, show_tooltip, hide_tooltip):
    for widget in mid_frame.winfo_children():
        widget.pack_forget()

    right_frame.pack_forget()

    container = tk.Frame(mid_frame)
    container.pack(fill="both", expand=True)

    # 性能模式选择
    tk.Label(container, text="性能模式选择：", font=("微软雅黑", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=10)

    performance_combobox = ttk.Combobox(
        container,
        values=["高性能模式", "低性能模式"],
        textvariable=g.performance
    )
    performance_combobox.grid(row=0, column=1, sticky="w", padx=5, pady=10)

    performance_tip = "这里的性能指的是你的网速以及分配给模拟器的性能，\n高性能模式点击速度更快但可能会导致运行异常。"
    performance_combobox.bind("<Enter>", lambda event: show_tooltip(event, performance_tip))
    performance_combobox.bind("<Leave>", hide_tooltip)

    # 模拟器选择
    tk.Label(container, text="模拟器选择：", font=("微软雅黑", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=10)

    emulator_combobox = ttk.Combobox(
        container,
        values=["MuMu", "雷电"],
        textvariable=g.emulator
    )
    emulator_combobox.grid(row=1, column=1, sticky="w", padx=5, pady=10)

    emulator_tip = "请根据你所使用的模拟器类型选择。"
    emulator_combobox.bind("<Enter>", lambda event: show_tooltip(event, emulator_tip))
    emulator_combobox.bind("<Leave>", hide_tooltip)

    check_maid_checkbox = tk.Checkbutton(
        container,
        text="有没有开管家",
        variable=g.check,
        font=("微软雅黑", 11),
        command=save_data
    )
    check_maid_checkbox.grid(row=2, column=0, sticky="w", padx=5, pady=10)
    save_data()
