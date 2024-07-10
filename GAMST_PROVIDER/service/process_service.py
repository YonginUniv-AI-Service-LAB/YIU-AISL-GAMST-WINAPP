import json
import win32api
import win32con
import win32gui
import win32process


def get_process_information_json():
    x, y = win32gui.GetCursorPos()
    cursor_hwnd = win32gui.WindowFromPoint((x, y))
    foreground_hwnd = win32gui.GetForegroundWindow()

    cursor_process = get_process_information(cursor_hwnd)
    foreground_process = get_process_information(foreground_hwnd)

    process_dict = {
        "foreground": {
            "name": foreground_process[0],
            "title": foreground_process[1]
        },
        "cursor": {
            "name": cursor_process[0],
            "title": cursor_process[1]
        }
    }
    process_json = json.dumps(process_dict)

    return process_json


def get_process_information(hwnd):
    tid, pid = win32process.GetWindowThreadProcessId(hwnd)
    process_handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    process_name_with_path = win32process.GetModuleFileNameEx(process_handle, 0)
    process_name = process_name_with_path.split("\\")[-1]

    window_title = win32gui.GetWindowText(hwnd)

    return process_name, window_title


if __name__ == '__main__':
    import time

    while True:
        data = get_process_information_json()
        print(type(data))
        print(data)

        time.sleep(1)
