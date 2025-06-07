import tkinter as tk
from utils import global_state as g


def show_tooltip(event, text):
    """显示气泡提示"""
    if not g.root:
        return  # 如果 root 还未初始化，直接跳过（也可抛异常）

    tooltip = tk.Label(g.root, text=text, font=("微软雅黑", 10), bg="lightyellow", relief="solid", bd=1)
    tooltip.place(x=200, y=70)


def hide_tooltip(event):
    """隐藏气泡提示"""
    if not g.root:
        return

    for widget in g.root.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("bg") == "lightyellow":
            widget.destroy()
