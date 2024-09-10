import os
import cv2
import sys
import atexit
import signal
import socket
import struct
import pickle
import numpy as np

from GAMST_OBSERVER.connection.address import *
from GAMST_OBSERVER.domain.Flag import *

global client_socket


def cleanup():
    cv2.destroyAllWindows()
    # out.release()  # 영상 저장 마무리
    print("프로그램이 종료되면서 자원을 정리합니다.")


def signal_handler(sig, frame):
    print(f"프로그램 종료 신호를 받았습니다: {sig}")
    cleanup()
    sys.exit(0)


# atexit를 사용하여 프로그램 종료 시 cleanup 함수를 호출
atexit.register(cleanup)

# SIGINT, SIGTERM 신호를 처리하도록 signal 모듈 설정
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


# def receive_video(button_index):
def receive_video(button_index):
    global client_socket
    # winname = f"seat position: {button_index}"
    data = b""
    payload_size = struct.calcsize("L")
    try:
        Flag.is_view = True
        while Flag.is_view:

            while len(data) < payload_size:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet
            if not data:
                break
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)
            frame = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)

            cv2.imshow("", frame)
            # out.write(frame)  # 수신한 프레임을 파일에 저장

            if cv2.waitKey(1) & 0xFF == 27:
                cv2.destroyWindow("")
                break
            if cv2.getWindowProperty("", cv2.WND_PROP_VISIBLE) < 1:
                break

    except Exception as e:
        print(f"! {button_index}번 영상 스레드, 오류 발생: {e}")
    finally:
        cv2.destroyWindow("")
        print(f"{button_index}번 좌석의 윈도우 삭제")
        client_socket.close()


def start_image_observer_client_socket(host, identifier):
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, IMAGE_SOCKET_PORT))
    print("TCP 서버에 연결되었습니다.")

    receive_video(identifier)
    # receive_video(button_index)

    client_socket.close()
    print("서버와 연결이 종료되었습니다.")


if __name__ == '__main__':
    start_image_observer_client_socket("localhost", 0)
