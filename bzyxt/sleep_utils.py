import time


def interruptible_sleep(seconds, stop_event, interval=0.2):
    """支持中断的 sleep，用于响应 stop_event"""
    slept = 0
    while slept < seconds:
        if stop_event.is_set():
            break
        time.sleep(interval)
        slept += interval
