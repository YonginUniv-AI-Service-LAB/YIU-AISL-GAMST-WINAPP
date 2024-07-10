import cv2
import pickle
import struct
import pyautogui
import numpy as np
import threading


def send_image(conn):
    try:
        while True:
            # 데스크탑 화면 캡처
            screenshot = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (1280, 720))

            data = pickle.dumps(cv2.imencode('.jpg', frame)[1])
            message_size = struct.pack("L", len(data))

            conn.sendall(message_size + data)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"! send_video(), 이미지 처리 오류 발생: {e}")
    finally:
        conn.close()
