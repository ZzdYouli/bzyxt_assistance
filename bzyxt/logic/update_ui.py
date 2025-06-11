# logic/ui_utils.py
from utils import global_state as g


def update_ui(progress=None, level=None, remaining_time=None, mode="", countdown=None, time=None):
    if progress is None:
        progress = [0, 0]
    if remaining_time is None:
        remaining_time = 0

    if mode == "practice":
        if remaining_time >= 100:
            hours = int(remaining_time // 60)
            minutes = int(remaining_time % 60)
            remaining_display = f"{hours}小时{minutes}分钟"
        else:
            remaining_display = f"{remaining_time:.1f} 分钟"
        info_text = (
            f"正在修炼：{g.art_name.get()}\n"
            f"当前等级：{level}\n"
            f"进度：[ {progress[0]} / {progress[1]} ]\n"
            f"预计剩余时间：{remaining_display}"
        )
    elif mode == "retreat":
        info_text = f"闭关中：{g.art_name.get()}\n闭关倒计时：{countdown}"
    elif mode == "stump":
        info_text = f"正在打桩\n打桩时间：{time}"
    elif mode == "running":
        info_text = "正在前往师傅处"
    elif mode == "adventure":
        info_text = "刷奇遇中……"
    elif mode == "weeding":
        info_text = "除草中……"
    else:
        info_text = "正在初始化"

    if g.info_label:
        g.info_label.config(text=info_text)
