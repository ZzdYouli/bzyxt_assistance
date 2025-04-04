from stop_event import stop_event


def check_stop():
    if stop_event.is_set():
        return False
