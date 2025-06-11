import subprocess
import os
import time
from datetime import datetime
from utils_path import get_adb_path
from utils import global_state as g


def capture_screenshot(folder_path="../screen_temp"):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if not isinstance(folder_path, str):
        raise TypeError(f"folder_path 必须是字符串路径，但收到的是 {type(folder_path)}")
    device_id = g.adb_target_device
    device_path = "/data/local/tmp/screenshot_temp.png"  # 更保险的路径
    for attempt in range(5):
        try:
            # 可选：检查设备是否在线
            result = subprocess.run([get_adb_path(), "-s", device_id, "get-state"],
                                    capture_output=True, text=True)
            if "device" not in result.stdout:
                raise RuntimeError("设备未连接")

            # 截图
            subprocess.run([get_adb_path(), "-s", device_id, "shell", "screencap", "-p", device_path],
                           check=True)

            # pull 到本地
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            local_path = os.path.join(folder_path, f"screenshot_{timestamp}.png")

            subprocess.run([get_adb_path(), "-s", device_id, "pull", device_path, local_path],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            return local_path  # 成功返回

        except Exception as e:
            print(f"[截图重试] 第 {attempt + 1} 次失败: {e}")
            time.sleep(2)

    raise RuntimeError("连续五次截图失败")
