PROCESS_SOCKET_PORT = 19998
IMAGE_SOCKET_PORT = 20001

INBOUND_HOST = "0.0.0.0"
OUTBOUND_HOST = {
    0: "localhost",
    1: "localhost",
    2: "localhost",
    3: "localhost",
    4: "localhost",
    5: "localhost",
    6: "localhost",
    7: "localhost",
    8: "localhost",
    9: "localhost",
    10: "localhost",
    11: "localhost",
    12: "localhost",
    13: "localhost",
    14: "localhost",
    15: "localhost",
    16: "localhost",
    17: "localhost",
    18: "localhost",
    19: "localhost",
    20: "localhost",
    21: "localhost",
    22: "localhost",
    23: "localhost",
    24: "localhost",
    25: "localhost",
    26: "localhost",
    27: "localhost",
    28: "localhost",
    29: "localhost",
    30: "localhost",
    31: "localhost",
    32: "localhost",
    33: "localhost",
    34: "localhost",
    35: "localhost",
    36: "localhost",
    37: "localhost",
    38: "localhost",
    39: "localhost",
}

if __name__ == "__main__":
    for i in range(40):
        print(f"{i}: \"localhost\",")

    print(len(OUTBOUND_HOST))
