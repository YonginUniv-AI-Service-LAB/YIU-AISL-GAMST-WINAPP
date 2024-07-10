import threading


class Mutex:
    lock = threading.Lock()
