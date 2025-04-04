import pytesseract
from PIL import Image
import re
from action_engine import detect_image

# 配置 Tesseract 路径（如果已经添加到系统 PATH，则这行也可以删）
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# 解析进度条中的数据
def extract_progress_data(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    # 匹配进度：如 44134/88657
    match = re.search(r'(\d+)\s*/\s*(\d+)', text)
    current, total = None, None
    if match:
        current = int(match.group(1))
        total = int(match.group(2))

    # 匹配等级：如 Lv251
    lv_match = re.search(r'[Ll][vV]?\s*(\d+)', text)
    level = None
    if lv_match:
        level = int(lv_match.group(1))

    return current, total, level


# 新增：提取闭关倒计时
def extract_countdown_timer(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='chi_sim+eng')  # 加强中英文识别支持
    # 多种可能的匹配方案（带冗余容错）
    patterns = [
        r'(\d{2}[:：]\d{2}[:：]\d{2})',  # 纯时间（没有“闭关”字眼）
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match and detect_image("../assets/main_if/countdown.png"):
            return match.group(1).replace("：", ":")  # 替换中文冒号

    return None
