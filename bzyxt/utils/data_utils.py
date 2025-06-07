# utils/data_utils.py
import json
import os
from utils import global_state as g

data_file = 'settings.json'


def save_data():
    data = {
        'sleep_data': {
            'speed': g.speed.get(),
            'art_name': g.art_name.get(),
            'discount': g.discount.get(),
            'check': g.check.get()
        },
        'adventure_data': {
            'adventure_name': g.adventure_name.get(),

        },
        'task_data': {
            'task': g.task.get()
        },
        'performance_data': {
            'performance': g.performance.get()
        },
        'emulator_data': {
            'emulator': g.emulator.get()
        },
        'other_data': {
            'weeding': g.weeding.get()
        }
    }

    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

            sleep_data = data.get('sleep_data', {})
            g.speed.set(sleep_data.get('speed', 100000))
            g.art_name.set(sleep_data.get('art_name', "玉女剑法"))
            g.discount.set(sleep_data.get('discount', 0.0))

            adventure_data = data.get('adventure_data', {})
            g.adventure_name.set(adventure_data.get('adventure_name', '赌场'))


            task_data = data.get('task_data', {})
            g.task.set(task_data.get('task', '躺床'))

            performance_data = data.get('performance_data', {})
            g.performance.set(performance_data.get('performance', '高性能模式'))

            emulator_data = data.get('emulator_data', {})
            g.emulator.set(emulator_data.get('emulator', 'MuMu'))

            other_data = data.get('other_data', {})
            g.weeding.set(other_data.get('weeding', True))
            g.check.set(sleep_data.get('check', True))  # 默认 true
