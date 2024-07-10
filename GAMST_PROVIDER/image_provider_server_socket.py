import sys
import time
import atexit
import socket
import signal

from configuration.address import *
from service.image_service import *

global server_socket


def cleanup():
    server_socket.close()
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


def start_image_provider_server_socket():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((INBOUND_HOST, VIDEO_SOCKET_PORT))
    server_socket.listen(1)
    print("1. TCP 영상 서버가 시작되었습니다. 연결을 기다리는 중...")

    # 안전한 연결을 위한 시간 대기
    time.sleep(1)

    while True:
        conn, addr = server_socket.accept()
        print(f"2. {addr}에서 연결되었습니다.")

        thread = threading.Thread(target=send_image, args=(conn,))
        thread.start()


if __name__ == "__main__":
    start_image_provider_server_socket()
