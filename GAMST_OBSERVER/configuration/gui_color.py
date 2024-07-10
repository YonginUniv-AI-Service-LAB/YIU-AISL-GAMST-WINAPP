def rgb(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


""" 기본 """
DEFAULT_COLOR = rgb(240, 240, 240)

""" 프로세스 상태 """
GOOD_COLOR = rgb(172, 202, 105)
SUSPECT_COLOR = rgb(246, 187, 67)
WARNING_COLOR = rgb(240, 86, 80)

""" 배경 """
BACKGROUND_FRAME_COLOR = rgb(255, 255, 255)

""" 좌석 상태 """
SEAT_ONLINE_COLOR = DEFAULT_COLOR
SEAT_OFFLINE_COLOR = rgb(170, 170, 170)

""" 녹화 색상 """
RECORDING_COLOR = rgb(200, 150, 150)
