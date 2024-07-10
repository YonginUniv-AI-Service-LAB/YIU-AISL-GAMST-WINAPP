PROCESS_SOCKET_PORT = 19998
VIDEO_SOCKET_PORT = 20001

INBOUND_HOST = "0.0.0.0"
OUTBOUND_HOST = {
    0: "localhost",
    1: "localhost",
    2: "localhost",
    3: "localhost",
    # 추가 예정
}

if __name__ == "__main__":
    # for i in range(40):
    #     print(f"{i}: \"localhost\",")
    print(len(OUTBOUND_HOST))
