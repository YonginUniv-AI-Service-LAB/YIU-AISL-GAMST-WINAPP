import json
import win32api
import win32con
import win32gui
import win32process
from datetime import datetime  # 시간 정보를 가져오기 위해 datetime 모듈을 추가로 임포트합니다.


def get_process_information_json():
    x, y = win32gui.GetCursorPos()
    cursor_hwnd = win32gui.WindowFromPoint((x, y))
    foreground_hwnd = win32gui.GetForegroundWindow()

    cursor_process = get_process_information(cursor_hwnd)
    foreground_process = get_process_information(foreground_hwnd)

    # 현재 시간을 가져와서 원하는 포맷으로 문자열로 변환합니다.
    current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    process_dict = {
        "time": current_time,  # 시간 정보를 추가합니다.
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
