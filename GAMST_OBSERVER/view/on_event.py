import multiprocessing
import threading

from configuration.gui_color import *
from configuration.address import *
from connection.image_observer_client_socket import *
from connection.image_recorder_client_socket import *
from dto.Flag import *
from dto.Collection import *
from dto.ReportedInformation import *


def on_seat_button_click(button_index):
    Flag.is_view = False

    print("seat_event(), 1. 좌석 버튼 감지 0.1초간 대기")
    time.sleep(0.1)

    print(f"seat_event(), 2. 좌석 버튼 {button_index}번이 눌렸습니다.")
    view_thread = threading.Thread(target=start_image_observer_client_socket,
                                   args=(Collection.client_ip[button_index], button_index)
                                   )
    # view_thread.daemon = True
    view_thread.start()

    print(f"seat_event(), 3. 좌석 영상 프로세스 {button_index}번 시작")


def on_record_button_click(button_object):
    if not Flag.is_record:
        Flag.is_record = True
        for identifier, ip in Collection.client_ip.items():
            # record_process = threading.Thread(target=start_image_recorder_client_socket,
            ps = multiprocessing.Process(target=start_image_recorder_client_socket,
                                         args=(ip, identifier)
                                         )
            ps.daemon = True
            ps.start()
            Collection.record_process.append(ps)
        time.sleep(0.5)
        print("녹화 시작")
        button_object.config(text="중지", bg=RECORDING_COLOR)

    else:
        Flag.is_record = False
        for record_process in Collection.record_process:
            record_process.terminate()
        print("녹화 중지")
        button_object.config(text="시작", bg=DEFAULT_COLOR)
