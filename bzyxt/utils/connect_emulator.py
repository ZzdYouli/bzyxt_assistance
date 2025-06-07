import subprocess
import tkinter.messagebox as msgbox
from utils_path import get_adb_path
from utils import global_state as g


def connect_emulator():
    """根据 g.emulator.get() 优先连接设置的模拟器，如果失败则尝试其他已连接设备"""
    try:
        subprocess.run([get_adb_path(), "disconnect"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        emulator = g.emulator.get()
        emulator_ports = {
            "MuMu": "127.0.0.1:7555",
            "雷电": "127.0.0.1:5555"
        }

        ip_port = emulator_ports.get(emulator)

        if ip_port:
            try:
                subprocess.run([get_adb_path(), "connect", ip_port],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                g.adb_target_device = ip_port
                print(f"[连接成功] 使用模拟器：{emulator} ({ip_port})")
                return True
            except subprocess.CalledProcessError:
                print(f"[连接失败] 无法连接 {emulator} 模拟器 ({ip_port})，尝试检测已连接设备")

        # 如果无法连接，尝试检测当前已连接设备列表
        result = subprocess.run([get_adb_path(), "devices"], capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()[1:]  # 跳过表头
        for line in lines:
            if "device" in line:
                serial = line.split()[0]
                g.adb_target_device = serial
                print(f"[回退连接] 选用已连接设备：{serial}")
                return True

        msgbox.showerror("ADB 错误", f"无法连接模拟器 {emulator}，也未发现其他可用设备")
        return False

    except Exception as e:
        msgbox.showerror("ADB 异常", f"连接模拟器失败：{str(e)}")
        return False
