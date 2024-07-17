import sys
import json
import atexit
import signal
import socket

from GAMST_OBSERVER.configuration.address import *
from GAMST_OBSERVER.dto.PsInfo import *

global server_socket


def cleanup():
    server_socket.close()
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


def start_process_observer_server_socket():
    global server_socket
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((INBOUND_HOST, PROCESS_SOCKET_PORT))
    print("UDP 프로세스 서버가 실행되었습니다. 수신을 기다리는 중...")

    while True:
        try:
            byte_addr_pair = server_socket.recvfrom(1024)
            data = byte_addr_pair[0]
            addr = byte_addr_pair[1]

            decode_message = data.decode("utf-8")
            ps_identifier, message_json = decode_message.split("/", 1)
            message_dict = json.loads(message_json)

            print(message_dict)
            ps_name = message_dict["foreground"]["name"]
            ps_title = message_dict["foreground"]["title"]
            ps_time = message_dict["time"]
            PsInfo.update_state(ps_identifier, ps_name, ps_title, ps_time)
        except Exception as e:
            print(f"데이터 수신 오류: {e}")


if __name__ == "__main__":
    start_process_observer_server_socket()
