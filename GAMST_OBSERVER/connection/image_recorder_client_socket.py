import os
import cv2
import sys
import time
import atexit
import pickle
import signal
import socket
import struct
import datetime
import numpy as np

from GAMST_OBSERVER.dto.Flag import *
from GAMST_OBSERVER.dto.Mutex import *

global client_socket
global video_output


def cleanup():
    # Ensure to release resources properly
    try:
        video_output.release()  # 영상 저장 마무리
    except Exception as e:
        print(f"cleanup(), 오류 발생: {e}")
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


def receive_video(client_socket, out):
    data = b""
    payload_size = struct.calcsize("L")
    try:
        while Flag.is_record:
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

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)

            out.write(frame)  # 수신한 프레임을 파일에 저장

    except Exception as e:
        print(f"receive_video(), 오류 발생: {e}")
    finally:
        client_socket.close()


def start_image_recorder_client_socket(host, port, identifier):
    global video_output

    # 영상 저장 경로 설정
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%y%m%d_%H%M%S")
    directory_path = "./videos/" + current_datetime.strftime("%y%m%d") + f"/{identifier}번좌석"

    with Mutex.lock:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    output_filename = os.path.join(directory_path, f"{identifier}번좌석_{formatted_datetime}.avi")

    # 영상 포맷 설정
    FOURCC = cv2.VideoWriter_fourcc(*'XVID')
    FPS = 30.0
    FRAME_SIZE = (1280, 720)  # 화면 크기에 맞게 조정

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    time.sleep(1)
    print(f"{identifier}번 스레드, TCP 영상 서버에 연결되었습니다.")

    video_output = cv2.VideoWriter(output_filename, FOURCC, FPS, FRAME_SIZE)  # VideoWriter 객체 생성
    receive_video(client_socket, video_output)

    client_socket.close()
    print(f"{identifier}번 스레드, TCP 영상 서버와 연결이 종료되었습니다.")


if __name__ == '__main__':
    from ..configuration.address import *

    Flag.is_record = True
    start_image_recorder_client_socket("220.66.61.75", VIDEO_SOCKET_PORT, 0)
