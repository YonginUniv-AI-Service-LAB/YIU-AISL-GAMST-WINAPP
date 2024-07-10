import sys
import time
import atexit
import socket
import signal

from configuration.address import *
from service.process_service import *

global client_socket


def cleanup():
    client_socket.close()
    print("! 프로그램이 종료되면서 자원을 정리합니다.")


def signal_handler(sig, frame):
    print(f"! 프로그램 종료 신호를 받았습니다: {sig}")
    cleanup()
    sys.exit(0)


# atexit를 사용하여 프로그램 종료 시 cleanup 함수를 호출
atexit.register(cleanup)

# SIGINT, SIGTERM 신호를 처리하도록 signal 모듈 설정
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def send_to_server(socket, identifier, message):
    msg_from_client = identifier + "/" + message
    bytes_to_send = str.encode(msg_from_client)

    try:
        # 소켓을 UDP로 열고 서버의 IP/PORT로 메시지를 보낸다.
        socket.sendto(bytes_to_send, (OUTBOUND_HOST, PROCESS_SOCKET_PORT))

    except Exception as e:
        print(f"send_to_server(), 오류 발생: {e}")

    return bytes_to_send


def start_process_provider_client_socket():
    global client_socket
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print("1. UDP 프로세스 클라이언트가 시작되었습니다.")

    process_json = None
    prev_process_json = None
    while True:
        time.sleep(1)

        try:
            process_json = get_process_information_json()
        except Exception as e:
            print(f"! get_process_information_json(), 오류 발생: {e}")

        if process_json != prev_process_json:
            bytes_to_send = send_to_server(client_socket, MY_UDP_IDENTIFIER, process_json)
            prev_process_json = process_json

            print("# 갱신 정보:", process_json)
            print("# 전송 정보:", bytes_to_send)


if __name__ == '__main__':
    start_process_provider_client_socket()
