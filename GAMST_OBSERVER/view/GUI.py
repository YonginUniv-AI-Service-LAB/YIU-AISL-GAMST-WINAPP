from tkinter import *
from functools import partial

from GAMST_OBSERVER.configuration.gui_color import *
from GAMST_OBSERVER.configuration.process_word import *
from GAMST_OBSERVER.dto.PsInfo import *
from GAMST_OBSERVER.view.on_event import *


def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("GAMST - 용인대학교 강의실 관제 프로그램")
        self.root.config(bg=BACKGROUND_FRAME_COLOR)
        self.root.resizable(False, False)

        self.init_seat_frame()
        self.init_record_frame()
        self.update_seat_button_texts()

        self.root.mainloop()

    def init_seat_frame(self):
        self.seat_frame = LabelFrame(self.root, text="좌석", bg=BACKGROUND_FRAME_COLOR)
        self.seat_frame.pack(padx=30, pady=10)

        self.seat_grids = []
        for index in range(40):
            button = Button(self.seat_frame, width=15, height=7, wraplength=110)
            button.config(command=partial(on_seat_button_click, index), bg=SEAT_OFFLINE_COLOR)  # 버튼 생성 후 command 설정
            self.seat_grids.append(button)

        for row in range(5):
            for column in range(8):
                if column == 0:
                    self.seat_grids[row * 8 + column].grid(row=row, column=column, padx=(20, 0))  # 왼쪽에 패딩 추가
                elif column % 2 == 1:
                    self.seat_grids[row * 8 + column].grid(row=row, column=column, padx=(0, 20))  # 오른쪽에 패딩 추가
                if row == 0:
                    self.seat_grids[row * 8 + column].grid(row=row, column=column, pady=(10, 0))  # 왼쪽에 패딩 추가
                elif row == 4:
                    self.seat_grids[row * 8 + column].grid(row=row, column=column, pady=(0, 15))  # 왼쪽에 패딩 추가
                else:
                    self.seat_grids[row * 8 + column].grid(row=row, column=column)

    def init_record_frame(self):
        self.record_frame = LabelFrame(self.root, text="영상 녹화", bg=BACKGROUND_FRAME_COLOR)
        self.record_frame.pack(padx=30, pady=20, side=RIGHT)

        self.record_start_button = Button(self.record_frame, text="시작", width=15, height=7)
        self.record_start_button.config(command=partial(on_record_button_click, self.record_start_button))
        self.record_start_button.grid(row=0, column=0, padx=20, pady=10)

    def update_seat_button_texts(self):
        if PsInfo.identifier is not None:
            new_text = f"좌석: {PsInfo.identifier}\n창: {PsInfo.name}\n상세: {truncate_text(PsInfo.title, 35)}"
            # print(PsInfo.time)
            if PsInfo.name in GOOD_PROCESS:
                bg = GOOD_COLOR
            elif PsInfo.name in SUSPECT_PROCESS:
                bg = SUSPECT_COLOR
            elif PsInfo.name in WARNING_PROCESS:
                bg = WARNING_COLOR
            else:
                bg = SEAT_ONLINE_COLOR
            self.seat_grids[int(PsInfo.identifier)].config(text=new_text, bg=bg)
        self.root.after(1000, self.update_seat_button_texts)  # stackoverflow X, eventloop 에 의해 발생.


if __name__ == "__main__":
    GUI()
