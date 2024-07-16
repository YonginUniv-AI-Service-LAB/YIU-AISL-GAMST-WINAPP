import threading

from GAMST_OBSERVER.configuration.gui_color import *
from GAMST_OBSERVER.configuration.address import *
from GAMST_OBSERVER.connection.image_observer_client_socket import *
from GAMST_OBSERVER.connection.image_recorder_client_socket import *
from GAMST_OBSERVER.dto.Flag import *
from GAMST_OBSERVER.dto.Mutex import *


def on_seat_button_click(button_index):
    # with Mutex.lock:
    Flag.is_view = False

    print("seat_event(), 1. 좌석 버튼 감지 0.1초간 대기")
    time.sleep(0.1)

    print(f"seat_event(), 2. 좌석 버튼 {button_index}번이 눌렸습니다.")
    thread = threading.Thread(target=start_image_observer_client_socket,
                              args=(OUTBOUND_HOST[button_index], button_index)
                              )
    thread.start()

    print(f"seat_event(), 3. 좌석 영상 스레드 {button_index}번 시작")


def on_record_button_click(button_object):
    if not Flag.is_record:
        Flag.is_record = True
        for identifier in range(len(OUTBOUND_HOST)):
            record_thread = threading.Thread(target=start_image_recorder_client_socket,
                                             args=(OUTBOUND_HOST[identifier], identifier)
                                             )
            record_thread.daemon = True
            record_thread.start()
        time.sleep(0.5)
        print("녹화 시작")
        button_object.config(text="중지", bg=RECORDING_COLOR)

    else:
        Flag.is_record = False
        print("녹화 중지")
        button_object.config(text="시작", bg=DEFAULT_COLOR)
