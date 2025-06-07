# ui/adventure_page.py
import tkinter as tk
from tkinter import ttk

from utils import global_state as g


def adventure_page(mid_frame, right_frame, save_data):
    for widget in mid_frame.winfo_children():
        widget.pack_forget()

    right_frame.pack_forget()

    container = tk.Frame(mid_frame)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="奇遇：", font=("微软雅黑", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=10)
    adventure_combobox = ttk.Combobox(container, values=["赌场", "残破的小镇"],
                                      textvariable=g.adventure_name)
    adventure_combobox.grid(row=0, column=1, sticky="w", padx=5, pady=10)

    save_data()
