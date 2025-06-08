import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk

from utils import global_state as g
from utils.data_utils import save_data  # 如果你把保存写进专门模块


def sleep_page(mid_frame, right_frame, save_data):
    for widget in mid_frame.winfo_children():
        widget.pack_forget()

    right_frame.pack_forget()

    container = tk.Frame(mid_frame)
    container.pack(fill="both", expand=True)

    top_frame = tk.Frame(container)
    top_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

    # 分类字典
    method_categories = {
        "拳法": ["七杀拳", "虾米拳", "九阴白骨爪", "血杀掌", "伊贺体术", "如来神掌", "万毒手", "（真）降龙十八掌",
                 "雪山六阳掌", "咏春拳", "纯阳指", "雪山六阳掌", "千蛛万毒手", "玄冥神掌", "素心掌"],
        "剑法": ["玉女剑法", "芙蓉剑法", "唐诗剑法", "玉女素心剑", "飞雪剑法", "流星蝴蝶剑"],
        "暗器": ["天龙八音", "赌神飞牌", "小李飞刀", "投石术"],
        "棍法": ["霸王枪法", "岳家枪法"],
        "鞭法": ["女王鞭法", "天女鞭法"],
        "刀法": ["杀猪刀法", "血魔刀法", "影忍三刀流", "狂风刀法"],
        "轻功": ["飞蝶舞步", "血影步", "草上飞", "影遁之术", "疾风步", "五毒幻形"]
    }
    category_list = list(method_categories.keys())

    # 分类下拉
    tk.Label(top_frame, text="分类：", font=("微软雅黑", 12)).grid(row=0, column=0, sticky="w")
    category_combobox = ttk.Combobox(top_frame, values=category_list, state="readonly", textvariable=g.art_type)
    category_combobox.grid(row=0, column=1, sticky="w", padx=5)

    # 功法下拉（与 g.art_name 绑定）
    tk.Label(top_frame, text="武学：", font=("微软雅黑", 12)).grid(row=1, column=0, sticky="w")
    method_combobox = ttk.Combobox(top_frame, state="readonly", textvariable=g.art_name)
    method_combobox.grid(row=1, column=1, sticky="w", padx=5)

    # 绑定分类选择事件
    def update_methods(event):
        selected_category = category_combobox.get()
        methods = method_categories.get(selected_category, [])
        method_combobox["values"] = methods
        if methods:
            g.art_name.set(methods[0])  # 默认选第一个
            method_combobox.current(0)

    category_combobox.bind("<<ComboboxSelected>>", update_methods)

    # 初始化分类和武学显示（避免覆盖已保存设置）
    if g.art_type.get() in category_list:
        category_combobox.set(g.art_type.get())
    else:
        category_combobox.current(0)
        g.art_type.set(category_list[0])

    # 初始化武学列表（不设置默认选中武学）
    selected_category = category_combobox.get()
    methods = method_categories.get(selected_category, [])
    method_combobox["values"] = methods
    if g.art_name.get() in methods:
        method_combobox.set(g.art_name.get())
    elif methods:
        method_combobox.current(0)
        g.art_name.set(methods[0])

    check_discount_checkbox = tk.Checkbutton(
        container,
        text="是否卡门派升级？",
        variable=g.check,
        font=("微软雅黑", 11),
        command=save_data
    )
    check_discount_checkbox.pack(pady=(10, 5), anchor="w", padx=10)

    separator = tk.Frame(container, bg="gray", height=2)
    separator.pack(fill="x", padx=5)

    bottom_frame = tk.Frame(container)
    bottom_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    tk.Label(bottom_frame, text="修炼速度：", font=("微软雅黑", 11)).grid(row=0, column=0, sticky="w", pady=5)
    speed_entry = tk.Entry(bottom_frame, textvariable=g.speed)
    speed_entry.grid(row=0, column=1, sticky="w")

    tk.Label(bottom_frame, text="潜能减免：", font=("微软雅黑", 11)).grid(row=1, column=0, sticky="w", pady=5)
    discount_entry = tk.Entry(bottom_frame, textvariable=g.discount)
    discount_entry.grid(row=1, column=1, sticky="w")
    tk.Label(bottom_frame, text="%", font=("微软雅黑", 10)).grid(row=1, column=2, sticky="w", padx=5)

    previous_discount = discount_entry.get()

    def validate_discount(event=None):
        nonlocal previous_discount
        value = discount_entry.get()
        try:
            num = float(value)
            if not 0 <= num <= 100:
                raise ValueError
        except ValueError:
            msgbox.showerror("输入错误", "请输入0到100之间的整数")
            g.discount.set(float(previous_discount))
            discount_entry.focus_set()

    discount_entry.bind("<Return>", validate_discount)
    discount_entry.bind("<FocusOut>", validate_discount)

    save_data()
