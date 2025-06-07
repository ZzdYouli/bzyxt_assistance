# main.py
import tkinter as tk
from utils import global_state as g
from utils.data_utils import load_data, save_data
from pages.home import home_page
from pages.sleep import sleep_page
from pages.adventure import adventure_page
from pages.options import options_page
from utils.tooltip import show_tooltip, hide_tooltip
from logic.control import start_button_click, stop_button_click

# 初始化主窗口
g.root = tk.Tk()
g.root.title("睡觉也修炼")
g.root.geometry("800x600")
g.init_variables(g.root)

# 读取数据
load_data()

# 主体布局
main_frame = tk.Frame(g.root)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# 左侧按钮区
left_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
left_frame.pack(side="left", fill="y", padx=(0, 10), ipadx=10, ipady=10)

tk.Button(left_frame, text="主页", font=("微软雅黑", 12), width=12,
          command=lambda: home_page(mid_frame, right_frame, save_data, start_button_click, stop_button_click)).pack(pady=10)
tk.Button(left_frame, text="修炼", font=("微软雅黑", 12), width=12,
          command=lambda: sleep_page(mid_frame, right_frame, save_data)).pack(pady=10)
tk.Button(left_frame, text="奇遇", font=("微软雅黑", 12), width=12,
          command=lambda: adventure_page(mid_frame, right_frame, save_data)).pack(pady=10)
tk.Button(left_frame, text="设置", font=("微软雅黑", 12), width=12,
          command=lambda: options_page(mid_frame, right_frame, save_data, show_tooltip, hide_tooltip)).pack(pady=10)

# 中右区域容器
mid_frame = tk.Frame(main_frame, bg="#f8f8f8", bd=1, relief="solid")
mid_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), ipadx=10, ipady=10)

right_frame = tk.Frame(main_frame, bg="#f8f8f8", bd=1, relief="solid")
g.mid_frame = mid_frame
g.right_frame = right_frame

# 初始显示
home_page(mid_frame, right_frame, save_data, start_button_click, stop_button_click)

# 窗口关闭时保存
g.root.protocol("WM_DELETE_WINDOW", lambda: (save_data(), g.root.destroy()))

# 启动主循环
g.root.mainloop()
