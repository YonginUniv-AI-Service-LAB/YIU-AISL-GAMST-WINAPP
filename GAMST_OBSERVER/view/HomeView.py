import time
from tkinter import *
from functools import partial

from GAMST_OBSERVER.controller.HomeController import *
from GAMST_OBSERVER.domain.process_word import *
from GAMST_OBSERVER.domain.ReportedInformation import *


class HomeView:
    def __init__(self):
        self.root = Tk()
        self.root.title("GAMST - 용인대학교 강의실 관제 프로그램")
        self.root.config(bg=BACKGROUND_FRAME_COLOR)
        self.root.resizable(False, False)

        self.seat_frame = None
        self.seat_grids = None

        self.init_seat_frame()
        self.init_record_frame()
        self.update_seat_button_texts()

        self.root.mainloop()

    def init_seat_frame(self):
        self.seat_frame = LabelFrame(self.root, text="좌석", bg=BACKGROUND_FRAME_COLOR)
        self.seat_frame.pack(padx=30, pady=10)

        self.seat_grids = []

        row_count = 5
        column_count = 8

        for index in range(row_count * column_count):
            button = Button(self.seat_frame, width=15, height=7, wraplength=110)
            button.config(command=partial(on_seat_button_event, index), bg=SEAT_OFFLINE_COLOR)  # 버튼 생성 후 command 설정
            self.seat_grids.append(button)

        for row in range(row_count):
            for column in range(column_count):
                if column == 0:
                    self.seat_grids[row * column_count + column].grid(row=row, column=column, padx=(20, 0))  # 좌측 패딩 추가
                elif column % 2 == 1:
                    self.seat_grids[row * column_count + column].grid(row=row, column=column, padx=(0, 20))  # 우측 패딩 추가
                if row == 0:
                    self.seat_grids[row * column_count + column].grid(row=row, column=column, pady=(10, 0))  # 상단 패딩 추가
                elif row == row_count - 1:
                    self.seat_grids[row * column_count + column].grid(row=row, column=column, pady=(0, 15))  # 하단 패딩 추가
                else:
                    self.seat_grids[row * column_count + column].grid(row=row, column=column)

    def init_record_frame(self):
        record_frame = LabelFrame(self.root, text="영상 녹화", bg=BACKGROUND_FRAME_COLOR)
        record_frame.pack(padx=30, pady=20, side=RIGHT)

        record_start_button = Button(record_frame, text="시작", width=15, height=7)
        record_start_button.config(command=partial(on_record_button_event, record_start_button))
        record_start_button.grid(row=0, column=0, padx=20, pady=10)

    def update_seat_button_texts(self):
        LIFETIME = 7
        for ps in ps_informations:
            if ps.identifier is not None:
                if time.time() - ps.unix_time > LIFETIME:
                    self.seat_grids[int(ps.identifier)].config(text="", bg=SEAT_OFFLINE_COLOR)
                    continue
                elif ps.foreground_name in WARNING_PROCESS or ps.cursor_name in WARNING_PROCESS:
                    bg = WARNING_COLOR
                elif ps.foreground_name in SUSPECT_PROCESS or ps.cursor_name in SUSPECT_PROCESS:
                    bg = SUSPECT_COLOR
                elif ps.foreground_name in GOOD_PROCESS or ps.cursor_name in GOOD_PROCESS:
                    bg = GOOD_COLOR
                else:
                    bg = SEAT_ONLINE_COLOR

                new_text = (f"{self.truncate_text(ps.foreground_name, 15)}\n"
                            f"{self.truncate_text(ps.foreground_title, 15)}\n"
                            f"{self.truncate_text(ps.cursor_name, 15)}\n"
                            f"{self.truncate_text(ps.cursor_title, 15)}\n"
                            )
                self.seat_grids[int(ps.identifier)].config(text=new_text, bg=bg)

        self.root.after(1000, self.update_seat_button_texts)  # stackoverflow X, eventloop 에 의해 발생.

    @staticmethod
    def truncate_text(text, max_length):
        if len(text) > max_length:
            return text[:max_length] + '..'
        return text


if __name__ == '__main__':
    HomeView()
